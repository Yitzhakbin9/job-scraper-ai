import requests
from bs4 import BeautifulSoup
import time

def scrape_linkedin_jobs(keywords="Full Stack Developer", location="Israel", num_pages=3):
    jobs = []
    seen = set()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for page in range(num_pages):
        start = page * 25
        url = (
            f"https://www.linkedin.com/jobs/search?"
            f"keywords={keywords.replace(' ', '%20')}"
            f"&location={location}"
            f"&f_TPR=r86400"
            f"&start={start}"
        )

        print(f"Scanning page {page + 1}...")
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Error on page {page + 1}: status {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all("div", class_="base-card")

        if not job_cards:
            print(f"No jobs found on page {page + 1}")
            break

        for card in job_cards:
            try:
                title = card.find("h3", class_="base-search-card__title")
                company = card.find("h4", class_="base-search-card__subtitle")
                location_tag = card.find("span", class_="job-search-card__location")
                link_tag = card.find("a", class_="base-card__full-link")

                title_text = title.get_text(strip=True) if title else "N/A"
                company_text = company.get_text(strip=True) if company else "N/A"

                key = f"{title_text}|{company_text}"
                if key in seen:
                    continue
                seen.add(key)

                job = {
                    "title": title_text,
                    "company": company_text,
                    "location": location_tag.get_text(strip=True) if location_tag else "N/A",
                    "link": str(link_tag["href"]).strip() if link_tag else "N/A",
                }
                jobs.append(job)

            except Exception as e:
                print(f"Warning: Error parsing card: {e}")
                continue

        time.sleep(2)

    print(f"Found {len(jobs)} unique jobs")
    return jobs


if __name__ == "__main__":
    jobs = scrape_linkedin_jobs()
    for job in jobs[:5]:
        print(job)