import os
import pandas as pd
import requests
from pandas import DataFrame
from io import StringIO
from urllib.parse import urlencode

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(**kwargs) -> DataFrame:
    password = os.environ.get('SPACETRACK_API_PW', '')
    identity = os.environ.get('SPACETRACK_USER', '')
    
    # Check if either password or identity is an empty string, indicating they weren't set correctly
    if not password or not identity:
        raise Exception("Environment variables for SpaceTrack API credentials are not set or empty.")

    url = "https://www.space-track.org/ajaxauth/login"

    # Dynamically include the identity and password in the payload
    query = "https://www.space-track.org/basicspacedata/query/class/satcat/norad_cat_id/4321/format/csv"
    payload = urlencode({
        'identity': identity,
        'password': password,
        'query': query
    })

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.request("POST", url, headers=headers, data=payload)

    # Check response status and handle potential errors before attempting to read the CSV data
    if response.status_code != 200:
        raise Exception(f"Failed to load data from API. Status code: {response.status_code}, Response: {response.text}")

    return pd.read_csv(StringIO(response.text))


@test
def test_output(df) -> None:
    """
    Template code for testing the output of the block.
    """
    assert df is not None, 'The output is undefined'
