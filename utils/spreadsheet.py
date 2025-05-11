from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
 
SERVICE_ACCOUNT_FILE = './google-sheets-api.json'
 
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
 
credential = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
 
SPREADSHEET_ID = '176cmvosMUzcpj_I4N_I8ZUOnnC1Wbgc89djbxERB2ZI'
RANGE_NAME = 'Sheet1!A1:J900'
 
def insertToSpreadsheet(values_list):
    try:
        service = build('sheets', 'v4', credentials=credential)
        sheet = service.spreadsheets()
        values = values_list
        body = {
            'values': values
        }
 
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            body=body
        ).execute()
 
        print("Spreadsheet Message: Berhasil menambahkan data ke spreadsheet!")
    except Exception as e:
         print(f"An error occurred: {e}")
         