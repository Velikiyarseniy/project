from baseparser import Baseparser
from time import time
from mixin import ProductDetailParser
from database import Database
class TexnomartParser(Baseparser, ProductDetailParser, Database):
    def __init__(self):
        Database.__init__(self)
        Baseparser.__init__(self)
        self.data = {}

    def get_data(self):
        self.create_categories_table()
        self.create_products_table()
        soup = self.get_soup(self.get_html())
        catalog_wrapper = soup.find('div', class_='catalog-top-wrapper')
        categories = catalog_wrapper.find_all('a', class_='top-catalog__item')

        for category in categories[:3]:
            category_title = category.get_text(strip=True)
            self.save_category(category_title)
            category_link = self.host + category.get('href')
            print(category_title)
            print(category_link)
            self.get_products_page(category_title, category_link)

    def get_products_page(self, category_title, category_link):
        soup = self.get_soup(self.get_html(category_link))
        category_id = self.get_category_id(category_title)[0]
        block = soup.find('div', class_='products-box')
        products = block.find_all('div', class_='product-item-wrapper')
        for product in products[:3]:
            product_title = product.find('div', class_='product-bottom__left').get_text(strip=True)
            product_link = self.host + product.find('a', class_='product-name').get('href')
            product_price = product.find('div', class_='product-price__current').get_text(strip=True)
            product_price = int(''.join([i for i in product_price if i.isdigit()]))
            print(product_title)
            print(product_link)
            print(product_price)
            product_soup = self.get_soup(self.get_html(product_link))
            characteristics = self.get_product_char(product_soup)
            print(characteristics)
            self.save_product(product_title=product_title,
                              product_price=product_price,
                              product_link=product_link,
                              characteristics=characteristics,
                              category_id=category_id)
def start_parsing():
    print('Парсер начал работу')
    start = time()
    parser = TexnomartParser()
    parser.get_data()
    finish = time()
    print(f'Парсер отработал за {finish - start} секунд')


start_parsing()
