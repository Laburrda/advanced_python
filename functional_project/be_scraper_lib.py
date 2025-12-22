from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from time import sleep
from typing import Any, Callable, Dict, List, Optional, Tuple

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ValidationError(Exception):
    pass


#data class, zeby driver na pewno sie zamykal po uzyciu
@dataclass(frozen=True)
class DriverSession:
    driver: webdriver.Chrome

    def __enter__(self) -> webdriver.Chrome:
        return self.driver

    def __exit__(self, exc_type, exc, tb) -> None:
        try:
            self.driver.quit()
        except Exception:
            pass


#zwraca opcje do webdrivera
def get_options() -> Options:
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return options

#zwraca webdriver
def build_driver(options: get_options()) -> webdriver.Chrome:
    return webdriver.Chrome(options=options)

#funkcja zwraca obiekt soup do parsowania htmla
def fetch_soup(
        driver: build_driver(get_options()), #zlozenie
        url: str, wait_seconds: int = 5
) -> BeautifulSoup:
    driver.get(url)
    sleep(wait_seconds)
    html = driver.page_source
    return BeautifulSoup(html, "html.parser")


#funkcja do zapisywania wynikow scrapowania w pliku
def write_json(data: Any, file_name: str) -> None:
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


#walidacja zeskrapowanych informacji
def validate_modify_info(info_ls: List[str]) -> None:
    if len(info_ls) != 4:
        print(info_ls)
        raise ValidationError(f"Length: {len(info_ls)} differs from expected length.")
    if "Theme" not in info_ls[0]:
        raise ValidationError('The input list does not contain the "Theme".')
    if "Year" not in info_ls[1]:
        raise ValidationError('The input list does not contain the "Year".')
    if "Availability" not in info_ls[-1]:
        raise ValidationError('The input list does not contain the "Availability".')


#modyfikacja informacji o danym zestawie
def modify_info(info_ls: List[str]) -> Dict[str, Any]:
    if len(info_ls) > 4:
        info_ls.pop(-1)
    validate_modify_info(info_ls)

    data: Dict[str, Any] = {}

    theme = info_ls[0].split("/")[-1].strip()
    year = int(info_ls[1].split(" ")[-1])
    availability = info_ls[3].split(" ")[-1]

    data["theme"] = theme
    data["year"] = year
    data["availability"] = availability

    elements = info_ls[2]

    if "Pieces" in elements and "Minifigs" in elements:
        temp_ls = elements.split(" ")
        pieces = int(temp_ls[3].replace(",", ""))
        minifigs = int(temp_ls[5])
        data["Pieces"] = pieces
        data["Minifigs"] = minifigs
        return data

    if "Pieces" in elements:
        pieces = int(elements.split(" ")[-1].replace(",", ""))
        data["Pieces"] = pieces
        return data

    if "Minifigs" in elements:
        minifigs = int(elements.split(" ")[-1])
        data["Minifigs"] = minifigs
        return data

    return data

#zamienia cene ze string na float, i obsluguje znak waluty i przecinek co 3 miejsca dziesietne
def clear_value(price_text: str) -> float:
    raw_price = price_text.split(" ")[1]
    price = raw_price[1:]

    if price and price[0] == "$":
        price = raw_price[2:]

    if "," in price:
        price = price.replace(",", "")

    return float(price)


def modify_prices(prices_ls: List[str]) -> Dict[str, Any]:
    data: Dict[str, Any] = {}

    if prices_ls[0][:3] == "pro":
        data["Retail"] = "Promotional"
        data["Value"] = clear_value(prices_ls[1])
        return data

    if prices_ls[1][:1] == "N":
        data["Retail"] = clear_value(prices_ls[0])
        data["Value"] = "Not yet released"
        return data

    if prices_ls[0] == "":
        data["Retail"] = "Promotional or Unknown"
        data["Value"] = clear_value(prices_ls[1])
        return data

    data["Retail"] = clear_value(prices_ls[0])
    if prices_ls[1][:1] == "A":
        data["Value"] = prices_ls[1]
    else:
        data["Value"] = clear_value(prices_ls[1])

    return data

#wyciaga informacje o danych zestawie
def scrap_lego_set(lego_set) -> Optional[Tuple[str, Dict[str, Any]]]:
    left_table = lego_set.find("td", class_="ctlsets-left")
    if left_table is None:
        return None

    index = left_table.find("a", href=True)
    if index is None:
        return None

    raw_info_ls = left_table.find_all("div", class_="mb-2")
    in_info_ls = [info.text for info in raw_info_ls]
    info_dict = modify_info(in_info_ls)

    raw_stores = left_table.find_all("span", title=True)
    stores = [store.text for store in raw_stores]

    right_table = lego_set.find("td", class_="ctlsets-right text-right")
    if right_table is None:
        return None

    price_divs = [div.text for div in right_table.find_all("div")[1:3]]
    prices = modify_prices(price_divs)

    data = {
        "set_info": info_dict,
        "stores": stores,
        "prices": prices,
    }

    return index.text, data

#wyciaga tabele z interesujacymi informacjami
def get_main_table(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    data: List[Dict[str, Any]] = []
    if not soup:
        return data

    main_table = soup.find("table", class_="table table-hover ctlsets-table")
    if main_table is None:
        return data

    sets = main_table.select("tr:has(td.ctlsets-left)")
    for lego_set in sets:
        result = scrap_lego_set(lego_set)
        if result is None:
            continue
        index, set_data = result
        data.append({index: set_data})

    return data

#wyciaga informacje o zakladkach
def scrape_tabs(
    tabs: List[str],
    base_url: str = "https://www.brickeconomy.com/sets/theme/star-wars/subtheme/",
    wait_seconds: int = 5,
    logger: Optional[Callable[[str], None]] = print,
    #zlozenie
    driver = build_driver(get_options()),
) -> List[Dict[str, Any]]:
    start_time = datetime.now()
    output: List[Dict[str, Any]] = []

    with DriverSession(driver) as driver:
        for tab in tabs:
            url = base_url + tab
            soup = fetch_soup(driver, url, wait_seconds=wait_seconds)

            if not soup:
                if logger:
                    logger(f"Failed to scrape subtheme {tab} page.")
                continue

            set_info = get_main_table(soup)
            output.extend(set_info)

            if logger:
                logger(f"Successfully scraped subtheme {tab}. The data added to the output list.")

    end_time = datetime.now()
    if logger:
        logger(f"The total execution time was: {end_time - start_time}")

    return output
