import gspread
import json
import base64
import gspread
from google.oauth2.service_account import Credentials
import os


# open google sheet 'googleIntegrator'
def open_google():
    credentials_json_string = os.environ.get('credentials_json_string')
    credentials_json = json.loads(base64.b64decode(credentials_json_string))
    sheet_id = os.environ.get('sheet_id')
    # Collect all environment variables that start with 'param'
    params = {key: os.environ[key] for key in os.environ if key.startswith('param')}

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    creds = Credentials.from_service_account_info(credentials_json, scopes=scopes)
    client = gspread.authorize(creds)

    book = client.open_by_key(sheet_id)

    return book, params

