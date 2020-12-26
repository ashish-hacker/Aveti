import re
import sys

user = 'ashish'
password = "AshishSQL100@2020"
host = "localhost"
database = "mydatabase"


#url = https://docs.google.com/spreadsheets/d/           1gJKZmIuckbdHhGDJ7xqokvmDexNYdlpEU6gZxs-ajdw/edit#gid=0
# The ID and range of a sample spreadsheet.
url_range = sys.argv[1]
url, ranges = url_range.split(",")
url_array = url.split("/")
SAMPLE_SPREADSHEET_ID = url_array[5]
SAMPLE_RANGE_NAME = ranges