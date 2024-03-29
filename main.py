import requests
import csv
from bs4 import BeautifulSoup
import time
import random

class LinkedInScraper:

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        }

    def login(self):
        login_url = "https://www.linkedin.com/login"
        response = self.session.get(login_url, headers=self.headers)
        soup = BeautifulSoup(response.content, "html.parser")
        csrf_token = soup.find("input", {"name": "loginCsrfParam"})["value"]
        data = {
            "session_key": self.email,
            "session_password": self.password,
            "loginCsrfParam": csrf_token
        }
        login_attempt = self.session.post(login_url, data=data, headers=self.headers)
        return login_attempt.status_code == 200

    def scrape_profiles(self, num_profiles):
        profiles = []
        for _ in range(num_profiles):
            profile_url = "https://www.linkedin.com/in/random-profile"  # Replace with actual profile URL
            response = self.session.get(profile_url, headers=self.headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                name = soup.find("h1", class_="text-heading-xlarge").get_text().strip()
                email = ""  # Replace with code to extract email
                company_name = soup.find("a", class_="link-without-visited-state").get_text().strip()
                phone_number = ""  # Replace with code to extract phone number
                country = ""  # Replace with code to extract country
                profiles.append([name, email, company_name, phone_number, country])
            time.sleep(random.uniform(1, 5))  # Sleep to avoid rate limiting
        return profiles

    def export_to_csv(self, profiles):
        with open("linkedin_profiles.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name", "Email", "Company Name", "Phone Number", "Country"])
            writer.writerows(profiles)

if __name__ == "__main__":
    linkedin_email = "your_email@example.com"
    linkedin_password = "your_password"
    num_profiles_to_scrape = 1000
    scraper = LinkedInScraper(linkedin_email, linkedin_password)
    if scraper.login():
        print("Logged in successfully.")
        profiles = scraper.scrape_profiles(num_profiles_to_scrape)
        scraper.export_to_csv(profiles)
        print(f"Scraped {len(profiles)} profiles and exported data to 'linkedin_profiles.csv'.")
    else:
        print("Failed to login. Check your credentials.")
