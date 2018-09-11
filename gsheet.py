import numpy as np
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import pygsheets

# change this client_secret to your client secret(Keep it safe), which can be obtained google API wesite.
# And there are a lot of tutorial for this part.
client_secret = /dir1/dir2/your_client_secret.json

class google_df(object):
    def __init__(self):
        gc = pygsheets.authorize(outh_file=client_secret)
        print('Pygsheet Autorisation Done')
        self.ps = gc

    def get_all_name(self, verbose = 'name', show = 10):
        # get all the spreadsheet name and ID
        info = self.ps.list_ssheets()
        if verbose == 'name':
            for a, b in enumerate(list(map(lambda x: x['name'], info))[:show]):
                print('{} Name: {}'.format(a+1, b))
        elif verbose == 'both':
            for a, b in enumerate(list(map(lambda x: (x['name'], x['id']), info))[:show]):
                print('{} Name: {}\nID:{}\n{}'.format(a+1, b[0], b[1], '-'*20))
        else: raise Exception('verbose error')

    def get_all_sheetname(self, filename):
        file1 = self.ps.open(filename)
        print('All the sheets in the workbook: {}'\
             .format(file1.worksheets()))

    def create_spreadsheet(self, filename, edit = False):
        # Use for create a workbook
        self.ps.create(filename)
        if edit == True:
            return self.open_spreadsheet(filename, show=False)
        else: pass
    
    def open_spreadsheet(self, filename, show =True):
        # Open workbook
        file1 = self.ps.open(filename)
        if show == True:
            print('All the sheets in the workbook: {}'\
            .format(file1.worksheets()))
        else: pass

        def add_work_sheet(sheetname, row = '200', col='200'):
            file1.add_worksheet(sheetname,rows=row,cols=col)
            return print('sheet: {} is added/n rows = {}/n col = {}'.format(sheetname, row, col))
        return file1
    
    def sheet2df(self, filename, sheetname):
        # get as a dataframe from sheet
        gsheet = self.open_spreadsheet(filename, show=False).worksheet_by_title(sheetname)
        df_NaN = gsheet.get_as_df().replace(r'^\s*$', np.nan, regex=True)
        df_NaN = df_NaN[[i for i in df_NaN.columns if i !='']]
        return df_NaN

    def df2sheet(self, filename, sheetname, df):
        # upload a dataframe to googlesheet
        gsheet = self.open_spreadsheet(filename, show=False)
        allsheet = [str(i)[12:-10] for i in gsheet.worksheets()]
        df_no_NaN = df.fillna('', axis=1)
        if sheetname in allsheet:
            sheet1 = gsheet.worksheet_by_title(sheetname)
            sheet1.clear()
            sheet1.set_dataframe(df_no_NaN, (1,1), fit=True)
            print('update sucessfully!')
        else:
            gsheet.add_worksheet(sheetname)\
            .set_dataframe(df_no_NaN, (1,1), fit=True)
            print('The sheetname does not exist, but created, update sucessfully!')
