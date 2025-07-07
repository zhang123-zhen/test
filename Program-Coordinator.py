from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import unittest

class ProgramCoordinatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configure download directory
        cls.download_dir = os.path.join(os.getcwd(), "downloads")
        if not os.path.exists(cls.download_dir):
            os.makedirs(cls.download_dir)
        
        # Set Chrome download options
        options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": cls.download_dir}
        options.add_experimental_option("prefs", prefs)
        
        # Initialize browser
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 20)
        
        # Navigate to Program Coordinator page
        cls.driver.get("http://localhost:5173/programCoordinator")
        cls.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//h1[contains(., 'Program Coordinator')]")
        ))
        print("Navigated to Program Coordinator page")
    
    def test_chair_reassignment(self):
        """Test chairperson reassignment functionality"""
        print("\n=== Starting chairperson reassignment test ===")
        
        # Fix: Add step to get student card
        student_card = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[.//span[contains(., 'Chair Assigned')]][1]")
        ))
        
        # Click Reassign button
        student_card.find_element(
            By.XPATH, ".//button[contains(., 'Reassign')]"
        ).click()
        
        # Verify modal opens
        modal = self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".fixed.inset-0.bg-black")
        ))
        print("Chair assignment modal opened")
        
        # Locate dropdown element
        dropdown = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#root > div > div > div > div.fixed.inset-0.bg-black.bg-opacity-50.flex.items-center.justify-center.z-50 > div > div.space-y-4 > div > select")
        ))
        time.sleep(1)  # Wait for dropdown to load

        select = Select(dropdown)
        select.select_by_visible_text("PM DR. WAN NORMEZA BINTI WAN ZAKARIA")
        print(f"Selected chairperson: PM DR. WAN NORMEZA BINTI WAN ZAKARIA")
        time.sleep(1)  # Wait for dropdown to update

        
        # Wait for modal to close
        self.wait.until(EC.invisibility_of_element(modal))
        print("Modal closed")
        time.sleep(2)  # Wait for page to update
        
        # Refresh student card information
        student_card = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[.//span[contains(., 'Chair Assigned')]][1]")
        ))
        time.sleep(1)  # Wait for student card to update
        # Verify chairperson update
        updated_chair = student_card.find_element(
            By.XPATH, ".//div[contains(., 'Chairperson')]/following-sibling::div"
        ).text
        print(f"Updated chairperson: {updated_chair}")
    
    def test_report_download(self):
        """Test report download functionality"""
        print("\n=== Starting report download test ===")
        
        # Clear download directory
        for f in os.listdir(self.download_dir):
            if f.endswith(".csv"):
                os.remove(os.path.join(self.download_dir, f))
        
        # Ensure no modal is blocking
        self.close_any_open_modals()
        
        # Find download button
        download_btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[contains(., 'Download Report')]]")
        ))
        print("Found download report button")
        
        # Use JavaScript click to avoid blocking issues
        self.driver.execute_script("arguments[0].click();", download_btn)
        print("Clicked download report button")
        
        # Wait for file download to complete
        file_found = False
        start_time = time.time()
        while time.time() - start_time < 30:  # 30-second timeout
            files = [f for f in os.listdir(self.download_dir) 
                    if f.startswith("First_Stage_Evaluation_Report_") and f.endswith(".csv")]
            if files:
                file_path = os.path.join(self.download_dir, files[0])
                # Wait for file to finish downloading (size stabilizes)
                prev_size = -1
                current_size = os.path.getsize(file_path)
                while current_size > prev_size:
                    prev_size = current_size
                    time.sleep(0.5)
                    current_size = os.path.getsize(file_path)
                
                if current_size > 0:  # Ensure file is not empty
                    file_found = True
                    print(f"Downloaded report: {files[0]}")
                    break
            time.sleep(1)
        
        self.assertTrue(file_found, "File download failed or timed out")
        print("=== Report download test passed ===")
    
    def close_any_open_modals(self):
        """Close any open modals that might be blocking"""
        try:
            # Try to find modal
            modal = self.driver.find_element(By.CSS_SELECTOR, ".fixed.inset-0.bg-black")
            if modal.is_displayed():
                # Try to click close button
                try:
                    close_btn = modal.find_element(By.XPATH, ".//button[contains(., 'Cancel')]")
                    close_btn.click()
                    print("Clicked cancel button to close modal")
                    time.sleep(0.5)
                except:
                    # Click outside modal to close
                    ActionChains(self.driver).move_by_offset(10, 10).click().perform()
                    print("Clicked outside to close modal")
                    time.sleep(0.5)
        except:
            pass  # Continue if no modal found
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        print("\nTesting completed, browser closed")

if __name__ == "__main__":
    unittest.main()