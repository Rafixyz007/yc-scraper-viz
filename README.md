# yc-scraper-viz

## Problem statement:

[The Y Combinator](https://www.ycombinator.com)
startup directory contains valuable information on thousands of startups, including their industry, location, batch, and other key attributes. However, this data is scattered across multiple web pages and lacks a structured, easily analyzable format. Analysts, researchers, and enthusiasts struggle to extract insights about startup trends, geographic distribution, and sector growth efficiently.

## Project Goals:

### The goal of this project is to:

1. Automate data collection from [Y Combinator](https://www.ycombinator.com/companies) using Selenium to scrape company details including name, batch, location, type, founder, status, and team size.

2. Clean and structure the data for analysis (e.g., standardize batch names, handle missing fields, extract founding years).

3. Provide actionable insights via Tableau visualizations, including:

    * Company founding trends over the years.

    * Distribution of companies by batch and status.

    * Top founders by the number of companies founded.

    * Average team size per company status.

    * Distribution of company types across countries.

    * Companies per batch categorized by types.

4. Provide insights into YC startup ecosystem trends for better understanding and decision-making.
   
The project ultimately aims to help investors, analysts, and researchers understand the YC startup ecosystem in terms of growth, sector distribution, and founder impact.

### [You can visit the public dashboard here]( https://public.tableau.com/app/profile/md.shakhawat.hossain7416/viz/StartupLandscapeDashboard20052025/StartupLandscapeDashboard20052025#1)

# Key Findings from Analysis [Dashboard](https://public.tableau.com/app/profile/md.shakhawat.hossain7416/viz/StartupLandscapeDashboard20052025/StartupLandscapeDashboard20052025#1)

1. Company Formation during COVID-19

      * The highest number of companies were founded during 2020–2021, coinciding with the COVID-19 pandemic.

2. Team Size by Company Type

      * Public companies have a larger average team size compared to private or acquired companies.

3. Serial Founders

     * Approximately 250 founders have founded two or more companies.

5. Top Founder by Number of Companies

      * The founder with the highest number of companies is Jay Patel, who has founded 5 companies.



## Build from sources
1. Clone the repo
```bash
git clone https://github.com/Rafixyz007/yc-scraper-viz.git
```
2. Initialize and activate virtual environment (for windows)
```bash
source cap_project_01/Scripts/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Run the scraper
```bash
    1. url_collect_01.py  # it will get all company urls
    2. ycombinator_scraper_02.py # it will scrape the data
    3. merge_failed_chunk_03.py # it will merge all the failed url
    4. failed_urls_scraper_04.py # it will scrape the failed urls
    5. clean_data_05.ipynb  # it will clean the data
```
5. You will get a file name "yc_company_data.csv" containing all data we scraped

alternatively: check it here: https://github.com/Rafixyz007/yc-scraper-viz/blob/main/capstone%20project%2001/yc_company_data.csv


    
