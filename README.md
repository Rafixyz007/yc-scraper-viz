<div align="center">
  <h1>Y Combinator Startup Analysis & Landscape Dashboard (2005–2025)</h1>
  <p>Analyze and visualize Y Combinator startups by scraping their data and building an interactive dashboard.</p>

  <p>
    <img src="https://img.shields.io/badge/Project%20Status-Completed-green">
    <img src="https://img.shields.io/badge/Python-3.13-blue">
    <img src="https://img.shields.io/badge/Selenium-4.34.2-red">
    <img src="https://img.shields.io/badge/Pandas-2.3.1-informational">
    <a href="https://public.tableau.com/app/profile/md.shakhawat.hossain7416/viz/StartupLandscapeDashboard20052025/StartupLandscapeDashboard20052025#1" target="_blank">
  <img src="https://img.shields.io/badge/Tableau-View-blue?style=flat-square&logo=tableau&logoColor=white">
</a>

  </p>
</div>

---

## Table of Contents
- [Problem Statement](#problem-statement)
- [Project Goals](#project-goals)
- [Dashboard Preview](#dashboard-preview)
- [Key Findings](#-key-findings-from-analysis)
- [Build From Sources](#build-from-sources)
- [Workflow Overview](#workflow-overview)
- [License](#license)

---

## Problem Statement

The [Y Combinator](https://www.ycombinator.com) startup directory contains valuable information on thousands of startups, including their industry, location, batch, and other key attributes. However, this data is scattered across multiple web pages and lacks a structured, easily analyzable format. Analysts, researchers, and enthusiasts struggle to extract insights about startup trends, geographic distribution, and sector growth efficiently.
In this project, data for **4,932 YC companies** was scraped, cleaned, and structured for analysis.


---

## Project Goals

### The goal of this project is to:

1.  **Automate data collection** from [Y Combinator](https://www.ycombinator.com/companies) using Selenium to scrape company details including name, batch, location, type, founder, status, and team size.

2.  **Clean and structure the data** for analysis (e.g., standardize batch names, handle missing fields, extract founding years).

3.  **Provide actionable insights** via Tableau visualizations, including:
    * Company founding trends over the years.
    * Distribution of companies by batch and status.
    * Top founders by the number of companies founded.
    * Average team size per company status.
    * Distribution of company types across countries.
    * Companies per batch categorized by types.

4.  **Provide insights** into the YC startup ecosystem trends for better understanding and decision-making.

The project ultimately aims to help investors, analysts, and researchers understand the YC startup ecosystem in terms of growth, sector distribution, and founder impact.

[**You can visit the public dashboard here**](https://public.tableau.com/app/profile/md.shakhawat.hossain7416/viz/StartupLandscapeDashboard20052025/StartupLandscapeDashboard20052025#1)

---

## [Dashboard Preview](https://public.tableau.com/app/profile/md.shakhawat.hossain7416/viz/StartupLandscapeDashboard20052025/StartupLandscapeDashboard20052025)

![Dashboard_01 Preview](https://github.com/Rafixyz007/yc-scraper-viz/blob/main/Yc_scraper/assets/dashboard_01.png)
![Dashboard_02 Preview](https://github.com/Rafixyz007/yc-scraper-viz/blob/main/Yc_scraper/assets/dashboard_02.png)


## 📊 Key Findings from Analysis

- **Company Formation during COVID-19:**  
  The highest number of YC companies were founded in **2020–2021**, coinciding with the global COVID-19 pandemic.  

- **Team Size by Company Type:**  
  **Public companies** have a significantly larger average team size compared to private or acquired companies.  

- **Serial Founders:**  
  Around **250 founders** have founded **two or more companies**, highlighting strong entrepreneurial repetition within YC.  

- **Top Founder by Number of Companies:**  
  **Jay Patel** stands out as the top founder, having founded **5 companies**.  

- **Surge in Internet-based Startups (2019–2023):**  
  Most YC-backed startups in this period were **online/internet-related**, reflecting the growing dominance of digital-first businesses.  

- **Short-lived Categories:**  
  Some industries (e.g., **3D Printing, Air Taxis, Airlines**) appeared briefly in the portfolio but did not sustain long-term growth.  

---

## Build From Sources

1.  Clone the repository:
    ```bash
    git clone https://github.com/Rafixyz007/yc-scraper-viz.git
    ```
2.  Initialize and activate the virtual environment (for Windows):
    ```bash
    source cap_project_01/Scripts/activate
    ```
3.  Install dependencies from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the scraper scripts in the specified order:
    ```bash
    # 1. it will get all company urls
    python company_url_scraper_01.py 

    # 2. it will scrape the data
    python company_data_scraper_02.py 

    # 3. it will merge all the failed urls
    python merge_failed_chunk_03.py 

    # 4. it will scrape the failed urls
    python failed_company_data_scraper_04.py
    ```

---

## Workflow Overview

Below is a diagram showing how the scraper processes YC company URLs:

                    ┌────────────────────────────┐
                    │ Input CSV: company_urls.csv│
                    └─────────────┬─────────────┘
                                  ▼
                    ┌────────────────────────────┐
                    │ Preprocess DataFrame       │
                    │ - Extract company_name     │
                    │ - Rename column            │
                    │ - Initialize columns:      │
                    │   founded_date, batch, ... │
                    │   founder_1...founder_N    │
                    └─────────────┬─────────────┘
                                  ▼
                    ┌────────────────────────────┐
                    │ Split DataFrame into chunks│
                    │ for parallel processing    │
                    └─────────────┬─────────────┘
                                  ▼
                    ┌────────────────────────────┐
                    │ Multiprocessing Pool       │
                    │ - num_browser workers      │
                    │ - Each worker runs         │
                    │   scrape_chunk(chunk)      │
                    └─────────────┬─────────────┘
                                  ▼
          ┌───────────────────────┴───────────────────────┐
          │ scrape_chunk() processes each row (company)   │
          └───────────────────────┬───────────────────────┘
                                  ▼
                   ┌─────────────────────────────────┐
                   │ Per-company URL processing:     │
                   │ - Retry page load up to 3 times │
                   │ - Scrape fields:                │
                   │   founded_date, batch, team_size│
                   │   status, location, slogan      │
                   │   website URL, types            │
                   │   founders (up to max_founders) │
                   │ - Update DataFrame row          │
                   └─────────────┬───────────────────┘
                                 ▼
                   ┌───────────────────────────────┐
                   │ After chunk finished:         │
                   │ - Save chunk CSV:             │
                   │   output_chunk_<id>.csv       │
                   │ - Save failed URLs:           │
                   │   failed_chunk_<id>.txt       │
                   └─────────────┬─────────────────┘
                                 ▼
                   ┌───────────────────────────────┐
                   │ Combine all chunk CSVs → final │
                   │ CSV: ycombinator_company_data.csv │
                   └─────────────┬─────────────────┘
                                 ▼
                   ┌───────────────────────────────┐
                   │ Scraping Complete              │
                   │ Failed URLs saved in failed_chunk_*.txt │
                   └───────────────────────────────┘

Legend / Notes:
- max_founders : Maximum number of founder columns per company
- num_browser  : Number of parallel browser processes
- chunk CSV    : Intermediate CSV files for each chunk
- failed_chunk_*.txt : List of URLs that failed for retry


## Using Pandas for Data Cleaning
After the scraping scripts have run, the data is collected and processed using the **Pandas** library within the `clean_data_05.ipynb` Jupyter Notebook. Pandas was used to:
* **Load and merge** the scraped data from CSV files.
* **Handle missing values** and incorrect data types.
* **Extract meaningful insights**, such as the founding year from the batch name.
* **Export the final cleaned dataset** to a single CSV file, ready for visualization in Tableau.

5.  Run the data cleaning script:
    ```bash
    jupyter notebook data_preprocessing_05.ipynb
    ```
6.  You will get a file named `"yc_company_data.csv"` containing all the scraped data.
    * **Alternatively, check the file here:** [yc_company_data.csv](https://github.com/Rafixyz007/yc-scraper-viz/blob/main/capstone%20project%2001/source/yc_company_data.csv)

---


## About the Author
**Md. Shakhawat Hossain**

An aspiring Data Scientist passionate about leveraging data to solve complex problems and build impactful dashboards. This project showcases my foundational skills in data collection, cleaning, and visualization.

-   [Email](shakhawat430007@gmail.com)

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
