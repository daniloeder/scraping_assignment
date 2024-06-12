import pandas as pd
import requests
from bs4 import BeautifulSoup
from scrapers.abstract.abstract_scraper import AbstractScraper

class NotinoScraper(AbstractScraper):

    BASE_URL = "https://www.notino.cz/zubni-pasty/"

    def scrape(self):
        products = []
        page = 1
        
        while True:
            url = f"{self.BASE_URL}?page={page}"
            response = self.send_get_request(url)
            if not response:
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            product_cards = soup.find_all('div', class_='product-item')

            if not product_cards:
                break
            
            for card in product_cards:
                name = card.find('span', class_='product-item__name').text.strip()
                brand = card.find('span', class_='product-item__brand').text.strip()
                price = card.find('span', class_='price').text.strip()
                product_url = card.find('a', class_='product-item__link')['href']
                image_url = card.find('img', class_='product-item__image')['data-src']
                price_after_sale = card.find('span', class_='price--discount')

                if price_after_sale:
                    price_after_sale = price_after_sale.text.strip()
                else:
                    price_after_sale = None

                products.append({
                    'name': name,
                    'brand': brand,
                    'price': price,
                    'price_after_sale': price_after_sale,
                    'url': product_url,
                    'image': image_url
                })

            page += 1

        return pd.DataFrame(products)

def main(retailer: str, country: str) -> pd.DataFrame:
    scraper = NotinoScraper(retailer=retailer, country=country)
    products_df = scraper.scrape()
    return products_df

if __name__ == "__main__":
    df_raw = main(retailer="notino", country="cz")
    df_raw.to_csv("notino_raw.csv", index=False)
