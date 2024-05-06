# import any libraries you want
import pandas as pd

from scrapers.abstract.abstract_scraper import AbstractScraper

class NotinoScraper(AbstractScraper):
    # implement scraper for notino - toothpastes
    # choose any Notino website your prefer (they operates in 28 countries) 
    # https://www.notino.cz/zubni-pasty/ // https://www.notino.co.uk/toothpaste/ // https://www.notino.de/zahnpasten/ ...

    # to each product get at least (but the more, the better) these data:
    # - product name
    # - brand
    # - price
    # - price after sale (if any)
    # - promocode (if any)
    # - url
    # - image

    # place for your code here...
    
    def scrape(self):
        pass

def main(retailer: str, country: str) -> pd.DataFrame:
    scraper = NotinoScraper(retailer=retailer, country=country)
    products_df = scraper.scrape()

    return products_df

if __name__ == "__main__":
    df_raw = main(retailer="notino", country="cz")
    df_raw.to_csv("notino_raw.csv", index=False)