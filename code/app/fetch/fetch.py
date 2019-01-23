from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pandas as pd


SPREADSHEET_ID = "1B2oDDPR1MF5OtFd3ZH89d01uEhRS8wyK-9uv8934gjA"
RANGE_NAME = "Statement of Activity Detail"


def get_google_sheet(spreadsheet_id, store, secret):
    """ Retrieve sheet data using OAuth credentials and Google Python API. """
    scopes = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    # Setup the Sheets API
    # store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(secret, scopes)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    range_name = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()["sheets"][0]["properties"]["title"]
    gsheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    return gsheet


def gsheet2df(gsheet):
    """ Converts Google sheet data to a Pandas DataFrame.
    Note: This script assumes that your data contains a header file on the first row!
    Also note that the Google API returns 'none' from empty cells - in order for the code
    below to work, you'll need to make sure your sheet doesn't contain empty cells,
    or update the code to account for such instances.
    """
    values = gsheet.get('values', [])[:]  # Everything else is data.

    if not values:
        print('No data found.')
    else:
        df = pd.DataFrame(data=values)
        return df

def get_sheet(spreadsheet_id, store, secret):
    return gsheet2df(get_google_sheet(spreadsheet_id,
        store, secret))
