from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select  # Added Select class for dropdown handling
import time

# Initialize browser
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("http://localhost:5173/supervisor")

# Wait for page to load
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, "//table"))
)

def find_student(name):
    """Find student row"""
    # Search for student
    search_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search students...']"))
    )
    search_box.clear()
    search_box.send_keys(name)
    
    # Wait for search results
    time.sleep(1)
    
    # Return student row
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//tr[td[contains(., '{name}')]]"))
    )

def click_action_button(student_name, button_title):
    """Click action button"""
    # Build button XPath
    button_xpath = f"//tr[td[contains(., '{student_name}')]]//button[@title='{button_title}']"
    
    # Wait for button to be clickable and click
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, button_xpath))
    ).click()

def test_submit_research_title():
    print("===== Test 1: Submit Research Title =====")
    
    try:
        # Find student
        student_row = find_student("Jane Smith")
        
        # Click edit button
        click_action_button("Jane Smith", "Edit Research Title")
        
        # Wait for modal to appear
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h3[contains(., 'Enter Research Title')]"))
        )
        
        # Enter research title
        title_field = driver.find_element(By.XPATH, "//textarea")
        title_field.clear()
        title_field.send_keys("Advanced AI Systems for Renewable Energy")
        
        # Click save button
        save_button = driver.find_element(By.XPATH, "//button[contains(., 'Save Title')]")
        save_button.click()
        
        # Wait for modal to close
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, "//h3[contains(., 'Enter Research Title')]"))
        )
        
        # Verify status update
        time.sleep(1)
        updated_row = find_student("Jane Smith")
        status_badge = updated_row.find_element(By.XPATH, ".//span[contains(@class, 'bg-')]")
        assert "Title Submitted" in status_badge.text
        print("Test 1 passed: Research title submitted successfully!")
        return True
    except Exception as e:
        print(f"Test 1 failed: {str(e)}")
        return False

def test_submit_postponement():
    print("===== Test 2: Submit Postponement Request =====")
    
    try:
        # Find student
        student_row = find_student("John Doe")
        
        # Click postponement button
        click_action_button("John Doe", "Postponement Request")
        
        # Wait for modal to appear
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h3[contains(., 'Postponement Request')]"))
        )
        
        # Use more reliable way to handle dropdown
        request_select = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//select"))
        )
        
        # Use Selenium's Select class to handle dropdown
        select = Select(request_select)
        
        # Try to select "withdraw" option - using multiple methods
        try:
            # Method 1: Select by visible text
            select.select_by_visible_text("withdraw")
        except:
            try:
                # Method 2: Select by value attribute
                select.select_by_value("withdraw")
            except:
                try:
                    # Method 3: Select by index (usually the second option)
                    select.select_by_index(1)
                except:
                    # Method 4: Click option directly
                    request_select.find_element(By.XPATH, ".//option[contains(., 'withdraw')]").click()
        
        print("Request type selected")
        
        # Enter reason
        reason_field = driver.find_element(By.XPATH, "//textarea")
        reason_field.send_keys("1")
        print("Reason entered")
        
        # Submit request
        submit_button = driver.find_element(By.XPATH, "//button[contains(., 'Submit Request')]")
        submit_button.click()
        print("Request submitted")
        
        # Wait for modal to close
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, "//h3[contains(., 'Postponement Request')]"))
        )
        print("Modal closed")
        
        # Verify status
        time.sleep(1)
        updated_row = find_student("John Doe")
        status_badge = updated_row.find_element(By.XPATH, ".//span[contains(@class, 'bg-')]")
        status_text = status_badge.text
        print(f"Current status: {status_text}")
        
        if "Postponement Requested" in status_text:
            print("Test 2 passed: Postponement request submitted successfully!")
            return True
        else:
            print(f"Test 2 failed: Status not updated, current status: {status_text}")
            return False
    except Exception as e:
        print(f"Test 2 failed: {str(e)}")
        return False

# Run tests
try:
    # Test 1
    test1_passed = test_submit_research_title()
    
    # Test 2
    test2_passed = test_submit_postponement()
    
    if test1_passed and test2_passed:
        print("\n===== All tests passed! =====")
    else:
        print("\n===== Tests not fully passed =====")
        print(f"Test 1: {'Passed' if test1_passed else 'Failed'}")
        print(f"Test 2: {'Passed' if test2_passed else 'Failed'}")
    
except Exception as e:
    print(f"\nTest failed: {str(e)}")
    # Save error screenshot
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    driver.save_screenshot(f"test_error_{timestamp}.png")
    print(f"Saved error screenshot: test_error_{timestamp}.png")
    
    # Save page HTML
    with open(f"test_error_{timestamp}.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print(f"Saved page HTML: test_error_{timestamp}.html")
    
finally:
    # Close browser
    driver.quit()