import os
import json
import gspread
import requests
import re
import time
from bs4 import BeautifulSoup
from datetime import datetime
from google.oauth2.service_account import Credentials

def run_automation():
    # --- 1. AUTHENTICATION (Dual: GitHub & Local) ---
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds_json = os.environ.get("GCP_SERVICE_ACCOUNT_KEY")
        
        if creds_json:
            # If running on GitHub
            creds_info = json.loads(creds_json)
            creds = Credentials.from_service_account_info(creds_info, scopes=scope)
        else:
            # Fallback for local testing in PyCharm
            creds = Credentials.from_service_account_file("creds.json", scopes=scope)

        client = gspread.authorize(creds)
        sheet = client.open("[DSA4154] Group 3 Scraped Data Output").sheet1
        print("✅ Auth Success")
    except Exception as e:
        print(f"Authentication Error: {e}")
        return

    # --- 2. SCRAPING LOGIC ---
    urls = {
        "Caloocan": "https://www.accuweather.com/en/ph/caloocan/264875/air-quality-index/264875",
        "Las Piñas": "https://www.accuweather.com/en/ph/las-pi%C3%B1as/264877/air-quality-index/264877",
        "Makati": "https://www.accuweather.com/en/ph/makati-city/21-264878_1_al/air-quality-index/21-264878_1_al",
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
        "Valenzuela": "https://www.accuweather.com/en/ph/valenzuela/3424474/air-quality-index/3424474"
    }

    cities = {}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0"}

    for city, url in urls.items():
        print(f"Scraping {city}...")
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the pollutant indices
            pols_idx_divs = soup.find_all("div", class_="pollutant-index")

            # Use original slicing logic but clean the text first
            pols_texts = [div.get_text(strip=True) for div in pols_idx_divs]

            # Extract just the numbers to prevent "0" or "ValueError"
            clean_indices = []
            for t in pols_texts:
                match = re.search(r'\d+', t)
                clean_indices.append(int(match.group()) if match else 0)

            # Slicing logic from your original bridge
            pols_idx = clean_indices[::2]

            if len(pols_idx) >= 4:
                cities[city] = {
                    "PM2.5": pols_idx[0],
                    "PM10": pols_idx[1],
                    "O3": pols_idx[3],
                    "NO2": pols_idx[2]
                }
                
            # Crucial: Website blocks you if you don't wait between requests
            time.sleep(2)

    # --- 3. PREPARE DATA ---
    lats_longs = {"Caloocan": {"Latitude":14.6489905, "Longitude":120.985759},
                  "Las Piñas": {"Latitude":14.4495367, "Longitude":120.9800033},
                  "Makati": {"Latitude":14.5704593, "Longitude":121.0246962},
                  "Malabon": {"Latitude":14.6576887, "Longitude":120.9483737},
                  "Mandaluyong": {"Latitude":14.5777433, "Longitude":121.0311517},
                  "Manila": {"Latitude":14.5895137, "Longitude":120.9790363},
                  "Marikina": {"Latitude":14.6330712, "Longitude":121.0965852},
                  "Muntinlupa": {"Latitude":14.3950501, "Longitude":121.0416651},
                  "Navotas": {"Latitude":14.6580425, "Longitude":120.9452721},
                  "Parañaque": {"Latitude":14.4705872, "Longitude":121.0196963},
                  "Pasay": {"Latitude":14.5437, "Longitude":120.9922929,},
                  "Pasig": {"Latitude":14.5596217, "Longitude":121.0786218},
                  "Pateros": {"Latitude":14.5420872, "Longitude":121.0620681},
                  "Quezon City": {"Latitude":14.6464639, "Longitude":121.0475227},
                  "San Juan": {"Latitude":14.6050626, "Longitude":121.0269975},
                  "Taguig": {"Latitude":14.528924, "Longitude":121.0673155},
                  "Valenzuela": {"Latitude":14.528924, "Longitude":121.0673155}}

    now = datetime.now()
    day_str = now.strftime("%A")
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    final_data = [["City / Municipality", "Date Scraped", "Day / Time Scraped", "Latitude", "Longitude", "PM 2.5", "PM 10", "O3", "NO2"]]

    for city in sorted(cities.keys()):
        data = cities[city]
        final_data.append([
            city,
            date_str,
            f"{day_str}, {time_str}",
            str(lats_longs[city]["Latitude"]),
            str(lats_longs[city]["Longitude"]),
            data["PM2.5"],
            data["PM10"],
            data["O3"],
            data["NO2"]
        ])

    # --- 4. OVERWRITE SHEET ---
    if len(final_data) > 1:
        sheet.clear()
        sheet.update(final_data, 'A1')
        print(f"✅ Success: {len(final_data) - 1} cities updated.")

if __name__ == "__main__":
    run_automation()
