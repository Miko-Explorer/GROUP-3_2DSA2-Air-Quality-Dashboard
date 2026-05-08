import requests
from bs4 import BeautifulSoup

urls_pl = {"Caloocan": "https://air.plumelabs.com/air-quality-in-Caloocan%20City-7dun",
           "Taguig": "https://air.plumelabs.com/air-quality-in-City%20of%20Taguig-74ag",
           "Las Piñas": "https://air.plumelabs.com/air-quality-in-Las%20Pi%C3%B1as-7a74",
           "Makati": "https://air.plumelabs.com/air-quality-in-Makati%20City-798t",
           "Mandaluyong": "https://air.plumelabs.com/air-quality-in-Mandaluyong%20City-78L4",
           "Manila": "https://air.plumelabs.com/air-quality-in-Manila-78Gg",
           "Navotas": "https://air.plumelabs.com/air-quality-in-Navotas-77GC",
           "Pasay": "https://air.plumelabs.com/air-quality-in-Pasay-76Qr",
           "Pasig": "https://air.plumelabs.com/air-quality-in-Pasig-uAAa",
           "Quezon City": "https://air.plumelabs.com/air-quality-in-Quezon%20City-76dq"}

urls_accu = {"Marikina": "https://www.accuweather.com/en/ph/marikina-heights/1707180/air-quality-index/1707180",
             "Malabon": "https://www.accuweather.com/en/ph/barangay-660-a/3423800/air-quality-index/3423800",
             "Muntinlupa": "https://www.accuweather.com/en/ph/muntinlupa/264879/air-quality-index/264879",
             "Paranaque": "https://www.accuweather.com/en/ph/don-bosco/3424484/air-quality-index/3424484",
             "Pateros": "https://www.accuweather.com/en/ph/pateros/764136/air-quality-index/764136",
             "San Juan": "https://www.accuweather.com/en/ph/san-juan/264882/air-quality-index/264882",
             "Valenzuela": "https://www.accuweather.com/en/ph/valenzuela/3424474/air-quality-index/3424474"}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}

cities = {}

for city, url in urls_accu.items():
    # Accessing the website
    response = requests.get(url, headers=headers) 
    if response.status_code == 200:

        # Parse the website
        soup = BeautifulSoup(response.text, "html.parser")

        air_pollution_measures = soup.find_all("div", class_="air-quality-pollutant new-colors")
        
        # Pollutants
        pols_idx_divs = soup.find_all("div", class_="pollutant-index")

        pols_idx = []

        for div in pols_idx_divs:
            pols_idx.append(div.text)

        pols_idx = list(set(pols_idx))

        cities[city] = {"PM2.5": pols_idx[0],
                        "PM10": pols_idx[1],
                        "O3": pols_idx[2],
                        "NO2": pols_idx[3]}
    else:
        continue

for city, url in urls_pl.items():
    # Accessing the website
    response = requests.get(url, headers=headers) 
    if response.status_code == 200:

        # Parse the website
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Pollutants
        pols_idx_divs = soup.find_all("div", class_="pollutant-table__concentration")

        pols_idx = []

        for div in pols_idx_divs:
            pols_idx.append(div.text)

        pols_idx = list(set(pols_idx))

        cities[city] = {"PM2.5": pols_idx[0],
                        "PM10":pols_idx[1],
                        "O3": pols_idx[3],
                        "NO2": pols_idx[2]}
    else:
        continue

cities = dict(sorted(cities.items()))

print(cities)