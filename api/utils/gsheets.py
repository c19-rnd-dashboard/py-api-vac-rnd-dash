import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd
from api.config import Config


class GSheet:
    def __init__(self, SPREADSHEET_ID, RANGE_NAME, SCOPES):
        self.spreadsheet_id = SPREADSHEET_ID
        self.range_name = RANGE_NAME
        self.scopes = SCOPES
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    Config.CRED_PATH, Config.SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

        self.service = build("sheets", "v4", credentials=creds)

    def get_google_sheet(self):
        # Call the Sheets API
        gsheet = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=self.spreadsheet_id, range=self.range_name)
            .execute()
        )
        return gsheet

    def gsheet2df(self):
        """ Converts Google sheet data to a Pandas DataFrame.
        Note: This script assumes that your data contains a header file on the first row!
        Also note that the Google API returns 'none' from empty cells - in order for the code
        below to work, you'll need to make sure your sheet doesn't contain empty cells,
        or update the code to account for such instances.
        """
        gsheet = self.get_google_sheet()
        header = gsheet.get("values", [])[0]  # Assumes first line is header!
        values = gsheet.get("values", [])[1:]  # Everything else is data.
        if not values:
            print("No data found.")
        else:
            all_data = []
            for col_id, col_name in enumerate(header):
                column_data = []
                for row in values:
                    column_data.append(row[col_id])
                ds = pd.Series(data=column_data, name=col_name)
                all_data.append(ds)
            df = pd.concat(all_data, axis=1)
            return df


gsheet = GSheet(Config.SPREADSHEET_ID, Config.RANGE_NAME, Config.SCOPES)
df = gsheet.gsheet2df()
print("Dataframe size = ", df.shape)
print(df.head())
