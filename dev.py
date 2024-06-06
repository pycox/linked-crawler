from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests


import time

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
driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to be located


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

        # Click sign-in button
        driver.find_element(By.XPATH, "//button[text()='Sign in']").click()

        time.sleep(8)

    except Exception as e:
        print("Error logging in to LinkedIn:", e)


login_to_linkedin(linkedin_email, linkedin_password)


def main():
    driver.get("https://www.linkedin.com/in/dmytro-maloshtan-8a61702b0")

    time.sleep(8)

    name = driver.find_element(By.CSS_SELECTOR, "h1").text.strip()
    
    company = driver.find_element(
        By.CSS_SELECTOR, "ul.pv-text-details__right-panel > li"
    ).text.strip()
    
    address = driver.find_element(
        By.CSS_SELECTOR, ".pv-text-details__right-panel + .mt2 span:first-of-type"
    ).text.strip()

    driver.find_element(By.CSS_SELECTOR, "a#top-card-text-details-contact-info").click()

    time.sleep(4)
    
    dom = driver.find_element(By.CSS_SELECTOR, "div#artdeco-modal-outlet").get_attribute("outerHTML")

    soup = BeautifulSoup(dom, 'html.parser')

    profile_section = soup.find('h3', string=lambda text: 'Profile' in text)
    profile_link_tag = profile_section.find_next_sibling() if profile_section else None
    profile_link = profile_link_tag.find('a')['href'] if profile_link_tag and profile_link_tag.find('a') else None

    website_section = soup.find('h3', string=lambda text: 'Website' in text)
    website_link_tag = website_section.find_next_sibling() if website_section else None
    website_link = website_link_tag.find('a')['href'] if website_link_tag and website_link_tag.find('a') else None

    email_section = soup.find('h3', string=lambda text: 'Email' in text)
    email = email_section.find_next_sibling().get_text(strip=True) if email_section and email_section.find_next_sibling() else None

    phone_section = soup.find('h3', string=lambda text: 'Phone' in text)
    phone = phone_section.find_next_sibling().get_text(strip=True) if phone_section and phone_section.find_next_sibling() else None


main()
