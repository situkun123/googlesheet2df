# googlesheet2df
A extremely light wrapper around **pygsheets** to obtain google sheet as a dataframe and upload dataframes to a google sheet 

## script aim
The aim of this script is to find a qucik, easy and flexible way to upload dataframes to your desirable google sheet and transform google sheet into dataframe, so you don't need to import csv anymore.

## requirement
* [pygsheets](https://github.com/nithinmurali/pygsheets) - The core package powering this wrapper
<br>__following the link for installation__
* [google_sheets api](https://developers.google.com/sheets/api/)
* [google_drive api](https://developers.google.com/drive/)
<br>__Obtain OAuth2 credentials from Google Developers Console for google spreadsheet api and drive api and save the file as client_secret.json__
## exception
- Error will occur when headers are the same, make sure all headers are unique
## examples

### import the package and create session
```
from gsheet import google_df
sess = google_df()
```
- google will ask you to authorise your account when you initialise the session for the first time.
- Then it will save a copy of client_secret.json in the working directory

### get all the spreadsheet names
```
sess.get_all_name()
```
**default setting: verbose = 'name', show = 10**

- **_get name and id_**
```
sess.get_all_name(verbose = 'both)
```

- **_show 50 spreadsheets_**
```
sess.get_all_name(show=50)
```

### upload df to google_sheet
```
sess.df2sheet('spreadsheet_name', 'tab_name', 'df_name')
```

- **if tab_name doesn't exist, it will create the tab with the tab_name in the spreadsheet.**

### download google_sheet and load as df
```
df = sess.sheet2df('spreadsheet_name', 'tab_name')
```
