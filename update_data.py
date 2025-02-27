import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
import uuid

# Initialize Google Sheets API
# Define the scope for accessing Google Sheets and Drive
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Load Google credentials from environment variable
GOOGLE_CREDENTIALS = json.loads(os.environ['GOOGLE_CREDENTIALS'])
CREDS = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_CREDENTIALS, SCOPE)
client = gspread.authorize(CREDS)

# Open the Google Sheet by its ID
# Replace the sheet ID with your own or use `client.open("Sheet Name")` to open by name
sheet = client.open_by_key("1QiDkMOz-xppKFG5UEf-zMbuE5_0yZFhorALU-mbfn8w").sheet1

# Fetch all data from the sheet, including headers and empty cells
all_rows = sheet.get_all_values()
headers = all_rows[0]  # The first row contains the headers

# Find the index of the "UUID" column
# This ensures the script knows where to read/write UUIDs
try:
    uuid_col_idx = headers.index("UUID")  # 0-based index
except ValueError:
    raise Exception("No 'UUID' column found in the sheet. Add it manually first!")

# Initialize an empty list to store book data
books = []

# Iterate over rows (skip the header row)
# `row_idx` starts at 2 because Google Sheets uses 1-based indexing
for row_idx, row in enumerate(all_rows[1:], start=2):
    # Extract data from each column
    title = row[headers.index("Title")]
    author = row[headers.index("Author")]
    category = row[headers.index("Category")]
    pdf_url = row[headers.index("PDF URL")]
    existing_uuid = row[uuid_col_idx].strip()  # Get the existing UUID (if any)

    # Generate a new UUID only if it doesn't exist
    if not existing_uuid:
        new_uuid = str(uuid.uuid4())  # Generate a unique UUID
        sheet.update_cell(row_idx, uuid_col_idx + 1, new_uuid)  # Write the new UUID back to the sheet
        existing_uuid = new_uuid  # Use the new UUID for this record

    # Append the book data to the list
    books.append({
        "title": title,
        "author": author,
        "category": category,
        "pdf_url": pdf_url,
        "uuid": existing_uuid  # Use the persisted UUID
    })

# Reverse the books list to ensure the newest entry is at the top
books.reverse()

# Build the JSON data structure
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
    "books": books  # Include the list of books in the JSON
}

# Save the JSON data to a file
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)

print("data.json updated with persistent UUIDs and newest entries at the top!")
