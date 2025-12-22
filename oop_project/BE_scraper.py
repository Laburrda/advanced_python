from bs4 import BeautifulSoup
import json
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class ValidationError(Exception):

    def __init__(self, message) -> None:
        self.message = message
        super().__init__()

    def __str__(self):
        return f"{self.message} (Error Code: {self.error_code})"

class Scraper:
    def __init__(self) -> None:
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = webdriver.Chrome(options=options)

    def get_soup(self, url: str) -> BeautifulSoup:
        self.driver.get(url)

        sleep(5)

        html = self.driver.page_source
        return BeautifulSoup(html, "html.parser")

    def close(self):
        self.driver.quit()

class ScrapBrickEconomy(Scraper):
    def __init__(self, tabs: list[str]) -> None:
        super().__init__()
        self.tabs: list[str] = tabs

    def __validate_modify_info(self, info_ls) -> None:
        if len(info_ls) != 4:
            raise ValidationError(f'The lenght: {len(info_ls)} differ from expected length.')
            
        if 'Theme' not in info_ls[0]:
            raise ValidationError(f'The input list does not contain the "Theme".')
        
        if 'Availability' not in info_ls[-1]:
            raise ValidationError(f'The input list does not contain the "Availability".') 

        if 'Year' not in info_ls[1]:
            raise ValidationError(f'The input list does not contain the "Year".') 


    def modify_info(self, info_ls: list) -> dict:
        data = {}

        if len(info_ls) > 4:
            info_ls.pop(-1)
        self.__validate_modify_info(info_ls)
        
        theme = info_ls[0].split('/')[-1]
        year = info_ls[1].split(' ')[-1]
        availability = info_ls[3].split(' ')[-1]

        data['theme'] = theme.strip()
        data['year'] = int(year)
        data['availability'] = availability

        elements = info_ls[2]
        if 'Pieces' in elements and 'Minifigs' in elements:
            temp_ls = elements.split(' ')

            pieces = temp_ls[3]
            pieces = pieces.replace(',', '')
            data['Pieces'] = int(pieces)

            minifigs = temp_ls[5]
            data['Minifigs'] = int(minifigs)

            return data
        
        if 'Pieces' in elements:
            pieces = elements.split(' ')[-1]
            pieces = pieces.replace(',', '')
            data['Pieces'] = int(pieces)

            return data
        
        if 'Minifigs' in elements:
            minifigs = elements.split(' ')[-1]
            data['Minifigs'] = int(minifigs)

            return data

    def modify_prices(self, prices_ls) -> None:

        def _clear_value(string: str) -> float:
            raw_price = string.split(' ')[1]
            price = raw_price[1:]

            if price[0] == '$':
                price = raw_price[2:]
            
            if ',' in price:
                price = price.replace(',', '')

            price = float(price)

            return price

        data = {}
        if prices_ls[0][:3] == 'pro':
            data['Retail'] = 'Promotional'

            value = _clear_value(prices_ls[1])
            data['Value'] = value

            return data
        
        elif prices_ls[1][:1] == 'N':
            retail = _clear_value(prices_ls[0])
            data['Retail'] = retail

            data['Value'] = 'Not yet released'

            return data

        elif prices_ls[0] == '':
            data['Retail'] = 'Promotional or Unknown'

            value = _clear_value(prices_ls[1])
            data['Value'] = value

            return data

        else:
            retail = _clear_value(prices_ls[0])
            data['Retail'] = retail

            if prices_ls[1][:1] == 'A':
                data['Value'] = prices_ls[1]
            else:
                value = _clear_value(prices_ls[1])
                data['Value'] = value

            return data    
    
    def scrap_lego_set(self, lego_set):
        left_table = lego_set.find('td', class_='ctlsets-left')
        if left_table is None:
            return None

        index = left_table.find('a', href=True)

        raw_info_ls = left_table.find_all('div', class_='mb-2')
        in_info_ls = [info.text for info in raw_info_ls]
        info_ls = self.modify_info(in_info_ls)

        raw_stores = left_table.find_all('span', title=True)
        stores = [store.text for store in raw_stores]

        right_table = lego_set.find('td', class_='ctlsets-right text-right')
        prices = self.modify_prices(
            [div.text for div in right_table.find_all('div')[1:3]]
        )

        data = {
            "set_info": info_ls,
            "stores": stores,
            "prices": prices,
        }

        return index.text, data

    
    def get_main_table(self, soup: BeautifulSoup) -> list:
        data = []

        if not soup:
            return data

        main_table = soup.find('table', class_ = 'table table-hover ctlsets-table')

        sets = main_table.select("tr:has(td.ctlsets-left)")

        for lego_set in sets:
            result = self.scrap_lego_set(lego_set)

            index, set_data = result
            data.append({index: set_data})

        return data
    
    def scrape(self) -> list:
        data = []
        start_time = datetime.now()

        for tab in self.tabs:
            url = 'https://www.brickeconomy.com/sets/theme/star-wars/subtheme/'
            url = url + tab
            
            soup = self.get_soup(url)
            
            if not soup:
                print(f'Failed to scrape subtheme {tab} page.')
                continue
            
            set_info = self.get_main_table(soup)
            print(f'Successfully scraped subtheme {tab}. The data added to the output list.')

            data.extend(set_info)
        
        end_time = datetime.now()
        execition_time = end_time - start_time
        print(f'The total execution time was: {execition_time}')

        return data
    
    def write_json(self, data: dict) -> None:
        version = 'final'
        file_name = f'scraped_brickeconomy_{version}.json'

        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

























