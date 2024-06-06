from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import time
import csv
import os

linkedin_email = "roman777bor@gmail.com"
linkedin_password = "star040308"

# Configure Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
options.add_argument("--log-level=3")
# options.add_argument('--headless')  # Optional: Run in headless mode to hide browser window

# Initialize WebDriver with implicit wait
driver = webdriver.Chrome(options=options)

metadata_csv_path = "metadata.csv"
if not os.path.exists(metadata_csv_path):
    with open(metadata_csv_path, mode="w", newline="") as metadata_file:
        metadata_writer = csv.writer(metadata_file)
        # Write the header row
        metadata_writer.writerow(
            ["Name", "Company", "Address", "profile_link", "email", "phone", "website"]
        )


def login_to_linkedin(email, password):
    try:
        # Navigate to the LinkedIn login page
        driver.get("https://www.linkedin.com/login")

        # Enter email and password
        email_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "username"))
        )
        email_field.send_keys(email)

        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        
        password_field.send_keys(Keys.ENTER)

        time.sleep(2)

        # Click sign-in button
        # driver.find_element(
        #     By.CSS_SELECTOR, 'button[data-id="sign-in-form__submit-btn"]'
        # ).click()

        time.sleep(8)

    except Exception as e:
        print("Error logging in to LinkedIn:", e)


login_to_linkedin(linkedin_email, linkedin_password)


def extract_profile_urls(driver):
    profile_urls = set()  # Using a set to store unique URLs
    # Find all profile elements
    profile_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/in/')]")
    # Filter out the profile URLs ending with "origin=FACETED_SEARCH"
    for element in profile_elements:
        href = element.get_attribute("href")
        if not href.endswith("origin=FACETED_SEARCH"):
            profile_urls.add(href)
    return profile_urls


# Define the base URL to start collecting profile URLs from
base_url = "https://www.linkedin.com/search/results/people/?geoUrn=%5B%22101282230%22%5D&origin=FACETED_SEARCH&titleFreeText=CEO"

# Collect profile URLs from all pages
all_profile_urls = set()  # Using a set to ensure unique URLs
for page_number in range(1, 99):  # Loop from page 1 to 100
    # Visit the page
    driver.get(f"{base_url}&page={page_number}")

    time.sleep(8)

    # Extract profile URLs from the current page
    profile_urls = extract_profile_urls(driver)
    # Add the extracted URLs to the set of all profile URLs
    all_profile_urls.update(profile_urls)
    print(profile_urls)


def fetch_profile(link):
    driver.get(link)

    time.sleep(8)

    try:
        name = driver.find_element(By.CSS_SELECTOR, "h1").text.strip()
    except:
        name = None

    try:
        company = driver.find_element(
            By.CSS_SELECTOR, "ul.pv-text-details__right-panel > li"
        ).text.strip()
    except:
        company = None

    try:
        address = driver.find_element(
            By.CSS_SELECTOR, ".pv-text-details__right-panel + .mt2 span:first-of-type"
        ).text.strip()
    except:
        address = None

    driver.find_element(By.CSS_SELECTOR, "a#top-card-text-details-contact-info").click()

    time.sleep(4)

    dom = driver.find_element(
        By.CSS_SELECTOR, "div#artdeco-modal-outlet"
    ).get_attribute("outerHTML")

    soup = BeautifulSoup(dom, "html.parser")

    profile_section = soup.find("h3", string=lambda text: "Profile" in text)
    profile_link_tag = profile_section.find_next_sibling() if profile_section else None
    profile_link = (
        profile_link_tag.find("a")["href"]
        if profile_link_tag and profile_link_tag.find("a")
        else None
    )

    website_section = soup.find("h3", string=lambda text: "Website" in text)
    website_link_tag = website_section.find_next_sibling() if website_section else None
    website_link = (
        website_link_tag.find("a")["href"]
        if website_link_tag and website_link_tag.find("a")
        else None
    )

    email_section = soup.find("h3", string=lambda text: "Email" in text)
    email = (
        email_section.find_next_sibling().get_text(strip=True)
        if email_section and email_section.find_next_sibling()
        else None
    )

    phone_section = soup.find("h3", string=lambda text: "Phone" in text)
    phone = (
        phone_section.find_next_sibling().get_text(strip=True)
        if phone_section and phone_section.find_next_sibling()
        else None
    )

    with open(metadata_csv_path, mode="a", newline="") as metadata_file:
        metadata_writer = csv.writer(metadata_file)
        # Write the header row
        row = [name, company, address, profile_link, email, phone, website_link]

        metadata_writer.writerow(row)

        print(row)


# Print collected profile URLs
for url in all_profile_urls:
    fetch_profile(url)

# Close the WebDriver session
driver.quit()
