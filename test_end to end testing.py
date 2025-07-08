import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_e2e_add_employee_and_assign_leave(driver):
    # Step 1: Login
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    assert "dashboard" in driver.current_url.lower()

    # Step 2: Go to PIM > Add Employee
    driver.find_element(By.XPATH, "//span[text()='PIM']").click()
    driver.find_element(By.LINK_TEXT, "Add Employee").click()
    time.sleep(2)
    driver.find_element(By.NAME, "firstName").send_keys("E2EUser")
    driver.find_element(By.NAME, "lastName").send_keys("Test")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(3)

    # Step 3: Go to Leave > Apply Leave
    driver.find_element(By.XPATH, "//span[text()='Leave']").click()
    driver.find_element(By.LINK_TEXT, "Apply").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//label[text()='Leave Type']/following::div[1]").click()
    driver.find_element(By.XPATH, "//span[text()='CAN - Personal']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//label[text()='From Date']/following::input[1]").send_keys("2025-07-15")
    driver.find_element(By.XPATH, "//label[text()='To Date']/following::input[1]").send_keys("2025-07-15")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    assert "Successfully Submitted" in driver.page_source or "Leave" in driver.title

    # Step 4: Logout
    driver.find_element(By.CLASS_NAME, "oxd-userdropdown-name").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Logout").click()
    time.sleep(2)
    assert "login" in driver.current_url.lower()
