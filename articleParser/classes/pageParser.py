import requests
from requests.exceptions import HTTPError

class PageParser():
    
    def __init__(self, url: str):
        self.url = url
    
    def get_page_data(self):
        try:
            page = requests.get(self.url)
            page.raise_for_status()
        
        except HTTPError as http_error:
            print(f'Response code: {http_error}')
            page = None
        
        except Exception as exception:
            print(f'Unexpected!: {exception}')
        
        return page
