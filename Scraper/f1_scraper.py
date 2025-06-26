from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
from io import StringIO
from datetime import datetime

# Get the current year
current_year = datetime.now().year

# Set up Selenium (headless)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Prepare data storage
all_data = []

# Loop from 2021 to current year (e.g. 2025)
for year in range(2021, current_year + 1):
    print(f"🔍 Scraping season: {year}")
    url = f"https://www.formula1.com/en/results.html/{year}/drivers.html"
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    try:
        # Try multiple selectors to ensure table is found
        selectors = [
            "table.resultsarchive-table",
            "table",
            "[data-testid='results-table']",
            ".results-table"
        ]

        table = None
        for selector in selectors:
            table = soup.select_one(selector)
            if table:
                print(f"✅ Found table using selector: {selector}")
                break

        if table:
            df = pd.read_html(StringIO(str(table)))[0]
            df["Season"] = year
            all_data.append(df)
            print(f"✅ Successfully scraped {year} - {len(df)} drivers")
        else:
            print(f"⚠️ No table found for {year}")
    except Exception as e:
        print(f"❌ Error scraping {year}: {e}")

driver.quit()

# Save data
if all_data:
    df_all = pd.concat(all_data, ignore_index=True)
    df_all.to_csv("driver_stats.csv", index=False)
    df_all.to_json("driver_stats.json", orient="records", indent=2)
    print("✅ All seasons saved successfully.")
else:
    print("❌ No data scraped.")
