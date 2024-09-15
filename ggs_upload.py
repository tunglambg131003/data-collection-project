import gspread 
from oauth2client.service_account import ServiceAccountCredentials

drive_spread_sheet_name = ""
csv_file_name = ""

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)

#gs_credentials.json on https://medium.com/craftsmenltd/from-csv-to-google-sheet-using-python-ef097cb014f9

client = gspread.authorize(credentials)

#Open

spreadsheet = client.open(drive_spread_sheet_name)

#Create
# spreadsheet = client.create(drive_spread_sheet_name, folder_id = '')

with open(csv_file_name, 'r') as file_obj:
    content = file_obj.read()
    client.import_csv(spreadsheet.id, data=content)
