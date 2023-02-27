# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# library modules
import os
import base64
import gspread
import json
import warnings

def get_gspread(credentials_key='CREDENTIALS_JSON'):
    credentialsb64 = os.getenv(credentials_key)
    credentials = base64.b64decode(credentialsb64)
    json_credentials = json.loads(credentials)
    gs = gspread.service_account_from_dict(json_credentials)
    return gs
