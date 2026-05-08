# GROUP-3_2DSA2-Air-Quality-Dashboard
**DSA4154 Group 3 - Automated AQI Monitoring System**
This project provides a real-time data pipeline that scrapes Air Quality Index (AQI) data for 17 cities in Metro Manila. The data is processed via GitHub Actions, stored in Google Sheets, and visualized through a live Tableau Dashboard.

---

## The Data Pipeline
The project follows a "Serverless" architecture to ensure 24/7 updates without manual effor:
1. **Scrape:** Python scripts extract pollutant data (PM2.5, PM10, O3, NO2) from AccuWeather and PlumeLabs.
2. **Automate:** Github Aactions triggers the script every hour.
3. **Store:** The "Bridge" script overwrites a Google Sheet with cleaned, timestamped data.
4. **Visualize:** Tableau Desktop / Tableau Public.

---

## Repository Structure
* `.github/workflows/main.yml`: The automation schedule (Cron job).
* `bridge.py`: The main execution script that scrapes data and pushes to Google Sheets 
* `requirements.txt`: List of Python dependencies for the Github runner.
* `creds.json` (Stored in Secrets): Encrypted Google Sevice Account credentials.

---

## How to Setup
1. **Github Secrets:** Ensure the `GCP_SERVICE_ACCOUNT_KEY` is added to your repository secrets.
2. **Google Sheets:** The target sheet must be shared with service account email as an **Editor**.
3. **Tableau Connection:** Open Tableau.
   - Connect to Google Sheets.
   - Select `[DSA4154] Group 3 Scraped Data Output`.
   - Set the data to refresh to capture the hourly updates.
  
---

## Output Schema
The automated script genrates the following columns for the dashboard:
* **Column:**
  - **City / Municipality:** The specific location in Metro Manila
  - **Date Scraped:** YYYY-MM-DD of the scrape
  - **Time Scraped:** HH:MM:SS of the scrape
  - **PM 2.5 / PM 10:** Fine and coarse particulate matter levels
  - **O3 / NO2:** Ozone and Nitrogen Dioxide concentrations

---

## Group Members (Group#3)
* **Benedict Caliba & Aaron Kane Dungca** - Lead Developer / Web Scraping
* **Enrico Migeul Veloso** - Automation & API Integration
* **Marcelo Cosme & Shane Hans Uyy** - Tableau Dashboard Design

## License 
* Educational project for DSA#4154 (IPV). 
