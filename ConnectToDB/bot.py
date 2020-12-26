""" 
This Program is not completed
"""


from __future__ import print_function
from telegram.ext import Updater, CommandHandler
import requests
import re


def main():
    updater = Updater("1215259726:AAECqFU9Wp5wOfL53I-JiBI4wPjLh7vJrpo")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('hello',hello))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

