from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re
# from us_schools_scraper import get_current_date


def get_current_date():
    return time.strftime("%Y-%m-%d", time.localtime())

def clean_info(*args):
    cleaned_infos = []
    for arg in args:
        cleaned_infos.append(re.sub(r"\s+", " ", arg).replace('"', "").strip())
    return cleaned_infos


def harvard_seas(driver, school_headers, school_url, school_csv, school_last_names):
    """
    Scrape Vietnamese profiles from Harvard University - John Alfred Paulson School of Engineering and Applied Sciences.
    """
    driver.get(school_url)
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.ID, "edit-search")))
    
    current_date = get_current_date()

    with open(f"US Engineering Schools/Profiles/{current_date}_{school_csv}.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=school_headers)
        writer.writeheader()

        for last_name in school_last_names:
            print("Finding profiles of people with last name of " + last_name)
            search_box = driver.find_element(By.ID, "edit-search") # Re-locate the search box inside the loop to avoid stale reference
            search_box.clear()
            search_box.send_keys(last_name)
            search_box.submit()
            time.sleep(3)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            profiles = soup.find_all("div", "views-row")

            for profile in profiles:
                print("Finding profiles of people with last name of " + last_name)
                name = profile.find("span", class_="person__name").text
                title = profile.find("div", class_= "person__primary-title").find("div", class_="field-item").text
                email = profile.find("a", href=lambda href: href and href[:7]=="mailto:").text if profile.find("a", href=lambda href: href and href[:7]=="mailto:") else ""
                address = profile.find("div", class_='person__office').find("div", class_="field-item").text if profile.find("div", class_="person__office") else ""
                phone_number = profile.find("div", class_="person__phone").find("div", class_="field-item").text if profile.find("div", class_="person__phone") else ""

                cleaned_infos = clean_info(name, title, email, phone_number, address)

                print(f"Adding profile: {cleaned_infos[0]}, {cleaned_infos[1]}, {cleaned_infos[2]}, {cleaned_infos[3]}, {cleaned_infos[4]}")
                
                writer.writerow({
                    'Name': cleaned_infos[0],
                    'Title': cleaned_infos[1],
                    'Email': cleaned_infos[2],
                    'Phone Number': cleaned_infos[3],
                    'Address': cleaned_infos[4]
                })


def ucb_eng(driver, school_headers, school_url, school_csv, school_last_names):
    """
    Scrape Vietnamese profiles from University of California, Berkeley - College of Engineering.
    """
    driver.get(school_url)
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.ID, "txtFacultySearch")))

    current_date = get_current_date()

    with open(f"US Engineering Schools/Profiles/{current_date}_{school_csv}.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=school_headers)
        writer.writeheader()

        for last_name in school_last_names:
            print("Finding profiles of people with last name of " + last_name)
            search_box = driver.find_element(By.ID, "txtFacultySearch")
            search_box.clear()
            search_box.send_keys(last_name)
            search_box.submit()
            time.sleep(3)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            profiles = soup.find_all("div", class_='vcard')

            for profile in profiles:
                name = profile.find("h2", class_="fn").text
                title = profile.find("h3", class_="category").text
                email = profile.find("a", href=lambda href: href and href[:7] == "mailto:").text if profile.find("a", href=lambda href: href and href[:7] == "mailto:") else ""
                phone_number = profile.find("a", href=lambda href: href and href[:4] == "tel:").text if profile.find("a", href=lambda href: href and href[:4] == "tel:") else ""
                address = profile.find("div", class_="adr").text if profile.find("div", class_="adr") else ""
                
                cleaned_infos = clean_info(name, title, email, phone_number, address)

                print(f"Adding profile: {cleaned_infos[0]}, {cleaned_infos[1]}, {cleaned_infos[2]}, {cleaned_infos[3]}, {cleaned_infos[4]}")
                
                writer.writerow({
                    'Name': cleaned_infos[0],
                    'Title': cleaned_infos[1],
                    'Email': cleaned_infos[2],
                    'Phone Number': cleaned_infos[3],
                    'Address': cleaned_infos[4]
                })