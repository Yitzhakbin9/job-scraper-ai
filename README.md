# Job Scraper AI

An AI-powered job scraper that searches LinkedIn for job listings, analyzes each one against your personal CV profile using Claude, and presents the results in both an Excel report and a React dashboard.

## How It Works

1. **Scraper** — fetches LinkedIn job listings posted in the last 24 hours for your chosen keywords and location
2. **Analyzer** — sends each listing to Claude Haiku, which scores it against your `cv_profile.txt` and returns a match percentage + reason
3. **Output** — saves results to a color-coded `.xlsx` file and a `jobs.json` file
4. **Dashboard** — a React frontend reads `jobs.json` and lets you filter/search jobs by match level

## Project Structure

```
job-agent/
├── main.py          # Entry point — orchestrates scraping, analysis, and output
├── scraper.py       # LinkedIn scraper (BeautifulSoup)
├── analyzer.py      # Claude AI job matcher
├── cv_profile.txt   # Your personal profile (edit this)
├── .env             # API key (never committed)
└── frontend/        # React + Vite dashboard
    └── src/
        └── App.jsx
```

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Yitzhakbin9/job-scraper-ai.git
cd job-scraper-ai
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Add your API key

Create a `.env` file in the root:

```
ANTHROPIC_API_KEY=your_api_key_here
```

### 4. Fill in your CV profile

Edit `cv_profile.txt` with your details — name, tech stack, location preferences, and what you're not looking for. The AI uses this to score each job.

### 5. Configure your search

In `main.py`, update the search parameters:

```python
jobs = scrape_linkedin_jobs(
    keywords="Full Stack Developer",
    location="Israel",
    num_pages=1
)
```

### 6. Run the scraper

```bash
python main.py
```

This will:
- Scrape LinkedIn for matching jobs
- Analyze each one with Claude
- Save a `jobs_YYYY-MM-DD.xlsx` file (opens automatically on Mac)
- Save `jobs.json` for the dashboard

## Dashboard

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) to view the dashboard.

Features:
- Filter by **High** (≥80%), **Mid** (≥50%), or **Low** match
- Search by job title or company name
- Shows API cost per run (input/output tokens)
- Click any job title to open it on LinkedIn

## Match Colors

| Color | Range | Meaning |
|-------|-------|---------|
| Green | ≥ 80% | Strong match |
| Yellow | 50–79% | Partial match |
| Red | < 50% | Weak match |

## Requirements

- Python 3.9+
- Node.js 18+
- [Anthropic API key](https://console.anthropic.com/)
