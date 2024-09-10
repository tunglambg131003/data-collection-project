from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import requests
import summarize

domain_url = "viterbi.usc.edu/directory/faculty/"
full_url = "https://viterbi.usc.edu/directory/faculty/"


def get_profiles():
    profile_urls = set()

    for last_name in last_names:
        # Locate the search box inside the loop to avoid stale reference
        search_box = driver.find_element(By.NAME, 'namefaculty')
        search_box.clear()
        search_box.send_keys(last_name)
        search_box.submit()
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        profiles = soup.find_all('div', 'faculty-member')

        for profile in profiles:
            profile = BeautifulSoup(str(profile), 'html.parser')
            profile_url = profile.find('a', href=True)['href']
            profile_urls.add(f"https://viterbi.usc.edu{profile_url}")

    return profile_urls

def get_profile_urls():
    # Re-use scraped profile URLs
    # Should update periodically
    return {'https://viterbi.usc.edu/directory/faculty/Nguyen/Hannah', 'https://viterbi.usc.edu/directory/faculty/Nguyen/Zune', 'https://viterbi.usc.edu/directory/faculty/Tu/Stephen', 'https://viterbi.usc.edu/directory/faculty/Mai/John', 'https://viterbi.usc.edu/directory/faculty/Nguyen/Calvin', 'https://viterbi.usc.edu/directory/faculty/Gencturk/Bora', 'https://viterbi.usc.edu/directory/faculty/Phan/Phan', 'https://viterbi.usc.edu/directory/faculty/Luhar/Mitul', 'https://viterbi.usc.edu/directory/faculty/Nguyen/Quan'}

last_names = ['Bui', 'Dang', 'Hoang', 'Huynh', 'Ngo', 'Nguyen', 'Pham', 'Phan', 'Tran', 'Tu', 'Vu']

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
element = wait.until(EC.presence_of_element_located((By.NAME, 'namefaculty')))
driver.execute_script("window.stop();")


# profile_urls = get_profiles() # Enable if need re-scraping
profile_urls = get_profile_urls() # Enable if reusing scraped profile URLs

with open('university websites/profiles/viterbi-usc.csv', 'w', newline='') as file_output:
    headers = ['Name', 'Title-Department', 'Contact Information', 'Profile URL', 'Biography', 'Research Summary', 'Address']
    writer = csv.DictWriter(file_output, fieldnames=headers)
    writer.writeheader()

    for profile_url in profile_urls:
        profile_content = requests.get(profile_url).content
        profile = BeautifulSoup(profile_content, 'html.parser')
        
        name = profile.find('h4', class_='facultyname').text
        title = profile.find('div', class_='education-piece').find('p').text if profile.find('div', class_='education-piece').find('p') else ''
        dept = profile.find('h6', string='Appointments').find_next('li').text if profile.find('h6', string='Appointments').find_next('ul') else ''        
        contact_info_1 = profile.find('h6', string="Contact Information").find_next('li')
        contact_info = contact_info_1.text if contact_info_1 else ''
        contact_info_2 = contact_info_1.find_next('li').text if contact_info_1.find_next('li') else ''
        contact_info = contact_info + ', ' + contact_info_2 if contact_info_2[-1] != ':' else contact_info

        bio = profile.find('div', class_='biography-piece').get_text(separator='\n') if profile.find('div', class_='biography-piece') else ''
        bio_summary = summarize.summarize_text(bio, 50, 25) if bio != '' else ''
        
        research = profile.find('div', class_='research-piece').get_text(separator='\n') if profile.find('div', class_='research-piece') else ''
        research_summary = summarize.summarize_text(research, 50, 25) if research != '' else ''

        address = profile.find('h6', string='Office').find_next('ul').get_text(separator='\n') if profile.find('h6', string='Office').find_next('ul') else None

        writer.writerow({
            'Name': name,
            'Title-Department': title.replace('"', '') + '-' + dept.replace('"', ''),
            'Contact Information': contact_info.replace('"', ''),
            'Profile URL': profile_url,
            'Biography': bio_summary,
            'Research Summary': research_summary,
            'Address': address.replace('"', ''),
        })

driver.quit()
print("Done and dusted!")