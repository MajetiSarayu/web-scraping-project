from bs4 import BeautifulSoup
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

def get_articles(url, filepath):
    driver = webdriver.Chrome(options=chrome_options)
    not_last = True
    driver.get(url)
    time.sleep(1)
    article_details = {}; article_headings = []; article_timings = []; article_descriptions = []; article_addresses = []; article_contacts = []; article_emails = []; article_website_links = []
    while not_last:
        articles = driver.find_elements(By.TAG_NAME, "article")
        for article in articles:
            heading = article.find_element(By.CSS_SELECTOR, ".result_hit_header h3").text
            article_headings.append(heading)
            try:
                timings = article.find_element(By.CSS_SELECTOR, "div.clearfix").text
            except Exception as e:
                timings = "Not Mentioned"
            article_timings.append(timings)
            article_description = article.find_element(By.CSS_SELECTOR, ".result-hit-body div")
            if article_description:
                article_description = article_description.text
            else:
                article_description = "No Description"
            article_descriptions.append(article_description)
            try:
                address = article.find_elements(By.CSS_SELECTOR, "div.mb-3 span.comma_split_line")
                print(address)
                address = [i.text for i in address]
                article_address = ",".join(address)
                if article_address == '':
                    article_address = "Not Mentioned"
            except Exception as e:
                article_address = "Not Mentioned"
            article_addresses.append(article_address)
            contacts = article.find_elements(By.CSS_SELECTOR, "ul li a:first-of-type")
            contact = email = website = True
            numbers = []
            for i in contacts[:3]:
                if i.text == "Email":
                    article_emails.append(i.get_attribute("href"))
                    email = False
                elif i.text == "Website":
                    article_website_links.append(i.get_attribute("href"))
                    website = False
                else:
                    numbers.append(i.get_attribute("href"))
                    contact = False
            if numbers:
                article_contacts.append([i for i in numbers])
            if email:
                article_emails.append("No Email")
            if website:
                article_website_links.append("No website link")
            if contact:
                article_contacts.append("No Contact")
        try:
            next_page = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.page-link[aria-label='Go to Next Page']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", next_page)
            driver.execute_script("arguments[0].click();", next_page)
            time.sleep(1)
        except Exception as e:
            print("No more pages")
            not_last = False
        article_details = {"name": article_headings, "timing": article_timings, "description": article_descriptions, "address": article_addresses, "contact": article_contacts, "email": article_emails, "website_link": article_website_links}
        df = pd.DataFrame(article_details)
        df.to_csv(f"{filepath}/articles.csv")
    driver.quit()


site_url = 'https://directory.wigan.gov.uk/kb5/wigan/fsd/home.page'

base_url = 'https://directory.wigan.gov.uk/kb5/wigan/fsd/'

def get_categories(path, url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        category_urls = [i.get("href") for i in soup.select(".category-block > a")]
        category_names = [i.get_text() for i in soup.select(".category-block > a > div.card-body")]
        if category_urls:
            for i in range(len(category_names)):
                safe_name = category_names[i].strip().replace(' ', '_').replace(',', '').replace('/', '_')
                try:
                    os.makedirs(f"{path}/{safe_name}/", exist_ok=True)
                except PermissionError as e:
                    print(f"Permission denied")
                    continue
                category_url = category_urls[i]
                if not category_url.startswith('http'):
                    category_url = f'{base_url}{category_url}'
                else:
                    pass
                get_categories(f"{path}/{safe_name}/", category_url)
        else:
            get_articles(url, path)
    else:
        print(f"error fetching {url}")
get_categories("milestone2/task4/task4_part2/categories", site_url)
