import pytest

from typing import List
from BE_scraper import ScrapBrickEconomy, ValidationError

@pytest.mark.modinfo
def test_modify_info_PiecesMinifigs():
    scraper: ScrapBrickEconomy = ScrapBrickEconomy([])

    input_info: List[str] = [
        'Theme / Subtheme Star Wars / 4 Plus', 
        'Year 2020', 
        'Pieces / Minifigs 91 / 2', 
        'Availability Retired'
    ]

    result: dict = scraper.modify_info(input_info)

    assert result == {
        "theme": "4 Plus",
        "year": 2020,
        "availability": "Retired",
        "Pieces": 91,
        "Minifigs": 2
    }

@pytest.mark.modinfo
def test_modify_info_Minifigs():
    scraper: ScrapBrickEconomy = ScrapBrickEconomy([])

    input_info: List[str] = [
        'Theme / Subtheme Star Wars / 4 Plus', 
        'Year 2020', 
        'Minifigs 2', 
        'Availability Retired'
    ]

    result: dict = scraper.modify_info(input_info)

    assert result == {
        "theme": "4 Plus",
        "year": 2020,
        "availability": "Retired",
        "Minifigs": 2
    }

@pytest.mark.modinfo
def test_modify_info_Pieces():
    scraper: ScrapBrickEconomy = ScrapBrickEconomy([])

    input_info: List[str] = [
        'Theme / Subtheme Star Wars / 4 Plus', 
        'Year 2020', 
        'Pieces 91', 
        'Availability Retired'
    ]

    result: dict = scraper.modify_info(input_info)

    assert result == {
        "theme": "4 Plus",
        "year": 2020,
        "availability": "Retired",
        "Pieces": 91
    }

@pytest.mark.modinfo
def test_modify_info_empty():
    scraper: ScrapBrickEconomy = ScrapBrickEconomy([])

    input_info: List[str] = []

    with pytest.raises(ValidationError):
        scraper.modify_info(input_info)

@pytest.mark.modinfo
def test_modify_info_themefail():
    scraper: ScrapBrickEconomy = ScrapBrickEconomy([])


    input_info: List[str] = [
        'empty', 
        'Year 2020', 
        'Pieces 91', 
        'Availability Retired'
    ]

    with pytest.raises(ValidationError):
        scraper.modify_info(input_info)

@pytest.mark.modinfo
def test_modify_info_availabilityfail():
    scraper: ScrapBrickEconomy = ScrapBrickEconomy([])


    input_info: List[str] = [
        'Theme / Subtheme Star Wars / 4 Plus', 
        'Year 2020', 
        'Pieces 91', 
        'av Retired'
    ]

    with pytest.raises(ValidationError):
        scraper.modify_info(input_info)

@pytest.mark.modinfo
def test_modify_info_YEARfail():
    scraper: ScrapBrickEconomy = ScrapBrickEconomy([])


    input_info: List[str] = [
        'Theme / Subtheme Star Wars / 4 Plus', 
        'YR 2020', 
        'Pieces 91', 
        'Availability Retired'
    ]

    with pytest.raises(ValidationError):
        scraper.modify_info(input_info)

@pytest.mark.modprice
def test_modify_prices_promotional():
    scraper = ScrapBrickEconomy([])

    prices_ls = [
        "promo",
        "Value $1,234.56"
    ]

    result = scraper.modify_prices(prices_ls)

    assert result == {
        "Retail": "Promotional",
        "Value": 1234.56
    }

@pytest.mark.modprice
def test_modify_prices_not_yet_released():
    scraper = ScrapBrickEconomy([])

    prices_ls = [
        "Retail $49.99",
        "Not yet released"
    ]

    result = scraper.modify_prices(prices_ls)

    assert result == {
        "Retail": 49.99,
        "Value": "Not yet released"
    }

@pytest.mark.modprice
def test_modify_prices_empty_retail():
    scraper = ScrapBrickEconomy([])

    prices_ls = [
        "",
        "Value $199.00"
    ]

    result = scraper.modify_prices(prices_ls)

    assert result == {
        "Retail": "Promotional or Unknown",
        "Value": 199.00
    }

@pytest.mark.modprice
def test_modify_prices_availability_value():
    scraper = ScrapBrickEconomy([])

    prices_ls = [
        "Retail $59.99",
        "Available"
    ]

    result = scraper.modify_prices(prices_ls)

    assert result == {
        "Retail": 59.99,
        "Value": "Available"
    }

@pytest.mark.modprice
def test_modify_prices_standard_case():
    scraper = ScrapBrickEconomy([])

    prices_ls = [
        "Retail $89.95",
        "Value $149.99"
    ]

    result = scraper.modify_prices(prices_ls)

    assert result == {
        "Retail": 89.95,
        "Value": 149.99
    }