from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Iterable
from urllib.parse import quote_plus, urljoin

from bs4 import BeautifulSoup
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError  # pyright: ignore[reportMissingImports]
from playwright.sync_api import sync_playwright  # pyright: ignore[reportMissingImports]

BASE_URL = "https://www.linkedin.com"
SEARCH_URL_TEMPLATE = (
    "https://www.linkedin.com/jobs/search?keywords={query}&location={location}"
    "&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"
)


def build_search_url(query: str, location: str) -> str:
    return SEARCH_URL_TEMPLATE.format(query=quote_plus(query), location=quote_plus(location))


def build_paginated_search_urls(search_url: str, max_results: int, page_size: int = 25) -> list[str]:
    safe_page_size = max(1, page_size)
    total_pages = max(1, math.ceil(max_results / safe_page_size))
    urls: list[str] = []

    for page_idx in range(total_pages):
        start = page_idx * safe_page_size
        separator = "&" if "?" in search_url else "?"
        urls.append(f"{search_url}{separator}start={start}")

    return urls


def _load_more_job_cards(page, target_cards: int, timeout_ms: int) -> None:
    target_cards = max(1, target_cards)
    stagnant_rounds = 0
    max_rounds = max(20, target_cards // 3)

    for _ in range(max_rounds):
        current_count = page.locator("div.base-card").count()
        if current_count >= target_cards:
            return

        page.mouse.wheel(0, 5000)
        page.wait_for_timeout(800)

        show_more = page.locator(
            "button.infinite-scroller__show-more-button, button:has-text('See more jobs')"
        ).first
        if show_more.count() > 0 and show_more.is_visible():
            show_more.click(timeout=timeout_ms)
            page.wait_for_timeout(1000)

        updated_count = page.locator("div.base-card").count()
        if updated_count <= current_count:
            stagnant_rounds += 1
            if stagnant_rounds >= 5:
                return
        else:
            stagnant_rounds = 0


def fetch_listing_html(
    search_url: str,
    headless: bool = True,
    timeout_ms: int = 15000,
    target_cards: int = 100,
) -> str:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(search_url, wait_until="domcontentloaded", timeout=timeout_ms)

        try:
            page.wait_for_selector("div.base-card", timeout=timeout_ms)
        except PlaywrightTimeoutError:
            pass

        _load_more_job_cards(page, target_cards=target_cards, timeout_ms=timeout_ms)

        html = page.content()
        browser.close()
        return html


def fetch_listing_pages_html(
    search_url: str,
    max_results: int,
    headless: bool = True,
    timeout_ms: int = 15000,
    page_size: int = 25,
) -> list[str]:
    html_pages: list[str] = []
    urls = build_paginated_search_urls(search_url, max_results=max_results, page_size=page_size)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=headless)
        page = browser.new_page()

        for url in urls:
            page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)

            try:
                page.wait_for_selector("div.base-card", timeout=timeout_ms)
            except PlaywrightTimeoutError:
                pass

            _load_more_job_cards(page, target_cards=page_size, timeout_ms=timeout_ms)
            html_pages.append(page.content())

        browser.close()

    return html_pages


def parse_job_cards(html: str, max_results: int = 100) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("div.base-card")[:max_results]
    jobs: list[dict[str, str]] = []

    for card in cards:
        title = _text(card, "h3.base-search-card__title, h3.title, h2")
        company = _text(card, "h4.base-search-card__subtitle, h3.company, .base-search-card__subtitle")
        location = _text(card, "span.job-search-card__location, p.location, .job-search-card__location")
        link = card.select_one("a.base-card__full-link[href], a[href]")
        href = str(link.get("href")) if link and link.has_attr("href") else ""
        apply_link = urljoin(BASE_URL, href) if href else ""

        if title or company or location or apply_link:
            jobs.append(
                {
                    "title": title,
                    "company": company,
                    "location": location,
                    "apply_link": apply_link,
                }
            )

    return jobs


def _text(node, selector: str) -> str:
    found = node.select_one(selector)
    return found.get_text(strip=True) if found else ""


def export_jobs(jobs: Iterable[dict[str, str]], output_path: str) -> None:
    path = Path(output_path)
    rows = list(jobs)

    if path.suffix.lower() == ".json":
        path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        return

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "company", "location", "apply_link"])
        writer.writeheader()
        writer.writerows(rows)


def scrape_linkedin_jobs(query: str, location: str, output_path: str, max_results: int = 100, headless: bool = True) -> list[dict[str, str]]:
    search_url = build_search_url(query, location)
    html_pages = fetch_listing_pages_html(search_url, max_results=max_results, headless=headless)

    deduped_jobs: list[dict[str, str]] = []
    seen_keys: set[str] = set()

    for html in html_pages:
        for job in parse_job_cards(html, max_results=max_results):
            job_key = job["apply_link"] or f"{job['title']}|{job['company']}|{job['location']}"
            if job_key in seen_keys:
                continue
            seen_keys.add(job_key)
            deduped_jobs.append(job)
            if len(deduped_jobs) >= max_results:
                break
        if len(deduped_jobs) >= max_results:
            break

    jobs = deduped_jobs

    if not jobs:
        raise RuntimeError(
            "No job cards were found. LinkedIn may be showing a login page, challenge page, or a page that did not finish loading."
        )

    export_jobs(jobs, output_path)
    return jobs


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape LinkedIn job listings and export them to CSV or JSON.")
    parser.add_argument("--query", help="Job title or search keywords")
    parser.add_argument("--location", help="Job location")
    parser.add_argument("--output", default="linked_job.csv", help="Output file path (.csv or .json)")
    parser.add_argument("--max-results", type=int, default=100, help="Maximum number of jobs to keep")
    parser.add_argument("--headless", action="store_true", help="Run the browser in headless mode")
    parser.add_argument("--visible", action="store_true", help="Run the browser visibly for debugging")
    args = parser.parse_args()

    query = args.query or input("Enter the job role you want to search: ").strip()
    location = args.location or input("Enter the location(country name): ").strip()
    headless = args.headless or not args.visible

    jobs = scrape_linkedin_jobs(
        query=query,
        location=location,
        output_path=args.output,
        max_results=args.max_results,
        headless=headless,
    )
    print(f"Saved {len(jobs)} jobs to {args.output}")


if __name__ == "__main__":
    main()