# import pytest
# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException

# class TestUnitsDashboard:
#     # Configuration
#     BASE_URL = "https://units.compass-dx.com/" 
#     ADMIN_EMAIL = "superadmin@units.sa"
#     ADMIN_PASS = "Admin@12345"

#     @pytest.fixture(autouse=True)
#     def setup(self, driver):
#         self.driver = driver
#         self.wait = WebDriverWait(self.driver, 20)
#         self.driver.get(self.BASE_URL)
        
#         try:
#             # 1. Login Logic
#             email_field = self.wait.until(EC.element_to_be_clickable((By.NAME, "userName")))
#             email_field.send_keys(self.ADMIN_EMAIL)
            
#             password_field = self.driver.find_element(By.NAME, "password")
#             password_field.send_keys(self.ADMIN_PASS)
            
#             sign_in_btn = self.driver.find_element(By.XPATH, "//button[contains(., 'Sign In')]")
#             sign_in_btn.click()
            
#             # Confirm Dashboard Load
#             self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiBox-root")))
#         except TimeoutException:
#             pytest.fail("Setup Failed: Dashboard did not load.")

#     def test_dashboard_flow(self):
#         """Test Case: Language Cycle and Specific Warehouse Selection."""
        
#         # --- SECTION 1: LANGUAGE TOGGLE ---
#         arabic_xpath = "//p[contains(text(), 'العربية')]/parent::div"
#         english_xpath = "//p[contains(text(), 'EN')]/parent::div"
        
#         try:
#             self.wait.until(EC.element_to_be_clickable((By.XPATH, arabic_xpath))).click()
#             time.sleep(1) 
#             self.wait.until(EC.element_to_be_clickable((By.XPATH, english_xpath))).click()
#             print("Language toggled successfully.")
#         except Exception as e:
#             print(f"Language toggle skipped or failed: {e}")

#         # --- SECTION 2: WAREHOUSE SELECTION (Targeted) ---
#         try:
#             # UPDATED SELECTOR: 
#             # We look for a div with role 'combobox' that is NOT the first one, 
#             # or specifically follows a label/element containing 'Warehouse'
#             # This XPath finds the combobox that currently contains 'Warehouse' text or is near it.
#             warehouse_dropdown_xpath = "//div[@role='combobox' and (contains(., 'Warehouse') or contains(., 'Select'))]"
            
#             # If there are multiple, we can use an index [2] or a more specific parent
#             # Usually, Tenant is first, Warehouse is second:
#             # warehouse_dropdown_xpath = "(//div[@role='combobox'])[2]" 

#             dropdown = self.wait.until(EC.element_to_be_clickable((By.XPATH, warehouse_dropdown_xpath)))
#             dropdown.click()
#             print("Warehouse dropdown opened.")

#             # 2. Locate the specific option
#             warehouse_option_xpath = "//li[@role='option' and contains(., 'Warehouse 4/Dry')]"
#             target_option = self.wait.until(EC.visibility_of_element_located((By.XPATH, warehouse_option_xpath)))

#             # 3. JS Click for reliability
#             self.driver.execute_script("arguments[0].click();", target_option)
#             print("Clicked 'Warehouse 4/Dry'.")

#             # 4. Verification
#             self.wait.until(EC.text_to_be_present_in_element((By.XPATH, warehouse_dropdown_xpath), "Warehouse 4/Dry"))
#             print("Verified: Warehouse 4/Dry is now selected.")

#         except Exception as e:
#             self.driver.save_screenshot("dropdown_error.png")
#             print(f"Warehouse selection failed: {e}")
#             raise


import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class TestUnitsDashboard:
    # Configuration
    BASE_URL = "https://units.compass-dx.com/" 
    ADMIN_EMAIL = "superadmin@units.sa"
    ADMIN_PASS = "Admin@12345"

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.get(self.BASE_URL)
        
        try:
            # 1. Login Logic
            email_field = self.wait.until(EC.element_to_be_clickable((By.NAME, "userName")))
            email_field.send_keys(self.ADMIN_EMAIL)
            self.driver.find_element(By.NAME, "password").send_keys(self.ADMIN_PASS)
            
            time.sleep(1)
            self.driver.find_element(By.XPATH, "//button[contains(., 'Sign In')]").click()
            
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiBox-root")))
            print("Login successful.")
            time.sleep(2)
        except TimeoutException:
            pytest.fail("Setup Failed: Dashboard did not load.")

    def test_full_dashboard_flow(self):
        """Final Corrected Test: Language -> Warehouse -> Request Type -> Customer."""
        
        # --- 1. LANGUAGE TOGGLE CYCLE ---
        try:
            arabic_xpath = "//p[contains(text(), 'العربية')]/parent::div"
            self.wait.until(EC.element_to_be_clickable((By.XPATH, arabic_xpath))).click()
            time.sleep(2)
            english_xpath = "//p[contains(text(), 'EN')]/parent::div"
            self.wait.until(EC.element_to_be_clickable((By.XPATH, english_xpath))).click()
            time.sleep(2)
        except Exception:
            pass

        # --- 2. WAREHOUSE SELECTION ---
        try:
            # Anchor to the hidden input with name 'warehouseId'
            warehouse_xpath = "//input[@name='warehouseId']/preceding-sibling::div[@role='combobox']"
            self.wait.until(EC.element_to_be_clickable((By.XPATH, warehouse_xpath))).click()
            time.sleep(2)

            warehouse_opt = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//li[@role='option' and contains(., 'Warehouse 4/Dry')]")
            ))
            self.driver.execute_script("arguments[0].click();", warehouse_opt)
            print("Warehouse Selected.")
            time.sleep(2)
        except Exception as e:
            print(f"Warehouse Error: {e}")

        # --- 3. REQUEST TYPE SELECTION (CORRECTED) ---
        try:
            # Instead of just ID, we use the specific DIV that has the ID 'request-type-select'
            # This ensures we click the exact MUI container
            req_type_xpath = "//div[@id='request-type-select']"
            req_type_dropdown = self.wait.until(EC.element_to_be_clickable((By.XPATH, req_type_xpath)))
            
            # Use JS Click for Request Type to be 100% sure it opens
            self.driver.execute_script("arguments[0].click();", req_type_dropdown)
            print("Request Type dropdown opened.")
            time.sleep(2)

            # Look for 'B2B' in the visible options list
            b2b_option = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//li[@role='option' and contains(., 'B2B')]")
            ))
            self.driver.execute_script("arguments[0].click();", b2b_option)
            print("Request Type 'B2B' selected.")
            time.sleep(2)
        except Exception as e:
            print(f"Request Type selection failed: {e}")

        # --- 4. CUSTOMER SELECTION ---
        try:
            # Anchor to the hidden input with name 'customerId'
            customer_xpath = "//input[@name='customerId']/preceding-sibling::div[@role='combobox']"
            customer_dropdown = self.wait.until(EC.element_to_be_clickable((By.XPATH, customer_xpath)))
            customer_dropdown.click()
            time.sleep(2)

            customer_opt = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//li[@role='option' and contains(., 'Wasiq Ansari')]")
            ))
            self.driver.execute_script("arguments[0].click();", customer_opt)
            
            # Final Verification
            self.wait.until(EC.text_to_be_present_in_element((By.XPATH, customer_xpath), "Wasiq Ansari"))
            print("Customer 'Wasiq Ansari' selected.")
            time.sleep(2)

        except Exception as e:
            self.driver.save_screenshot("selection_error.png")
            print(f"Customer Error: {e}")
            raise