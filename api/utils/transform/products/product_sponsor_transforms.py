import pandas as pd 
import numpy as np 
import string
import hashlib

import logging

tlogg = logging.getLogger(__name__)

#########################
### Sponsor Transform ###
#########################


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
    tlogg.info("Starting prep_sponsors")
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