# googlesheet2df
A extremely light wrapper around **pygsheets** to obtain google sheet as a dataframe and upload dataframes to a google sheet

## script aim
The aim of this script is to find a qucik, easy and flexible way to upload to your desirable google sheet and transform google sheet into dataframe, so you don't need to import csv anymore.

## examples

### import the package
from gsheet import google_df  

### initialise the package
sess = google_df()

### get all the spreadsheet names
sess.get_all_name()

**default setting: verbose = 'name', show = 10**


**_get name and id_**<br><br>
sess.get_all_name(verbose = 'both)


**_show 50 spreadsheets_**<br><br>
sess.get_all_name(show=50)


### upload df to google_sheet
sess.df2sheet('spreadsheet_name', 'tab_name', 'df_name')


**if tab_name doesn't exist, it will create the tab with the tab_name in the spreadsheet.**

### download google_sheet and load as df
df = sess.sheet2df('spreadsheet_name', 'tab_name')
