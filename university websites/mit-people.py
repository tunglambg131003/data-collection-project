from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import csv

# Regex pattern to match a URL
HTTP_URL_PATTERN = r'^http[s]*://.+' # r = raw string, ^ = start of string, [s]* = 0 or more s, . = any character except newline, + = 1 or more of the preceding character

domain = "web.mit.edu/search/"
full_url = "https://web.mit.edu/search/"

params = {
    "q": "nguyen"  # The search query
}

def get_urls():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.search-result')))
    page_source = BeautifulSoup(driver.page_source, 'html.parser')
    profiles = page_source.find_all('li', class_='search-result')
    profile_urls = []
    for profile in profiles:
        profile_url = 
        if profile_url not in profile_urls:
            profile_urls.append(profile_url)
    return profile_urls

driver = webdriver.Chrome()
driver.get(full_url)
search_box = driver.find_element('name', 'q')
search_box.send_keys('nguyen')
search_box.submit()

people_button = driver.find_element(By.CSS_SELECTOR, 'a.search-tab__link[role="tab"][data-tab="directory"]')
driver.execute_script("arguments[0].click();", people_button)

profile_urls = get_urls()

print(profile_urls)

driver.quit()

# Common Vietnamese last names: Bui, Dang, Do, Duong, Ho, Hoang, Huynh, Le, Ly, Ngo, Nguyen, Pham, Phan, Tran, Van, Vo, Vu.

# Student (PG or Professor): name, department, school, student year, email
# Staff (STEM): name, department, email, phone, address, title

# with open('students.csv', 'w', newline='') as file_output:
#     headers = ['Name', 'Department', 'School', 'Student Year', 'Email', 'URL']
#     writer = csv.DictWriter(file_output, fieldnames=headers)
#     writer.writeheader()
#     for profile_url in profile_urls:
#         try:
#             driver.get(profile_url)
#             print('- Accessing profile: ', profile_url)
#             os.sleep(3)
#             page_source = BeautifulSoup(driver.page_source, "html.parser")
#             info_div = page_source.find('div', {'class': 'flex-1 mr5'})
#             if info_div:
#                 name = info_div.find('li', class_='inline t-24 t-black t-normal break-words')
#                 location = info_div.find('li', class_='t-16 t-black t-normal inline-block')
#                 title = info_div.find('h2', class_='mt1 t-18 t-black t-normal break-words')
#                 if name and location and title:
#                     writer.writerow({
#                         headers[0]: name.get_text().strip(),
#                         headers[1]: title.get_text().strip(),
#                         headers[2]: location.get_text().strip(),
#                         headers[3]: linkedin_url
#                     })
#                     print('--- Profile name is: ', name.get_text().strip())
#                     print('--- Profile location is: ', location.get_text().strip())
#                     print('--- Profile title is: ', title.get_text().strip())
#                 else:
#                     print('--- Incomplete profile information')
#             else:
#                 print('--- No profile information found')
#         except Exception as e:
#             print(f"Error extracting profile information: {e}")
#             continue

# with open('staff.csv', 'w', newline='') as file_output:
