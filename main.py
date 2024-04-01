import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException

chromedriver_path = 'chromedriver.exe'

os.environ['PATH'] += os.pathsep + os.path.dirname(chromedriver_path)

def extract_email(driver):
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div[2]/section/div/section[2]/div/a")))
        
        # Find the email element within the contact modal using XPath
        email_element = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/section/div/section[2]/div/a")

        # Extract the email text
        email = email_element.text
        
        return email
    except NoSuchElementException:
        return None

# Function to log in to LinkedIn
def login_to_linkedin(driver, email, password):
    try:
        # Navigate to the LinkedIn login page
        driver.get("https://www.linkedin.com/login")
        time.sleep(1)
        # Enter the email and password
        email_field = driver.find_element(By.ID, "username")
        email_field.send_keys(email)
        time.sleep(1)
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        time.sleep(1)
        # Click the sign-in button
        driver.find_element(By.XPATH, "//button[text()='Sign in']").click()
        time.sleep(1)
        # Wait for the login to complete
        WebDriverWait(driver, 10).until(EC.url_contains("https://www.linkedin.com/feed/"))
        
    except Exception as e:
        print("Error logging in to LinkedIn:", e)

# Configure Selenium options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
# options.add_argument('--headless')  # Optional: Run in headless mode to hide browser window

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

# Credentials for logging in to LinkedIn
linkedin_email = "vehini7842@laymro.com"
linkedin_password = "4b>nf=624O7J"

# Log in to LinkedIn
login_to_linkedin(driver, linkedin_email, linkedin_password)

# Read profile URLs from CSV using pandas
df = pd.read_csv('followers.csv')
profile_urls = df['profileUrl'].tolist()

# Create empty lists to store the output
output_urls = []
output_emails = []

# Loop through each profile URL
for url in profile_urls:
    try:
        # Visit the profile URL
        driver.get(url)

        time.sleep(2)
        
        # Wait for the "Contact Info" element to be clickable
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[2]/span[2]/a')))

        # Click on the "Contact Info" element
        contact_info_button = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[2]/span[2]/a')
        contact_info_button.click()

        # Extract email information from the contact modal
        email = extract_email(driver)
        time.sleep(1)
        
        # Append the URL and email to the output lists
        output_urls.append(url)
        if email:
            output_emails.append(email)
        else:
            output_emails.append("No email found")
        
    except Exception as e:
        print(f"Error processing profile URL: {url}")
        print(e)

# Create a DataFrame from the output lists
output_df = pd.DataFrame({"Profile URL": output_urls, "Email": output_emails})

# Write the DataFrame to a CSV file (overwrite mode)
output_df.to_csv("scraped_data.csv", mode='w', index=False)

# Quit the WebDriver
driver.quit()
