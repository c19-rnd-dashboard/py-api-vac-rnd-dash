"""
Transforms

Contains custom source transforms
"""

import pandas as pd
import numpy as np

from .common import *
from .milestones import milestone_transformer

from fuzzywuzzy import fuzz
from functools import partial
import string
import logging
import hashlib
from api.utils.geolocation import Geolocation


tlogg = logging.getLogger('.'.join(['api.app', __name__.strip('api.')]))


######################################
### Product Source Transformations ###
######################################


def clean_product_raw(data: pd.DataFrame):
    assert type(data) == pd.DataFrame
    assert len(data) > 0
    # Drop columns with no name (assume no data or not relevant)
    temp_data = drop_unnamed_columns(data).copy()
    # Rename columns to db format/names
    product_schema = {
        'ID': 'product_id',
        'Source?': 'source',
        'Product Name - Preferred': 'preferred_name',
        'Product Name - Chemical': 'chemical_name',
        'Product Name - Brand': 'brand_name',
        'Sponsor': 'sponsors',
        'Intervention Type': 'intervention_type',
        'Indication': 'indication',
        'Molecule Type': 'molecule_type',
        'Therapeutic Approach': 'therapeutic_approach',
        'New/Repurposed': 'repurposed',
        'Notes': 'notes',
        'Funding/Manufacturing/Research/Other Partners': 'other_partners',
        'Country': 'countries',
        'Current Status': 'current_status',
        'Pre-Clinical Studies Started': 'pre_clinical_studies_started_date',
        'Lead Selection Finalized': 'lead_selection_finalized_date',
        'Clinical Batch Finalized': 'clinical_batch_finalized_date',
        'IND or Equivalent Approval Finalized': 'ind_finalized_date',
        'Phase 1 Started': 'phase_1_started_date',
        'Phase 2 Started': 'phase_2_started_date',
        'Phase 3 Started': 'phase_3_started_date',
        'NDA or equivalent Approval Finalized': 'nda_finalized',
        'Phase': 'phase',
        'Condition or Disease': 'condition_or_disease',
        'Number of Participants': 'number_participants',
        'Accepts Healthy Subjects': 'accepts_healthy_subjects',
        '# of Sites': 'num_sites',
        'Sites Locations': 'site_locations',
        'Study Start Date': 'study_start_date',
        'Primary Completion DAte': 'primary_completion_date',
        'Study Completion Date': 'study_completion_date',
        'How to participate': 'participation_link',
        'Discovery Started': 'discovery_started_date',
        'CTG Identifier': 'trial_id',
        'Status': 'status',
    }
    temp_data = temp_data.rename(columns=product_schema)

    # Clean Sources and append to data rows
    def get_unique_sources(row_list: list) -> dict:
        url_list = []
        for item in row_list:
            if ('http' in item):
                if item not in url_list:
                    url_list.append(item)
        urls = ','.join(url_list)
        product_id = row_list[0]
        return {
            'product_id': product_id,
            'sources': urls,
        }

    def clean_valid_sources(df: pd.DataFrame):
        data_rows = df.query("source == 'No'")
        source_rows = df.query("source == 'Yes'")

        clean_sources = []
        for i in range(len(source_rows)):
            row_list = source_rows.iloc[i].to_list()
            clean_sources.append(get_unique_sources(row_list=row_list))

        source_frame = pd.DataFrame(clean_sources)
        clean_frame = data_rows.drop(columns=['source']).merge(
            source_frame, on='product_id')
        return clean_frame

    temp_data = clean_valid_sources(temp_data)

    # Infer preferred_name from other names
    def build_missing_preferred_names(df: pd.DataFrame) -> pd.DataFrame:
        def clean_(item):
            teststr = item
            return teststr.translate(str.maketrans('', '', string.punctuation)).replace(' ', '_')

        df1 = df.copy()
        for i in range(len(df)):
            row = df1.iloc[i]
            if len(row.preferred_name) < 2:
                if len(row.chemical_name) > 0:
                    df1.iloc[i].preferred_name = clean_(row.chemical_name)
                elif len(row.brand_name) > 0:
                    df1.iloc[i].preferred_name = clean_(row.brand_name)
                elif (len(row.sponsors) > 0):
                    df1.iloc[i].preferred_name = '-'.join(
                        [
                            clean_(row.sponsors.split(',')[0]),
                            row.product_id
                        ])

        return df1[df1.preferred_name.str.len() > 0]

    temp_data = build_missing_preferred_names(temp_data)

    # Generate country code lists
    temp_data["country_codes"] = temp_data["countries"].apply(clean_country)

    # Lowercase the dataset
    def lower(x):
        """
        Lowers capitalization of all observations in a given str type column.
        """
        try:
            return x.lower()
        except:
            return x

    for col in temp_data.columns[temp_data.dtypes == object]:
        temp_data[col] = temp_data[col].apply(lower)
        temp_data[col] = temp_data[col].apply(clean_lists)

    # Finally, return the prepared dataframe
    return temp_data


####################################
### Trial Source Transformations ###
####################################

def infer_trial_products(data: pd.DataFrame):
    df = data.copy()
    tlogg.info("Inferring product names")
    # Build search string
    df["search_string"] = df["title"] + " " + df["intervention"]
    # Dump product names from database
    product_names = get_product_names()

    def get_name(val, product_names):
        list_vals = val.split()
        matches = []
        for name in product_names:
            if fuzz.partial_ratio(name, list_vals) > 80:
                matches.append(name)
        data = ",".join(matches)
        if len(data) == 0:
            data = None
        return data

    get_name_fn = partial(get_name, product_names=product_names)
    df["inferred_product"] = df["search_string"].apply(get_name_fn)
    return df


def trial_cleaner(data: pd.DataFrame):
    df = data
    tlogg.info("Starting trial_cleaner.")

    def lower(x):
        """
        Lowers capitalization of all observations in a given str type column.
        """
        return x.lower()

    def clean_lists(x):
        if "," in x:
            temp_list = x.split(",")
        elif ";" in x:
            temp_list = x.split(";")
        else:
            return x

        def clean_list_item(item: str = None):
            assert type(item) == str
            temp_item = item
            temp_item = temp_item.strip()
            temp_item = temp_item.replace('"', "")
            return temp_item

        return ",".join([clean_list_item(item) for item in temp_list])

    def rename_cols(X):
        X = X.rename(
            columns={
                "normed_spon_names": "sponsors",
                "source_register": "registry",
                "date_registration": "registration_date",
                "date_enrollement": "enrollment_date",
                "public_title": "title",
                "results_url_link": "results_link",
                "web_address": "data_source",
                "trialid": "trial_id",
            }
        )
        return X

    # Apply function
    df = rename_cols(df)
    for col in df.columns[df.dtypes == object]:
        df[col] = df[col].apply(lower)
        df[col] = df[col].apply(clean_lists)

    df["country_codes"] = df["countries"].apply(clean_country)
    tlogg.info(f'Trial Columns: {df.columns}')
    if 'target_enrollment' in df.columns:
        df["target_enrollment"] = cast_to_int(df.target_enrollment)
    return df


#########################
### Sponsor Transform ###
#########################

# TODO: SponsorTransform
# Expand any lists found.
# Clean sponsor names of all punctuation.
# Capitalize names.

def prep_product_sponsors(data: pd.DataFrame) -> pd.DataFrame:
    tlogg.info("Starting prep_product_sponsors")
    tlogg.info(
        f"Transforming frame of shape {data.shape} and columns {data.columns}")

    def filter_raw(df: pd.DataFrame) -> np.array:
        data_rows = df[df['Source?'] == 'No']
        return data_rows[['ID', 'Sponsor']].to_numpy()

    def clean_sponsors(sponsors_raw: np.array) -> pd.DataFrame:
        def split_list(sponsor_string: str) -> list:
            # Infer separator
            if ';' in sponsor_string:
                separator = ';'
            elif ',' in sponsor_string:
                separator = ','
            else:
                separator = None
            # Split the string or return unmodified
            if separator is not None:
                sponsors = sponsor_string.split(separator)
            else:
                sponsors = [sponsor_string]
            return sponsors

        def clean_punct(single_sponsor: str) -> str:
            return single_sponsor.translate(str.maketrans('', '', string.punctuation)).strip()

        link_id = 0
        product_sponsor_list = []
        for item in sponsors_raw:
            for sponsor in split_list(item[1]):
                product_sponsor_list.append(
                    (link_id, item[0], clean_punct(sponsor))
                )
                link_id += 1
        sponsor_frame = pd.DataFrame(product_sponsor_list, columns=[
                                     'link_id', 'product_id', 'sponsor_name'])
        return sponsor_frame[sponsor_frame.sponsor_name.str.len() > 1]

    def generate_sponsor_id(sponsor_name: str) -> str:
        return hashlib.sha1(sponsor_name.encode('utf-8')).hexdigest()

    raw_product_sponsors = filter_raw(data)
    prepared_product_sponsors = clean_sponsors(raw_product_sponsors)
    prepared_product_sponsors['sponsor_id'] = prepared_product_sponsors.sponsor_name\
        .apply(generate_sponsor_id)
    tlogg.info(f"prepared product sponsors {prepared_product_sponsors}")
    return prepared_product_sponsors


def prep_sponsors(data: pd.DataFrame) -> pd.DataFrame:
    tlogg.info(
        f"Transforming frame of shape {data.shape} and columns {data.columns}")

    def filter_raw(df: pd.DataFrame) -> np.array:
        data_rows = df[df['Source?'] == 'No']
        return data_rows.Sponsor.to_list()

    def clean_sponsors(sponsors_raw: list) -> pd.DataFrame:
        def split_list(sponsor_string: str) -> list:
            # Infer separator
            if ';' in sponsor_string:
                separator = ';'
            elif ',' in sponsor_string:
                separator = ','
            else:
                separator = None
            # Split the string or return unmodified
            if separator is not None:
                sponsors = sponsor_string.split(separator)
            else:
                sponsors = [sponsor_string]
            return sponsors

        def clean_punct(single_sponsor: str) -> str:
            return single_sponsor.translate(str.maketrans('', '', string.punctuation)).strip()

        sponsor_list = []
        for item in sponsors_raw:
            for sponsor in split_list(item):
                sponsor_list.append(
                    clean_punct(sponsor)
                )
        sponsor_frame = pd.DataFrame({'sponsor_name': sponsor_list})
        return sponsor_frame[sponsor_frame.sponsor_name.str.len() > 1]

    def generate_sponsor_id(sponsor_name: str) -> str:
        return hashlib.sha1(sponsor_name.encode('utf-8')).hexdigest()

    raw_sponsors = filter_raw(data)
    prepared_sponsors = clean_sponsors(raw_sponsors)
    prepared_sponsors['sponsor_id'] = prepared_sponsors.sponsor_name.apply(
        generate_sponsor_id)
    return prepared_sponsors


def prep_product_sitelocation(data: pd.DataFrame):
    return Geolocation.transform(data)
