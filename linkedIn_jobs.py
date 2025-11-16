from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv



def fetch_jobs_from_linkedin(query: str, location: str, max_results=100):
    jobs = []
    search_url = f"https://www.linkedin.com/jobs/search?keywords={query}&location={location}&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"
    
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)  # headless=False for debugging
        page = browser.new_page()
        page.goto(search_url)
        page.wait_for_timeout(3000)  # wait for JS content to load
        html = page.content()
        browser.close()
    
    soup = BeautifulSoup(html, "html.parser")
    job_cards = soup.find_all("div", class_="base-card")[:max_results]
    
    
    with open("linked.csv","a",newline="",encoding="utf-8") as file:
        writer =csv.writer(file)
    
        for card in job_cards:
            title_elem = card.find("h3", class_="base-search-card__title")
            company_elem = card.find("h4", class_="base-search-card__subtitle")
            location_elem = card.find("span", class_="job-search-card__location")
            link= card.find("a", class_="base-card__full-link", href=True)
            
            
            row = [
                title_elem.text.strip() if title_elem else None,
                company_elem.text.strip() if company_elem else None,
                location_elem.text.strip() if location_elem else None,
                link["href"] if link else None
                ]
            writer.writerow(row)
            jobs.append(row)

    return jobs


location =input("Enter the location: ")
job_role =input("Enter the job role you want to search: ")
fetch_jobs_from_linkedin(job_role, location, max_results=100)
print("Job data has been written to linked.csv")    