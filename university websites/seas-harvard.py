from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

domain_url = "seas.harvard.edu/about-us/directory"
full_url = "https://seas.harvard.edu/about-us/directory"

def get_names():
    names = []
    with open('seas-harvard.csv', 'r') as file_input:
        reader = csv.DictReader(file_input)
        for row in reader:
            names.append(row['Name'])
    return names

last_names = ['Bui', 'Dang', 'Do', 'Duong', 'Ho', 'Hoang', 'Huynh', 'Le', 'Ly', 'Ngo', 'Nguyen', 'Pham', 'Phan', 'Tran', 'Van', 'Vo', 'Vu']

driver = webdriver.Chrome()
driver.get(full_url)

with open('seas-harvard.csv', 'w', newline='') as file_output: # syntax: with open('filename', 'mode', newline='') as file_object
    headers = ['Name', 'Title', 'Email', 'Address', 'Phone Number']
    writer = csv.DictWriter(file_output, fieldnames=headers)
    writer.writeheader()

    for last_name in last_names:
        # Locate the search box inside the loop to avoid stale reference
        search_box = driver.find_element(By.ID, 'edit-search')
        search_box.clear()
        search_box.send_keys(last_name)
        search_box.submit()
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        profiles = soup.find_all('div', 'views-row')

        for profile in profiles:
            profile = BeautifulSoup(str(profile), 'html.parser')
            name = profile.find('span', class_='person__name').text
            title = profile.find('div', class_= 'person__primary-title').find('div', class_='field-item').text
            email = profile.find('a', href=lambda href: href and href[:7]=='mailto:').text if profile.find('a', href=lambda href: href and href[:7]=='mailto:') else ''
            address = profile.find('div', class_='person__office').find('div', class_='field-item').text if profile.find('div', class_='person__office') else ''
            phone_number = profile.find('div', class_='person__phone').find('div', class_='field-item').text if profile.find('div', class_='person__phone') else ''

            if name not in get_names():
                print('Name:', name)
                print(get_names())
                writer.writerow({
                    'Name': name,
                    'Title': title,
                    'Email': email,
                    'Address': address,
                    'Phone Number': phone_number
                })

driver.quit()
print("Done and dusted!")