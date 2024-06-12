import pandas as pd
from bs4 import BeautifulSoup
from scrapers.abstract.abstract_scraper import AbstractScraper

class NotinoScraper(AbstractScraper):

    BASE_URL = "https://www.notino.cz/zubni-pasty/"

    def scrape(self):
        products = []
        page = 1
        last_page = None

        while not last_page or last_page > page:
            url = f"{self.BASE_URL}?page={page}"
            response_text = self.send_get_request(url).text

            if not response_text:
                break

            soup = BeautifulSoup(response_text, 'html.parser')

            if not last_page or last_page == 1:
                last_page = int(soup.find_all('span', {'data-testid': 'page-item'})[-1].text)
                if last_page > 1:
                    input_text = f"Scrap data to all {last_page} available pages? y/n ('y' to confirm, 'n' to scrap only first page): "
                    user_input = input(input_text.lower())
                    if user_input.lower() != 'y':
                        last_page = 1
            else:
                self.logger.info(f" Scraping page {page}/{last_page}")

            product_cards = soup.select('div.sc-bSstmL.sc-bYpRZF.iJzxKb.llgfxg')

            if not product_cards:
                break

            for card in product_cards:
                try:
                    link = card.find('a', class_='sc-jdHILj OFtqG')
                    if not link:
                        continue
                    product_url = card.find('a', class_='sc-jdHILj OFtqG')['href']
                    full_product_url = f"https://www.notino.cz{product_url}"
                    
                    image_tag = card.find('img', class_='sc-iKOmoZ gTqEqC')
                    image_url = image_tag['src'] if image_tag else None
                    
                    brand = card.find('h2', class_='sc-guDLey sc-jPpdYo kbBsIA dloLns').text.strip()
                    name = card.find('h3', class_='sc-dmyCSP sc-ftxyOh eDlssm icLilU').text.strip() + " " + card.find('p', class_='sc-FjMCv hnrOiP').text.strip()
                    
                    price_tag = card.find('span', {'data-testid': 'price-component'})
                    price = float(price_tag.text.replace(',', '.')) if price_tag else None
                    
                    price_after_sale_tag = card.find('div', {'data-testid': 'additional-info'})
                    price_after_sale = None
                    if price_after_sale_tag:
                        price_after_sale_span = price_after_sale_tag.find('span', {'data-testid': 'price-component'})
                        if price_after_sale_span:
                            price_after_sale = float(price_after_sale_span.text.replace(' ', '').replace(',', '.').replace('\xa0', ''))
                    
                    product = {
                        'name': name,
                        'brand': brand,
                        'price': price,
                        'price_after_sale': price_after_sale,
                        'url': full_product_url,
                        'image': image_url
                    }
                    if product not in products:
                        products.append(product)
                except Exception as e:
                    self.logger.error(f"Error processing product card: {e}")

            page += 1

        self.logger.info(f" Scraped {len(products)} products")
        return pd.DataFrame(products)

def main(retailer: str, country: str) -> pd.DataFrame:
    scraper = NotinoScraper(retailer=retailer, country=country)
    products_df = scraper.scrape()
    return products_df

if __name__ == "__main__":
    df_raw = main(retailer="notino", country="cz")
    df_raw.to_csv("notino_raw.csv", index=False)
