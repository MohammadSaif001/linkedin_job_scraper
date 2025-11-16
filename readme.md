LinkedIn Job Scraper (Playwright + BeautifulSoup)

This project extracts job listings from LinkedIn using Playwright to load dynamic content and BeautifulSoup to parse the rendered HTML. The script collects job titles, companies, locations, and application links, then stores them in a CSV file.

FEATURES
- Automates browser using Playwright (Chromium)
- Loads full JavaScript-rendered job listings
- Scrapes job title, company, job location, and apply link
- Saves data into linked.csv
- Simple function call based on user input

REQUIREMENTS
Install dependencies:
pip install playwright
pip install beautifulsoup4
pip install lxml

Install Playwright browsers:
playwright install

HOW TO RUN
Run the script:
python linkedIn_jobs.py

The script will ask:
Enter the location:
Enter the job role you want to search:

OUTPUT
All extracted job data is appended to "linked.csv".

COLUMNS:
title | company | location | apply_link

HOW IT WORKS
1. Playwright opens a headless Chromium browser.
2. Loads the LinkedIn jobs search URL.
3. Waits for JavaScript to load completely.
4. BeautifulSoup parses the HTML.
5. The script extracts job fields from each job card.
6. The CSV writer saves each row.

NOTES
- LinkedIn uses bot detection, scraping may fail sometimes.
- Only the first page of results is scraped.
- CSV file is appended on every run.

FUTURE ENHANCEMENTS
- Add scrolling to load more jobs
- Add pagination
- Add user-agent spoofing
- Store data in a database
- Add proxy support
