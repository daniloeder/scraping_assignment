import logging
import cloudscraper
from abc import ABC
import time

class AbstractScraper(ABC):
    
    def __init__(self, retailer, country):
        self.retailer = retailer
        self.country = country
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.scraper = cloudscraper.create_scraper()

    def send_get_request(self, url, **kwargs):
        try:
            for _ in range(5):
                try:
                    response = self.scraper.get(url, **kwargs)
                    response.raise_for_status()
                    if response.text:
                        return response
                except:
                    time.sleep(1)
        except Exception as e:
            self.logger.error(f"Error sending GET request to {url}: {e}")
            return None
