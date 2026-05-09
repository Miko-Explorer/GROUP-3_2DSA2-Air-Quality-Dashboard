import requests
from bs4 import BeautifulSoup
import time

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

for city, url in urls.items():
    # Accessing the website
    response = requests.get(url, headers=headers) 
    time.sleep(2)
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

cities = dict(sorted(cities.items()))

if __name__ == '__main__':
    for item in cities.items():
        print(item)
