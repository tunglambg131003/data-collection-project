import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Regex pattern to match a URL
HTTP_URL_PATTERN = r'^http[s]*://.+' # r = raw string, ^ = start of string, [s]* = 0 or more s, . = any character except newline, + = 1 or more of the preceding character

domain = "web.mit.edu/search/"
full_url = "https://web.mit.edu/search/"

params = {
    "q": "nguyen"  # The search query
}

def crawl(url):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = []
    while True:
        # Wait for the page to load (adjust as necessary)
        time.sleep(2)
    
        # Update soup with the current page's source
        soup = BeautifulSoup(driver.page_source, "html.parser")

        for link in soup.find_all('div', 'gs-bidi-start-align gs-visibleUrl gs-visibleUrl-long'):
            links.append(link.text) # link is a tag because it is an element of the soup
        
        # Try to find the "Next" button (adjust the selector as needed)
        try:
            wait = WebDriverWait(driver, 10)
            current_button = driver.find_element(By.CSS_SELECTOR, "div.gsc-cursor-page.gsc-cursor-current-page")
            current_page = current_button.text
            print(f"Current page: {current_page}")

            next_page = str(int(current_page) + 1)
            # next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"div.gsc-cursor-page[aria-label='Page {next_page}'][role='link'][tabindex='0']")))
            # if there is no more next page, the next_button will be None
            if next_page == '11':
                break
            else:
                next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"div.gsc-cursor-page[aria-label='Page {next_page}'][role='link'][tabindex='0']")))

            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", next_button)

            print(f"Moved to page: {next_page}")
        except Exception as e:
            print(f"Click intercepted: {e}")
        
    links = list(set(link.strip() for link in links if ' ' not in link))
    print(links)

    # Parse the content of each link to its own file
    local_domain = urlparse(url).netloc

    if not os.path.exists("text/"):    
        os.mkdir("text/")
    
    if not os.path.exists(f"text/{local_domain}/"):
        os.mkdir(f"text/{local_domain}/")
    
    for link in links:
        print("Processing link:", link)
        with open('text/'+local_domain+'/'+link[8:].replace("/", "_") + ".txt", "w", encoding="UTF-8") as f:
            soup = BeautifulSoup(requests.get(link).content, "html.parser")
            content = soup.get_text()
            f.write(content)
    return links

driver = webdriver.Chrome()
driver.get(full_url)
search_box = driver.find_element("name", "q") # find the element that has the name attribute equal to q
search_box.send_keys('nguyen')
search_box.submit()

print(crawl(driver.current_url))

driver.quit()