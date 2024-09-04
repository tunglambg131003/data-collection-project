import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from time import sleep
import os
import csv

# Path to your cookie file
cookies_file = "cookies.pkl"

# Function to save cookies
def save_cookies(driver, path):
    with open(path, "wb") as file:
        pickle.dump(driver.get_cookies(), file)

# Function to load cookies
def load_cookies(driver, path):
    with open(path, "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

# Initialize the driver
driver = webdriver.Chrome()

# Load environment variables
# load_dotenv()
# username = os.getenv('LINKEDIN_LOGIN_USERNAME')
# password = os.getenv('LINKEDIN_LOGIN_PASSWORD')

# Load cookies in subsequent runs
driver.get("https://www.linkedin.com/login")
load_cookies(driver, cookies_file)
driver.refresh()  # Refresh to apply cookies

# Now you can navigate to other LinkedIn pages as a logged-in user
driver.get("https://www.linkedin.com/feed/")

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
    print(f'--- Page {page + 1} has {len(urls_one_page)} profiles')
    print(urls_one_page)
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

with open('output.csv', 'w', newline='') as file_output:
    headers = ['Name', 'Job Title', 'Location', 'URL']
    writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n', fieldnames=headers)
    writer.writeheader()
    for linkedin_url in urls_all_pages:
        try:
            driver.get(linkedin_url)
            print('- Accessing profile: ', linkedin_url)
            sleep(3)
            page_source = BeautifulSoup(driver.page_source, "html.parser")
            info_div = page_source.find('div', {'class': 'ph5 '})
            if info_div:
                name = info_div.find('li', class_='inline t-24 t-black t-normal break-words')
                location = info_div.find('li', class_='t-16 t-black t-normal inline-block')
                title = info_div.find('h2', class_='mt1 t-18 t-black t-normal break-words')
                if name and location and title:
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