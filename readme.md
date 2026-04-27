LinkedIn Job Scraper (Playwright + BeautifulSoup)

This project extracts job listings from LinkedIn using Playwright to load dynamic content and BeautifulSoup to parse the rendered HTML. The script collects job titles, companies, locations, and application links, then stores them in a CSV file.

FEATURES
- Automates browser using Playwright (Chromium)
- Loads full JavaScript-rendered job listings
- Scrapes job title, company, job location, and apply link
- Saves data into linked.csv
- Simple function call based on user input

INSTALLATION
1. Clone or download this project
2. Navigate to the project directory:
   cd scrapers
3. Install dependencies:
   pip install -r requirement.txt
4. Install Playwright browsers:
   playwright install

REQUIREMENTS
Install dependencies:
pip install -r requirement.txt

Install Playwright browsers:
playwright install

HOW TO RUN
1. Run the script:
   python linkedin_job_scraper.py
2. The script will prompt you for input:
   Enter the location (country name): [type location, e.g., "India"]
   Enter the job role you want to search: [type role, e.g., "Python Developer"]
3. Wait for the script to complete (takes 5-10 seconds)
4. Check the output file "linked.csv" for results

USAGE EXAMPLE
python linkedin_job_scraper.py
Enter the location(country name): India
Enter the job role you want to search: Data Scientist
Job data has been written to linked.csv

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

AUTHORS
- Saif
- Zawberus

