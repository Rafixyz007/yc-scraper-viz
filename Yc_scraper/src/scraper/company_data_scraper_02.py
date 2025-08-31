import time
import random
import pandas as pd
from multiprocessing import Pool
from selenium import webdriver
# from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from geonamescache import GeonamesCache


# GECKO_DRIVER_PATH = r"D:\scraping\scraping projects\selenium+bs4 infinte scroll\geckodriver-v0.36.0-win64\geckodriver.exe"
input_file = "company_urls.csv"
max_founders = 3
num_browser = 4  # Adjust based on your CPU cores in my case i am launching 4 processes simultaneously
chunk_size = 50  # None for auto chunking based on NUM_WORKERS


gc = GeonamesCache() # Initialize GeonamesCache
# Get all cities from GeonamesCache which will be used to filter out city names from company types
# This helps in avoiding false positives where a company type might be a city name

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


def scrape_chunk(args): # Function to scrape a chunk of data

    """ Scrape a chunk of company data from Y Combinator website.
    Args:
        args (tuple): A tuple containing the DataFrame chunk and its ID.
    Returns:
        str: The output file name where the scraped data is saved.
    """
    chunk_df, chunk_id = args # Unpack the arguments 
    failed_urls = []  # track failed URLs

    
    options = Options() # Set up Firefox options
    options.headless = True # Run in headless mode
    # service = Service(GECKO_DRIVER_PATH) # Set up the geckodriver service
    driver = webdriver.Firefox(options=options) # Initialize the Firefox driver
    driver.set_page_load_timeout(180) # Set page load timeout.

    for index, row in chunk_df.iterrows(): # Iterate over each row in the chunk
        url = row['company_urls'] # Get the company URL

        # Retry loop
        for attempt in range(3): # Try to load the page up to 3 times
            try: 
                driver.get(url) # Load the company page
                time.sleep(random.uniform(0.5, 1.2)) # Random sleep to mimic human behavior
                break  # Exit retry loop if successful
            except Exception as e: # Handle any exceptions during page load
                print(f"[Chunk {chunk_id}] Retry {attempt+1} for {url} failed: {e}") # Log the error
                if attempt == 2:  # If all retries failed, log the URL
                    failed_urls.append(url) # append to failed URLs
                    continue # skip to next URL
                time.sleep(5)

        if url in failed_urls: # If the URL is in failed URLs, skip further processing
            continue  # skip extraction if all retries failed

        
        founded_date = batch = team_size = status_text = location_text = slogan_text = company_website_url = "Not available" # Initialize variables
        company_types = []
        founders = {f"founder_{i}": 'Not available' for i in range(1, max_founders+1)} # Initialize founders dictionary

        # Extract data from the page using Selenium
        try:
            
            try:
                founded = driver.find_element(
                    By.XPATH,
                    '//div[@class="flex flex-row justify-between"][contains(translate(., "FOUNDED", "founded"), "founded")]'
                )
                founded_date = founded.text.split('\n')[-1]
            except:
                pass

            # Batch
            try:
                batch_element = driver.find_element(
                    By.XPATH,
                    '//div[@class="flex flex-row justify-between"][contains(translate(., "BATCH", "batch"), "batch")]'
                )
                batch = batch_element.text.split(":")[-1].strip().split("-")[-1].strip()
            except:
                pass

            # Team Size
            try:
                team = driver.find_element(
                    By.XPATH,
                    '//div[@class="flex flex-row justify-between"][contains(translate(., "TEAM SIZE", "team size"), "team size")]'
                )
                team_size = team.text.split('\n')[-1]
            except:
                pass

            # Status
            try:
                status = driver.find_element(
                    By.XPATH,
                    '//div[@class="flex flex-row justify-between"][contains(translate(., "STATUS", "status"), "status")]'
                )
                status_text = status.text.split('\n')[-1]
            except:
                pass

            # Location
            try:
                location = driver.find_element(
                    By.XPATH,
                    '//div[@class="flex flex-row justify-between"][contains(translate(., "LOCATION", "location"), "location")]'
                )
                location_text = location.text.split('\n')[-1]
            except:
                pass

            # Slogan
            try:
                slogan = driver.find_element(By.XPATH, '//div[@class="text-xl"]')
                slogan_text = slogan.text.strip()
            except:
                pass

            # Website URL
            try:
                website_link = driver.find_element(
                    By.XPATH,
                    '//div[@class="group flex flex-row items-center px-3 leading-none text-linkColor "]//a'
                )
                company_website_url = website_link.get_attribute('href').split('?')[0]
            except:
                pass

            # Company Types
            try:
                elements = driver.find_elements(By.XPATH, '//div[@class="align-center flex flex-row flex-wrap gap-x-2 gap-y-2"]')
                for element in elements:
                    children = element.find_elements(By.XPATH, './*')
                    if len(children) <= 2:
                        continue
                    values = [child.text for child in children[2:]]
                    company_types.extend([v for v in values if v.lower() not in ALL_CITIES])
            except:
                pass

            # Founders
            try:
                founder_elements = driver.find_elements(By.XPATH, '//div[@class="min-w-0 flex-1"]')
                for i, element in enumerate(founder_elements[:max_founders], start=1):
                    founder_name = element.text.strip()
                    founders[f"founder_{i}"] = founder_name if founder_name else 'Not available'
            except:
                pass

        except Exception as e:
            print(f"[Chunk {chunk_id}] Error processing {url}: {str(e)}")
            failed_urls.append(url)

        # Update the DataFrame with the extracted data

        chunk_df.at[index, 'founded_date'] = founded_date
        chunk_df.at[index, 'batch'] = batch
        chunk_df.at[index, 'team_size'] = team_size
        chunk_df.at[index, 'status'] = status_text
        chunk_df.at[index, 'location'] = location_text
        chunk_df.at[index, 'slogan'] = slogan_text
        chunk_df.at[index, 'company_website_url'] = company_website_url
        chunk_df.at[index, 'company_types'] = ', '.join(company_types) if company_types else 'Not available'
        for i in range(1, max_founders+1): # Update founders data
            chunk_df.at[index, f'founder_{i}'] = founders[f"founder_{i}"] # If founder is not available, it will remain 'Not available'

    driver.quit()

    # Save results
    output_file = f"output_chunk_{chunk_id}.csv" # Define output file name
    chunk_df.to_csv(output_file, index=False) # Save the DataFrame to CSV

    # Save failed URLs for later retry
    if failed_urls: # If there are any failed URLs, save them to a file

        with open(f"failed_chunk_{chunk_id}.txt", "w") as f: # Open file in write mode
            for url in failed_urls: # Write each failed URL to the file
                f.write(url + "\n") # Newline for each URL

    print(f"[Chunk {chunk_id}] Saved {len(chunk_df)} rows to {output_file}, {len(failed_urls)} failed.")
    return output_file


if __name__ == "__main__": # Main function to run the scraper
    df = pd.read_csv(input_file) # Read the input CSV file containing company URLs
    df['company_name'] = df['Company URL'].str.split('/').str[-1] # Extract company names from URLs  last part of the URL
    df = df.rename(columns={'Company URL': 'company_urls'}) # Rename the column

    # Initialize new columns with default values
    df['founded_date'] = 'Not available'
    df['batch'] = 'Not available'
    df['team_size'] = 'Not available'
    df['status'] = 'Not available'
    df['location'] = 'Not available'
    df['slogan'] = 'Not available'
    df['company_website_url'] = 'Not available'
    df['company_types'] = 'Not available'
    for i in range(1, max_founders+1): # Initialize founder columns
        df[f'founder_{i}'] = 'Not available'

    # Split into chunks
    chunks = []
    chunk_size = len(df) // num_browser if chunk_size is None else chunk_size # Calculate chunk size based on number of workers or use provided CHUNK_SIZE
    for i in range(0, len(df), chunk_size): # Create chunks of the DataFrame
        chunks.append((df.iloc[i:i+chunk_size].copy(), len(chunks))) # Append the chunk and its ID to the list

    # Run in parallel
    with Pool(processes=num_browser) as pool: # Create a pool of workers in my case 4
        output_files = pool.map(scrape_chunk, chunks) # Scrape each chunk in parallel

    # Combine
    final_df = pd.concat([pd.read_csv(file) for file in output_files], ignore_index=True) # Combine all output files into a single DataFrame
    final_df.to_csv("ycombinator_company_data.csv", index=False) # Save the final DataFrame to a CSV file
    print(f"\n All data saved to ycombinator_company_data.csv")
    print(" Failed URLs saved in failed_chunk_*.txt files for retry.")
