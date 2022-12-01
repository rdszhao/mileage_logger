# %%
import requests
from pandas import json_normalize
import json
import datetime
import time
from os import remove
from pytz import UTC as utc
import gspread
import swagger_client
from swagger_client.rest import ApiException
from oauth2client.service_account import ServiceAccountCredentials
# %%
response = requests.post(
    url = 'https://www.strava.com/oauth/token',
    data = {
            'client_id': [60423],
            'client_secret': ['70452786e2068633e53d1a4e0fb13e674cda6380'],
            'code': ['3e69f37f0156c069c35a3e705311e4924b2b6052'],
            'grant_type': 'authorization_code'
            }
)
strava_tokens = response.json()
new_strava_tokens = response.json()
strava_tokens = new_strava_tokens
# %%
url = "https://www.strava.com/api/v3/activities"
configuration = swagger_client.Configuration()
configuration.access_token = strava_tokens['access_token']

# create an instance of the API class
api_instance = swagger_client.ActivitiesApi(swagger_client.ApiClient(configuration))
page = 1
per_page = 200

try: 
    # List Athlete Activities
    api_response = api_instance.get_logged_in_athlete_activities(page=page, per_page=per_page)
except ApiException as e:
    print(f"Exception when calling ActivitiesApi->getLoggedInAthleteActivities: {e}s\n")
# %%
start_date = datetime.datetime(2022, 11, 1)
id_df = json_normalize([r.__dict__ for r in api_response])
ids = id_df[id_df['_start_date_local'] >= utc.localize(start_date)]['_id'].to_list()
df = json_normalize([api_instance.get_activity_by_id(id) for id in ids])
# %%
df
# %%
# getting sheets
scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]
file_name = 'client_key.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
client = gspread.authorize(creds)
open('client_key.json', 'w').close(),
open('client_secret.json', 'w').close()
remove('client_key.json')
remove('client_secret.json')

# opening the sheet
sheet_name = 'SDDBT - CCNC Training' 
worksheet_name = 'Group 8'
sheet = client.open(sheet_name).worksheet(worksheet_name)