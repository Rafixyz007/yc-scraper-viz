from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC # Import expected conditions for waiting
import urllib.parse # For URL encoding
import pandas as pd
import time


industry_tags = [
    "Analytics", "Engineering, Product and Design", "Finance and Accounting",
    "Human Resources", "infrastructure", "Marketing", "Legal", "office Management",
    "operations", "productivity", "Recruiting and Talent", "Retail", "Sales",
    "Security", "Supply Chain and Logistics", "Fintech", "Healthcare", "Consumer",
    "Education", "Real Estate and Construction", "Industrials",
    "Government", "Unspecified"
]

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 5)

base_url = "https://www.ycombinator.com/companies?industry="

company_links = []

for tag in industry_tags: # Loop through each industry tag
    encoded_tag = urllib.parse.quote(tag) # URL encode the tag
    # Construct the URL with the encoded tag
    url = base_url + encoded_tag # Construct the full URL
    # Print the URL being visited for debugging
    # This is useful to see which URL is being processed
    print(f" Visiting: {url}")
    driver.get(url)

    # Initial wait for at least one company card to appear
    wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="!py-4 _company_i9oky_355"]')))
    
    last_count = 0 # Initial count of company cards
    # Retry logic to scroll and load more company cards
    retries = 0 # Initial retry count
    # Set a maximum number of retries to avoid infinite loops
    max_retries = 4 # Maximum retries before giving up

    while retries < max_retries: # Loop until max retries reached
        # Check if the number of company cards has changed
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll to the bottom of the page

        # Wait for new elements (or timeout after 3 sec)
        try:
            wait.until(lambda d: len(d.find_elements(By.XPATH, '//a[@class="!py-4 _company_i9oky_355"]')) > last_count) # Wait until new elements are loaded
            # If new elements loaded, update the count and reset retries    
            # If new elements loaded, reset retries and update count
            last_count = len(driver.find_elements(By.XPATH, '//a[@class="!py-4 _company_i9oky_355"]')) # Update the count of company cards
            retries = 0 # Reset retries since new elements were loaded
        except:
            # No new elements loaded within timeout
            retries += 1
            time.sleep(1)

    # Collect final company links
    cards = driver.find_elements(By.XPATH, '//a[@class="!py-4 _company_i9oky_355"]') # Find all company cards
    # Extract the href attribute from each card
    for card in cards: # Loop through each card
        # Get the href attribute which contains the company URL
        href = card.get_attribute("href") # Extract the URL from the card
        # Append the URL to the company_links list
        company_links.append(href)

driver.quit()

# Remove duplicates and save
df = pd.DataFrame(sorted(set(company_links)), columns=["Company URL"]) # Convert to DataFrame and remove duplicates
df.to_csv("companyi_urls.csv", index=False) # Save to CSV without index
print(f" scraper1 saved {len(df)} links.") # This will print the number of unique company URLs saved
# This is useful to verify the number of unique URLs collected