from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re
# import summy_example


def get_current_date():
    return time.strftime("%Y-%m-%d", time.localtime())

def clean_info(*args):
    cleaned_infos = []
    for arg in args:
        cleaned_infos.append(re.sub(r"\s+", " ", arg).replace('"', "").strip())
    return cleaned_infos

def mit_superurop(driver, school_headers, school_csv, profile_urls):
    """
    Scrape Vietnamese profiles from Harvard University - SuperUROP Program.
    """
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div/div[2]/div[1]/div[1]/div[4]/input")))

    current_date = get_current_date()

    with open(f"US Engineering Schools/Profiles/{current_date}_{school_csv}.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=school_headers)
        writer.writeheader()

        for profile_url in profile_urls:
            print(f"Accessing: {profile_url}")
            driver.get(profile_url)
            time.sleep(3)

            profile = BeautifulSoup(driver.page_source, "html.parser")

            name_tag = profile.find("h2", class_="name") if profile.find("h2", class_="name") else None
            scholar_title_tag = profile.find("div", string="Scholar Title").find_next_sibling() if profile.find("div", string="Scholar Title") else None
            email_tag = profile.find("a", href=re.compile(r"^mailto:")) if profile.find("a", href=re.compile(r"^mailto:")) else None
            research_title_tag = profile.find("div", string="Research Title").find_next_sibling() if profile.find("div", string="Research Title") else None
            research_areas_tag = profile.find("ul", class_="research-areas") if profile.find("div", string="Research Areas") else None
            research_abstract_tag = profile.find("div", string="Abstract").find_next_sibling() if profile.find("div", string="Abstract") else None
            supervisor_tag = profile.find("div", class_="supervisor").find_next_sibling() if profile.find("div", class_="supervisor") else None
            cohort_tag = profile.find("div", string="Cohort").find_next_sibling() if profile.find("div", string="Cohort") else None
            quote_tag = profile.find("div", string="Quote") if profile.find("div", string="Quote") else None

            name = name_tag.text if name_tag else ""
            scholar_title = scholar_title_tag.text if scholar_title_tag else ""
            email = email_tag.text if email_tag else ""
            research_title = research_title_tag.text if research_title_tag else ""
            research_areas = research_areas_tag.text if research_areas_tag else ""
            research_abstract = research_abstract_tag.text if research_abstract_tag else ""
            supervisor = supervisor_tag.text if supervisor_tag else ""
            cohort = cohort_tag.text if cohort_tag else ""
            quote = quote_tag.text if quote_tag else ""

            cleaned_infos = clean_info(name, scholar_title, email, research_title, research_areas, research_abstract, supervisor, cohort, quote)

            print(f"Adding profile: {cleaned_infos[0]}, {cleaned_infos[1]}, {cleaned_infos[2]}, {cleaned_infos[3]}, {cleaned_infos[4]}, {cleaned_infos[5]}, {cleaned_infos[6]}, {cleaned_infos[7]}, {cleaned_infos[8]}, {profile_url}")

            writer.writerow({
                'Name': cleaned_infos[0],
                'Email': cleaned_infos[1],
                'Scholar Title': cleaned_infos[2],
                'Research Title': cleaned_infos[3],
                'Research Areas': cleaned_infos[4],
                'Research Abstract': cleaned_infos[5],
                'Supervisor': cleaned_infos[6],
                'Cohort': cleaned_infos[7],
                'Quote': cleaned_infos[8],
                'Profile URL': profile_url
            })


def mit_pages(driver, school_headers, school_csv, profile_urls):
    pass


def uci_samueli(driver, school_headers, school_csv, profile_urls):
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.ID, "edit-name")))

    current_date = get_current_date()

    with open(f"US Engineering Schools/Profiles/{current_date}_{school_csv}.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=school_headers)
        writer.writeheader()

        for profile_url in profile_urls:
            print(f"Accessing: {profile_url}")
            driver.get(profile_url)
            # or profile_content = requests.get(profile_url).content
            time.sleep(3)

            profile = BeautifulSoup(driver.page_source, "html.parser")

            name = profile.find("div", class_="pane-node-title").find("h1").text
            title_dept = profile.find("div", class_="field_pdept").get_text(separator=", ", strip=True) if profile.find("div", class_="field_pdept") else ""
            email = profile.find("a", href=re.compile(r'^mailto:'))["href"].split(':')[1] if profile.find("a", href=re.compile(r"^mailto:")) else ""
            bio = profile.find("div", class_="field_bio").get_text(separator='\n') if profile.find("div", class_="field_bio") else ""
            research_summary = profile.find("div", class_="field_research").get_text(separator='\n') if profile.find("div", class_="field_research") else ""
            address = profile.find("div", class_="field_room").text if profile.find("div", class_="field_room") else ""
            phone_number = profile.find("div", class_="field_phone").text if profile.find("div", class_="field_phone") else ""

            cleaned_infos = clean_info(name, email, bio, research_summary, address, phone_number)

            print(f"Adding profile: {cleaned_infos[0]}, {title_dept}, {cleaned_infos[1]}, {cleaned_infos[2]}, {cleaned_infos[3]}, {cleaned_infos[4]}, {cleaned_infos[5]}, {profile_url}")

            writer.writerow({
                'Name': cleaned_infos[0],
                'Title, Department': title_dept,
                'Email': cleaned_infos[1],
                'Biography': cleaned_infos[2],
                'Research Summary': cleaned_infos[3],
                'Address': cleaned_infos[4].replace("Location ", ""),
                'Phone Number': cleaned_infos[5].replace("Phone ", ""),
                'Profile URL': profile_url
            })


def ucsd_jacobs(driver, school_headers, school_csv, profile_urls):
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.ID, "edit-field-profile-last-name-value")))

    current_date = get_current_date()

    with open(f"US Engineering Schools/Profiles/{current_date}_{school_csv}.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=school_headers)
        writer.writeheader()

        for profile_url in profile_urls:
            print(f"Accessing: {profile_url}")
            driver.get(profile_url)
            # or profile_content = requests.get(profile_url).content
            time.sleep(3)

            profile = BeautifulSoup(driver.page_source, "html.parser")

            name_tag = profile.find("h3", class_="faculty_profile_name")
            title_dept_tag = name_tag.find_next_sibling()
            email_tag = profile.find("img", class_="mb-4").find_next_sibling()

            name = name_tag.text
            title_dept = title_dept_tag.text
            email = email_tag.text
            bio = profile.find("p", string="Capsule Bio:").find_next_sibling().text
            research_summary = title_dept_tag.find_next_sibling().find_next_sibling().text
            phone_number = email_tag.find_next_sibling().text

            cleaned_infos = clean_info(name, email, bio, research_summary, phone_number)

            print(f"Adding profile: {cleaned_infos[0]}, {title_dept}, {cleaned_infos[1]}, {cleaned_infos[2]}, {cleaned_infos[3]}, {cleaned_infos[4]}, {profile_url}")

            writer.writerow({
                'Name': cleaned_infos[0],
                'Title, Department': title_dept,
                'Email': cleaned_infos[1].replace("Email:", ""),
                'Biography': cleaned_infos[2],
                'Research Summary': cleaned_infos[3],
                'Phone Number': cleaned_infos[4].replace("Phone", ""),
                'Profile URL': profile_url
            })


def uiuc_grainger(driver, school_headers, school_csv, profile_urls):
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.ID, "department-filter-button")))

    current_date = get_current_date()

    with open(f"US Engineering Schools/Profiles/{current_date}_{school_csv}.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=school_headers)
        writer.writeheader()

        for profile_url in profile_urls:
            print(f"Accessing: {profile_url}")
            driver.get(profile_url)
            # or profile_content = requests.get(profile_url).content
            time.sleep(3)

            profile = BeautifulSoup(driver.page_source, "html.parser")

            title_tag = profile.find("div", class_='title') if profile.find("div", class_="title") else None
            title_li_tags = title_tag.find_all("li") if title_tag else None
            education_tag = profile.find("h2", string="Education").find_next_sibling() if profile.find("h2", string="Education") else None
            education_li_tags = education_tag.find_all("li") if education_tag else None
            research_int_tag = profile.find("h2", string="Research Interests").find_next_sibling() if profile.find("h2", string="Research Interests") else None
            research_int_li_tags = research_int_tag.find_all("li") if research_int_tag else None
            research_areas_tag = profile.find("h2", string="Research Areas").find_next_sibling() if profile.find("h2", string="Research Areas") else None
            research_areas_li_tags = research_areas_tag.find_all("li") if research_areas_tag else None
            academic_posts_tag = profile.find("h2", string="Academic Positions").find_next_sibling() if profile.find("h2", string="Academic Positions") else None
            academic_posts_li_tag = academic_posts_tag.find_all("li") if academic_posts_tag else None
            pro_highs_tag = profile.find("h2", string="Professional Highlights").find_next_sibling() if profile.find("h2", string="Professional Highlights") else None
            pro_highs_li_tag = pro_highs_tag.find_all("li") if pro_highs_tag else None

            name = profile.find("div", id="hero").text
            title = '\n'.join([li.get_text() for li in title_li_tags]) if title_li_tags else ""
            email = profile.find("a", href=re.compile(r"^mailto:")).text if profile.find("a", href=re.compile(r"^mailto:")) else ""
            education = '\n'.join([li.get_text() for li in education_li_tags]) if education_li_tags else ""
            research_int = '\n'.join([li.get_text() for li in research_int_li_tags]) if research_int_li_tags else ""
            research_areas = '\n'.join([li.get_text() for li in research_areas_li_tags]) if research_areas_li_tags else ""
            academic_posts = '\n'.join([li.get_text() for li in academic_posts_li_tag]) if academic_posts_li_tag else ""
            pro_highs = '\n'.join([li.get_text() for li in pro_highs_li_tag]) if pro_highs_li_tag else ""
            address = profile.find("div", class_="office").text if profile.find("div", class_="office") else ""
            phone_no = profile.find("div", class_="phone").text if profile.find("div", class_="phone") else ""
            
            cleaned_infos = clean_info(name, title, email, education, research_int, research_areas, academic_posts, pro_highs, address, phone_no)

            print(f"Adding profile: {cleaned_infos[0]}, {cleaned_infos[1]}, {cleaned_infos[2]}, {cleaned_infos[3]}, {cleaned_infos[4]}, {cleaned_infos[5]}, {cleaned_infos[6]}, {cleaned_infos[7]}, {cleaned_infos[8]}, {cleaned_infos[9]}, {profile_url}")

            writer.writerow({
                'Name': cleaned_infos[0],
                'Title': cleaned_infos[1],
                'Email': cleaned_infos[2],
                'Education': cleaned_infos[3],
                'Research Interests': cleaned_infos[4],
                'Research Areas': cleaned_infos[5],
                'Research Positions': cleaned_infos[6],
                'Professional Highlights': cleaned_infos[7],
                'Address': cleaned_infos[8],
                'Phone Number': cleaned_infos[9],
                'Profile URL': profile_url
            })


def usc_viterbi(driver, school_headers, school_csv, profile_urls):
    # NOTE: Slow website, need to force stop
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.NAME, "namefaculty")))
    driver.execute_script("window.stop();")
    
    current_date = get_current_date()

    with open(f"US Engineering Schools/Profiles/{current_date}_{school_csv}.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=school_headers)
        writer.writeheader()

        for profile_url in profile_urls:
            print(f"Accessing: {profile_url}")
            driver.get(profile_url)
            # or profile_content = requests.get(profile_url).content
            time.sleep(3)

            profile = BeautifulSoup(driver.page_source, "html.parser")

            contact_info_1_tag = profile.find("h6", string="Contact Information").find_next("li") if profile.find("h6", string="Contact Information") else None
            contact_info_2_tag = contact_info_1_tag.find_next("li") if contact_info_1_tag else None

            name = profile.find("h4", class_="facultyname").text
            title = profile.find("div", class_="education-piece").find("p").text if profile.find("div", class_="education-piece").find("p") else ""
            dept = profile.find("h6", string="Appointments").find_next("li").text if profile.find("h6", string="Appointments").find_next("ul") else ""       
            title_dept = title + ", " + dept
            contact_info = contact_info_1_tag.text if contact_info_1_tag else ""
            contact_info = contact_info + ", " + contact_info_2_tag.text if contact_info_2_tag.text[-1] != ':' else contact_info
            bio = profile.find("div", class_="biography-piece").get_text(separator='\n') if profile.find("div", class_="biography-piece") else ""
            research = profile.find("div", class_="research-piece").get_text(separator='\n') if profile.find("div", class_="research-piece") else ""
            address = profile.find("h6", string="Office").find_next("ul").get_text(separator='\n') if profile.find("h6", string="Office").find_next("ul") else None

            cleaned_infos = clean_info(name, title_dept, bio, research, address)

            print(f"Adding profile: {cleaned_infos[0]}, {cleaned_infos[1]}, {contact_info}, {cleaned_infos[2]}, {cleaned_infos[3]}, {cleaned_infos[4]}, {profile_url}")

            writer.writerow({
                'Name': cleaned_infos[0],
                'Title, Department': cleaned_infos[1],
                'Contact Information': contact_info,
                'Biography': cleaned_infos[2],
                'Research Summary': cleaned_infos[3],
                'Address': cleaned_infos[4],
                'Profile URL': profile_url
            })


def uta_cockrell(driver, school_headers, school_csv, profile_urls):
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.ID, "mod_search_searchword")))

    current_date = get_current_date()

    with open(f"US Engineering Schools/Profiles/{current_date}_{school_csv}.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=school_headers)
        writer.writeheader()

        for profile_url in profile_urls:
            print(f"Accessing: {profile_url}")
            driver.get(profile_url)
            # or profile_content = requests.get(profile_url).content
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "facdata")))
            time.sleep(3)

            profile = BeautifulSoup(driver.page_source, "html.parser")

            info_tag = profile.find("div", class_="facdata")
            photo_tag = profile.find("div", class_="facphoto")
            fact_tag = profile.find("div", class_="facarticle")
            edu_tags = fact_tag.find_all("p") if fact_tag else None
            edu_tag = next((tag for tag in edu_tags if "PhD" in tag.get_text() or "Ph.D." in tag.get_text()), None) if edu_tags else None
            research_tag_1 = fact_tag.find("strong", string=re.compile(r"Research", re.IGNORECASE)) if fact_tag else None
            research_tag_2 = research_tag_1.find_next() if research_tag_1 else None
            research_li_tag = research_tag_2.find_all("li") if research_tag_2 else None        

            name = info_tag.find("h3").text if info_tag else ""
            title = info_tag.find("h5").text if info_tag else ""
            email = photo_tag.find("a", href=True)["href"] if photo_tag else ""
            edu = edu_tag.text if edu_tag else ""
            research = '\n'.join([li.get_text() for li in research_li_tag]) if research_li_tag else ""

            cleaned_infos = clean_info(name, title, email, edu, research)
            
            print(f"Adding profile: {cleaned_infos[0]}, {cleaned_infos[1]}, {cleaned_infos[2]}, {cleaned_infos[3]}, {cleaned_infos[4]}, {profile_url}")

            writer.writerow({
                'Name': cleaned_infos[0],
                'Title': cleaned_infos[1],
                'Email': cleaned_infos[2].replace("mailto:", ""),
                'Education': cleaned_infos[3],
                'Research Interests': cleaned_infos[4],
                'Profile URL': profile_url
            })