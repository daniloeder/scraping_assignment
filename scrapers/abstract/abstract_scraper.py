import logging
import cloudscraper
from abc import ABC

class AbstractScraper(ABC):
    
    def __init__(self, retailer, country):
        self.retailer = retailer
        self.country = country
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.scraper = cloudscraper.create_scraper()

    def send_get_request(self, url, **kwargs):
        try:
            response = self.scraper.get(url, **kwargs)
            response.raise_for_status()
            return response
        except cloudscraper.exceptions.RequestException as e:
            self.logger.error(f"GET request failed: {e}")
            return None

    def send_post_request(self, url , **kwargs):
        try:
            response = self.scraper.post(url, **kwargs)
            response.raise_for_status()
            return response
        except cloudscraper.exceptions.RequestException as e:
            self.logger.error(f"POST request failed: {e}")
            return None
