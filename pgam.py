import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PGAMNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize browser driver
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)
        
        # Directly access PGAM Dashboard page
        cls.driver.get("http://localhost:5173/pgam")  # Replace with actual deployment URL
        print("PGAM Dashboard loaded")

    def test_overview_navigation(self):
        """Verify Overview navigation item loads overview page"""
        # Click Overview navigation item
        overview_nav = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Overview']]"))
        )
        overview_nav.click()
        
        # Verify unique elements on overview page
        self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//h3[text()='Students by Department']")
        ))
        self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//h3[text()='Evaluation Process Status']")
        ))
        print("Overview page verified")

    def test_students_navigation(self):
        """Verify All Students navigation item loads student list page"""
        # Click All Students navigation item
        students_nav = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='All Students']]"))
        )
        students_nav.click()
        
        # Verify unique elements on student list page
        self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//th[text()='Student']")
        ))
        self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//input[@placeholder='Search students, titles, supervisors...']")
        ))
        print("All Students page verified")

    def test_workload_navigation(self):
        """Verify Workload Analysis navigation item loads workload analysis page"""
        # Click Workload Analysis navigation item
        workload_nav = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Workload Analysis']]"))
        )
        workload_nav.click()
        
        # Verify unique elements on workload analysis page
        self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//h3[text()='Examiner Workload']")
        ))
        self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//h3[text()='Chairperson Workload']")
        ))
        print("Workload Analysis page verified")

    @classmethod
    def tearDownClass(cls):
        # Close browser
        cls.driver.quit()
        print("Testing completed, browser closed")

if __name__ == "__main__":
    unittest.main()