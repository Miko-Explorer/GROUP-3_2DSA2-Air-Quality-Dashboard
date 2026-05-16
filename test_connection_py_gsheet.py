import os
import json
import gspread
from google.oauth2.service_account import Credentials

def test_connection():
    print("🧪 Starting Connection Test...")
    
    # --- 1. AUTHENTICATION SETUP ---
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    
    try:
        # Check if running on GitHub or Locally
        creds_json = os.environ.get("GCP_SERVICE_ACCOUNT_KEY")
        
        if creds_json:
            print("☁️ Detected GitHub environment. Using Secrets...")
            creds_info = json.loads(creds_json)
            creds = Credentials.from_service_account_info(creds_info, scopes=scope)
        else:
            print("💻 Detected Local environment. Looking for creds.json...")
            creds = Credentials.from_service_account_file("creds.json", scopes=scope)

        # --- 2. TRY TO CONNECT ---
        client = gspread.authorize(creds)
        
        # Replace with your exact sheet name
        sheet_name = "[DSA4154] Group 3 Scraped Data Output"
        sheet = client.open(sheet_name).sheet1
        
        # --- 3. TRY TO READ ---
        cell_value = sheet.acell('A1').value
        
        print("-" * 30)
        print(f"✅ CONNECTION SUCCESSFUL!")
        print(f"📄 Sheet Found: {sheet_name}")
        print(f"📥 Content of Cell A1: {cell_value}")
        print("-" * 30)

    except FileNotFoundError:
        print("❌ Error: 'creds.json' not found in this folder.")
    except json.JSONDecodeError:
        print("❌ Error: 'creds.json' is not a valid JSON file.")
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"❌ Error: Could not find a sheet named '{sheet_name}'.")
        print("💡 Check the spelling or ensure you shared the sheet with the Service Account email.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_connection()
