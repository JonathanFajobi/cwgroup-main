from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
import time

# Test class
class TestAppE2E:
    def setupMethod(self, browser="chrome"):
        """Setup browser before each test."""
        if browser.lower() == "chrome":
            self.driver = webdriver.Chrome(service=ChromeService())
        elif browser.lower() == "firefox":
            self.driver = webdriver.Firefox(service=FirefoxService())
        elif browser.lower() == "edge":
            self.driver = webdriver.Edge(service=EdgeService())
        else:
            raise ValueError("Unsupported browser! Use 'chrome', 'firefox', or 'edge'.")
        
        self.driver.maximize_window()

    def teardownMethod(self):
        """Tear down browser after each test."""
        self.driver.quit()

    def accountCreationTest(self):
        """Test user signup process."""
        driver = self.driver
        driver.get("http://localhost:8000/signup")
        
        # Fill out the signup form
        driver.find_element(By.NAME, "name").send_keys("Test User")
        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "email").send_keys("testuser@example.com")
        driver.find_element(By.NAME, "password").send_keys("testpassword")
        driver.find_element(By.NAME, "confirm_password").send_keys("testpassword")
        driver.find_element(By.NAME, "date_of_birth").send_keys("2000-01-01")
        driver.find_element(By.ID, "signup-btn").click()

        time.sleep(3)  # Wait for signup process to complete

        # Assert successful signup (e.g., redirect to login page)
        assert "Login" in driver.title, "Signup failed or incorrect page redirection"

    def loginTest(self):
        """Test user login process."""
        driver = self.driver
        driver.get("http://localhost:8000/login")
        
        # Fill out the login form
        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("testpassword")
        driver.find_element(By.ID, "login-btn").click()

        time.sleep(3)  # Wait for login process to complete

        # Assert successful login (e.g., redirect to dashboard)
        assert "Dashboard" in driver.title, "Login failed or incorrect page redirection"

    def profileEditTest(self):
        """Test editing user profile."""
        driver = self.driver
        driver.get("http://localhost:8000/login")
        
        # Log in
        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("testpassword")
        driver.find_element(By.ID, "login-btn").click()
        
        time.sleep(3)

        # Navigate to profile page
        driver.find_element(By.ID, "profile-link").click()

        # Edit profile details
        driver.find_element(By.NAME, "name").clear()
        driver.find_element(By.NAME, "name").send_keys("Updated Test User")
        driver.find_element(By.ID, "save-profile-btn").click()

        time.sleep(3)

        # Assert profile updated (e.g., check for success message or updated value)
        assert "Profile updated" in driver.page_source, "Profile update failed"

    # Add other test methods similarly...


# Run tests
if __name__ == "__main__":
    test_app = TestAppE2E()

    for browser in ["chrome", "firefox", "edge"]:  # Test across multiple browsers
        print(f"Running tests on {browser}...")
        test_app.setup_method(browser)
        try:
            test_app.test_account_creation()
            test_app.test_login()
            test_app.test_edit_profile()
            # Call other test methods here...
        finally:
            test_app.teardown_method()
