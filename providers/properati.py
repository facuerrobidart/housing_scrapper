from bs4 import BeautifulSoup
import logging
from providers.base_provider import BaseProvider

class Properati(BaseProvider):
    def props_in_source(self, source):
        page = 1
        page_link = self.provider_data['base_url'] + "/%s" % page + source

        print(page_link)

        while page <= 4:

            logging.info("Requesting %s" % page_link)
            page_response = self.request(page_link)

            if page_response.status_code != 200:
                break

            page_content = BeautifulSoup(page_response.content, 'lxml')
            properties = page_content.find_all('div', class_='listing-card')

            if len(properties) == 0:
                break

            for prop in properties:
                link = 'https://www.properati.com.ar' + prop.parent['href']
                title = prop.find('div', class_= 'listing-card__title').get_text().strip()
                price = prop.find('div', class_='price')
                internal_id = prop['data-idanuncio']

                if price:
                    price = price.get_text().strip()

                yield {
                    'title': title,
                    'url': link,
                    'internal_id': internal_id,
                    'provider': self.provider_name,
                    'price': price
                }

            page += 1
            page_link = self.provider_data['base_url'] + "/%s" % page + source
