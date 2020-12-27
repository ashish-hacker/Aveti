from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import mysql.connector
import MySQLCredentials as mc
import datetime
import logging
import sys
import re

logs = logging.getLogger()
#from oauth2client.service_account import ServiceAccountCredentials
#url = https://docs.google.com/spreadsheets/d/           1gJKZmIuckbdHhGDJ7xqokvmDexNYdlpEU6gZxs-ajdw/edit#gid=0
# The ID and range of a sample spreadsheet.
url_range = sys.argv[1]
url, ranges = url_range.split(",")
url_array = url.split("/")
SAMPLE_SPREADSHEET_ID = url_array[5]
SAMPLE_RANGE_NAME = ranges


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def insertDataToSQL(data, sql_statement, TableName):
    connection = mysql.connector.connect(
        user = mc.user,
        password = mc.password,
        host = mc.host,
        database = mc.database,
        #auth_plugin='mysql_native_password'
        ) 
    connection.autocommit = True
    cursor = connection.cursor(buffered=True)
    
    f = open("lastRow.txt", "r+")
    x = int(f.read())
    f.close()
    rown = x   
    for i in range(len(data)):   
        insert_data = sql_statement.format(TableName)
        cursor.execute("SELECT COUNT(*) FROM {};".format(TableName))
        RowCount = cursor.fetchone()[0]
        print("Total Rows Now in the SQL Table is:", RowCount)
        if i >= x:
            cursor.execute(insert_data, data[i])
            rown += 1
    f = open("lastRow.txt", "w")
    f.write(str(rown))
    f.close()
    
    if connection.is_connected():
        cursor.close()
        connection.close()
        logs.info('MySQL connection is closed.')
    


def createSQLTable(TableName, sql_statement):
    connection = mysql.connector.connect(
        user = mc.user,
        password = mc.password,
        host = mc.host,
        database = mc.database,
        #auth_plugin='mysql_native_password'
        ) 
    connection.autocommit = True
    cursor = connection.cursor(buffered=True)
    
    try:
        sql_create_table = sql_statement.format(TableName)
        cursor.execute(sql_create_table)
    except mysql.connector.ProgrammingError as e:
        print(e)
        logs.info(e)
    #connection.commit()
    if connection.is_connected():
        cursor.close()
        connection.close()
        logs.info('MySQL connection is closed.')
    




def getData():
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
    result = sheet.values().get(spreadsheetId= SAMPLE_SPREADSHEET_ID,
                                range= SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    for value in values[1:]:
        #print(value[0])
        #value[0] = value[0].replace('/', '-')
        value[0] = datetime.datetime.strptime(value[0], '%d/%m/%Y %H:%M:%S')
        userScore = value[1][0]
        FullScore = value[1][-2:]
        #print(value)
        #print(userScore, FullScore)
        del(value[1])
        value.insert(1,FullScore)
        value.insert(1,userScore)
        if len(value) == 8:
            value.append("")
        value = tuple(value)
        #print(value)

    if not values:
        #print('No data found.')
        return None
    else:
        #print(values[0])
        return values[1:]


def main():
    data = getData()
    sql_insert_statement = """INSERT INTO {}( 
            TimeStamp,
            UserScore,
            FullScore,
            Name,
            School,
            Block,
            District,
            PhoneNo,
            IsInstalledApp
            )
            VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s );"""
    
    sql_create_table = """CREATE TABLE {}( 
            TimeStamp DATETIME,
            UserScore VARCHAR(10),
            FullScore VARCHAR(10),
            Name VARCHAR(100),
            School VARCHAR(100),
            Block VARCHAR(100),
            District VARCHAR(100),
            PhoneNo VARCHAR(13),
            IsInstalledApp VARCHAR(10)
            );"""
    createSQLTable("exam", sql_create_table)
    insertDataToSQL(data, sql_insert_statement, "exam")

           
            
if __name__ == "__main__":
    main()
    connection = mysql.connector.connect(
        user = mc.user,
        password = mc.password,
        host = mc.host,
        database = mc.database,
        #auth_plugin='mysql_native_password'
        ) 
    connection.autocommit = True
    cursor = connection.cursor(buffered=True)
    cursor.execute("select * from exam")
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)
