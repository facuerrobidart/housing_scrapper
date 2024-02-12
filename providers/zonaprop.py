#import requests
from bs4 import BeautifulSoup
import logging
from providers.base_provider import BaseProvider

class Zonaprop(BaseProvider):
    def props_in_source(self, source):
        page_link = self.provider_data['base_url'] + source
        page = 1
        processed_ids = []

        while(True):
            logging.info(f"Requesting {page_link}")
            page_response = self.request(page_link)
            
            if page_response.status_code != 200:
                logging.error(f"Error requesting {page_link}. Status code: {page_response.status_code}")
                print(f"Error requesting {page_link}. Status code: {page_response.status_code}")
                break
            
            page_content = BeautifulSoup(page_response.content, 'lxml')
            
            properties = page_content.find_all('div', class_='sc-i1odl-0')

            for prop in properties:
                # if data-id was already processed we exit
                if page >= 4:
                    return
                processed_ids.append(prop['data-id'])
                title = prop.find('a', class_='sc-i1odl-12').get_text().strip()
                price_section = prop.find('div', class_='sc-12dh9kl-0')

                if price_section is not None:
                    price = price_section.find('div', class_='sc-12dh9kl-4').get_text().strip()
                    print(price)
                    
                yield {
                    'title': title, 
                    'price': price,
                    'url': self.provider_data['base_url'] + prop['data-to-posting'],
                    'internal_id': prop['data-id'],
                    'provider': self.provider_name
                    }

            page += 1
            page_link = self.provider_data['base_url'] + source.replace(".html", f"-pagina-{page}.html")
    