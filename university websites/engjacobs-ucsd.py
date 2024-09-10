from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import csv
import re
import summarize

domain_url = "jacobsschool.ucsd.edu/faculty/profiles"
full_url = "https://jacobsschool.ucsd.edu/faculty/profiles"


def get_profiles():
    profile_urls = set()

    for last_name in last_names:
        # Locate the search box inside the loop to avoid stale reference
        search_box = driver.find_element(By.ID, 'edit-field-profile-last-name-value')
        search_box.clear()
        search_box.send_keys(last_name)
        search_box.submit()
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        profiles = soup.find_all('div', class_='row')

        for profile in profiles:
            profile = BeautifulSoup(str(profile), 'html.parser')
            profile_url = profile.find('a', href=True)['href']
            if profile_url != '/' and profile_url != '/faculty/profile/update':
                profile_urls.add(f"https://jacobsschool.ucsd.edu{profile_url}")
    
    return profile_urls

def get_profile_urls():
    # Re-use scraped profile URLs
    # Should update periodically
    return {'https://jacobsschool.ucsd.edu/people/profile/truong-q-nguyen'}

last_names = ['Bui', 'Dang', 'Hoang', 'Huynh', 'Ngo', 'Nguyen', 'Pham', 'Tran', 'Vu']

# Run Chrome in the background

# Step 1: Set up ChromeOptions and its arguments
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")  # Add this if running in Docker or Linux environments
chrome_options.add_argument("--disable-dev-shm-usage")  # Required for running in some systems
chrome_options.add_argument("--window-size=1920x1080")

# Step 2: Change the page load strategy to none
chrome_options.page_load_strategy = 'none'  # Avoid full page load

# Step 3: Initialize the WebDriver with merged options
driver = webdriver.Chrome(options=chrome_options)
# Step 4: Navigate to a URL
driver.get(full_url)

# Step 5: Perform actions on the page
wait = WebDriverWait(driver, 20)
element = wait.until(EC.presence_of_element_located((By.ID, 'edit-field-profile-last-name-value')))
driver.execute_script("window.stop();")

# profile_urls = get_profiles() # Enable if need re-scraping
profile_urls = get_profile_urls() # Enable if reusing scraped profile URLs
print("Profiles URLs:", profile_urls)

with open('university websites/profiles/engjacobs-ucsd.csv', 'w', newline='') as file_output:
    headers = ['Name', 'Title-Department', 'Email', 'Phone Number', 'Profile URL', 'Biography', 'Research Summary']
    writer = csv.DictWriter(file_output, fieldnames=headers)
    writer.writeheader()

    for profile_url in profile_urls:
        profile_content = requests.get(profile_url).content
        profile = BeautifulSoup(profile_content, 'html.parser')

        name_tag = profile.find('h3', class_='faculty_profile_name')
        title_dept_tag = name_tag.find_next_sibling()
        research_summary_tag = title_dept_tag.find_next_sibling().find_next_sibling()
        img_tag = profile.find('img', class_='mb-4')
        email_tag = img_tag.find_next_sibling()
        phone_number_tag = email_tag.find_next_sibling()
        bio_tag = profile.find('p', string="Capsule Bio:").find_next_sibling()

        name_cleaned = re.sub(r'\s+', ' ', name_tag.get_text().replace('"', '')).strip()
        title_dept_cleaned = re.sub(r'\s+', ' ', title_dept_tag.get_text().replace('"', '')).strip()
        research_summary_cleaned = re.sub(r'\s+', ' ', research_summary_tag.get_text().replace('"', '')).strip()
        email_cleaned = re.sub(r'\s+', ' ', email_tag.get_text().replace('Email:', '').replace('"', '')).strip()
        phone_number_cleaned = re.sub(r'\s+', ' ', phone_number_tag.get_text().replace('Phone:', '').replace('"', '')).strip()
        bio_summary = summarize.summarize_text(bio_tag.get_text(), 50, 25) if bio_tag else ''
        bio_summary_cleaned = re.sub(r'\s+', ' ', bio_summary.replace('"', '')).strip()

        writer.writerow({
            'Name': name_cleaned,
            'Title-Department': title_dept_cleaned,
            'Email': email_cleaned,
            'Phone Number': phone_number_cleaned,
            'Profile URL': profile_url,
            'Biography': bio_summary_cleaned,
            'Research Summary': research_summary_cleaned,
        })

driver.quit()
print("Done and dusted!")