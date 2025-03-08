# Books Automation

This repository automatically fetches data from a Google Sheet and updates a `data.json` file using GitHub Actions.

## How It Works
- The `update_data.py` script fetches data from Google Sheets.
- The GitHub Actions workflow runs the script daily and updates the `data.json` file.
- The updated `data.json` file is pushed back to the repository.

## Setup
1. Add your Google credentials as a secret (`GOOGLE_CREDENTIALS`) in the repository settings.
2. Update the `update_data.py` script with your Google Sheet ID.
3. The workflow will run automatically every month

## Setting Up Google Sheets API

To fetch data from a Google Sheet, you need to enable the Google Sheets API and create credentials for authentication. Follow these steps to set up the Google Sheets API:

---

### Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click on the project dropdown at the top of the page and select **New Project**.
3. Give your project a name (e.g., `Books Automation`) and click **Create**.

---

### Step 2: Enable Google Sheets API and Google Drive API

1. In the Google Cloud Console, navigate to **APIs & Services > Library**.
2. Search for **Google Sheets API** and click on it.
3. Click **Enable** to enable the API for your project.
4. Repeat the process for the **Google Drive API**:
   - Search for **Google Drive API** and click on it.
   - Click **Enable**.

---

### Step 3: Create a Service Account

1. Go to **APIs & Services > Credentials**.
2. Click **Create Credentials** and select **Service Account**.
3. Give your service account a name (e.g., `books-automation`).
4. Assign the **Editor** role to the service account.
5. Click **Continue** and then **Done**.

---

### Step 4: Generate and Download Credentials

1. In the **Credentials** tab, find your service account and click on it.
2. Go to the **Keys** tab and click **Add Key > Create New Key**.
3. Select **JSON** as the key type and click **Create**.
4. A JSON file containing your credentials will be downloaded. Save this file securely.

---

### Step 5: Share the Google Sheet with the Service Account

1. Open your Google Sheet.
2. Click the **Share** button.
3. Add the email address of your service account (found in the JSON file) as an **Editor**.
4. Click **Send**.

---

### Step 6: Use the Credentials in Your Project

1. Add the JSON credentials file to your project or use its content as an environment variable.
2. In the Python script, use the `gspread` library to authenticate with the Google Sheets API using the credentials.

---

### Step 7: Add Credentials to GitHub Secrets (for GitHub Actions)

1. Go to your GitHub repository.
2. Navigate to **Settings** > **Secrets and variables** > **Actions**.
3. Add a new secret:
   - **Name**: `GOOGLE_CREDENTIALS`
   - **Value**: Paste the entire content of the JSON credentials file.

---

## Step 8: Verify Access

1. Run the Python script locally to ensure it can access the Google Sheet.
2. Check that the `data.json` file is created/updated with the correct data.

### Example: Authenticating with Google Sheets API

```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# Google Sheets API setup
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Paste your Google credentials here
GOOGLE_CREDENTIALS = {
    "type": "service_account",
    "project_id": "your-project-id",
    "private_key_id": "your-private-key-id",
    "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
    "client_email": "your-service-account-email@your-project-id.iam.gserviceaccount.com",
    "client_id": "your-client-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account-email%40your-project-id.iam.gserviceaccount.com"
}


# Authenticate using the credentials
CREDS = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_CREDENTIALS, SCOPE)
client = gspread.authorize(CREDS)

# Open the Google Sheet by ID or name
sheet = client.open_by_key("1QiDkMOz-xppKFG5UEf-zMbuE5_0yZFhorALU-mbfn8w").sheet1  # Replace with your Sheet ID or use client.open("Sheet Name")

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
```
---

## Troubleshooting

- **Error: SpreadsheetNotFound**
  - Ensure the Sheet ID is correct and the service account has access to the Google Sheet.
- **Error: Permission Denied**
  - Verify the service account has Editor access to the Google Sheet.
- **Error: Invalid Credentials**
  - Double-check the JSON credentials file and ensure it’s correctly set as an environment variable.

By following these steps, you can successfully set up the Google Sheets API and integrate it with your project.

