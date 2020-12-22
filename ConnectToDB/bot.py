from __future__ import print_function
from telegram.ext import Updater, CommandHandler
import requests
import re

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1QZdFqcIPacozq22JgdwjP2vQoKSB4-cFIuiFQTl-ubM'
SAMPLE_RANGE_NAME = 'C1:E9'

data_url = "https://docs.google.com/spreadsheets/d/1QZdFqcIPacozq22JgdwjP2vQoKSB4-cFIuiFQTl-ubM/edit?usp=sharing"

#chat_id = update.message.chat_id
http_API = "1215259726:AAECqFU9Wp5wOfL53I-JiBI4wPjLh7vJrpo"



def hello(update:Updater, context:CommandHandler):
    
    update.message.reply_text("Hii")



#def main():
    #updater = Updater("1215259726:AAECqFU9Wp5wOfL53I-JiBI4wPjLh7vJrpo")
    #dp = updater.dispatcher
    #dp.add_handler(CommandHandler('hello',hello))
    #updater.start_polling()
    #updater.idle()
    
def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    sum = 0
    msg = ''
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
        print('Name, Major:')
        for row in values[1:]:
            # Print columns A and E, which correspond to indices 0 and 4.
            #print('%s, %s' % (row[0], row[4]))
            sum += int(row[0])
        print(sum/len(values))
        msg = 'hello!! Average is ='+str(sum)
    updater = Updater("1215259726:AAECqFU9Wp5wOfL53I-JiBI4wPjLh7vJrpo")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('hello',hello))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

