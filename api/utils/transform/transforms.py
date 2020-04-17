"""
Transforms

Contains custom source transforms
"""

from sqlalchemy import inspect
import pandas as pd
import numpy as np
from datetime import datetime
from api.models import *
from api.db import get_session
from dateutil.parser import parse
from fuzzywuzzy import fuzz
from functools import partial
import string
import logging
import pycountry


tlogg = logging.getLogger('.'.join(['api.app', __name__.strip('api.')]))

########################
### Helper Functions ###
########################


def get_columns(model):
    """ Get all column names from SQL Alchemy Model """
    inst = inspect(model)
    column_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
    return column_names


def convert_to_datetime(time_string):
    try:
        date_val = parse(time_string)
        if pd.isnull(date_val):
            return None
        return date_val
    except:
        return None


def get_product_names():
    """ Get all product preferred names currently in raw """
    with get_session() as session:
        prod_names = session.query(ProductRaw.preferred_name).all()
    return [x[0] for x in prod_names]


def clean_country(country_names: str) -> str:
    result = []
    for country in country_names.split(","):
        try:
            curr_country = pycountry.countries.search_fuzzy(country)
            result.append(curr_country[0].alpha_3)
        except LookupError:
            pass
        except Exception as e:
            tlogg.error(f"Error in country standardization {e}")
    if len(result) == 0:
        return None
    return ",".join(result)


def clean_lists(x):
    if x is None:
        return None 

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

##############################
### DataFrame Manipulation ###
##############################


def filter_columns(data: pd.DataFrame, model):
    """ Return only columns that match filter from DataFrame """
    valid_columns = set(get_columns(model))
    supplied_columns = set(data.columns)
    tlogg.info(f"Supplied Columns: {supplied_columns}\nValid Columns: {valid_columns}")
    filter_set = list(valid_columns.intersection(supplied_columns))
    return data[filter_set]


def cast_dates(data: pd.DataFrame):
    """ Check for date columns and cast objects as datetime """
    tlogg.info("Starting date casting")
    temp_data = data.copy()
    date_columns = [column for column in temp_data.columns if "date" in column]
    for col in date_columns:
        temp_data[col] = temp_data[col].apply(convert_to_datetime)
    return temp_data


def clean_null(data: pd.DataFrame):
    # Force all null values to None rather than mixed type with np.nan
    def replace_nat(x):
        if pd.isnull(x):
            return None
        return x
    def replace_empty_strings(x):
        if x == '':
            return None 
        return x

    temp_data = data
    temp_data = temp_data.where(data.notnull(), None)
    for col in temp_data.columns[temp_data.dtypes == object]:
        temp_data[col] = temp_data[col].apply(replace_empty_strings)
    # Date cleanup
    date_columns = [column for column in temp_data.columns if "date" in column]
    for col in date_columns:
        temp_data[col] = temp_data[col].apply(replace_nat)
    return temp_data


def drop_unnamed_columns(df:pd.DataFrame)->pd.DataFrame:
    keep_columns = [col for col in df.columns if len(col)>0]
    return df[keep_columns].copy()


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
    def get_unique_sources(row_list:list)->dict:
        url_list = []
        for item in row_list:
            if ('http' in item):
                if item not in url_list:
                    url_list.append(item)
        urls = ','.join(url_list)
        product_id = row_list[0]
        return {
        'product_id': product_id,
        'source': urls,
        }

    def clean_valid_sources(df:pd.DataFrame):
        data_rows = df.query("source == 'No'")
        source_rows = df.query("source == 'Yes'")
        
        clean_sources = []
        for i in range(len(source_rows)):
            row_list = source_rows.iloc[i].to_list()
            clean_sources.append(get_unique_sources(row_list=row_list))
        
        source_frame = pd.DataFrame(clean_sources)
        clean_frame = data_rows.drop(columns=['source']).merge(source_frame, on='product_id')
        
        return clean_frame
    
    temp_data = clean_valid_sources(temp_data)

    # Infer preferred_name from other names
    def build_missing_preferred_names(df:pd.DataFrame)->pd.DataFrame:
        def clean_(item):
            teststr = item
            return teststr.translate(str.maketrans('', '', string.punctuation)).replace(' ', '_')

        df1 = df.copy()
        for i in range(len(df)):
            row = df1.iloc[i]
            if len(row.preferred_name) < 2:
                if len(row.brand_name) > 0:
                    df1.iloc[i].preferred_name = clean_(row.brand_name)
                elif (len(row.sponsors) > 0) and (len(row.chemical_name) > 0):
                    df1.iloc[i].preferred_name = '-'.join([clean_(row.sponsors), row.chemical_name, row.product_id])
        
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

    return df
