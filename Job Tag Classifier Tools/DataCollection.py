"""
Matthew Ciolino - Job Tag Classifier
Collection of data collection functions that imports
and cleans our data before feature engineering
"""
from sqlalchemy import create_engine
from nltk.corpus import wordnet
import pandas as pd
import numpy as np
import traceback
import psycopg2
import sys


def load_data(data_file):
    try:
        df = pd.read_csv(data_file)
    except:
        print("ERROR: Unable to read data into pandas dataframe")
        traceback.print_exc(file=sys.stdout)
        sys.exit(0)
    return df


def remove_unwanted_rows(df):

    def detect_non_english(sentence, m=0):
        for words in sentence:
            if m == 2:
                return True
            if not wordnet.synsets(words):
                return False
            m = m + 1

    try:
        # remove empty title/descriptions
        df['job_description'].replace('', np.nan, inplace=True)
        df['job_title'].replace('', np.nan, inplace=True)
        df.dropna(subset=['job_description'], inplace=True)
        df.dropna(subset=['job_title'], inplace=True)
        # remove non english rows
        df = df[df.job_title.map(lambda x: detect_non_english(x))]
    except:
        print("ERROR: Unable to remove unwanted rows from the dataframe")
        traceback.print_exc(file=sys.stdout)
        sys.exit(0)
    return df


def add_new_data(df, file_name):
    try:
        with open(file_name, 'a') as f:
            df.to_csv(f, header=False)
    except:
        print("ERROR: Unable to save new dataframe to sql table")
        traceback.print_exc(file=sys.stdout)
        sys.exit(0)

    df.check_size

    return True if length > 25 else False


def data_collection(data_file):

    df = load_data(data_file)
    df = remove_unwanted_rows(df)

    return df
