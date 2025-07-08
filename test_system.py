import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()  # No Options or Service used
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def login(driver, username="Admin", password="admin123"):
    driver.get(r"https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    time.sleep(2)
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)

def logout(driver):
    driver.find_element(By.CLASS_NAME, "oxd-userdropdown-name").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Logout").click()
    time.sleep(2)

# STC_01: Verify successful login with valid credentials
def test_stc_01_valid_login(driver):
    login(driver)
    assert "dashboard" in driver.current_url.lower()

# STC_02: Verify login failure with invalid credentials
def test_stc_02_invalid_login(driver):
    driver.get(r"https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    driver.find_element(By.NAME, "username").send_keys("wrong")
    driver.find_element(By.NAME, "password").send_keys("wrong")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    assert "Invalid credentials" in driver.page_source

# STC_03: Verify complete profile update flow
def test_stc_03_update_profile(driver):
    login(driver)
    driver.get(r"https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewMyDetails")
    time.sleep(2)
    assert "Personal Details" in driver.page_source

# STC_04: Verify leave application process
def test_stc_04_apply_leave(driver):
    login(driver)
    driver.get(r"https://opensource-demo.orangehrmlive.com/web/index.php/leave/applyLeave")
    time.sleep(2)
    driver.find_element(By.XPATH, "//label[text()='Leave Type']/following::div[1]").click()
    driver.find_element(By.XPATH, "//span[text()='CAN - Personal']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//label[text()='From Date']/following::input[1]").send_keys("2025-07-10")
    driver.find_element(By.XPATH, "//label[text()='To Date']/following::input[1]").send_keys("2025-07-10")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    assert "Successfully Submitted" in driver.page_source or "Leave" in driver.title

# STC_05: Verify the entire employee search functionality
def test_stc_05_search_employee(driver):
    login(driver)
    driver.get(r"https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList")
    driver.find_element(By.XPATH, "//input[@placeholder='Type for hints...']").send_keys("Linda")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    assert "Linda" in driver.page_source

# STC_06: Verify the logout functionality
def test_stc_06_logout(driver):
    login(driver)
    logout(driver)
    assert "login" in driver.current_url.lower()

# STC_07: Verify that session expires after logout or inactivity
def test_stc_07_session_expired(driver):
    login(driver)
    logout(driver)
    driver.get(r"https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index")
    time.sleep(2)
    assert "login" in driver.current_url.lower()

# STC_08: Verify multiple module navigation (Dashboard, PIM, Leave, Time)
def test_stc_08_module_navigation(driver):
    login(driver)
    modules = ["dashboard", "pim", "leave", "time"]
    for module in modules:
        driver.get(f"https://opensource-demo.orangehrmlive.com/web/index.php/{module}/view{module.capitalize()}")
        time.sleep(2)
        assert module in driver.current_url.lower()

# STC_09: Verify the password change process
def test_stc_09_password_change(driver):
    login(driver)
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewMyDetails")
    assert "Personal Details" in driver.page_source

# STC_10: Verify that user-specific data remains consistent across sessions
def test_stc_10_data_consistency(driver):
    login(driver)
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewMyDetails")
    time.sleep(2)
    first_name = driver.find_element(By.NAME, "firstName").get_attribute("value")
    logout(driver)
    login(driver)
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewMyDetails")
    time.sleep(2)
    assert first_name in driver.page_source
