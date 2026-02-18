import anthropic
import os
import json
import re
import time
from anthropic.types import TextBlock
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

total_input_tokens = 0
total_output_tokens = 0

def get_cost_summary() -> dict:
    input_cost = (total_input_tokens / 1_000_000) * 0.80
    output_cost = (total_output_tokens / 1_000_000) * 4.00
    total_cost = input_cost + output_cost
    return {
        "input_tokens": total_input_tokens,
        "output_tokens": total_output_tokens,
        "total_cost_usd": round(total_cost, 5)
    }

def load_cv_profile():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cv_path = os.path.join(base_dir, "cv_profile.txt")
    with open(cv_path, "r", encoding="utf-8") as f:
        return f.read()

def analyze_job(job: dict, cv_profile: str) -> dict:
    global total_input_tokens, total_output_tokens

    prompt = f"""
You are a job matching expert. Given a candidate profile and a job listing, analyze the match.

CANDIDATE PROFILE:
{cv_profile}

JOB LISTING:
Title: {job['title']}
Company: {job['company']}
Location: {job['location']}

You must respond with ONLY a JSON object, no other text, no markdown, no backticks.
Example response:
{{"match_percentage": 85, "reason": "Strong React and Node.js match"}}

Rules:
- match_percentage: number 0-100
- reason: one short sentence
- Penalize heavily if job is Java-only
- Penalize if job is outside center of Israel
- Boost if job requires React, Node.js, JavaScript
"""

    for attempt in range(3):
        try:
            message = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )

            total_input_tokens += message.usage.input_tokens
            total_output_tokens += message.usage.output_tokens

            content_block = message.content[0]
            if not isinstance(content_block, TextBlock):
                raise ValueError("Unexpected response type")

            raw = content_block.text.strip()
            match = re.search(r'\{.*\}', raw, re.DOTALL)
            if not match:
                raise ValueError(f"No JSON found in response: {raw}")

            result = json.loads(match.group())
            job["match_percentage"] = result.get("match_percentage", 0)
            job["reason"] = result.get("reason", "")
            return job

        except Exception as e:
            if "overloaded" in str(e).lower() and attempt < 2:
                wait = (attempt + 1) * 5
                print(f"API overloaded, retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"Warning: Error analyzing job: {e}")
                job["match_percentage"] = 0
                job["reason"] = "Error"
                return job

    return job


def analyze_all_jobs(jobs: list) -> list:
    cv_profile = load_cv_profile()
    analyzed = []

    for i, job in enumerate(jobs):
        print(f"Analyzing job {i+1}/{len(jobs)}: {job['title']} @ {job['company']}")
        analyzed_job = analyze_job(job, cv_profile)
        analyzed.append(analyzed_job)

    analyzed.sort(key=lambda x: x["match_percentage"], reverse=True)
    return analyzed