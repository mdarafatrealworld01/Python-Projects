import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import time


class JobScraper:
    def __init__(self):
        self.jobs = []

    def scrape_indeed(self, query="python developer", location="remote", pages=1):
        print("🔍 Scraping Indeed...")
        for page in range(pages):
            url = f"https://www.indeed.com/jobs?q={query}&l={location}&start={page*10}"
            try:
                r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
                soup = BeautifulSoup(r.text, "html.parser")
                for div in soup.find_all("div", class_="job_seen_beacon"):
                    job = {
                        "title": div.find("h2", class_="jobTitle").text.strip() if div.find("h2", class_="jobTitle") else "",
                        "company": div.find("span", class_="companyName").text.strip() if div.find("span", class_="companyName") else "",
                        "location": div.find("div", class_="companyLocation").text.strip() if div.find("div", class_="companyLocation") else "",
                        "summary": div.find("div", class_="job-snippet").text.strip().replace("\n", " ") if div.find("div", class_="job-snippet") else "",
                        "source": "Indeed"
                    }
                    self.jobs.append(job)
            except Exception as e:
                print(f"Error scraping Indeed page {page}: {e}")
            time.sleep(1)

    def scrape_remotive(self):
        print("Scraping Remotive...")
        try:
            r = requests.get("https://remotive.io/api/remote-jobs")
            jobs = r.json().get("jobs", [])
            for job in jobs:
                self.jobs.append({
                    "title": job.get("title", ""),
                    "company": job.get("company_name", ""),
                    "location": job.get("candidate_required_location", ""),
                    "summary": job.get("description", "")[:150],
                    "source": "Remotive"
                })
        except Exception as e:
            print(f"Error scraping Remotive: {e}")

    def clean_data(self):
        print("Cleaning data...")

        if not self.jobs:
            print("No jobs collected. Skipping cleaning.")
            return

        df = pd.DataFrame(self.jobs)

        # Ensure required columns exist
        required_columns = ["title", "company", "location", "summary", "source"]
        for col in required_columns:
            if col not in df.columns:
                df[col] = ""

        df.drop_duplicates(subset=["title", "company", "location"], inplace=True)
        df.dropna(subset=["title", "company"], inplace=True)
        df.reset_index(drop=True, inplace=True)
        self.jobs = df.to_dict(orient="records")

    def save_to_csv(self, filename="job_listings.csv"):
        if not self.jobs:
            print("No data to save.")
            return
        df = pd.DataFrame(self.jobs)
        df.to_csv(filename, index=False)
        print(f"Saved to {filename}")

    def save_to_db(self, db_name="jobs.db"):
        if not self.jobs:
            print("No data to save in DB.")
            return
        print("Saving to SQLite DB...")
        conn = sqlite3.connect(db_name)
        df = pd.DataFrame(self.jobs)
        df.to_sql("job_listings", conn, if_exists="replace", index=False)
        conn.close()
        print(f"Data saved in {db_name}")

    def run(self):
        self.scrape_indeed()
        self.scrape_remotive()
        self.clean_data()
        self.save_to_csv()
        self.save_to_db()


if __name__ == "__main__":
    scraper = JobScraper()
    scraper.run()
