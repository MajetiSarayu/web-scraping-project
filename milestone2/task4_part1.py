from bs4 import BeautifulSoup
import requests
import os

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
                os.makedirs(f"{path}/{category_names[i].strip().replace(' ', '_')}/", exist_ok=True)
                category_url = category_urls[i]
                if not category_url.startswith('http'):
                    category_url = f'{base_url}{category_url}'
                else:
                    continue
                get_categories(f"{path}/{category_names[i].strip().replace(' ', '_')}/", category_url)
        else:
            return
    else:
        print(f"error fetching {url}")
    
get_categories("milestone2/task4/task4_part1/categories/", site_url)
