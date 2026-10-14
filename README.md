# LinkedIn Job Scraper

A Python application that collects publicly available LinkedIn job listings using Playwright and BeautifulSoup. The scraper extracts job titles, company names, locations, and application links, then exports the results to CSV or JSON.

## Features

- Search by job title, keywords, and location
- Support for paginated job searches
- JavaScript-rendered page handling with Playwright
- Duplicate job removal
- CSV and JSON export
- Headless operation by default
- Optional visible-browser mode for troubleshooting

## Project Structure

```text
.
├── src/
│   ├── output/
│   │   ├── linked_job.csv
│   │   └── linked_job.json
│   └── scrapers/
│       ├── __init__.py
│       ├── linkedin_job_fetcher.py
│       └── linkedin_job_scraper.py
├── pyproject.toml
├── uv.lock
├── .python-version
└── README.md
```

## Requirements

- Python 3.14 or later
- [uv](https://docs.astral.sh/uv/)
- Internet access
- Chromium, installed through Playwright

## Installation

Clone the repository and change to the project directory:

```bash
git clone https://github.com/MohammadSaif001/linkedin_job_scraper.git
cd linkedin_job_scraper
```

Install the Python dependencies defined in `pyproject.toml`:

```bash
uv sync
```

Install the Playwright Chromium browser:

```bash
uv run playwright install chromium
```

On Linux, install the required system dependencies if Playwright reports missing libraries:

```bash
uv run playwright install --with-deps chromium
```

## Usage

### Command-line mode

The recommended scraper is `linkedin_job_fetcher.py`:

```bash
uv run python -m scrapers.linkedin_job_fetcher \
  --query "Python Developer" \
  --location "India" \
  --output "src/output/jobs.csv" \
  --max-results 100
```

### Interactive mode

Omit `--query` and `--location` to enter the values interactively:

```bash
uv run python -m scrapers.linkedin_job_fetcher
```

### JSON export

Set the output file extension to `.json`:

```bash
uv run python -m scrapers.linkedin_job_fetcher \
  --query "Data Scientist" \
  --location "United States" \
  --output "src/output/jobs.json" \
  --max-results 50
```

### Visible-browser mode

Use `--visible` to display the Chromium browser while the scraper runs. This is useful for troubleshooting page loading and bot-detection behavior:

```bash
uv run python -m scrapers.linkedin_job_fetcher \
  --query "Python Developer" \
  --location "India" \
  --output "src/output/jobs.csv" \
  --max-results 20 \
  --visible
```

## Command-line Options

| Option | Description | Default |
| --- | --- | --- |
| `--query` | Job title or search keywords | Prompted interactively |
| `--location` | Job location | Prompted interactively |
| `--output` | Destination file ending in `.csv` or `.json` | `linked_job.csv` |
| `--max-results` | Maximum number of jobs to export | `100` |
| `--headless` | Run Chromium without a visible window | Enabled unless `--visible` is used |
| `--visible` | Display the browser while scraping | Disabled |

## Output

Each record contains the following fields:

```json
{
  "title": "Senior Python Developer",
  "company": "Example Company",
  "location": "San Francisco",
  "apply_link": "https://www.linkedin.com/jobs/view/..."
}
```

When the output path ends in `.csv`, the same fields are written as CSV columns.

## Programmatic Usage

```python
from scrapers.linkedin_job_fetcher import scrape_linkedin_jobs

jobs = scrape_linkedin_jobs(
    query="Data Scientist",
    location="United States",
    output_path="src/output/results.json",
    max_results=100,
    headless=True,
)
```

## Troubleshooting

### No jobs found

Verify the network connection and run the scraper with `--visible` to inspect the page. LinkedIn may display a login page, CAPTCHA, or bot-detection challenge instead of job listings.

### Browser or import errors

Reinstall the project dependencies and the Chromium browser:

```bash
uv sync
uv run playwright install chromium
```

### Slow scraping

Reduce `--max-results` or use a narrower search query. Scraping time depends on the number of requested results and the response time of LinkedIn.

## Responsible Use

This project is intended for educational and research purposes. Use it responsibly, comply with LinkedIn's Terms of Service, respect applicable laws, and avoid collecting or processing personal data without appropriate authorization.

## License

This project is available under the MIT License.
