from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv

for i in range(1,10):

    def fetch_jobs_from_linkedin(query: str, location: str, max_results=1000):
        global jobs
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
        with open("content.html","w",encoding="utf-8") as files:
            files.write(soup.text)
        
        with open("linked.csv","a",newline="",encoding="utf-8") as file:
            writer =csv.writer(file)
        #  writer.writerow(["title","company","location","apply_link"])
            for card in job_cards:
                title_elem = card.find("h3", class_="base-search-card__title").text.strip()
                company_elem = card.find("h4", class_="base-search-card__subtitle").text.strip()
                location_elem = card.find("span", class_="job-search-card__location").text.strip()
                link= card.find("a", class_="base-card__full-link", href=True)
                link_elem =link["href"] if link else None
                writer.writerow([title_elem,company_elem,location_elem,link_elem])
                

        return jobs

if __name__ == "__main__":
    fetch_jobs_from_linkedin("python", "UAE", max_results=700)
    