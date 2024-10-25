from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import json
import glob
import pandas as pd
import time

from scrape_one_step import harvard_seas, ucb_eng
from scrape_two_steps import mit_superurop, mit_pages, uci_samueli, ucsd_jacobs, uiuc_grainger, usc_viterbi, uta_cockrell

from fetch_profile_urls import fetch_profile_urls

def get_mode() -> int:
    """
    Get the scraping preference from User.
    """
    prompt = """Please choose a scraping mode by entering the corresponding number:\n
    "1": view existing profiles
    "2": re-scrape profiles\n
    Enter the mode: """
    
    available_modes = {"1", "2"}
    mode = input(prompt)

    while mode not in available_modes:
        print("Invalid input. Please try again.")
        mode = input(prompt)
    
    print()
    return int(mode)


def get_code_and_scraper() -> int:
    """
    Get the school that User wants to scrape.\n
    Categorize the school's scraping type (pre-defined).
    """
    prompt = """Please choose a school from the list below by entering the corresponding code:\n
    "mitsuperurop": Massachusetts Institute of Technology - SuperUROP Scholars
    "mitpages": Massachusetts Institute of Technology - Miscellaneous Pages
    "harvardseas": Harvard University - Faculty (ONE STEP, QUICKER!)
    "ucb": University of California, Berkeley (ONE STEP, QUICKER!)
    "uci": University of California, Irvine
    "ucsd": University of California, San Diego
    "uiuc": University of Illinois Urbana-Champaign
    "usc": University of Southern California
    "uta": University of Texas at Austin\n
    Enter the code: """

    available_codes = {"mitsuperurop", "mitpages", "harvardseas", "ucb", "uci", "ucsd", "uiuc", "usc", "uta"}
    code = input(prompt)

    while code not in available_codes:
        print("Invalid code. Please try again.")
        code = input(prompt)
    
    print()
    return code


# Scraper for one-step code
def fetch_indirectory_profiles(code: str, school_headers: list, school_func: str, school_url: str, school_csv: str, school_last_names: list) -> None:
    """
    Fetch in-directory profiles (for one-step school code).\n
    Information is retrieved directly from the directory without accessing a second link.\n
    """
    school_funcs = {
        "harvardseas": harvard_seas,
        "ucb": ucb_eng
        }

    school_funcs[code](driver, school_headers, school_url, school_csv, school_last_names)
    
    return None


# Scraper for two-step code
def fetch_secondary_profiles(code: str, school_headers: list, school_func: str, school_csv, profile_urls) -> None:
    """
    Fetch secondary profiles (for two-step school code).\n
    Information is retrieved by accessing a second link.\n
    Pre-requisite: List of profile links.
    """
    school_funcs = {
        "mitsuperurop": mit_superurop,
        "mitpages": mit_pages,
        "uci": uci_samueli,
        "ucsd": ucsd_jacobs,
        "uiuc": uiuc_grainger,
        "usc": usc_viterbi,
        "uta": uta_cockrell
        }

    school_funcs[code](driver, school_headers, school_csv, profile_urls)


def csv_to_xlsx(csv_file, xlsx_file):
    """
    Convert a CSV file to an Excel spreadsheet (XLSX).
    """
    print(csv_file)
    df = pd.read_csv(csv_file)
    df.to_excel(xlsx_file, index=False, engine="openpyxl")
    

def get_current_date():
    return time.strftime("%Y-%m-%d", time.localtime())


if __name__ == "__main__":
    mode = get_mode()
    code = get_code_and_scraper()

    # Retrieve the school's information
    with open("US Engineering Schools/school_infos.json", "r") as file:
        j = json.load(file)
        code_nos = j[code+"_number_of_steps"] # 1 or 2
        school_headers = j[code+"_headers"]
        school_url = j[code]
        school_func = j[code+"_func"]
        school_csv = j[code+"_csv"]
        school_last_names = j[code+"_last_names"]
        school_comment = j[code+"_comment"]

    if mode == 1:
        files = glob.glob(f"**/*{school_csv}*.csv", recursive=True)

        with open(files[0], "r") as f:
            content = f.read()
            print(content)

        print("CSV file with your requested information is available!")

        while True:
            excel = input("Do you want to get the Excel spreadsheet version? (y/n) ")
            if excel != "y" and excel != "n":
                print("Invalid input. Please key in 'y' or 'n'.")
            else:
                break
            
        if excel == "y":
            current_date = get_current_date()
            csv_file = files[0]
            xlsx_file = files[0].replace(".csv", ".xlsx")
            csv_to_xlsx(csv_file, xlsx_file)

    else:
        # Set up options for Chrome WebDriver
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless") # Opt out for USC Viterbi
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox") # Add this if running in Docker or Linux environment
        chrome_options.add_argument("--disable-dev-shm-usage") # Required for running in some systems
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.page_load_strategy = "none" # Do not wait for the entire page to load (skip waiting for unimportant elements), check out for certain codes

        # Inititate Chrome WebDriver
        driver = webdriver.Chrome(options=chrome_options)

        # Accessing profiles
        if code_nos == 1:
            print("Fetching in-directory profiles...")
            fetch_indirectory_profiles(code, school_headers, school_func, school_url, school_csv, school_last_names)
        elif code_nos == 2:
            print("Fetching profile URLs...")
            profile_urls = fetch_profile_urls(driver, code, school_url, school_last_names)
            print("Profile URLs to be scraped: ", end="")
            print(", ".join(profile_urls))

            print("Fetching secondary profiles...")
            fetch_secondary_profiles(code, school_headers, school_func, school_csv, profile_urls)
        
        print("CSV file with your requested information is available!")

        while True:
            excel = input("Do you want to get the Excel spreadsheet version? (y/n) ")
            if excel != "y" and excel != "n":
                print("Invalid input. Please key in 'y' or 'n'.")
            else:
                break
            
        if excel == "y":
            current_date = get_current_date()
            csv_file = f"US Engineering Schools/Profiles/{current_date}_{school_csv}.csv"
            xlsx_file = f"US Engineering Schools/Profiles/{current_date}_{school_csv}.xlsx"
            csv_to_xlsx(csv_file, xlsx_file)

    # Quite Chrome WebDriver after scraping
    driver.quit()
    print("Done and dusted!")