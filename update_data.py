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

# Open the Google Sheet by its ID
sheet = client.open_by_key("1QiDkMOz-xppKFG5UEf-zMbuE5_0yZFhorALU-mbfn8w").sheet1

# Fetch all data from the sheet, including headers and empty cells
all_rows = sheet.get_all_values()
headers = all_rows[0]  # The first row contains the headers

# Initialize an empty list to store data
data_list = []

# Iterate over rows (skip the header row)
for row_idx, row in enumerate(all_rows[1:], start=2):
    # Create a dictionary for each row dynamically based on headers
    row_data = {}
    for col_idx, header in enumerate(headers):
        row_data[header] = row[col_idx].strip()  # Add each column value to the dictionary

    # Generate a UUID if it doesn't exist
    if "UUID" not in row_data or not row_data["UUID"]:
        new_uuid = str(uuid.uuid4())  # Generate a unique UUID
        uuid_col_idx = headers.index("UUID") if "UUID" in headers else len(headers)  # Find or add UUID column
        sheet.update_cell(row_idx, uuid_col_idx + 1, new_uuid)  # Write the new UUID back to the sheet
        row_data["UUID"] = new_uuid  # Use the new UUID for this record

    # Append the row data to the list
    data_list.append(row_data)

# Reverse the data list to ensure the newest entry is at the top
data_list.reverse()

# Build the JSON data structure dynamically
data = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["data"],
    "properties": {
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["UUID"],  # Only UUID is required
                "properties": {
                    # Dynamically generate properties based on headers
                    **{header: {"type": "string"} for header in headers}
                }
            }
        }
    },
    "data": data_list  # Include the list of data in the JSON
}

# Save the JSON data to a file
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)

print("data.json updated with dynamic headers and persistent UUIDs!")
