import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
import uuid

# Initialize Google Sheets API
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
GOOGLE_CREDENTIALS = json.loads(os.environ['GOOGLE_CREDENTIALS'])
CREDS = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_CREDENTIALS, SCOPE)
client = gspread.authorize(CREDS)

# Open the sheet
sheet = client.open_by_key("1QiDkMOz-xppKFG5UEf-zMbuE5_0yZFhorALU-mbfn8w").sheet1  # Replace with your Sheet ID

# Fetch all data (including headers and empty cells)
all_rows = sheet.get_all_values()
headers = all_rows[0]  # First row is headers

# Find the index of the UUID column
try:
    uuid_col_idx = headers.index("UUID")  # 0-based index
except ValueError:
    raise Exception("No 'UUID' column found in the sheet. Add it manually first!")

books = []

# Iterate over rows (skip the header row)
for row_idx, row in enumerate(all_rows[1:], start=2):  # Row indices start at 2 in Google Sheets
    title = row[headers.index("Title")]
    author = row[headers.index("Author")]
    category = row[headers.index("Category")]
    pdf_url = row[headers.index("PDF URL")]
    existing_uuid = row[uuid_col_idx].strip()

    # Generate UUID only if it doesn't exist
    if not existing_uuid:
        new_uuid = str(uuid.uuid4())
        sheet.update_cell(row_idx, uuid_col_idx + 1, new_uuid)  # +1 because Sheets uses 1-based indexing
        existing_uuid = new_uuid

    books.append({
        "title": title,
        "author": author,
        "category": category,
        "pdf_url": pdf_url,
        "uuid": existing_uuid  # Use persisted UUID
    })

# Build JSON data
data = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["books"],
    "properties": {
        "books": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["title", "pdf_url", "uuid"],
                "properties": {
                    "title": {"type": "string"},
                    "pdf_url": {"type": "string", "format": "uri"},
                    "author": {"type": "string"},
                    "category": {"type": "string"},
                    "uuid": {"type": "string"}
                }
            }
        }
    },
    "books": books
}

# Save to data.json
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)

print("data.json updated with persistent UUIDs!")