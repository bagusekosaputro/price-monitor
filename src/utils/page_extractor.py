import requests

from bs4 import BeautifulSoup


class PageExtractor:
    def __init__(self, link):
        self.__product_link = link

    def extract_page(self):
        page = requests.get(self.__product_link)

        extractor = BeautifulSoup(page.text, "html.parser")
        product_id = None
        result = {

        }

        if page.status_code == 200:
            product_tag = extractor.find(id="product-ratings").attrs
            product_id = product_tag['data-product-id']
            
            price_tag_id = f"product-price-{product_id}"

            price_tag = extractor.find(id=price_tag_id).attrs

            description_tag = extractor.find(class_="product-info__description")

            title_tag = extractor.find(attrs={"data-ui-id": "page-title-wrapper"})

            # images_tags = extractor.find('img')
            images = []

            # for image_tag in images_tags:
            #     image = image_tag
            #     images.append(str(image))
            
            result['source_product_id'] = int(product_id)
            result['price'] = int(price_tag['data-price-amount'])
            result['description'] = description_tag.text
            result['images'] = str(images)
            result['link'] = self.__product_link
            result['name'] = title_tag.text
        
        return result
