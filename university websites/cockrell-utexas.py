from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re

domain_url = "cockrell.utexas.edu/faculty-directory/search"
full_url = "https://cockrell.utexas.edu/faculty-directory/search"

def get_profiles():
    
    profile_urls = set()

    for last_name in last_names:
        search_box = driver.find_element(By.CLASS_NAME, 'inputbox')
        search_box.clear()
        search_box.send_keys(last_name)
        search_box.submit()
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        profiles = soup.find_all('div', class_='facinfo')

        for profile in profiles:
            profile = BeautifulSoup(str(profile), 'html.parser')
            profile_tag = profile.find('p', class_='contact').find_next_sibling()
            profile_url = profile_tag.find('a', href=True)['href']
            profile_urls.add(profile_url)
    
    return profile_urls

def get_profile_urls():
    # Re-use scraped profile URLs
    # Should update periodically
    return {'http://www.ae.utexas.edu/people/faculty/faculty-directory/doan', 'http://www.ae.utexas.edu/people/faculty/faculty-directory/bui-thanh', 'http://www.pge.utexas.edu/facultystaff/faculty-directory/nguyen'}

last_names = ['Bui', 'Dang', 'Doan', 'Duong', 'Hoang', 'Huynh', 'Nguyen', 'Pham']

mode = input("Do you want to use previously scraped profiles? (y/n): ")
while mode != 'n' and mode != 'y':
    mode = input("Invalid input. Please enter 'y' or 'n': ")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.page_load_strategy = 'none'

driver = webdriver.Chrome(options=chrome_options)

wait = WebDriverWait(driver, 20)

if mode == 'n':
    driver.get(full_url)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'inputbox')))
    driver.execute_script("window.stop();")
    profile_urls = get_profiles()
elif mode == 'y':
    profile_urls = get_profile_urls()

print("Profiles URLs:", profile_urls)

with open('university websites/profiles/cockrell-utexas.csv', 'w', newline='') as file_output:
    headers = ['Name', 'Title', 'Email', 'Education', 'Research Interests', 'Profile URL']
    writer = csv.DictWriter(file_output, fieldnames=headers)
    writer.writeheader()

    for profile_url in profile_urls:
        print(f"Accessing: {profile_url}")
        driver.get(profile_url)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'facdata')))
        
        profile = BeautifulSoup(driver.page_source, 'html.parser')

        info_tag = profile.find('div', class_='facdata')
        photo_tag = profile.find('div', class_='facphoto')    
        fact_tag = profile.find('div', class_='facarticle')
        edu_tags = fact_tag.find_all('p')
        edu_tag = next((tag for tag in edu_tags if "PhD" in tag.get_text() or "Ph.D." in tag.get_text()), None)
        research_tag = fact_tag.find('strong', string=re.compile(r"Research", re.IGNORECASE)).find_next() if fact_tag.find('strong', string=re.compile(r"Research", re.IGNORECASE)) else None
        research_li_tag = research_tag.find_all('li') if research_tag else None        

        # syntax: re.sub(pattern, repl, string), pattern \s+ being one or more whitespace characters
        name_cleaned = re.sub(r'\s+', ' ', info_tag.find('h3').get_text()).replace('"', '').strip() if info_tag else ''
        title_cleaned = re.sub(r'\s+', ' ', info_tag.find('h5').get_text()).replace('"', '').strip() if info_tag else ''
        email_cleaned = re.sub(r'\s+', ' ', photo_tag.find('a', href=True)['href']).replace('mailto:', '').strip() if photo_tag else ''
        edu_cleaned = re.sub(r'\s+', ' ', edu_tag.get_text()).replace('"', '').strip() if edu_tag else ''
        research = '\n'.join([li.get_text() for li in research_li_tag]) if research_li_tag else ''
        research_cleaned = re.sub(r'\s+', ' ', research) if research_tag else ''

        writer.writerow({
            'Name': name_cleaned,
            'Title': title_cleaned,
            'Email': email_cleaned,
            'Education': edu_cleaned,
            'Research Interests': research_cleaned,
            'Profile URL': profile_url
        })

driver.quit()
print("Done and dusted!")