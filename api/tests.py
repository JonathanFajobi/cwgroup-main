from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import Select
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
        driver.get("http://localhost:8000/signup/")
        
        # Fill out the signup form
        driver.find_element(By.ID, "username").send_keys("test0000")
        driver.find_element(By.ID, "password").send_keys("test0000")
        driver.find_element(By.ID, "first_name").send_keys("testttt")
        driver.find_element(By.ID, "last_name").send_keys("testtttest")
        driver.find_element(By.ID, "email").send_keys("test4@test.com")
        driver.find_element(By.ID, "dob").send_keys("0101-20-01")
        
        dropdown = Select(driver.find_element(By.ID, "hobbies"))
        dropdown.select_by_visible_text("swimming")
        
        driver.find_element(By.ID, "signupbutton").click()

        time.sleep(2)  # Wait for signup process to complete

        # Assert successful signup (e.g., redirect to login page)
        assert driver.current_url=="http://127.0.0.1:8000/login/", "Signup failed or incorrect page redirection"
        print("Signup succeeded, and the user was redirected to the login page.")

    def loginTest(self):
        """Test user login process."""
        driver = self.driver
        driver.get("http://localhost:8000/login/")
        
        # Fill out the login form
        driver.find_element(By.ID, "username").send_keys("test0000")
        driver.find_element(By.ID, "password").send_keys("test0000")
        driver.find_element(By.ID, "loginbutton").click()

        time.sleep(2)  # Wait for login process to complete

        # Assert successful login (e.g., redirect to dashboard)
        assert driver.current_url=="http://127.0.0.1:5173/", "Login failed or incorrect page redirection"

    def editTest(self):
        """Test editing user profile."""
        driver = self.driver
        driver.get("http://localhost:8000/login/")
        
        # Fill out the login form
        driver.find_element(By.ID, "username").send_keys("test0000")
        driver.find_element(By.ID, "password").send_keys("test0000")
        driver.find_element(By.ID, "loginbutton").click()

        time.sleep(2)  # Wait for login process to complete

        # Navigate to profile page
        driver.find_element(By.ID, "profilebutton").click()

        # Edit profile details
        driver.find_element(By.ID, "username").clear()
        driver.find_element(By.ID, "username").send_keys("test00001")
        driver.find_element(By.ID, "firstName").clear()
        driver.find_element(By.ID, "firstName").send_keys("tttttest")
        driver.find_element(By.ID, "lastName").clear()
        driver.find_element(By.ID, "lastName").send_keys("ttestttttest")
        driver.find_element(By.ID, "email").clear()
        driver.find_element(By.ID, "email").send_keys("ttest@ttestttttest.com")
        driver.find_element(By.ID, "dob").clear()
        driver.find_element(By.ID, "dob").send_keys("0202-20-02")
        
        dropdown = Select(driver.find_element(By.ID, "hobbiesupdate"))
        dropdown.select_by_visible_text("cycling")
        
        update_button = driver.find_element(By.ID, "updateprofilebutton")
        driver.execute_script("arguments[0].click();", update_button)

        time.sleep(2)
        
        passwordButton = driver.find_element(By.ID, "updatepasswordbutton")
        driver.execute_script("arguments[0].scrollIntoView();", passwordButton)
        driver.find_element(By.ID, "currentPassword").clear()
        driver.find_element(By.ID, "currentPassword").send_keys("test0000")
        driver.find_element(By.ID, "newPassword").clear()
        driver.find_element(By.ID, "newPassword").send_keys("test00001")
        
        driver.find_element(By.ID, "updatepasswordbutton").click()
        
        time.sleep(2)

        driver.refresh()
        
        time.sleep(3)
        updated_name = driver.find_element(By.ID, "username").text  # Replace 'user-name' with the actual ID or selector
        assert updated_name == "test0001", "Profile update failed: Name not updated on the page"

    def filterTest(self):
        """Test viewing users."""
        driver = self.driver
        driver.delete_all_cookies()
        driver.get("http://localhost:8000/login/")
        
        # Fill out the login form
        driver.find_element(By.ID, "username").send_keys("test1")
        driver.find_element(By.ID, "password").send_keys("test1")
        driver.find_element(By.ID, "loginbutton").click()

        time.sleep(2)  # Wait for login process to complete

        # Navigate to profile page
        driver.find_element(By.ID, "userbutton").click()
        
        initial_rows = driver.find_elements(By.XPATH, "//table[@id='userfiltertable']/tbody/tr")
        
        driver.find_element(By.ID, "startageinput").send_keys("5")
        driver.find_element(By.ID, "endageinput").send_keys("10")
        
        time.sleep(2)
        
        filter_rows = driver.find_elements(By.XPATH, "//table[@id='userfiltertable']/tbody/tr")
        
        assert len(filter_rows) < len(initial_rows), "Filtering did not reduce the number of rows"


# Run tests
if __name__ == "__main__":
    test_app = TestAppE2E()

    for browser in ["chrome", "firefox", "edge"]:  # Test across multiple browsers
        print(f"Running tests on {browser}...")
        test_app.setupMethod(browser)
        try:
            #uncomment out the relevant tests that you wish to test
            #please note some tests may return an error when run multiple times as the hardcoded values for user fields may already exist in the database
            
            #test_app.accountCreationTest()
            test_app.loginTest()
            #test_app.editTest()
            #test_app.filterTest()
        finally:
            test_app.teardownMethod()
