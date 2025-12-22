import pytest
from unittest.mock import MagicMock, patch
from typing import List

from brick_scraper import BrickEconomyScraper
from exceptions import ValidationError

@pytest.fixture
def scraper():
    with patch('base_scraper.webdriver.Chrome') as mock_driver:
        scraper_instance = BrickEconomyScraper([])
        return scraper_instance

def test_extract_details_full(scraper):
    """Testuje pełny zestaw danych: Pieces i Minifigs."""
    input_info: List[str] = [
        'Theme / Subtheme Star Wars / 4 Plus',
        'Year 2020',
        'Pieces / Minifigs 91 / 2',
        'Availability Retired'
    ]

    result = scraper._extract_set_details(input_info)

    assert result == {
        "theme": "4 Plus",
        "year": 2020,
        "availability": "Retired",
        "Pieces": 91,
        "Minifigs": 2
    }

def test_extract_details_only_minifigs(scraper):
    """Testuje zestaw tylko z minifigurkami (bez liczby elementów - rzadki przypadek, ale możliwy)."""
    input_info: List[str] = [
        'Theme / Subtheme Star Wars / 4 Plus',
        'Year 2020',
        'Minifigs 2',
        'Availability Retired'
    ]

    result = scraper._extract_set_details(input_info)

    assert result['theme'] == "4 Plus"
    assert result['Minifigs'] == 2
    assert 'Pieces' not in result

def test_extract_details_only_pieces(scraper):
    """Testuje zestaw tylko z liczbą elementów."""
    input_info: List[str] = [
        'Theme / Subtheme Star Wars / 4 Plus',
        'Year 2020',
        'Pieces 91',
        'Availability Retired'
    ]

    result = scraper._extract_set_details(input_info)

    assert result['Pieces'] == 91
    assert 'Minifigs' not in result

def test_extract_details_validation_error_empty(scraper):
    """Testuje pustą listę wejściową."""
    input_info: List[str] = []

    with pytest.raises(ValidationError):
        scraper._extract_set_details(input_info)

def test_extract_details_validation_error_theme(scraper):
    """Testuje brak pola Theme."""
    input_info: List[str] = [
        'Just Some Text',
        'Year 2020',
        'Pieces 91',
        'Availability Retired'
    ]

    with pytest.raises(ValidationError) as excinfo:
        scraper._extract_set_details(input_info)
    assert "Theme" in str(excinfo.value)

def test_extract_details_validation_error_year(scraper):
    """Testuje brak pola Year."""
    input_info: List[str] = [
        'Theme / Star Wars',
        'No Date Here',
        'Pieces 91',
        'Availability Retired'
    ]

    with pytest.raises(ValidationError) as excinfo:
        scraper._extract_set_details(input_info)
    assert "Year" in str(excinfo.value)

# --- Testy parsowania cen (_extract_prices) ---

def test_extract_prices_standard(scraper):
    """Testuje standardowy przypadek: Retail i Value są liczbami."""
    prices_ls = [
        "Retail $89.95",
        "Value $149.99"
    ]

    result = scraper._extract_prices(prices_ls)

    assert result == {
        "Retail": 89.95,
        "Value": 149.99
    }

def test_extract_prices_promotional(scraper):
    """Testuje zestaw promocyjny (brak ceny detalicznej)."""
    prices_ls = [
        "promo",
        "Value $1,234.56"
    ]

    result = scraper._extract_prices(prices_ls)

    assert result["Retail"] == "Promotional or Unknown"
    assert result["Value"] == 1234.56

def test_extract_prices_not_yet_released(scraper):
    """Testuje zestaw jeszcze niewydany."""
    prices_ls = [
        "Retail $49.99",
        "Not yet released"
    ]

    result = scraper._extract_prices(prices_ls)

    assert result["Retail"] == 49.99
    assert result["Value"] == "Not yet released"

def test_extract_prices_available_retail(scraper):
    """Testuje zestaw dostępny w sklepie (Value = Available)."""
    prices_ls = [
        "Retail $59.99",
        "Available at retail"
    ]

    result = scraper._extract_prices(prices_ls)

    assert result["Retail"] == 59.99
    # Logika w kodzie sprawdzała startswith('A')
    assert "Available" in result["Value"]

def test_extract_prices_empty_retail(scraper):
    """Testuje brak ceny retail (pusty string)."""
    prices_ls = [
        "",
        "Value $199.00"
    ]

    result = scraper._extract_prices(prices_ls)

    assert result["Retail"] == "Promotional or Unknown"
    assert result["Value"] == 199.00