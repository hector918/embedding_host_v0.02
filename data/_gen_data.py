# TODO: Add dataset description print for tuning hyperparameters like max_len.

# importing packages
import os
import sys

import pandas as pd

import psycopg2
from sqlalchemy import create_engine
from urllib.parse import quote_plus



# configuration
_db_meta = {
    "HOST":"150.230.113.32",
    "PORT":"8899",
    "USER": "yima",
    "PASSWORD": "yima@09012024",
    "DB_TABLES": {
        "rss_embedding": ["news_2024",],
        "rss_reader": [
            "z_rss_t_bbc_world",
            "z_rss_t_google",
            "z_rss_t_washingtonpost_world",
            ],
    },
}

root = "/scratch/ym2380/data/news"



# get dataframe helper
def get_df(db_name):
    '''
    WARNING: The function is not tested on rss_embedding table
    '''
    assert db_name in _db_meta["DB_TABLES"], f"Don't recognise {db_name}!"

    encoded_password = quote_plus(_db_meta["PASSWORD"])
    db_url = f"postgresql://{_db_meta['USER']}:{encoded_password}@{_db_meta['HOST']}:{_db_meta['PORT']}/{db_name}"
    engine = create_engine(db_url)

    dfs = list()
    required_columns = ["title", "description", "key_infomation"]   ### COMMENT: Original table has the typo
    for table_name in _db_meta["DB_TABLES"][db_name]:
        query = f"SELECT * FROM public.{table_name}"
        df = pd.read_sql(query, engine)

        try:
            df = df[required_columns]
        except KeyError as e:
            missing_columns = list(e.args[0])
            raise KeyError(f"Required columns are missing: {missing_columns}") 
        df.rename(columns={"key_infomation": "key_information"}, inplace=True)

        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)


    '''
    query = f"SELECT * FROM public.{_db_meta['DB_TABLES'][db_name]}"
    
    df = pd.read_sql(query, engine)

    if db_name == "rss_embedding":
        df.rename(columns={"publish_datetime": "datetime", "key_infomation": "key_information"}, inplace=True)
        df.drop(columns=["id", "hash_code", "table_name", "origin_url", "embedding"], inplace=True)
    '''
    return df


