# YC Scraper & Dashboard
Analyze and visualize Y Combinator startups by scraping their data and building an interactive dashboard.

---

## Table of Contents
- [Problem Statement](#problem-statement)
- [Project Goals](#project-goals)
- [Key Findings](#Key-Findings-from-Analysis)
- [Build From Sources](#build-from-sources)
- [Dashboard Preview](#dashboard-preview)
- [License](#license)

---

## Problem Statement

The [Y Combinator](https://www.ycombinator.com) startup directory contains valuable information on thousands of startups, including their industry, location, batch, and other key attributes. However, this data is scattered across multiple web pages and lacks a structured, easily analyzable format. Analysts, researchers, and enthusiasts struggle to extract insights about startup trends, geographic distribution, and sector growth efficiently.

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

## Key Findings from Analysis
Based on the analysis of the YC startup data, here are some key findings:

1.  **Company Formation during COVID-19:** The highest number of companies were founded during 2020–2021, coinciding with the COVID-19 pandemic.
2.  **Team Size by Company Type:** Public companies have a larger average team size compared to private or acquired companies.
3.  **Serial Founders:** Approximately 250 founders have founded two or more companies.
4.  **Top Founder by Number of Companies:** The founder with the highest number of companies is Jay Patel, who has founded 5 companies.

---

## Build From Sources

1.  Clone the repository:
    ```bash
    git clone [https://github.com/Rafixyz007/yc-scraper-viz.git](https://github.com/Rafixyz007/yc-scraper-viz.git)
    ```
2.  Initialize and activate the virtual environment (for Windows):
    ```bash
    source cap_project_01/Scripts/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the scraper scripts in the specified order:
    ```bash
    # 1. it will get all company urls
    python url_collect_01.py 

    # 2. it will scrape the data
    python ycombinator_scraper_02.py 

    # 3. it will merge all the failed urls
    python merge_failed_chunk_03.py 

    # 4. it will scrape the failed urls
    python failed_urls_scraper_04.py 

    # 5. it will clean the data
    jupyter notebook clean_data_05.ipynb
    ```
5.  You will get a file named `"yc_company_data.csv"` containing all the scraped data.
    * **Alternatively, check the file here:** [yc_company_data.csv](https://github.com/Rafixyz007/yc-scraper-viz/blob/main/capstone%20project%2001/yc_company_data.csv)

---

## Dashboard Preview

![Dashboard Preview](https://raw.githubusercontent.com/Rafixyz007/yc-scraper-viz/main/assets/dashboard.png)

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
