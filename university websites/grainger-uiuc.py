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

domain_url = "grainger.illinois.edu/about/directory/faculty"
full_url = "https://grainger.illinois.edu/about/directory/faculty"

def get_profiles():
    profiles = {}
    vietnamese_profiles = set()

    time.sleep(15)
    profile_tags_soup = BeautifulSoup(driver.page_source, 'html.parser')
    profile_tags = profile_tags_soup.select(".item.person")
    # or profile_tags = profile_tags_soup.find_all('div', class_=['item', 'person'])

    names_soup = BeautifulSoup(str(profile_tags), 'html.parser')
    name_tags = names_soup.find_all('a', href=lambda href: href and '/about/directory/faculty/' in href)
    # or name_tags = names_soup.find_all('a', href=re.compile(r'/about/directory/faculty/'))

    for name_tag in name_tags:
        names_soup = BeautifulSoup(str(name_tag), 'html.parser')
        name_tag = names_soup.find('a', href=True)
        profiles[name_tag.get_text()] = name_tag['href']

    for last_name in last_names:
        # if any key contains the last name
        for name in profiles.keys():
            if last_name in name:
                vietnamese_profiles.add(f"https://grainger.illinois.edu{profiles[name]}")
    
    return vietnamese_profiles

def get_profile_urls():
    # Re-use scraped profile URLs
    # Should update periodically
    return {'https://grainger.illinois.edu/about/directory/faculty/thn', 'https://grainger.illinois.edu/about/directory/faculty/huytran1'}

last_names = ['Bui', 'Dang', 'Hoang', 'Huynh', 'Nguyen', 'Pham', 'Tran', 'Vu']

mode = input("Do you want to use previously scraped profiles? (y/n): ")

while mode != 'n' and mode != 'y':
    mode = input("Invalid input. Please enter 'y' or 'n': ")

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

if mode == 'n':
    # Step 4: Navigate to a URL
    driver.get(full_url)

    # Step 5: Perform actions on the page
    profile_urls = get_profiles()
elif mode == 'y':
    profile_urls = get_profile_urls()

print("Profiles URLs:", profile_urls)

with open('university websites/profiles/grainger-uiuc.csv', 'w', newline='') as file_output:
    headers = ['Name', 'Title', 'Email', 'Education', 'Research Intererests', 'Research Areas', 'Academic Positions', 'Professional Highlights', 'Address', 'Phone Number', 'Profile URL']
    writer = csv.DictWriter(file_output, fieldnames=headers)
    writer.writeheader()

    for profile_url in profile_urls:
        print(f"Accessing: {profile_url}")
        driver.get(profile_url)
        time.sleep(5)
        profile = BeautifulSoup(driver.page_source, 'html.parser')

        name_tag = profile.find('div', id='hero')
        email_tag = profile.find('a', href=re.compile(r'^mailto:')) if profile.find('a', href=re.compile(r'^mailto:')) else None
        
        title_tag = profile.find('div', class_='title') if profile.find('div', class_='title') else None
        title_li_tags = title_tag.find_all('li')
        
        address_tag = profile.find('div', class_='office') if profile.find('div', class_='office') else None
        
        education_tag = profile.find('h2', string='Education').find_next_sibling()
        education_li_tags = education_tag.find_all('li')

        phone_no_tag = profile.find('div', class_='phone') if profile.find('div', class_='phone') else None
        
        research_int_tag = profile.find('h2', string="Research Interests").find_next_sibling() if profile.find('h2', string="Research Interests") else None
        research_int_li_tags = education_tag.find_all('li')

        research_areas_tag = profile.find('h2', string="Research Areas").find_next_sibling() if profile.find('h2', string="Research Areas") else None
        research_areas_li_tags = education_tag.find_all('li')

        academic_posts_tag = profile.find('h2', string="Academic Positions").find_next_sibling() if profile.find('h2', string="Academic Positions") else None
        academic_posts_li_tag = education_tag.find_all('li')

        pro_highs_tag = profile.find('h2', string="Professional Highlights").find_next_sibling() if profile.find('h2', string="Professional Highlights") else None
        pro_highs_li_tag = education_tag.find_all('li')
        
        # syntax: re.sub(pattern, repl, string), pattern \s+ being one or more whitespace characters
        name_cleaned = re.sub(r'\s+', ' ', name_tag.get_text()).replace('"', '').strip() if name_tag else ''
        email_cleaned = re.sub(r'\s+', ' ', email_tag.get_text()).replace('"', '').strip() if email_tag else ''

        title = '\n'.join([li.get_text() for li in title_li_tags]) if title_li_tags else ''
        title_cleaned = re.sub(r'\s+', ' ', title).replace('"', '').strip() if title else ''
        
        address_cleaned = re.sub(r'\s+', ' ', address_tag.get_text()).replace('"', '').strip() if address_tag else ''
        
        education = '\n'.join([li.get_text() for li in education_li_tags]) if education_li_tags else ''
        education_cleaned = re.sub(r'\s+', ' ', education).replace('"', '').strip() if education else ''
        
        phone_no_cleaned = re.sub(r'\s+', ' ', phone_no_tag.get_text()).replace('"', '').strip() if phone_no_tag else ''

        research_int = '\n'.join([li.get_text() for li in research_int_li_tags]) if research_int_li_tags else ''
        research_int_cleaned = re.sub(r'\s+', ' ', title).replace('"', '').strip() if title else ''

        research_areas = '\n'.join([li.get_text() for li in research_areas_li_tags]) if research_areas_li_tags else ''
        research_areas_cleaned = re.sub(r'\s+', ' ', title).replace('"', '').strip() if title else ''

        academic_posts_cleaned = '\n'.join([li.get_text() for li in academic_posts_li_tag]) if academic_posts_li_tag else ''
        academic_posts = re.sub(r'\s+', ' ', title).replace('"', '').strip() if title else ''

        pro_highs = '\n'.join([li.get_text() for li in pro_highs_li_tag]) if pro_highs_li_tag else ''
        pro_highs_cleaned = re.sub(r'\s+', ' ', title).replace('"', '').strip() if title else ''

        writer.writerow({
            'Name': name_cleaned,
            'Title': title_cleaned,
            'Email': email_cleaned,
            'Education': education_cleaned,
            'Research Intererests': research_int_cleaned,
            'Research Areas': research_areas_cleaned,
            'Academic Positions': academic_posts_cleaned,
            'Professional Highlights': pro_highs_cleaned,
            'Address': address_cleaned,
            'Phone Number': phone_no_cleaned,
            'Profile URL': profile_url
        })

driver.quit()
print("Done and dusted!")