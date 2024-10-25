from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import json


def fetch_profile_urls(driver, code, school_url, school_last_names):
    """
    Fetch (Scrape) profile URLs given last names (for two-step school code).
    """
    profile_urls = set()
    driver.get(school_url)
    wait = WebDriverWait(driver, 20)

    if code == "mitsuperurop":
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div/div[2]/div[1]/div[1]/div[4]/input")))
        # Remove the default cohort filter to also search for all previous cohorts
        clean_filter_button = driver.find_element(By.CLASS_NAME, "clean_filters")
        clean_filter_button.click()
        
        for last_name in school_last_names:
            print("Fetching profile URLs of people with last name of " + last_name)
            # Locate the search box inside the loop to avoid stale reference
            search_box = driver.find_element(By.XPATH, "/html/body/main/div/div[2]/div[1]/div[1]/div[4]/input")
            search_box.clear()
            search_box.send_keys(last_name) # alternative: search_box.submit()
            
            submit_button = driver.find_element(By.CSS_SELECTOR, ".mit-icon.icon-search")
            submit_button.click()
            time.sleep(3)
            
            soup = BeautifulSoup(driver.page_source, "html.parser")
            profiles = soup.find_all("div", class_="m_scholar-card")

            for profile in profiles:
                profile_url = profile.find("a", href=True)["href"]
                profile_urls.add(profile_url)

    elif code == "mitpages":
        wait.until(EC.presence_of_element_located((By.NAME, "q")))     
        for last_name in school_last_names:
            num_of_pages = 10 if last_name == "Nguyen" else 3
            print(f"Fetching URLs in {num_of_pages} pages of people with last name of {last_name}")
            search_box = driver.find_element(By.NAME, "q")
            search_box.clear()
            search_box.send_keys(last_name)
            search_box.submit()
            time.sleep(3)
            
            for page in range(1, num_of_pages+1):
                soup = BeautifulSoup(driver.page_source, "html.parser")
                profiles = soup.find_all("div", class_="gs-webResult")

                for profile in profiles:
                    profile_url = profile.find("a", class_="gs-title", href=True)["href"] if profile.find("a", class_="gs-title", href=True) else None
                    print(profile_url)
                    if profile_url:
                        profile_urls.add(profile_url)
                
                # Load new page
                current_button = driver.find_element(By.XPATH, f"/html/body/main/div[2]/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div/div/div[5]/div[2]/div/div/div[2]/div/div[{page}]")
                next_button = driver.find_element(By.XPATH, f"/html/body/main/div[2]/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div/div/div[5]/div[2]/div/div/div[2]/div/div[{page+1}]")
                
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", next_button)

                # Wait for the new page to load
                time.sleep(3)
                print(f"Moved to page: {next_page}")

    elif code == "uci":
        wait.until(EC.presence_of_element_located((By.ID, "edit-name")))
        for last_name in school_last_names:
            print("Fetching profile URLs of people with last name of " + last_name)
            search_box = driver.find_element(By.ID, "edit-name")
            search_box.clear()
            search_box.send_keys(last_name)
            search_box.submit()

            soup = BeautifulSoup(driver.page_source, "html.parser")
            profiles = soup.find_all("tr", class_=re.compile(r"^(odd|even)"))

            for profile in profiles:
                profile_url = profile.find("a", href=True)["href"]
                profile_urls.add(f"https://engineering.uci.edu{profile_url}")
    
    elif code == "ucsd":
        wait.until(EC.presence_of_element_located((By.ID, "edit-field-profile-last-name-value")))
        for last_name in school_last_names:
            print("Fetching profile URLs of people with last name of " + last_name)
            search_box = driver.find_element(By.ID, "edit-field-profile-last-name-value")
            search_box.clear()
            search_box.send_keys(last_name)
            search_box.submit()

            soup = BeautifulSoup(driver.page_source, "html.parser")
            profiles = soup.find_all("div", class_="row")

            for profile in profiles:
                profile_url = profile.find("a", href=True)["href"]
                if profile_url != "/" and profile_url != "/faculty/profile/update":
                    profile_urls.add(f"https://jacobsschool.ucsd.edu{profile_url}")
        
    elif code == "uiuc":
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "campus-wordmark")))
        
        profiles = {} # No search box, so need to store all profile tags and filter by last name
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        profile_tags = soup.find_all("div", class_=["item", "person"])

        # Collect all <a> tags that match the pattern within the profile tags
        for tag in profile_tags:
            a_tag = tag.find("a", href=re.compile(r"/about/directory/faculty/"))
            if a_tag:
                href = a_tag.get("href")
                name = a_tag.text.strip()
                profiles[name] = href

        for last_name in school_last_names:
            print("Fetching profile URLs of people with last name of " + last_name)
            for name, url in profiles.items():
                print(name)
                if last_name.lower() in name.lower():
                    full_url = f"https://grainger.illinois.edu{url}"
                    profile_urls.add(full_url)
        
    elif code == "usc":
        wait.until(EC.presence_of_element_located((By.NAME, "namefaculty")))
        driver.execute_script("window.stop();")
        for last_name in school_last_names:
            print("Fetching profile URLs of people with last name of " + last_name)
            search_box = driver.find_element(By.NAME, "namefaculty")
            search_box.clear()
            search_box.send_keys(last_name)
            search_box.submit()
            
            soup = BeautifulSoup(driver.page_source, "html.parser")
            profiles = soup.find_all("div", "faculty-member")

            print(profiles)
            for profile in profiles:
                profile_url = profile.find("a", href=True)["href"]
                profile_urls.add(f"https://viterbi.usc.edu{profile_url}")
    
    elif code == "uta":
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inputbox")))        
        for last_name in school_last_names:
            print("Fetching profile URLs of people with last name of " + last_name)
            search_box = driver.find_element(By.CLASS_NAME, "inputbox")
            search_box.clear()
            search_box.send_keys(last_name)
            search_box.submit()
            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            profiles = soup.find_all("div", class_="facinfo")

            for profile in profiles:
                profile_tag = profile.find("p", class_="contact").find_next_sibling()
                profile_url = profile_tag.find("a", href=True)["href"]
                profile_urls.add(profile_url)

    # Update with newly scraped profile URLs
    print("Saving profile URLs...")
    with open("US Engineering Schools/profile_urls.json", "r") as file:
        j = json.load(file)
    
    j[code] = list(profile_urls)

    with open("US Engineering Schools/profile_urls.json", "w") as file:
        json.dump(j, file, indent=4)

    return profile_urls