# LinkedIn Job Scraper (v2.0)

Extract job listings from LinkedIn using Playwright and BeautifulSoup. This project provides multiple scraper implementations to collect job titles, companies, locations, and application links.

## 📋 Project Structure

```
linkedin-job-scrapers/
├── scrapers/
│   ├── linkedin_job_scraper.py       # Original scraper (interactive)
│   ├── linkedin_job_fetcher.py       # Enhanced scraper (recommended)
│   └── scraper_web.py                # Web scraper (legacy)
├── output/
│   ├── linked_job.csv
│   └── linked_job.json
├── requirement.txt
└── README.md
```

## ✨ Features

- **Multiple Scrapers**: Choose between interactive or programmatic scrapers
- **Playwright Integration**: Handles JavaScript-rendered job listings
- **Multiple Formats**: Export to CSV or JSON
- **Deduplication**: Prevents duplicate job listings
- **Flexible Output**: Save to custom file paths
- **Pagination Support**: Scrape multiple pages of results
- **Job Descriptions**: Extract detailed job descriptions (enhanced version)

## 📦 INSTALLATION

1. Clone or download this project
2. Navigate to the project directory:
   ```
   cd linkedin-job-scrapers
   ```
3. Install dependencies:
   ```
   pip install -r requirement.txt
   ```
4. Install Playwright browsers:
   ```
   playwright install
   ```

## 🔧 REQUIREMENTS

```
pip install -r requirement.txt
playwright install
```

## 🚀 HOW TO RUN

### Option 1: Interactive Mode (linkedin_job_scraper.py)
```bash
python scrapers/linkedin_job_scraper.py
```
Then follow the prompts:
```
Enter the location (country name): United States
Enter the job role you want to search: Data Scientist
```

### Option 2: CLI Mode with Arguments (linkedin_job_fetcher.py - RECOMMENDED)
```bash
python scrapers/linkedin_job_fetcher.py \
  --query "Python Developer" \
  --location "India" \
  --output "output/jobs.csv" \
  --max-results 100
```

### Option 3: Programmatic Usage
```python
from scrapers.linkedin_job_fetcher import scrape_linkedin_jobs

jobs = scrape_linkedin_jobs(
    query="Data Scientist",
    location="United States",
    output_path="output/results.json",
    max_results=100,
    headless=True
)
```

## 📊 OUTPUT FORMATS

### CSV Output
```
title,company,location,apply_link
Senior Python Developer,Tech Corp,San Francisco,https://linkedin.com/jobs/view/...
Data Scientist,Analytics Inc,New York,https://linkedin.com/jobs/view/...
```

### JSON Output
```json
[
  {
    "title": "Senior Python Developer",
    "company": "Tech Corp",
    "location": "San Francisco",
    "apply_link": "https://linkedin.com/jobs/view/..."
  }
]
```

## 🔄 HOW IT WORKS

1. Playwright launches a headless Chromium browser
2. Navigates to LinkedIn job search URL with specified parameters
3. Waits for JavaScript to load job listings
4. Scrolls to load additional job cards
5. BeautifulSoup parses the rendered HTML
6. Extracts job fields from each job card
7. Deduplicates results
8. Exports to CSV or JSON

## ⚙️ Available Options

### linkedin_job_fetcher.py
- `--query`: Job title or keywords (required if not prompted)
- `--location`: Job location (required if not prompted)
- `--output`: Output file path (default: linked_job.csv)
- `--max-results`: Maximum number of jobs to scrape (default: 100)
- `--visible`: Show browser window for debugging (default: headless)

## ⚠️ NOTES

- LinkedIn uses bot detection; scraping may fail occasionally
- Respect LinkedIn's Terms of Service
- Scraping takes 10-30 seconds depending on results count
- Browser must load JavaScript - use `--visible` flag to debug
- CSV file appends on every run; JSON file overwrites
- For large result sets, increase timeout values

## 🐛 TROUBLESHOOTING

**No jobs found:**
- Check network connection
- Try with `--visible` flag to see what LinkedIn is showing
- LinkedIn may require login - consider adding authentication

**Slow performance:**
- Reduce `--max-results` value
- Increase `--timeout` if pages aren't loading

**Import errors:**
- Ensure `pip install -r requirement.txt` was completed
- Ensure `playwright install` was completed

## 📝 CHANGELOG

### v2.0 (Current)
- Reorganized scraper files into `scrapers/` folder
- Added enhanced `linkedin_job_fetcher.py` with better error handling
- Multiple output format support (CSV and JSON)
- Improved deduplication logic
- Better pagination handling

### v1.0
- Initial release with basic scraper

## 👨‍💻 AUTHORS

- Saif

## 📄 LICENSE

MIT License

