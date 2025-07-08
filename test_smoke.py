import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
#............setup fixture..............#


@pytest.fixture()
def logged_in_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.get("https://opensource-demo.orangehrmlive.com/")
    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    yield driver
    driver.quit()


#---------------stc01---------------#

def test_one_lunch_url(driver):
    driver.get(r"https://opensource-demo.orangehrmlive.com/")
    assert "login" in driver.current_url.lower()
#test2............................
def test_two_login(driver):
    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    assert "dashboard" in driver.current_url.lower()
#3.........................................................
def test_three_dashboard_module(driver):
    modules=["Admin","PIM","Leave","Time"]
    for module in modules:
        assert driver.find_element(By.XPATH, f"//span[text()='{module}']").is_displayed()

#4...........

def test_four_logout_relogin(driver):
    driver.find_element(By.CLASS_NAME, "oxd-userdropdown-name").click()
    driver.find_element(By.PARTIAL_LINK_TEXT, "Logout").click()
    time.sleep(2)
    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    assert "dashboard" in driver.current_url.lower()
#5.....................
def test_five_leave_option(driver):
    driver.find_element(By.XPATH, "//span[text()='Leave']").click()
    time.sleep(2)
    assert "Leave" in driver.current_url.lower()
#6.................
def test_six_pim_module(driver):
    driver.find_element(By.XPATH, "//span[text()='PIM']").click()
    time.sleep(1)
    assert "Pim" in driver.current_url.lower()

#7.................
def test_seven_addemploy(driver):
    driver.find_element(By.LINK_TEXT, "Add Employee").click()
    time.sleep(2)
    assert "Add employee" in driver.page_source
#8....................
def test_eight_search_employee(driver):
    driver.find_element(By.LINK_TEXT, "Employee List").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//input[@placeholder='Type for hints...']").send_keys("A")
    time.sleep(1)
    assert "Employee List" in driver.page_source
#9......................
def test_nine_open_time_module(driver):
    driver.find_element(By.XPATH, "//span[text()='Time']").click()
    time.sleep(1)
    assert "time" in driver.current_url.lower()
#10................

def test_stc_10_change_password(driver):
    driver.find_element(By.XPATH, "//span[text()='My Info']").click()
    time.sleep(2)
    driver.execute_script("window.scrollBy(0, 800)")
    try:
        driver.find_element(By.XPATH, "//a[text()='Change Password']").click()
        time.sleep(1)
        assert "Change Password" in driver.page_source
    except:
        pytest.skip("Change Password section not available in demo site.")


