import io
import os
import pandas as pd
import requests
from pandas import DataFrame

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(**kwargs) -> DataFrame:
    """
    Template for loading data from API
    """
    password = os.environ.get('SPACETRACK_API_PW')
    identity = os.environ.get('SPACETRACK_USER')

    url = "https://www.space-track.org/ajaxauth/login"

    payload = 'identity={}&password={password}&query=https%3A%2F%2Fwww.space-track.org%2Fbasicspacedata%2Fquery%2Fclass%2Fsatcat%2Fnorad_cat_id%2F4321%2Fformat%2Fcsv'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.request("POST", url, headers=headers, data=payload)

    return pd.read_csv(response.text)


@test
def test_output(df) -> None:
    """
    Template code for testing the output of the block.
    """
    assert df is not None, 'The output is undefined'
