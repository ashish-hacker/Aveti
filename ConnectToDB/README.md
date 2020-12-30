# This is all about the Conneting Google Sheet to SQL server
For the purpose of authentication we are using Google Appscript. The credentials are stored in a pickle file and in a json file. To run the files make sure you have all the files and credentials.

So make sure to follow these steps if you haven't:
## Step 1 and 2 from this:
[Enable Google Sheets API](https://developers.google.com/sheets/api/quickstart/python)


Before running the commands below make sure you have all requirements satisfied i.e, installed all the necessary modules and cloned the repository properly. And make sure that you are on right directory to run the commands i.e, ``ConnectToDB`` Folder.


## To pass the Sheet ID and the Range for data transfer to the SQL Table
If you want to pass a new sheet URL than your previous run , set the number in `lastRow.txt` to 0, so that the script will read from row number 0.
To get the sheetID and and the Range to be scraped , You can directly pass the URL to the sheet and after the URL specifying the Range after a ',' to the ``sql.py``. Example below:
``python3 sql.py "[URL to the sheet],[range]" ``

 `` python3 sql.py "https://docs.google.com/spreadsheets/d/1gJKZmIuckbdHhGDJ7xqokvmDasSfGShHDh6gZxs-ajke/edit#gid=0,A1:H100"``

The above code will transfer first 99 data rows from Google sheet of the specified URL to the SQL Table.

For details about the code you can check ``sql.py`` file.

## Data Transfer from Google Sheets to SQL Table

Table create SQL statement, Insert SQL statement and Table Name is specified in the `sql.py` file.

To transfer the data you need to execute the following command:
``python3 sql.py "[URL to the sheet],[range]"``

This will check if the Table is created in the SQL server, If not it will create the table with specified name. 
Then it keeps track of the row numbers inserted to the SQL Table in `lastRow.txt` file, and then it keeps on updating the last row number inserted to the table. This is to confirm that no rows are inserted more than once.



