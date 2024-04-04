from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_to_linkedin(driver, email, password):
    try:
        # Navigate to the LinkedIn login page
        driver.get("https://www.linkedin.com/login")
        
        # Enter email and password
        email_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "username")))
        email_field.send_keys(email)
        
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        
        # Click sign-in button
        driver.find_element(By.XPATH, "//button[text()='Sign in']").click()
        
        # Wait for login to complete
        WebDriverWait(driver, 10).until(EC.url_contains("https://www.linkedin.com/feed/"))
        
    except Exception as e:
        print("Error logging in to LinkedIn:", e)

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

# Configure Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
# options.add_argument('--headless')  # Optional: Run in headless mode to hide browser window

# Initialize WebDriver with implicit wait
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to be located

# LinkedIn credentials
linkedin_email = "bradyalyssa479@gmail.com"
linkedin_password = "Asdf@1234"

# Log in to LinkedIn
login_to_linkedin(driver, linkedin_email, linkedin_password)

# Define the base URL to start collecting profile URLs from
base_url = "https://www.linkedin.com/search/results/people/?currentCompany=%5B%228074624%22%5D&origin=FACETED_SEARCH&page={}&sid=aLd"

# Collect profile URLs from all pages
all_profile_urls = set()  # Using a set to ensure unique URLs
for page_number in range(1, 101):  # Loop from page 1 to 100
    # Visit the page
    page_url = base_url.format(page_number)
    driver.get(page_url)
    
    # Extract profile URLs from the current page
    profile_urls = extract_profile_urls(driver)
    # Add the extracted URLs to the set of all profile URLs
    all_profile_urls.update(profile_urls)
    print(profile_urls)

# Print collected profile URLs
for url in all_profile_urls:
    print(url)

# Close the WebDriver session
driver.quit()
