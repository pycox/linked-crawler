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

# Configure Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
# options.add_argument('--headless')  # Optional: Run in headless mode to hide browser window

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

# LinkedIn credentials
linkedin_email = "demo@gmail.com"
linkedin_password = "demo"

# Log in to LinkedIn
login_to_linkedin(driver, linkedin_email, linkedin_password)

# Now, you can perform further actions with the logged-in session

# For example, let's print the current URL
print("Current URL:", driver.current_url)
