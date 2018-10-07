import numpy as np
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import pygsheets

__version__ = "0.1.3"

# change this client_secret to your client secret(Keep it safe), which can be obtained google API wesite.
# And there are a lot of tutorial for this part.
client_secret = /dir1/dir2/your_client_secret.json

class google_df(object):
    def __init__(self):
        gc = pygsheets.authorize(outh_file=client_secret)
        print('Pygsheet Autorisation Done')
        self.ps = gc
        info = self.ps.list_ssheets()
        self.sheetlist = list(map(lambda x: x['name'], info))
        self.sheetlist_id = list(map(lambda x: (x['name'], x['id']), info))
        self.team = []
        
    def get_all_name(self, verbose = 'name', show = 10):
        separator = '-'*20
        # get all the spreadsheet name and ID
        print(f'Number of spreadsheet in the drive: {len(self.sheetlist)}')
        print(f'The first {show} are \n {separator}')
        if verbose == 'name':
            for a, b in enumerate(self.sheetlist[:show]):
                print(f'{a+1} Name: {b}')
        elif verbose == 'both':
            for a, b in enumerate(self.sheetlist_id[:show]):
                print(f'{a+1} Name: {b[0]} \n ID: {b[1]} \n {separator}')
        else: 
            raise Exception('verbose error')

    def get_all_sheetname(self, filename):
        file1 = self.ps.open(filename).worksheets()
        sheets = []
        for a, b in enumerate(file1):
            sheets.append((f'{a+1} Name: {b.title}'))
        return sheets
            

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
            print(f'All the sheets in the workbook: {file1.worksheets()}')
        else: pass

        def add_work_sheet(sheetname, row = '200', col='200'):
            file1.add_worksheet(sheetname,rows=row,cols=col)
            return print(f'sheet: {sheetname} is added/n rows = {row}/n col = {col}')
        return file1
    
    def delete_spreadSheet(self, filename):
        if filename in self.sheetlist:
            self.ps.delete(title = filename)
        else: 
            print(f'{filename} do not exist')

    
    def str_detect(self, df):
        '''change column type to string!'''
        time_series = [i for i in df.columns if df[i].dtypes == np.dtype('datetime64[ns]')]
        for i in time_series:
            df[i] = df[i].astype(str)
        return df
    
    def sheet2df(self, filename, sheetname):
        # get as a dataframe from sheet
        if filename not in self.sheetlist:
            print(f'{filename} do not exist')
        elif filename in self.sheetlist:
            sheets = [i[8:] for i in self.get_all_sheetname(filename)]
            if sheetname not in sheets:
                print(f'{sheetname} do not exist')
            else:
                gsheet = self.open_spreadsheet(filename, show=False).worksheet_by_title(sheetname)
                df_NaN = gsheet.get_as_df().replace(r'^\s*$', np.nan, regex=True)
                df_NaN = df_NaN[[i for i in df_NaN.columns if i !='']]
                return df_NaN

    def df2sheet(self, filename, sheetname, df):
        # upload a dataframe to googlesheet
        df = self.str_detect(df)
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
            
     def share(self, filename, name = self.team):
        ''' name must be a list
            default is sharing with everyone in the data team. '''
        name2 = [i+'@gmail.com' for i in name]
        for i in name2:
            self.ps.open(filename).share(i)
            print(f'Sucessfully shared with {i}')
        print('sharing completed!')
