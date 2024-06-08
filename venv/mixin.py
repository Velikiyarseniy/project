class ProductDetailParser:
    def get_product_char(self, soup):
        char = ''
        try:
            block = soup.find('div', class_='characteristic-wrap')
            lines = block.find_all('div', class_='list__item')
            for line in lines:
                left = line.find('div', class_='list__name').get_text(strip=True)
                right = line.find('div', class_='list__value').get_text(strip=True)
                char += f'{left}: {right}\n'
        except:
            charr = 'NO CHARACTERISTICS'
        return char