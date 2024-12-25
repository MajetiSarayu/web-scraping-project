# importing necessary modules and libraries

from bs4 import BeautifulSoup
import requests

# scraping the coin market cap website for details about various digital currencies
url = "https://coinmarketcap.com/"
response = requests.get(url)
print(response.status_code)
response.raise_for_status()

# making the soup
soup = BeautifulSoup(response.content, "html.parser")

# to get logo_images

logo_images = soup.select(".coin-logo")
image_urls = []
for i in logo_images:
    image_urls.append(i.get("src"))
print(image_urls)

# to get currency names

names = [i.get_text() for i in soup.select('.coin-item-name')]
print(names)

# to get currency symbols
symbols = [i.get_text() for i in soup.select(".coin-item-symbol")]
print(symbols)

# to get currency prices
prices = [i.get_text() for i in soup.select('#__next > div.sc-f9c982a5-1.bVsWPX.global-layout-v2 > div.main-content > div.cmc-body-wrapper > div > div:nth-child(1) > div.sc-7b3ac367-2.cFnHu > table > tbody > tr > td:nth-child(4) > div > span')]
print(prices)

# to get market caps
marketcaps = [i.get_text() for i in soup.select('#__next > div.sc-f9c982a5-1.bVsWPX.global-layout-v2 > div.main-content > div.cmc-body-wrapper > div > div:nth-child(1) > div.sc-7b3ac367-2.cFnHu > table > tbody > tr > td:nth-child(8) > p > span.sc-11478e5d-1.jfwGHx')]
print(marketcaps)

currencies = []

for i in range(10):
    currency = {"name":names[i],
                "symbol":symbols[i],
                "logo":image_urls[i],
                "price":prices[i],
                "market_cap":marketcaps[i]}
    currencies.append({f"currency_{i+1}":currency})
print(currencies)



