import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from geonamescache import GeonamesCache
import os


# GECKO_DRIVER_PATH = r"D:\scraping\scraping projects\selenium+bs4 infinte scroll\geckodriver-v0.36.0-win64\geckodriver.exe"
FAILED_URLS_FILE = "merged_failed_urls.txt"
FINAL_OUTPUT_FILE = "ycombinator_company_data.csv"
RETRY_OUTPUT_FILE = "retry_data.csv"
MAX_FOUNDERS = 3


gc = GeonamesCache()
cities = gc.get_cities()
ALL_CITIES = {city['name'].lower() for city in cities.values()}
ALL_CITIES.update({
    'al','ak','az','ar','ca','co','ct','de','fl','ga','hi','id','il','in',
    'ia','ks','ky','la','me','md','ma','mi','mn','ms','mo','mt','ne','nv',
    'nh','nj','nm','ny','nc','nd','oh','ok','or','pa','ri','sc','sd','tn',
    'tx','ut','vt','va','wa','wv','wi','wy',
    'nyc', 'sf', 'la', 'hk', 'dc',
    'bay area', 'silicon valley',
    'new york', 'san francisco', 'los angeles', 'chicago', 'atlanta',
    'boston', 'seattle', 'austin', 'denver', 'miami'
})

# ========= LOAD FAILED URLS =========
with open(FAILED_URLS_FILE, "r") as f:
    urls = [line.strip() for line in f if line.strip()]

# ========= INIT DATAFRAME =========
df = pd.DataFrame(urls, columns=['company_urls'])
df['company_name'] = df['company_urls'].str.split('/').str[-1]

# Init columns
df['founded_date'] = 'Not available'
df['batch'] = 'Not available'
df['team_size'] = 'Not available'
df['status'] = 'Not available'
df['location'] = 'Not available'
df['slogan'] = 'Not available'
df['company_website_url'] = 'Not available'
df['company_types'] = 'Not available'
for i in range(1, MAX_FOUNDERS+1):
    df[f'founder_{i}'] = 'Not available'

# ========= SCRAPER FUNCTION =========
options = Options()
options.headless = True
# service = Service(GECKO_DRIVER_PATH)
driver = webdriver.Firefox(options=options)
driver.set_page_load_timeout(180)

for index, row in df.iterrows():
    url = row['company_urls']
    try:
        driver.get(url)
        time.sleep(random.uniform(0.5, 1.5))
    except Exception as e:
        print(f"Failed to load {url}: {e}")
        continue

    # Extract fields
    try:
        # Founded Date
        try:
            founded = driver.find_element(By.XPATH,
                '//div[@class="flex flex-row justify-between"][contains(translate(., "FOUNDED", "founded"), "founded")]'
            )
            df.at[index, 'founded_date'] = founded.text.split('\n')[-1]
        except: pass

        # Batch
        try:
            batch_element = driver.find_element(By.XPATH,
                '//div[@class="flex flex-row justify-between"][contains(translate(., "BATCH", "batch"), "batch")]'
            )
            df.at[index, 'batch'] = batch_element.text.split(":")[-1].strip().split("-")[-1].strip()
        except: pass

        # Team Size
        try:
            team = driver.find_element(By.XPATH,
                '//div[@class="flex flex-row justify-between"][contains(translate(., "TEAM SIZE", "team size"), "team size")]'
            )
            df.at[index, 'team_size'] = team.text.split('\n')[-1]
        except: pass

        # Status
        try:
            status = driver.find_element(By.XPATH,
                '//div[@class="flex flex-row justify-between"][contains(translate(., "STATUS", "status"), "status")]'
            )
            df.at[index, 'status'] = status.text.split('\n')[-1]
        except: pass

        # Location
        try:
            location = driver.find_element(By.XPATH,
                '//div[@class="flex flex-row justify-between"][contains(translate(., "LOCATION", "location"), "location")]'
            )
            df.at[index, 'location'] = location.text.split('\n')[-1]
        except: pass

        # Slogan
        try:
            slogan = driver.find_element(By.XPATH, '//div[@class="text-xl"]')
            df.at[index, 'slogan'] = slogan.text.strip()
        except: pass

        # Website
        try:
            website_link = driver.find_element(By.XPATH,
                '//div[@class="group flex flex-row items-center px-3 leading-none text-linkColor "]//a'
            )
            df.at[index, 'company_website_url'] = website_link.get_attribute('href').split('?')[0]
        except: pass

        # Company Types
        try:
            elements = driver.find_elements(By.XPATH,
                '//div[@class="align-center flex flex-row flex-wrap gap-x-2 gap-y-2"]'
            )
            types = []
            for element in elements:
                children = element.find_elements(By.XPATH, './*')
                if len(children) <= 2:
                    continue
                values = [child.text for child in children[2:]]
                types.extend([v for v in values if v.lower() not in ALL_CITIES])
            if types:
                df.at[index, 'company_types'] = ', '.join(types)
        except: pass

        # Founders
        try:
            founder_elements = driver.find_elements(By.XPATH, '//div[@class="min-w-0 flex-1"]')
            for i, element in enumerate(founder_elements[:MAX_FOUNDERS], start=1):
                founder_name = element.text.strip()
                df.at[index, f'founder_{i}'] = founder_name if founder_name else 'Not available'
        except: pass

    except Exception as e:
        print(f"Error scraping {url}: {e}")

driver.quit()

# ========= SAVE RETRY DATA =========
df.to_csv(RETRY_OUTPUT_FILE, index=False)
print(f"Retry data saved to {RETRY_OUTPUT_FILE}")

# ========= MERGE WITH FINAL OUTPUT =========
if os.path.exists(FINAL_OUTPUT_FILE):
    final_df = pd.read_csv(FINAL_OUTPUT_FILE)
    merged_df = pd.concat([final_df, df], ignore_index=True)
    merged_df.to_csv(FINAL_OUTPUT_FILE, index=False)
    print(f"Final merged data saved to {FINAL_OUTPUT_FILE}")
else:
    df.to_csv(FINAL_OUTPUT_FILE, index=False)
    print(f"Final data saved to {FINAL_OUTPUT_FILE}")
