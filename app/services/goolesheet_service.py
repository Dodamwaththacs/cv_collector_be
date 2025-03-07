from flask import request, jsonify
import gspread
from google.oauth2 import service_account
import json

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'service.json'

def get_sheets_service():
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        return gspread.authorize(credentials)

    except Exception as e:
        print(f"Error getting Google Sheets service: {e}")
        return None



def store_data():
    try:
        # Use hardcoded data instead of request data
        data = {
            'field1': 'Test value 1',
            'field2': 'Test value 2',
            'field3': 'Test value 3'
        }

        # Connect to Google Sheets
        gc = get_sheets_service()

        # Open the spreadsheet (by key or by URL)
        spreadsheet = gc.open_by_key('1JmHSY-th187MplfrNrIV-tS-zKJFhWNZNw8qr3YXJC8')  # or gc.open_by_url('URL')

        # Select a worksheet
        worksheet = spreadsheet.worksheet('Sheet1')  # or by index: spreadsheet.get_worksheet(0)

        # Append row to the spreadsheet
        row = [data.get('field1', ''), data.get('field2', ''), data.get('field3', '')]
        worksheet.append_row(row)
        print("Data stored successfully!")

        return jsonify({"success": True, "message": "Data stored successfully!"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500