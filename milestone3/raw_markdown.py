from selenium import webdriver
from markdownify import markdownify as md
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import random, time
from assets_variables import USER_AGENTS
from bs4 import BeautifulSoup


def sel_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    user_agent = random.choice(USER_AGENTS)
    chrome_options.add_argument(f"user-agent={user_agent}")
    web_driver = webdriver.Chrome(options=chrome_options)
    return web_driver

def clean_raw_data(content):
    soup = BeautifulSoup(content, 'html.parser')
    if soup.header:
        soup.header.decompose()
    if soup.footer:
        soup.footer.decompose()
    return str(soup)

def markdown(url):
    driver = sel_driver()
    try:
        driver.get(url)
        time.sleep(2)

        # Scroll until no more scrolling is available
        scroll_pause_time = 2
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Fetch and process the page source
        html_content = driver.page_source
        cleaned_html = clean_raw_data(html_content)
        markdown_content = md(cleaned_html)

        # Save the markdown content to a file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"./output_raw_data/raw_data_{timestamp}.md", "w", encoding="utf-8") as file:
            file.write(markdown_content)

    finally:
        driver.quit()

    return markdown_content







