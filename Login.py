import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UTMLoginTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize browser driver
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)
        
        # Access login page
        cls.driver.get("http://localhost:5173/")  # Replace with actual deployment URL
        print("Accessed UTM login page")

    def test_successful_login_and_role_selection(self):
        """Test successful login and role selection"""
        print("\n=== Testing login process ===")
        
        # Enter username
        username_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "username")))
        username_field.send_keys("admin")
        print("Entered username: admin")
        
        # Enter password
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys("bugless2025")
        print("Entered password")
        
        # Click login button
        login_button = self.driver.find_element(
            By.XPATH, "//button[contains(text(), 'Login')]"
        )
        login_button.click()
        print("Clicked login button")
        
        # Wait for role selection page to load
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'Select your role to continue')]")))
        print("Role selection page loaded")
        
        # Select PGAM role
        pgam_role_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'PGAM (Postgraduate Academic & Student Affairs Manager)')]"))
        )
        pgam_role_button.click()
        print("Selected PGAM role")
        
        # Verify successful redirection to PGAM dashboard
        try:
            self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'PGAM Dashboard')]"))
            )
            print("Successfully redirected to PGAM dashboard")
            print("=== Login process test passed ===")
        except:
            self.fail("Failed to redirect to PGAM dashboard")
    
    @classmethod
    def tearDownClass(cls):
        # Close browser
        cls.driver.quit()
        print("\nTesting completed, browser closed")

if __name__ == "__main__":
    unittest.main()