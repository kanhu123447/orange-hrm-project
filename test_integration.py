mport time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# TC_01: Verify navigation from Login to Home page
def test_login_navigation(driver):
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    time.sleep(2)
    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    assert "dashboard" in driver.current_url.lower(), "User did not navigate to Home page after login."


# TC_02: Verify Home page loads after login
def test_home_page_elements(driver):
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    time.sleep(2)
    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(3)
    dashboard_element = driver.find_element(By.XPATH, "//h6[text()='Dashboard']")
    assert dashboard_element.is_displayed(), "Dashboard element not visible. Home page did not load properly."


# TC_03: Verify Home page displays correct username after login
def test_username_display(driver):
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    time.sleep(2)
    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(3)
    username_element = driver.find_element(By.XPATH, "//p[@class='oxd-userdropdown-name']")
    expected_username = "Paul Collings"
    assert username_element.text == expected_username, f"Expected username '{expected_username}', but got '{username_element.text}'"


# TC_04: Verify clicking on Profile redirects to Profile page
def test_click_profile(driver):
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    time.sleep(2)
    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(3)
    driver.find_element(By.CLASS_NAME, "oxd-userdropdown-tab").click()
    time.sleep(2)
    profile_options = driver.find_elements(By.XPATH, "//ul[@class='oxd-dropdown-menu']/li")
    assert len(profile_options) > 0, "Profile options not displayed."


# TC_05: Verify updating profile details are reflected after saving
def test_update_profile(driver):
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    time.sleep(2)
    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(3)
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewMyDetails")
    time.sleep(3)
    edit_button = driver.find_element(By.XPATH, "//button[@class='oxd-button oxd-button--medium oxd-button--secondary']")
    edit_button.click()
    time.sleep(2)
    first_name_field = driver.find_element(By.NAME, "firstName")
    first_name_field.clear()
    first_name_field.send_keys("TestUser")
    save_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    save_button.click()
    time.sleep(3)
    updated_name = driver.find_element(By.NAME, "firstName").get_attribute("value")
    assert updated_name == "TestUser", "Profile update not saved correctly."


# TC_06: Verify logout from Home page
def test_logout(driver):
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    time.sleep(2)
    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(3)
    driver.find_element(By.CLASS_NAME, "oxd-userdropdown-tab").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Logout").click()
    time.sleep(2)
    assert "auth/login" in driver.current_url.lower(), "User is not redirected to login page after logout."


# TC_07: Verify session is destroyed after logout
def test_session_destroyed_after_logout(driver):
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    time.sleep(2)
    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(3)
    driver.find_element(By.CLASS_NAME, "oxd-userdropdown-tab").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Logout").click()
    time.sleep(2)
    driver.back()
    time.sleep(2)
    assert "auth/login" in driver.current_url.lower(), "Session not destroyed. User can still access the previous page."


# TC_08: Verify multiple modules accessibility after login
def test_multiple_module_accessibility(driver):
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    time.sleep(2)
    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(3)

    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList")
    time.sleep(2)
    assert "viewEmployeeList" in driver.current_url, "PIM module not accessible."

    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/leave/viewLeaveList")
    time.sleep(2)
    assert "viewLeaveList" in driver.current_url, "Leave module not accessible."

    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/time/viewTimeModule")
    time.sleep(2)
    assert "viewTimeModule" in driver.current_url, "Time module not accessible."


# TC_09: Verify wrong URL access without login
def test_protected_url_without_login(driver):
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index")
    time.sleep(2)
    assert "auth/login" in driver.current_url.lower(), "User is not redirected to login page when accessing protected URL without login."


# TC_10: Verify consistency of user data across modules
def test_user_data_consistency(driver):
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    time.sleep(2)
    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(3)

    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewMyDetails")
    time.sleep(3)
    name_in_profile = driver.find_element(By.NAME, "firstName").get_attribute("value")

    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index")
    time.sleep(3)
    username_element = driver.find_element(By.XPATH, "//p[@class='oxd-userdropdown-name']")
    assert name_in_profile in username_element.text, "User data inconsistency across modules."


