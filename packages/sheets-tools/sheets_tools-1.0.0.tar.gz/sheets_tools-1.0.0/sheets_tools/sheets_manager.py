# sheets_manager.py

# %% PACKAGES
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from gspread_dataframe import get_as_dataframe,set_with_dataframe
import re

# %% CONSTANTS
scopes= ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/drive.file']

# %% CLASSES
class ServiceAccount:
    def __init__(self, keys_file, scopes):
        self.credentials = Credentials.from_service_account_file(keys_file, scopes=scopes)
        #initialize the creds and client
        self.client = gspread.authorize(self.credentials)

class SpreadSheet(ServiceAccount):
    def __init__(self, keys_file,scopes, url):
        super().__init__(keys_file, scopes)
        self.spreadsheet = self.client.open_by_url(url)

    def get_worksheets_name(self):
        return [re.findall("'(.*)'", str(x))[0] for x in self.spreadsheet.worksheets()]

    def get_worksheet(self, name):
        return self.spreadsheet.worksheet(name)

    def new_worksheet(self, name, rows=1000, cols=1000):
        self.spreadsheet.add_worksheet(title=name, rows=rows, cols=cols)

    def read(self, name, **options):
        worksheet = self.get_worksheet(name)
        df_ = get_as_dataframe(worksheet, evaluate_formulas=True,**options)
        df_ = df_.loc[:, ~df_.columns.str.contains('^Unnamed')]
        df_ = df_.dropna(how='all')
        return df_

    def write(self, name, df, **options):
        # if name doesnt exists, create worksheet first
        if (name in self.get_worksheets_name()) == False:
            self.new_worksheet(name)

        worksheet = self.get_worksheet(name)
        set_with_dataframe(worksheet, df ,include_index=False, **options)
