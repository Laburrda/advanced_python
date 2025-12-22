from datetime import datetime
from typing import List, Dict, Union, Optional
from bs4 import BeautifulSoup, Tag

from base_scraper import BaseScraper
from exceptions import ValidationError
from utils import parse_currency


class BrickEconomyScraper(BaseScraper):
    BASE_URL = 'https://www.brickeconomy.com/sets/theme/star-wars/subtheme/'

    def __init__(self, tabs: List[str]) -> None:
        super().__init__()
        self.tabs = tabs

    def _validate_info_list(self, info_ls: List[str]) -> None:
        """Sprawdza czy lista informacji o zestawie ma poprawną strukturę."""
        if len(info_ls) < 4:
            raise ValidationError(f'Info list length {len(info_ls)} is too short.')

        if 'Theme' not in info_ls[0]:
            raise ValidationError('Missing "Theme" in info list.')

        if not any('Year' in item for item in info_ls):
            raise ValidationError('Missing "Year" in info list.')

    def _extract_set_details(self, info_ls: List[str]) -> Dict[str, Union[str, int]]:
        """Parsuje listę stringów z detalami zestawu."""
        data = {}

        if len(info_ls) > 4:
            info_ls.pop(-1)

        self._validate_info_list(info_ls)

        # Parsowanie podstawowe
        data['theme'] = info_ls[0].split('/')[-1].strip()
        data['year'] = int(info_ls[1].split(' ')[-1])
        data['availability'] = info_ls[3].split(' ')[-1]

        # Parsowanie Pieces / Minifigs (element info_ls[2])
        elements = info_ls[2]

        if 'Pieces' in elements:
            temp_parts = elements.split(' ')

            try:
                if 'Pieces' in temp_parts:
                    p_idx = temp_parts.index('Pieces')
                    pieces_str = elements.split('Pieces')[-1].split('/')[0].replace('Minifigs', '').strip().replace(',',
                                                                                                                    '')
                    data['Pieces'] = int(pieces_str)

                if 'Minifigs' in temp_parts:
                    m_idx = elements.find('Minifigs')
                    minifigs_str = elements[m_idx:].split(' ')[-1]
                    data['Minifigs'] = int(minifigs_str)
            except (ValueError, IndexError):
                pass

        return data

    def _extract_prices(self, prices_ls: List[str]) -> Dict[str, Union[float, str]]:
        """Parsuje ceny Retail i Value."""
        data = {}

        retail_raw = prices_ls[0]
        value_raw = prices_ls[1]

        # 1. Retail
        if retail_raw.startswith('pro') or retail_raw == '':
            data['Retail'] = 'Promotional or Unknown'
        else:
            data['Retail'] = parse_currency(retail_raw)

        # 2. Value
        if value_raw.startswith('N'):  # Not yet released
            data['Value'] = 'Not yet released'
        elif value_raw.startswith('A'):  # Available
            data['Value'] = value_raw
        else:
            data['Value'] = parse_currency(value_raw)

        if data['Retail'] == 'Promotional or Unknown' and not isinstance(data['Value'], str):
            pass

        return data

    def _scrape_single_set(self, lego_set_row: Tag) -> Optional[tuple]:
        """Przetwarza jeden wiersz tabeli (jeden zestaw)."""
        left_table = lego_set_row.find('td', class_='ctlsets-left')
        if not left_table:
            return None

        # Nazwa zestawu i ID
        link_tag = left_table.find('a', href=True)
        set_name_key = link_tag.text if link_tag else "Unknown_Set"

        # Informacje
        raw_info_ls = left_table.find_all('div', class_='mb-2')
        in_info_ls = [info.text for info in raw_info_ls]

        try:
            info_data = self._extract_set_details(in_info_ls)
        except ValidationError:
            return None

        # Sklepy
        raw_stores = left_table.find_all('span', title=True)
        stores = [store.text for store in raw_stores]

        # Ceny
        right_table = lego_set_row.find('td', class_='ctlsets-right text-right')
        # Pobieramy 2 divy z cenami (z pominięciem pierwszego, który może być pusty w strukturze)
        price_divs = [div.text for div in right_table.find_all('div')[1:3]]
        price_data = self._extract_prices(price_divs)

        final_data = {
            "set_info": info_data,
            "stores": stores,
            "prices": price_data,
        }

        return set_name_key, final_data

    def run(self) -> List[Dict]:
        """Główna pętla scrapująca."""
        all_data = []
        start_time = datetime.now()

        for tab in self.tabs:
            url = self.BASE_URL + tab
            soup = self.get_soup(url)

            if not soup:
                print(f'[ERROR] Failed to scrape subtheme: {tab}')
                continue

            main_table = soup.find('table', class_='table table-hover ctlsets-table')
            if not main_table:
                print(f'[WARNING] No table found for subtheme: {tab}')
                continue

            sets_rows = main_table.select("tr:has(td.ctlsets-left)")

            subtheme_count = 0
            for row in sets_rows:
                result = self._scrape_single_set(row)
                if result:
                    index, set_data = result
                    all_data.append({index: set_data})
                    subtheme_count += 1

            print(f'[OK] Scraped {subtheme_count} sets from: {tab}')

        duration = datetime.now() - start_time
        print(f'Total execution time: {duration}')

        return all_data