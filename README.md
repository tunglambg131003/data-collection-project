# Data Collection Tool Development Project


This project is designed to automate the collection of academic profiles from various engineering school websites. The tool leverages Selenium and BeautifulSoup to extract relevant information and store it in structured formats like CSV and XLSX files.

# Features
- Store necessary information for scraping process in lightweight JSON files.
- Fetch and parse academic profile URLs from various school websites.
- Modular code to support scraping from various school websites/ profile URLs.
- Store scraped data in CSV format, with an option to convert into XLSX.

# Installation

## Step 1: Clone the Repository
```bash
git clone https://github.com/tunglambg131003/data-collection-project.git
cd data-collection-project
```

## Step 2: Set Up Virtual Environment (Optional)
```bash
ython -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

## Step 3: Install Dependencies
Make sure you have Python 3.7+ installed. Then, install the required packages:
```bash
pip install -r requirements.txt
```

# Usage
1. Configure Input Files
- `school_infos.json`: Contains information about the schools you want to scrape, including URLs, search parameters, headers, and comments.
- `profile_urls.json`: Stores URLs of the profiles that are fetched in the first step for two-step scraping processes.

2. Choose Scraping Mode
Run the scraper with the following command:
```bash
python us_schools_scraper.py
```
You will be prompted to choose a scraping mode:
- Mode 1: View existing profiles from previously generated CSV files.
- Mode 2: Re-scrape profiles from the school directories (recommended if data needs to be refreshed).

3. Choose the School to Scrape
After selecting the scraping mode, you will be prompted to enter a school code. The available options are:
```arduino
"mitsuperurop": Massachusetts Institute of Technology - SuperUROP Scholars
"mitpages": Massachusetts Institute of Technology - Miscellaneous Pages
"harvardseas": Harvard University - Faculty (One-step scraping)
"ucb": University of California, Berkeley - Faculty (One-step scraping)
"uci": University of California, Irvine
"ucsd": University of California, San Diego
"uiuc": University of Illinois Urbana-Champaign
"usc": University of Southern California
"uta": University of Texas at Austin
```

4. Scraping Workflow
- One-Step Scraping: Some schools allow scraping directly from the directory.
  - In this case, the scraper pulls profile data directly without following secondary links.
  - Example Schools: `harvardseas`, `ucb`
- Two-Step Scraping:
  - For some schools, you first need to fetch profile URLs. The scraper will access each URL to gather detailed profile information.
  - Example Schools: `mitsuperurop`, `mitpages`, `uci`, `ucsd`, `uiuc`, `usc`, `uta`

5. Output Files
- CSV Files: The scraped data is stored in the `US Engineering Schools/Profiles/` folder.
- Excel Files: You can optionally convert the CSV files to Excel by answering "y" when prompted.

6. Example Run
- Viewing Existing Profiles (Mode 1):
  - You’ll see the contents of the most recent CSV file for the selected school.
  - If you want an Excel version of the CSV, type "y" when prompted.

- Re-scraping Profiles (Mode 2):
  - The scraper will perform one-step or two-step scraping based on the school you selected.
  - For two-step scraping, URLs will be fetched first, and the profiles will be accessed through those URLs.

7. Chrome WebDriver Setup
The project uses Selenium WebDriver to automate browser interactions. Ensure you have Google Chrome installed and the matching ChromeDriver version in your system PATH.

For headless scraping (without GUI), you can uncomment the `chrome_options.add_argument("--headless")` line in `us_schools_scraper.py`.

# Project Structure
```graphql
data-collection-project/
│
├── US Engineering Schools/          
│   ├── school_infos.json          # Configuration for each school (URLs, headers, scraping steps)
us_schools_scraper.py
│   ├── profile_urls.json          # Stores URLs fetched in the first step for two-step scraping
│   └── Profiles/                  # Directory where scraped profiles (CSV/Excel) are saved
│
├── scrape_one_step.py/               # Contains scripts for one-step scraping logic
│
├── scrape_two_steps.py/              # Contains scripts for two-step scraping logic
│
├── fetch_profile_urls.py          # Contains logic to fetch profile URLs for two-step scraping
│
├── us_schools_scraper.py          # Main script to handle user inputs and execute the scraping process
│
├── requirements.txt               # List of Python dependencies required for the project
│
└── README.md                      # Documentation on how to use the project
```
Google Scholar Profile - Computer Science.csv

# Dependencies
Selenium, BeautifulSoup, pandas, openpyxl, Google Chrome & ChromeDriver, time, re, glob, json

# Contributing
Feel free to submit issues or pull requests if you have suggestions or improvements.

# Contact
For any questions or issues, please contact:
- Phan Nguyen Tuan Anh: nicophan.business@gmail.com
- Nguyen Tung Lam: repository owner
