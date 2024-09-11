from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from time import sleep
import os
import csv

# Initialize the driver
driver = webdriver.Chrome()
url = "https://www.linkedin.com/login"
driver.get(url)
print("- Finish initializing a driver")

# Load environment variables
load_dotenv()
username = os.getenv('LINKEDIN_LOGIN_USERNAME')
password = os.getenv('LINKEDIN_LOGIN_PASSWORD')

# Login to LinkedIn
try:
    signin_field = driver.find_element(By.ID, 'username')
    signin_field.send_keys(username)
    print('- Finish keying in email')
    sleep(3)

    signin_field = driver.find_element(By.ID, 'password')
    signin_field.send_keys(password)
    print('- Finish keying in password')
    sleep(2)

    signin_field.submit()
    print('- Finish Task 1: Login to LinkedIn')
except Exception as e:
    print(f"Error during login: {e}")

# Search for profiles
try:
    search_field = driver.find_element(By.XPATH, '//input[contains(@class, "search-global-typeahead__input")]')
    search_query = input('What profile do you want to scrape? ')
    search_field.send_keys(search_query)
    search_field.send_keys(Keys.RETURN)
    print('- Finish Task 2: Search for profiles')
except Exception as e:
    print(f"Error during search: {e}")

def get_urls():
    page_source = BeautifulSoup(driver.page_source, 'html.parser')
    profiles = page_source.find_all('a', class_='app-aware-link')
    all_profile_urls = []
    for profile in profiles:
        profile_url = profile.get('href')
        if profile_url and 'linkedin.com/in/' in profile_url and profile_url not in all_profile_urls:
            all_profile_urls.append(profile_url)
    return all_profile_urls

input_page = int(input('How many pages you want to scrape: '))
urls_all_pages = []

for page in range(input_page):
    urls_one_page = get_urls()
    sleep(2)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')  # Scroll to the end of the page
    sleep(3)
    try:
        next_button = driver.find_element(By.CLASS_NAME, "artdeco-pagination__button--next")
        driver.execute_script("arguments[0].click();", next_button)
        urls_all_pages.extend(urls_one_page)
        sleep(2)
    except Exception as e:
        print(f"Error navigating to next page: {e}")
        break

print('- Finish Task 3: Scrape the URLs')

with open('linkedin_profiles.csv', 'w', newline='') as file_output:
    headers = ['Name', 'Job Title', 'Location', 'URL']
    writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n', fieldnames=headers)
    writer.writeheader()
    for linkedin_url in urls_all_pages:
        try:
            driver.get(linkedin_url)
            print('- Accessing profile: ', linkedin_url)
            sleep(3)
            page_source = BeautifulSoup(driver.page_source, "html.parser")
            info_div = page_source.find('div', {'class': 'ph5 pb5'})
            if info_div:
                name = info_div.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words')
                location = info_div.find('span', class_='text-body-small inline t-black--light break-words')
                title = info_div.find('div', class_='text-body-medium break-words')
                if name :
                    writer.writerow({
                        headers[0]: name.get_text().strip(),
                        headers[1]: title.get_text().strip(),
                        headers[2]: location.get_text().strip(),
                        headers[3]: linkedin_url
                    })
                    print('--- Profile name is: ', name.get_text().strip())
                    print('--- Profile location is: ', location.get_text().strip())
                    print('--- Profile title is: ', title.get_text().strip())
                else:
                    print('--- Incomplete profile information')
            else:
                print('--- No profile information found')
        except Exception as e:
            print(f"Error extracting profile information: {e}")
            continue

print('Mission Completed!')
driver.quit()
