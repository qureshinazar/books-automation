import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

# Google Sheets API setup
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Read Google credentials from environment variable
GOOGLE_CREDENTIALS = json.loads(os.environ['GOOGLE_CREDENTIALS'])
CREDS = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_CREDENTIALS, SCOPE)
client = gspread.authorize(CREDS)

# Open the Google Sheet by ID or name
sheet = client.open_by_key("YOUR_SHEET_ID").sheet1  # Replace with your Sheet ID or use client.open("Sheet Name")

# Fetch all records
records = sheet.get_all_records()

# Format the data
books = []
for record in records:
    books.append({
        "title": record["Title"],
        "pdf_url": record["PDF URL"],
        "author": record["Author"],
        "category": record["Category"]
    })

data = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["books"],
    "properties": {
        "books": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["title", "pdf_url"],
                "properties": {
                    "title": {"type": "string"},
                    "pdf_url": {"type": "string", "format": "uri"},
                    "author": {"type": "string"},
                    "category": {"type": "string"}
                }
            }
        }
    },
    "books": books
}

# Write to data.json
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)

print("data.json updated successfully")