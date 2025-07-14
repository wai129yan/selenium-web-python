from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import json

# 👉 Load multiple form entries from JSON
with open("form_data.json", "r") as f:
    all_data = json.load(f)

# 👉 Your local HTML file path
file_path = f"file:///{os.getcwd()}/form_demo.html"

# 1. Chrome Browser ဖွင့်ပါ
driver = webdriver.Chrome()

# 2. Loop through each entry and fill the form
for idx, data in enumerate(all_data, start=1):
    driver.get(file_path)

    driver.find_element(By.NAME, "title").clear()
    driver.find_element(By.NAME, "title").send_keys(data["title"])

    driver.find_element(By.NAME, "body").clear()
    driver.find_element(By.NAME, "body").send_keys(data["body"])

    driver.find_element(By.NAME, "release_date").clear()
    driver.find_element(By.NAME, "release_date").send_keys(data["release_date"])

    driver.find_element(By.NAME, "end_date").clear()
    driver.find_element(By.NAME, "end_date").send_keys(data["end_date"])

    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    print(f"Submitted entry {idx}: {data['title']}")
    time.sleep(1)  # Wait briefly between submissions

# 3. Close browser
driver.quit()
