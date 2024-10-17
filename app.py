from flask import Flask, render_template, request, redirect, url_for
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import datetime

# Flask app initialization
app = Flask(__name__)

# Google Sheets API setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Replace this with your actual spreadsheet ID and range
SPREADSHEET_ID = '1wofU_lZ1Fqf-YhWO0kl4FMrjOvsLK4XsPpGrpbBTe3k'
SHEET_NAME = 'Sheet1!A:C'  # Assuming columns: [Name, Doubt, Date]

def get_sheets_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('sheets', 'v4', credentials=creds)
    return service.spreadsheets()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_doubt', methods=['POST'])
def submit_doubt():
    student_name = request.form['studentName']
    doubt = request.form['doubt']
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Append the data to Google Sheets
    sheets_service = get_sheets_service()
    values = [[student_name, doubt, current_date]]
    body = {'values': values}
    
    sheets_service.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=SHEET_NAME,
        valueInputOption='RAW',
        body=body
    ).execute()

    return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

# if __name__ == '__main__':
#     app.run(debug=True, port=8000)


