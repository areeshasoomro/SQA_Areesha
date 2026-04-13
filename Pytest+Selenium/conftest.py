#used this file to put a structure resuable once so all test can used thta '
import pytest
from selenium import webdriver

@pytest.fixture
def driver():
    # 1. OPEN browser
    driver = webdriver.Chrome()
    driver.maximize_window()

    # 2. GIVE driver to test
    yield driver

    # 3. CLOSE browser after test   works after alll test finishes 
    
    driver.quit()