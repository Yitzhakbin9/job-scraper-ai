import json
import os
import subprocess
from datetime import datetime
from scraper import scrape_linkedin_jobs
from analyzer import analyze_all_jobs, get_cost_summary


def load_search_settings() -> dict:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cv_path = os.path.join(base_dir, "cv_profile.txt")
    with open(cv_path, "r", encoding="utf-8") as f:
        content = f.read()

    keywords = "Full Stack Developer"
    location = "Israel"
    pages = 1

    for line in content.splitlines():
        if line.startswith("SEARCH KEYWORDS:"):
            keywords = line.split(":", 1)[1].strip()
        elif line.startswith("SEARCH LOCATION:"):
            location = line.split(":", 1)[1].strip()
        elif line.startswith("SEARCH PAGES:"):
            try:
                pages = int(line.split(":", 1)[1].strip())
            except ValueError:
                pass

    return {"keywords": keywords, "location": location, "pages": pages}


def save_to_json(jobs: list, cost: dict):
    data = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_jobs_found": len(jobs),
        "cost": cost,
        "jobs": jobs[:50]
    }

    base_dir = os.path.dirname(os.path.abspath(__file__))
    frontend_public = os.path.join(base_dir, "frontend", "public", "jobs.json")
    local_json = os.path.join(base_dir, "jobs.json")

    with open(local_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    if os.path.exists(os.path.dirname(frontend_public)):
        with open(frontend_public, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"JSON saved to frontend: {frontend_public}")

    print(f"JSON saved: {local_json}")


def main():
    settings = load_search_settings()
    print(f"Starting LinkedIn job scan...")
    print(f"Keywords: {settings['keywords']} | Location: {settings['location']} | Pages: {settings['pages']}\n")

    jobs = scrape_linkedin_jobs(
        keywords=settings["keywords"],
        location=settings["location"],
        num_pages=settings["pages"]
    )

    if not jobs:
        print("No jobs found. Try again later.")
        return

    print(f"\nAnalyzing {len(jobs)} jobs with Claude...\n")
    analyzed_jobs = analyze_all_jobs(jobs)
    cost = get_cost_summary()

    print("\nGenerating JSON...")
    save_to_json(analyzed_jobs, cost)

    print("\n--- TOP 5 JOBS ---")
    for job in analyzed_jobs[:5]:
        print(f"  {job['match_percentage']}% | {job['title']} @ {job['company']}")
        print(f"         {job.get('location', '')} | {job.get('reason', '')}")
        print()

    print(f"--- COST ---")
    print(f"  Input tokens:  {cost['input_tokens']:,}")
    print(f"  Output tokens: {cost['output_tokens']:,}")
    print(f"  Total cost:    ${cost['total_cost_usd']}")


if __name__ == "__main__":
    main()