import os
import json
import gspread
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

def run_automation():
    # --- 1. AUTHENTICATION ---
    try:
        creds_json = os.environ.get("GCP_SERVICE_ACCOUNT_KEY")
        if not creds_json:
            print("Error: GCP_SERVICE_ACCOUNT_KEY not found in environment.")
            return

        creds_dict = json.loads(creds_json)
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
    except Exception as e:
        print(f"Authentication Error: {e}")
        return

    # --- 2. SCRAPING LOGIC ---
    urls = {"Caloocan": "https://www.accuweather.com/en/ph/caloocan/264875/air-quality-index/264875",
            "Las Piñas":"https://www.accuweather.com/en/ph/las-pi%C3%B1as/264877/air-quality-index/264877",
            "Makati":"https://www.accuweather.com/en/ph/makati-city/21-264878_1_al/air-quality-index/21-264878_1_al",
            "Malabon": "https://www.accuweather.com/en/ph/san-roque/761333/air-quality-index/761333",
            "Mandaluyong": "https://www.accuweather.com/en/ph/mandaluyong/768148/air-quality-index/768148",
            "Manila": "https://www.accuweather.com/en/ph/manila/264885/air-quality-index/264885",
            "Marikina": "https://www.accuweather.com/en/ph/marikina-heights/1707180/air-quality-index/1707180",
            "Muntinlupa": "https://www.accuweather.com/en/ph/muntinlupa/264879/air-quality-index/264879",
            "Navotas": "https://www.accuweather.com/en/ph/navotas/765956/air-quality-index/765956",
            "Parañaque": "https://www.accuweather.com/en/ph/don-bosco/3424484/air-quality-index/3424484",
            "Pasay": "https://www.accuweather.com/en/ph/pasay-city/2-264881_1_al/air-quality-index/2-264881_1_al",
            "Pasig": "https://www.accuweather.com/en/ph/pasig/264876/air-quality-index/264876",
            "Pateros": "https://www.accuweather.com/en/ph/pateros/764136/air-quality-index/764136",
            "Quezon City": "https://www.accuweather.com/en/ph/quezon-city/264873/air-quality-index/264873",
            "San Juan": "https://www.accuweather.com/en/ph/san-juan/264882/air-quality-index/264882",
            "Taguig": "https://www.accuweather.com/en/ph/taguig/759349/air-quality-index/759349",
            "Valenzuela": "https://www.accuweather.com/en/ph/valenzuela/3424474/air-quality-index/3424474"}

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    cities = {}

    # Scrape
    for city, url in urls.items():
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            pols_idx_divs = soup.find_all("div", class_="pollutant-index")
            pols_idx = [div.text for div in pols_idx_divs][::2]
            if len(pols_idx) >= 4:
                cities[city] = {
                    "PM2.5": int(float(pols_idx[0].strip())),
                    "PM10": int(float(pols_idx[2].strip())),
                    "O3": int(float(pols_idx[1].strip())),
                    "NO2": int(float(pols_idx[3].strip()))
                }

    # --- 3. PREPARE DATA (Separating Date and Time) ---
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    final_data = [["City / Municipality", "Date Scraped", "Time Scraped", "PM 2.5", "PM 10", "O3", "NO2"]]

    for city in sorted(cities.keys()):
        data = cities[city]
        final_data.append([
            city,
            date_str,
            time_str,
            data["PM2.5"],
            data["PM10"],
            data["O3"],
            data["NO2"]
        ])

    # --- 4. OVERWRITE ---
    if len(final_data) > 1:
        sheet = client.open("[DSA4154] Group 3 Scraped Data Output").sheet1
        sheet.clear()
        sheet.update(final_data, 'A1')
        print(f"Success! Updated {len(final_data) - 1} cities.")

if __name__ == "__main__":
    run_automation()
