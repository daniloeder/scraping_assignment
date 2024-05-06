# import any libraries you want
import logging

from abc import ABC


class AbstractScraper(ABC):
    
    def __init__(self, retailer, country):
        self.retailer = retailer
        self.country = country
        # implement logger

    # implement methods for sending GET and POST requests
    # these methods should be able to handle sending requests to the url with headers, cookies, params & json (POST requests only)
    def send_get_request(self, url, **kwargs):
        pass

    def send_post_request(self, url , **kwargs):
        pass

    # feel free to add any other methods you think you might need or could be useful