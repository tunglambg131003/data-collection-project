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

domain_url = "engineering.uci.edu/directory"
full_url = "https://engineering.uci.edu/directory"


def get_profiles():
    profile_urls = set()

    for last_name in last_names:
        # Locate the search box inside the loop to avoid stale reference
        search_box = driver.find_element(By.ID, 'edit-name')
        search_box.clear()
        search_box.send_keys(last_name)
        search_box.submit()
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        profiles = soup.find_all('tr', class_=re.compile(r'^(odd|even)'))

        for profile in profiles:
            profile = BeautifulSoup(str(profile), 'html.parser')
            profile_url = profile.find('a', href=True)['href']
            profile_urls.add(f"https://engineering.uci.edu{profile_url}")

    return profile_urls

def get_profile_urls():
    # Re-use scraped profile URLs
    # Should update periodically
    return {'https://engineering.uci.edu/users/phu-nguyen', 'https://engineering.uci.edu/users/vicky-tran', 'https://engineering.uci.edu/users/amy-pham', 'https://engineering.uci.edu/users/quoc-viet-dang'}

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
element = wait.until(EC.presence_of_element_located((By.ID, 'edit-name')))
driver.execute_script("window.stop();")

# profile_urls = get_profiles() # Enable if need re-scraping
profile_urls = get_profile_urls() # Enable if reusing scraped profile URLs
print("Profiles URLs:", profile_urls)

with open('university websites/profiles/engsamueli-uci.csv', 'w', newline='') as file_output:
    headers = ['Name', 'Title-Department', 'Email', 'Phone Number', 'Profile URL', 'Biography', 'Research Summary', 'Address']
    writer = csv.DictWriter(file_output, fieldnames=headers)
    writer.writeheader()

    for profile_url in profile_urls:
        profile_content = requests.get(profile_url).content
        profile = BeautifulSoup(profile_content, 'html.parser')

        name = profile.find('div', class_='pane-node-title').find('h1').text
        title_dept = profile.find('div', class_='field_pdept').get_text(separator=' - ', strip=True) if profile.find('div', class_='field_pdept') else ''
        email = profile.find('a', href=re.compile(r'^mailto:'))['href'].split(':')[1] if profile.find('a', href=re.compile(r'^mailto:')) else ''
        phone_number = profile.find('div', class_='field_phone').text if profile.find('div', class_='field_phone') else ''
        phone_number_cleaned = re.sub(r'\s+', ' ', phone_number.replace('Phone', '').replace('"', '')).strip()

        bio = profile.find('div', class_='field_bio').get_text(separator='\n') if profile.find('div', class_='field_bio') else ''
        bio_summary = summarize.summarize_text(bio, 50, 25) if bio != '' else ''
        
        research_summary = profile.find('div', class_='field_research').get_text(separator='\n') if profile.find('div', class_='field_research') else ''
        research_summary_cleaned = re.sub(r'\s+', ' ', research_summary.replace('"', '').replace('Research', '')).strip()
        
        address = profile.find('div', class_='field_room').text if profile.find('div', class_='field_room') else ''
        address_cleaned = re.sub(r'\s+', ' ', address.replace('"', '').replace('Location', '')).strip()

        writer.writerow({
            'Name': name,
            'Title-Department': title_dept.replace('"', ''),
            'Email': email,
            'Phone Number': phone_number_cleaned,
            'Profile URL': profile_url,
            'Biography': bio_summary,
            'Research Summary': research_summary_cleaned,
            'Address': address_cleaned,
        })

driver.quit()
print("Done and dusted!")