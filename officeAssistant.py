from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

# Configure Chrome options to disable speech recognition
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-speech-api")  # Disable speech API
chrome_options.add_argument("--disable-features=SpeechRecognitionService")  # Disable speech recognition
chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Disable media stream permission requests
chrome_options.add_argument("--disable-notifications")  # Disable notifications

# Initialize browser
driver = webdriver.Chrome(options=chrome_options)
driver.get("http://localhost:5173/officeAssistant")
driver.maximize_window()
print("Test page opened")

def wait_and_click(xpath, timeout=10):
    """Wait for element to be clickable then click"""
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath)))
    element.click()
    return element

def wait_and_send_keys(xpath, keys, timeout=10):
    """Wait for element to appear then send keys"""
    element = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.XPATH, xpath)))
    element.clear()
    element.send_keys(keys)
    return element

def wait_for_element(xpath, timeout=10):
    """Wait for element to appear and be visible"""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.XPATH, xpath)))

def is_modal_open():
    """Check if modal is open"""
    try:
        return len(driver.find_elements(By.XPATH, "//div[contains(@class, 'fixed inset-0') and contains(@class, 'z-50')]")) > 0
    except:
        return False

def test_add_student():
    """Test adding a student"""
    print("\n=== Testing student addition ===")
    
    try:
        # Click Add Student button
        wait_and_click("//button[.//span[text()='Add Student']]")
        print("Clicked Add Student button")
        
        # Wait for modal to open
        WebDriverWait(driver, 10).until(
            lambda d: len(d.find_elements(By.XPATH, "//div[contains(@class, 'fixed inset-0') and contains(@class, 'z-50')]")) > 0
        )
        print("Modal opened")
        
        # Simplified positioning - directly use labels in modal
        # Enter student name
        name_xpath = "//*[@id='root']/div/div/div/div[4]/div/div/div[1]/input"
        wait_and_send_keys(name_xpath, "Z")
        print("Entered name: Z")
        time.sleep(2)  # Wait for field update
        
        # Select department
        dept_xpath = "//*[@id='root']/div/div/div/div[4]/div/div/div[2]/select"
        dept_dropdown = wait_for_element(dept_xpath)
        Select(dept_dropdown).select_by_visible_text("Engineering")
        print("Selected department: Engineering")
        time.sleep(2) 
        
        # Select supervisor
        supervisor_xpath = "//*[@id='root']/div/div/div/div[4]/div/div/div[3]/select"
        supervisor_dropdown = wait_for_element(supervisor_xpath)
        # Get available supervisor options
        options = Select(supervisor_dropdown).options
        if len(options) > 1:
            Select(supervisor_dropdown).select_by_index(1)  # Select first valid supervisor
            print("Selected supervisor")
        else:
            print("⚠️ No supervisors available, selection failed")
        time.sleep(2) 
        
        # Select program
        programme_xpath = "//label[contains(., 'Programme')]/following-sibling::select"
        programme_dropdown = wait_for_element(programme_xpath)
        Select(programme_dropdown).select_by_visible_text("Master of Engineering")
        print("Selected program: Master of Engineering")
        time.sleep(2) 
        
        # Select evaluation type
        eval_label_xpath = "//label[contains(., 'Evaluation Type')]"
        wait_and_click(eval_label_xpath)
        print("Clicked evaluation type label")
        
        # Directly select option
        eval_option_xpath = "//option[contains(., 'Viva Voce')]"
        wait_and_click(eval_option_xpath)
        print("Selected evaluation type: Viva Voce")

        # Click Create button
        create_button_xpath = "//button[contains(., 'Create')]"
        wait_and_click(create_button_xpath)
        print("Clicked Create button")
        
        # Wait for modal to close
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'fixed inset-0') and contains(@class, 'z-50')]"))
        )
        print("Modal closed")
        
        # Verify student was added
        time.sleep(1)  # Give list time to update
        last_student_xpath = "(//table/tbody/tr)[last()]/td[1]"
        try:
            last_student_name = wait_for_element(last_student_xpath, 5).text
            if "Z" in last_student_name:
                print("✅ Student added successfully: New student appears in list")
            else:
                print(f"❌ Failed to add student: Last student is {last_student_name}")
        except:
            print("❌ Failed to add student: Could not find student record")
    
    except Exception as e:
        print(f"❌ Error in add student test: {str(e)}")
        # Save screenshot for debugging
        driver.save_screenshot("add_student_error.png")
        print("Saved error screenshot: add_student_error.png")

def test_edit_student():
    """Test editing a student"""
    print("\n=== Starting student edit test ===")
    
    try:
        # Find target student record
        student_name = "John Doe"
        student_row_xpath = f"//table/tbody/tr[td[text()='{student_name}']]"
        student_row = wait_for_element(student_row_xpath)
        
        # Click edit button
        edit_button = student_row.find_element(By.XPATH, ".//button[1]")  # First button is edit
        edit_button.click()
        print(f"Clicked edit button for {student_name}")
        
        # Wait for edit modal to open
        WebDriverWait(driver, 10).until(
            lambda d: len(d.find_elements(By.XPATH, "//div[contains(@class, 'fixed inset-0') and contains(@class, 'z-50')]")) > 0
        )
        print("Edit modal opened")
        
        # Modify name
        name_xpath = "//*[@id='root']/div/div/div/div[4]/div/div/div[1]/input"
        name_field = wait_for_element(name_xpath)
        name_field.clear()
        new_name = "J"
        name_field.send_keys(new_name)
        print(f"Changed name to: {new_name}")
        
        # Click Update button
        update_button_xpath = "//button[contains(., 'Update')]"
        wait_and_click(update_button_xpath)
        print("Clicked Update button")
        
        # Wait for modal to close
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'fixed inset-0') and contains(@class, 'z-50')]"))
        )
        print("Modal closed")
        
        # Verify name was updated
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, f"//table/tbody/tr/td[text()='{new_name}']"), new_name)
        )
        print(f"✅ Student edit test passed: Name updated to {new_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Student edit test failed: {str(e)}")
        driver.save_screenshot("edit_student_error.png")
        return False

def test_delete_student():
    """Test deleting a student"""
    print("\n=== Starting student deletion test ===")
    
    try:
         # Get student count before deletion
        students_before = len(driver.find_elements(By.XPATH, "//table/tbody/tr"))
        print(f"Students before deletion: {students_before}")

        # Find target student record
        student_name = "Jane Smith"
        student_row_xpath = f"//table/tbody/tr[td[text()='{student_name}']]"
        student_row = wait_for_element(student_row_xpath)
        
        
        # Click delete button
        delete_button = student_row.find_element(By.XPATH, ".//button[2]")  # Second button is delete
        delete_button.click()
        print(f"Clicked delete button for {student_name}")
        
        # Wait for student to be deleted
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, student_row_xpath))
        )
        
        # Get student count after deletion
        students_after = len(driver.find_elements(By.XPATH, "//table/tbody/tr"))
        print(f"Students after deletion: {students_after}")
        
        # Verify deletion result
        if students_after == students_before - 1:
            print(f"✅ Student deletion test passed: {student_name} removed from list")
            return True
        else:
            print(f"❌ Student deletion test failed: Record count did not decrease")
            return False
            
    except Exception as e:
        print(f"❌ Student deletion test failed: {str(e)}")
        driver.save_screenshot("delete_student_error.png")
        return False

def test_search_student():
    """Test student search - using initial data with 'J'"""
    print("\n=== Starting student search test ===")
    
    try:
        # Refresh page to ensure initial data
        driver.refresh()
        print("Page refreshed")
        
        # Wait for page to reload
        wait_for_element("//table/tbody/tr", 10)
        print("Student list loaded")
        
        # Get initial student list
        students = driver.find_elements(By.XPATH, "//table/tbody/tr")
        initial_count = len(students)
        print(f"Initial student count: {initial_count}")
        
        # Search for 'J'
        search_box_xpath = "//input[@placeholder='Search students...']"
        search_box = wait_for_element(search_box_xpath)
        search_box.clear()
        search_box.send_keys("J")
        print("Searched for: J")
        
        # Wait for search results - ensure search completes
        time.sleep(2)  # Increase wait time
        
        # Get search results
        search_results = driver.find_elements(By.XPATH, "//table/tbody/tr")
        visible_names = []
        
        # Safely get student names
        for student in search_results:
            try:
                name = student.find_element(By.XPATH, "./td[1]").text
                visible_names.append(name)
            except:
                pass  # Ignore possibly stale elements
        
        print(f"Search results: {visible_names}")
        
        # Correct validation logic
        # 1. Verify all displayed names contain 'J' (case-insensitive)
        all_contain_j = all("J" in name.upper() for name in visible_names)
        
        # 2. Verify number of students displayed
        count_ok = len(visible_names) == 2  # Expect both students to contain 'J'
        
        if all_contain_j and count_ok:
            print("✅ Search test passed: All displayed students contain 'J'")
            result = True
        else:
            # Provide detailed failure info
            if not all_contain_j:
                invalid_names = [name for name in visible_names if "J" not in name.upper()]
                print(f"❌ Search test failed: These students don't contain 'J': {invalid_names}")
            if not count_ok:
                print(f"❌ Search test failed: Expected 2 students, found {len(visible_names)}")
            result = False
        
        return result
        
    except Exception as e:
        print(f"❌ Student search test failed: {str(e)}")
        driver.save_screenshot("search_student_error.png")
        return False

# Execute tests
try:
    test_add_student()
    test_edit_student()
    test_delete_student()
    test_search_student()
    print("\n===== All tests completed =====")
except Exception as e:
    print(f"\n❌ Test error: {str(e)}")
    # Save screenshot for debugging
    driver.save_screenshot("test_error.png")
    print("Saved error screenshot: test_error.png")
    import traceback
    traceback.print_exc()  # Print full stack trace
finally:
    # Keep browser open for inspection
    print("Testing completed, please inspect page manually")
    print("Browser remains open")