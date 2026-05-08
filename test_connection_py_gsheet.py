import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 1. Set up the Scope and Credentials:
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

try:
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    print("Step 1: Credentials accepted.")
except Exception as e:
    print(f"Step 1 Error: Could not read creds.json file. {e}")
    exit()

# 2. Attempt to open the Sheet:
sheet_name = "[DSA4154] Group 3 Scraped Data Output"

try:
    sheet = client.open(sheet_name).sheet1
    print(f"Step 2: Successfully connected to '{sheet_name}'.")
except Exception as e:
    print(f"Step 2 Error: Could not find the sheet. Did you share it with the bot email? {e}")
    exit()

# 3. Attempt a Test Write (Overwrite A1):
try:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    test_data = [["Connection Test", "Status", "Last Run"], ["Python to Google Sheets", "SUCCESSFUL", timestamp]]
    sheet.update('A1', test_data)
    print(f"Step 3: Data successfully written to the sheet at {timestamp}!")
    print("\nCheck your Google Sheet now. You should see the success message in cells A1:C2.")
except Exception as e:
    print(f"Step 3 Error: Connected to sheet, but failed to write data. {e}")