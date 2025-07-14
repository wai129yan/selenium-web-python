from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from datetime import datetime

def open_website_and_keep_open():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Maximize window
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Hide automation
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Initialize driver
    driver = webdriver.Chrome(options=chrome_options)
    
    # Hide automation notification
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        # Open website with basic auth
        print("Opening website with basic authentication...")
        username = "tokyo"
        password = "tokyo2024"
        
        # Create URL with basic auth
        auth_url = f"https://{username}:{password}@dev-saas-cms2.webow.jp/admin"
        driver.get(auth_url)
        
        # Wait for page to load
        time.sleep(3)
        
        # Find and fill login form
        print("Logging in...")
        try:
            # Find login_id field and fill
            login_id_field = driver.find_element(By.NAME, "login_id")
            login_id_field.clear()
            login_id_field.send_keys("outward")
            
            # Find login_password field and fill
            password_field = driver.find_element(By.NAME, "login_password")
            password_field.clear()
            password_field.send_keys("ow_outward")
            
            # Find and click login button
            login_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(@class, 'button')]")
            login_button.click()
            
            # Wait for page to load after login
            time.sleep(3)
            print("Login successful!")
            
            # First go to tokyo-static01.webow.jp to authenticate basic auth
            print("Going to tokyo-static01.webow.jp to authenticate basic auth...")
            static_url = "https://tokyo:tokyo2024@tokyo-static01.webow.jp/"
            driver.get(static_url)
            
            # Wait for page to load
            time.sleep(3)
            print("Basic auth authentication successful!")
            
            # Then go to article page
            print("Navigating to article page...")
            article_url = "https://dev-saas-cms2.webow.jp/admin/?controller=article"
            driver.get(article_url)
            
            # Wait for page to load
            time.sleep(3)
            print("Successfully navigated to article page!")
            
            # Perform click operations
            print("Performing click operations...")
            try:
                # Click first link
                print("Clicking first link...")
                first_link = driver.find_element(By.XPATH, '//*[@id="contents_main"]/div[2]/div/ul/li[1]/a[1]')
                first_link.click()
                time.sleep(2)
                
                # Click second link
                print("Clicking second link...")
                second_link = driver.find_element(By.XPATH, '//*[@id="contents_main"]/div[2]/div/ul/li[2]/ul/li/a')
                second_link.click()
                time.sleep(2)
                
                # Click third link
                print("Clicking third link...")
                third_link = driver.find_element(By.XPATH, '//*[@id="link_bar"]/div/ul/li[1]/a')
                third_link.click()
                time.sleep(2)
                
                print("Completed all click operations!")
                
                # Read data from data.json and create articles
                print("Reading data from data.json...")
                with open('data.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Iterate through each element to create articles
                for i, article_data in enumerate(data['rows']):
                    print(f"Creating article {i+1}/{len(data['rows'])}: {article_data['title']}")
                    
                    try:
                        # Fill title
                        title_field = driver.find_element(By.NAME, "title")
                        title_field.clear()
                        title_field.send_keys(article_data['title'])
                        
                        # Fill body
                        body_field = driver.find_element(By.NAME, "body")
                        body_field.clear()
                        body_field.send_keys(article_data['text'])
                        
                        # Fill open_start_date
                        start_date_field = driver.find_element(By.NAME, "open_start_date")
                        driver.execute_script("arguments[0].value = arguments[1];", start_date_field,article_data['open_start_date'])
                        
                        # Fill open_end_date
                        end_date_field = driver.find_element(By.NAME, "open_end_date")
                        driver.execute_script("arguments[0].value = arguments[1];", end_date_field,article_data['open_end_date'])
                        
                        # Click save button
                        save_button = driver.find_element(By.XPATH, "//button[@type='button' and contains(@class, 'modalInput') and contains(@onclick, 'article_add')]")
                        save_button.click()
                        
                        # Wait for save to complete and switch to edit screen
                        time.sleep(3)
                        print(f"Successfully created article: {article_data['title']}")
                        
                        # Press back button to continue creating next article
                        if i < len(data['rows']) - 1:  # If not the last article
                            try:
                                back_button = driver.find_element(By.XPATH, '//*[@id="link_bar"]/div/ul/li[1]/a')
                                back_button.click()
                                time.sleep(2)
                                print("Returned to article creation page")
                            except Exception as e:
                                print(f"Error when going back: {e}")
                        
                        # Wait a bit before creating next article
                        time.sleep(2)
                        
                    except Exception as e:
                        print(f"Error creating article {i+1}: {e}")
                        continue
                
                print(f"Completed creating {len(data['rows'])} articles!")
                
            except Exception as e:
                print(f"Error performing clicks: {e}")
            
            # Switch back to first tab (article page)
            driver.switch_to.window(driver.window_handles[0])
            print("Successfully opened image!")
            
        except Exception as e:
            print(f"Login error: {e}")
        
        print("Website opened successfully!")
        print("Press Enter to close browser...")
        
        
        # Keep browser open until user presses Enter
        input()
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close browser when user presses Enter
        driver.quit()
        print("Browser has been closed.")

if __name__ == "__main__":
    open_website_and_keep_open()

