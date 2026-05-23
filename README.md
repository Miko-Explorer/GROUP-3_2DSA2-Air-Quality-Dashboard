# GROUP-3_2DSA2-Air-Quality-Index-Dashboard
**DSA4154 Group 3 - Automated AQI Monitoring System of 17 cities in Metro Manila Philippines**
* This project provides a real-time data pipeline that scrapes Air Quality Index data for 17 cities in Metro Manila.
* The data is processed via GitHub Actions, stored in Google Sheets, & visualized through a live Tableau Dashboard.
* To add, the project follows a "Serverless" architecture to ensure 24/7 updates without manual effort.

---

## The Data Pipeline
**The project follows a "Serverless" architecture to ensure 24/7 updates without manual effort:**
1. **Scrape:** Python scripts extract pollutant data (PM2.5, PM10, O3, NO2) from AccuWeather.
2. **Automate:** GitHub Actions triggers the script every hour.
   * Adjusted to 30 mins since the delay would take 1 to 2 hours.
   * It would definitely meet the requirement of the workflow exactly triggering the script every hour.
3. **Store:** The "Bridge" script overwrites a Google Sheet with cleaned, timestamped data.
4. **Visualize:** Tableau Desktop / Tableau Public.

---

## Data Source (AccuWeather)
**The prototype dashboard scrapes real‑time and forecast air quality data from** **[AccuWeather](https://www.accuweather.com/)**.  
- AccuWeather provides hourly AQI values and pollutant concentrations for major cities worldwide.  
- Our scraper targets the 17 cities of Metro Manila, extracting the following core pollutant measurements:
  * **PM2.5**, **PM10**, **O3**, and **NO2**.  
- The data is updated every hour (via GitHub Actions) to maintain near‑real‑time accuracy for the dashboard.

---

## Key Pollutants: Definitions & Health Effects (Lethality)
* The dashboard tracks four pollutants that pose the greatest risk to human health. 
* Below are their definitions and the potential lethality associated with acute or chronic exposure.

| Pollutant | Definition | Health Effects & Lethality |
|-----------|------------|----------------------------|
| **PM2.5** (Fine Particulate Matter) | Inhalable particles with diameter ≤ 2.5 µm. Sources: combustion (vehicles, power plants, fires), industrial processes. | Penetrates deep into lungs and bloodstream → chronic bronchitis, lung cancer, heart attacks. **High lethality**: long‑term exposure reduces life expectancy; acute spikes (e.g., wildfire smoke) trigger thousands of premature deaths annually. |
| **PM10** (Coarse Particulate Matter) | Inhalable particles with diameter ≤ 10 µm. Sources: dust, construction, agriculture, pollen. | Deposits in upper airways and lungs → asthma exacerbation, COPD, respiratory infections. **Moderate‑to‑high lethality**: contributes to hospitalizations and mortality, especially in vulnerable populations (elderly, children). |
| **O3** (Ground‑Level Ozone) | A secondary pollutant formed when NOx and VOCs react in sunlight. Not to be confused with the stratospheric ozone layer. | Irritates the respiratory tract → chest pain, coughing, reduced lung function. Chronic exposure accelerates lung aging. **Lethal at high concentrations**: severe inflammation can cause pulmonary edema; responsible for thousands of respiratory deaths during summer smog episodes. |
| **NO2** (Nitrogen Dioxide) | A reddish‑brown gas from high‑temperature combustion (vehicles, power plants). Precursor to ozone and particulate matter. | Irritates airways → increased asthma attacks, reduced immunity to lung infections. **Lethality**: long‑term exposure linked to higher risk of COPD and premature death from respiratory or cardiovascular diseases. Children and asthmatics are especially vulnerable. |

> *Note*: Lethality is determined by both concentration and exposure duration. The AQI (Air Quality Index) thresholds (e.g., WHO guidelines) help predict when these pollutants become life‑threatening to sensitive or general populations.

---

## Repository Structure
* `.github/workflows/main.yml`: The automation schedule (Cron job).
* `bridge.py`: The main execution script that scrapes data and pushes to Google Sheets.
* `requirements.txt`: List of Python dependencies for the GitHub runner.
* `creds.json` (Stored in Secrets): Encrypted Google Service Account credentials.

---

## How to Setup
1. **GitHub Secrets:** Ensure the `GCP_SERVICE_ACCOUNT_KEY` is added to your repository secrets.
2. **Google Sheets:** The target sheet must be shared with service account email as an **Editor**.
3. **Tableau Connection:** Open Tableau.
   - Connect to Google Sheets.
   - Select `[DSA4154] Group 3 Scraped Data Output`.
   - Set the data to refresh to capture the hourly updates.

---

## Output Schema
The automated script generates the following columns for the dashboard:
* **Columns:**
  - **City / Municipality:** The specific location in Metro Manila
  - **Date Scraped:** YYYY-MM-DD of the scrape
  - **Day / Time Scraped:** The specific day of the week (e.g., Monday) and HH:MM:SS (time) of the scrape
  - **Latitude:** Pinpoint latitude location of a specific city in Metro Manila out of the 17 chosen cities
  - **Longtitude:** Pinpoint longitude location of a specific city in Metro Manila out of the 17 chosen cities
  - **PM 2.5 / PM 10:** Fine and coarse particulate matter levels
  - **O3 / NO2:** Ozone and Nitrogen Dioxide concentrations
 
  ---

## Group Members (Group #3)
* **Benedict Caliba & Aaron Kane Dungca** - Lead Developer / Web Scraping
* **Enrico Miguel Veloso** - Automation & API Integration
* **Marcelo Cosme & Shane Hans Uyy** - Tableau Dashboard Design

---

## License
* Educational project for DSA#4154 (IPV).
