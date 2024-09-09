from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re

domain_url = "engineering.berkeley.edu/directory"
full_url = "https://engineering.berkeley.edu/directory"

def get_profile_urls():
    # Re-use scraped profile URLs
    # Should update periodically
    return {'https://viterbi.usc.edu/directory/faculty/Nguyen/Hannah', 'https://viterbi.usc.edu/directory/faculty/Nguyen/Zune', 'https://viterbi.usc.edu/directory/faculty/Tu/Stephen', 'https://viterbi.usc.edu/directory/faculty/Mai/John', 'https://viterbi.usc.edu/directory/faculty/Nguyen/Calvin', 'https://viterbi.usc.edu/directory/faculty/Gencturk/Bora', 'https://viterbi.usc.edu/directory/faculty/Phan/Phan', 'https://viterbi.usc.edu/directory/faculty/Luhar/Mitul', 'https://viterbi.usc.edu/directory/faculty/Nguyen/Quan'}

last_names = ['Bui', 'Dang', 'Dat Le', 'Hoang', 'Huynh', 'Ngo', 'Nguyen', 'Pham', 'Phan', 'Tran', 'Tu', 'Vu']

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
element = wait.until(EC.presence_of_element_located((By.ID, 'txtFacultySearch')))

profile_urls = set()

with open('university websites/profiles/eng-ucb.csv', 'w', newline='') as file_output:
    headers = ['Name', 'Title', 'Email', 'Phone Number', 'Address']
    writer = csv.DictWriter(file_output, fieldnames=headers)
    writer.writeheader()

    for last_name in last_names:
        search_box = driver.find_element(By.ID, 'txtFacultySearch')
        search_box.clear()
        search_box.send_keys(last_name)
        search_box.submit()
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        profiles = soup.find_all('div', class_='vcard')

        for profile in profiles:
            profile = BeautifulSoup(str(profile), 'html.parser')
            name = profile.find('h2', class_='fn').text
            title = profile.find('h3', class_= 'category').text
            email = profile.find('a', href=lambda href: href and href[:7]=='mailto:').text if profile.find('a', href=lambda href: href and href[:7]=='mailto:') else ''
            phone_number = profile.find('a', href=lambda href: href and href[:4]=='tel:').text if profile.find('a', href=lambda href: href and href[:4]=='tel:') else ''
            address = profile.find('div', class_='adr').text if profile.find('div', class_='adr') else ''
            address_cleaned = re.sub(r'\s+', ' ', address.replace('"', '')).strip()

            print(f"Adding profile: {name}, {title}, {email}, {phone_number}, {address_cleaned}")
            
            writer.writerow({
                'Name': name,
                'Title': title,
                'Email': email,
                'Phone Number': phone_number,
                'Address': address_cleaned
            })

driver.quit()
print("Done and dusted!")