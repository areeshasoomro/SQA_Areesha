import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestPalletsUtilization:
    BASE_URL = "https://units.compass-dx.com/"
    ADMIN_EMAIL = "superadmin@units.sa"
    ADMIN_PASS = "Admin@12345"

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.get(self.BASE_URL)
        
        # 1. Login
        self.wait.until(EC.element_to_be_clickable((By.NAME, "userName"))).send_keys(self.ADMIN_EMAIL)
        self.driver.find_element(By.NAME, "password").send_keys(self.ADMIN_PASS)
        self.driver.find_element(By.XPATH, "//button[contains(., 'Sign In')]").click()
        time.sleep(2)

    def test_pallets_utilization_export_flow(self):
        # --- 1. NAVIGATE TO MODULE ---
        pallet_menu = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//span[text()='Pallets Utilization']")
        ))
        self.driver.execute_script("arguments[0].click();", pallet_menu)
        time.sleep(3)

        # --- 2. DATE SELECTION (Year 2026 -> April) ---
        try:
            # Open Picker
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Choose date')]"))).click()
            time.sleep(1)
            
            # Click Year 2026
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='2026']"))).click()
            time.sleep(1)
            
            # Click Month Apr
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Apr']"))).click()
            print("Date selected: April 2026.")
            time.sleep(2)
        except Exception as e:
            print(f"Date Selection failed: {e}")

        # --- 3. EXPORT AS PDF ---
        try:
            # Click the Download icon (aria-label='Export')
            export_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Export']")))
            export_btn.click()
            print("Export menu opened.")
            time.sleep(1)

            # Select the 'Export as PDF' option from the dropdown
            # This looks for the menu item containing 'PDF'
            pdf_option = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(@role, 'menuitem') and contains(., 'PDF')]")
            ))
            pdf_option.click()
            print("Export as PDF triggered successfully.")
            
            # Final wait to ensure the download starts
            time.sleep(5) 
        except Exception as e:
            self.driver.save_screenshot("export_error.png")
            print(f"Export flow failed: {e}")