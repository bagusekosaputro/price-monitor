from src.controllers.product_controller import ProductController
from src.utils.page_extractor import PageExtractor

class ScrapJob:
    # def __init__(self):
    #     self.__controller = ProductController()

    def check():
        controller = ProductController()

        products = controller.find_all()
        
        for product in products['data']:
            try:
                link = product['link']
                pid = product['id']
                extractor = PageExtractor(link).extract_page()

                if extractor:
                    controller.update(pid, extractor)
            except Exception as err:
                pass

        return True
