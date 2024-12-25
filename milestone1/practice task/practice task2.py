#Task 1 - Scrape any Website

import requests
from bs4 import BeautifulSoup
url = "https://books.toscrape.com/catalogue/category/books/childrens_11/index.html"
response = requests.get(url)
if response.status_code == 200:
    print(f"Successfully fetched the page")
else:
    print(f"Failed to fetch the page. Status code")  
    exit()
soup = BeautifulSoup(response.content, "html.parser")
books = soup.find_all('article', class_='product_pod')
print(f"Found {len(books)} books on the page.")
for book in books:
    title = book.h3.a['title']
    price = book.find('p', class_='price_color').text.strip()
    availability = book.find('p', class_='instock availability').text.strip()
    print(f"Title: {title}")
    print(f"Price: {price}")
    print(f"Availability: {availability}")
    print("-" * 40)