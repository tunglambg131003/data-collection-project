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

domain_url = "superurop.mit.edu/scholars/"
full_url = "https://superurop.mit.edu/scholars/"

def get_profiles():
    # Remove the default cohort filter to also search for all previous cohorts
    clean_filter_button = driver.find_element(By.CLASS_NAME, 'clean_filters')
    print(clean_filter_button)
    clean_filter_button.click()
    time.sleep(3)

    profile_urls = set()

    for last_name in last_names:
        search_box = driver.find_element(By.XPATH, "/html/body/main/div/div[2]/div[1]/div[1]/div[4]/input")
        search_box.clear()
        search_box.send_keys(last_name)
        submit_button = driver.find_element(By.CSS_SELECTOR, '.mit-icon.icon-search')
        submit_button.click()
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        profiles = soup.find_all('div', class_='m_scholar-card')

        for profile in profiles:
            profile = BeautifulSoup(str(profile), 'html.parser')
            profile_url = profile.find('a', href=True)['href']
            profile_urls.add(profile_url)
    
    return profile_urls

def get_profile_urls():
    # Re-use scraped profile URLs
    # Should update periodically
    return {'https://superurop.mit.edu/scholars/timothy-nguyen/', 'https://superurop.mit.edu/scholars/linh-nguyen/', 'https://superurop.mit.edu/scholars/hoang-nguyen/', 'https://superurop.mit.edu/scholars/huy-dang-pham/', 'https://superurop.mit.edu/scholars/alex-dang/', 'https://superurop.mit.edu/scholars/phu-nguyen/', 'https://superurop.mit.edu/scholars/phuong-mai-pham/', 'https://superurop.mit.edu/scholars/vivian-tran/', 'https://superurop.mit.edu/scholars/qui-nguyen/', 'https://superurop.mit.edu/scholars/erik-nguyen/', 'https://superurop.mit.edu/scholars/viet-tran-nguyen/'}

last_names = ['Bui', 'Dang', 'Hoang', 'Huynh', 'Nguyen', 'Pham', 'Tran', 'Vu']

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

print("hello")
# Step 5: Perform actions on the page
wait = WebDriverWait(driver, 20)
element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div/div[2]/div[1]/div[1]/div[4]/input")))
driver.execute_script("window.stop();")
print("hello")

# profile_urls = get_profiles() # Enable if need re-scraping
profile_urls = get_profile_urls() # Enable if reusing scraped profile URLs
print("Profiles URLs:", profile_urls)

with open('university websites/profiles/superurop-mit.csv', 'w', newline='') as file_output:
    headers = ['Name', 'Email', 'Scholar Title', 'Research Title', 'Research Areas', 'Research Abstract', 'Supervisor', 'Cohort', 'Quote', 'Profile URL']
    writer = csv.DictWriter(file_output, fieldnames=headers)
    writer.writeheader()

    for profile_url in profile_urls:
        print(f"Accessing: {profile_url}")
        driver.get(profile_url)
        time.sleep(3)
        profile = BeautifulSoup(driver.page_source, 'html.parser')

        name_tag = profile.find('h2', class_='name')
        email_tag = profile.find('a', href=re.compile(r'^mailto:')) if profile.find('a', href=re.compile(r'^mailto:')) else None
        scholar_title_tag = profile.find('div', string="Scholar Title").find_next_sibling() if profile.find('div', string="Scholar Title") else None
        research_title_tag = profile.find('div', string="Research Title").find_next_sibling() if profile.find('div', string="Research Title") else None
        research_areas_tag = profile.find('ul', class_='research-areas') if profile.find('div', string="Research Areas") else None
        research_abstract_tag = profile.find('div', string="Abstract").find_next_sibling() if profile.find('div', string="Abstract") else None
        supervisor_tag = profile.find('div', class_='supervisor').find_next_sibling() if profile.find('div', class_='supervisor') else None
        cohort_tag = profile.find('div', string="Cohort").find_next_sibling() if profile.find('div', string="Cohort") else None
        quote_tag = profile.find('div', string="Quote") if profile.find('div', string="Quote") else None

        # syntax: re.sub(pattern, repl, string), pattern \s+ being one or more whitespace characters
        name_cleaned = re.sub(r'\s+', ' ', name_tag.get_text().replace('"', '')).strip() if name_tag else ''
        email_cleaned = re.sub(r'\s+', ' ', email_tag.get_text().replace('"', '')).strip() if email_tag else ''
        scholar_title_cleaned = re.sub(r'\s+', ' ', scholar_title_tag.get_text().replace('"', '')).strip() if scholar_title_tag else ''
        research_title_cleaned = re.sub(r'\s+', ' ', research_title_tag.get_text().replace('"', '')).strip() if research_title_tag else ''
        research_areas_cleaned = re.sub(r'\s+', ' ', research_areas_tag.get_text().replace('"', '')).strip() if research_areas_tag else ''
        research_abstract_cleaned = re.sub(r'\s+', ' ', research_abstract_tag.get_text().replace('"', '')).strip() if research_abstract_tag else ''
        supervisor_cleaned = re.sub(r'\s+', ' ', supervisor_tag.get_text().replace('"', '')).strip() if supervisor_tag else ''
        cohort_cleaned = re.sub(r'\s+', ' ', cohort_tag.get_text().replace('"', '')).strip() if cohort_tag else ''
        quote_cleaned = re.sub(r'\s+', ' ', quote_tag.get_text().replace('"', '')).strip() if quote_tag else ''

        # title_dept_cleaned = re.sub(r'\s+', ' ', title_dept_tag.get_text().replace('"', '')).strip()
        # research_summary_cleaned = re.sub(r'\s+', ' ', research_summary_tag.get_text().replace('"', '')).strip()
        # email_cleaned = re.sub(r'\s+', ' ', email_tag.get_text().replace('Email:', '').replace('"', '')).strip()
        # phone_number_cleaned = re.sub(r'\s+', ' ', phone_number_tag.get_text().replace('Phone:', '').replace('"', '')).strip()
        # bio_summary = summarize.summarize_text(bio_tag.get_text(), 50, 25) if bio_tag else ''
        # bio_summary_cleaned = re.sub(r'\s+', ' ', bio_summary.replace('"', '')).strip()

        writer.writerow({
            'Name': name_cleaned,
            'Email': email_cleaned,
            'Scholar Title': scholar_title_cleaned,
            'Research Title': research_title_cleaned,
            'Research Areas': research_areas_cleaned,
            'Research Abstract': research_abstract_cleaned,
            'Supervisor': supervisor_cleaned,
            'Cohort': cohort_cleaned,
            'Quote': quote_cleaned,
            'Profile URL': profile_url
        })

driver.quit()
print("Done and dusted!")