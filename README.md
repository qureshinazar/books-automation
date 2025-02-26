# Books Automation

This repository automatically fetches data from a Google Sheet and updates a `data.json` file using GitHub Actions.

## How It Works
- The `update_data.py` script fetches data from Google Sheets.
- The GitHub Actions workflow runs the script daily and updates the `data.json` file.
- The updated `data.json` file is pushed back to the repository.

## Setup
1. Add your Google credentials as a secret (`GOOGLE_CREDENTIALS`) in the repository settings.
2. Update the `update_data.py` script with your Google Sheet ID.
3. The workflow will run automatically every day at midnight (UTC).