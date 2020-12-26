from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import mysql.connector
import MySQLCredentials as mc
import gspread
#from oauth2client.service_account import ServiceAccountCredentials
#AshishSQL100@2020


mydb = mysql.connector.connect(
  host = mc.host,
  user = mc.user,
  password = mc.password,
  database = mc.database,
  auth_plugin ='mysql_native_password'
)

mycursor = mydb.cursor(buffered=True)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1gJKZmIuckbdHhGDJ7xqokvmDexNYdlpEU6gZxs-ajdw'
SAMPLE_RANGE_NAME = 'A1:E9'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in values[1:]:
            print(row)
            # Insert the data into the SQL table lindata
            sql = "INSERT INTO lindata ({}, {}, {}, {}, {}, {}, {}, {}) VALUES (%s, %s, %s, %s, %s)".format(values[0][0], values[0][1], values[0][2], values[0][3], values[0][4], values[0][5], values[0][6]) 
            val = (row[0], row[1], row[2], row[3], row[4])
            mycursor.execute(sql, val)

            mydb.commit()

            print(mycursor.rowcount, "record inserted.")
            
            
if __name__ == "__main__":
    main()
    mycursor.execute("select * from exampledata")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
