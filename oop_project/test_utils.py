import pytest
from unittest.mock import patch, mock_open
from utils import parse_currency, save_to_json

def test_parse_currency_standard():
    """Testuje standardowy przypadek: Prefix Cena."""
    assert parse_currency("Retail $100.00") == 100.0
    assert parse_currency("Value $50.50") == 50.5


def test_parse_currency_with_comma():
    """Testuje ceny z przecinkami (tysiące)."""
    assert parse_currency("Value $1,234.56") == 1234.56
    assert parse_currency("Retail $1,000,000.00") == 1000000.0


def test_parse_currency_no_prefix_but_space():
    """
    Testuje przypadek, gdzie string zaczyna się od spacji.
    """
    assert parse_currency(" $50.00") == 50.0


def test_parse_currency_invalid_format_no_space():
    """
    Testuje przypadek, gdy nie ma spacji rozdzielającej.
    """
    assert parse_currency("$100.00") == 0.0
    assert parse_currency("100.00") == 0.0


def test_parse_currency_invalid_value_text():
    """Testuje przypadek, gdy po prefiksie nie ma liczby."""
    assert parse_currency("Retail N/A") == 0.0
    assert parse_currency("Value Unknown") == 0.0


def test_parse_currency_empty_string():
    """Testuje pusty string."""
    assert parse_currency("") == 0.0


def test_parse_currency_different_currency_symbol():
    """Testuje czy funkcja radzi sobie z innymi znakami."""
    assert parse_currency("Retail €100.00") == 0.0


@patch("utils.json.dump")
@patch("builtins.open", new_callable=mock_open)
@patch("utils.datetime")
def test_save_to_json_creates_file(mock_datetime, mock_file, mock_json_dump):
    """
    Testuje czy funkcja poprawnie tworzy nazwę pliku z datą i zapisuje dane.
    """
    # mockowanie daty
    mock_datetime.now.return_value.strftime.return_value = "20231201_120000"

    test_data = [{"id": 1, "name": "Lego X-Wing"}]
    prefix = "test_lego"

    # wywołanie funkcji
    save_to_json(test_data, prefix)

    # sprawdzenie czy plik został otwarty z dobrą nazwą
    expected_filename = "test_lego_20231201_120000.json"
    mock_file.assert_called_once_with(expected_filename, 'w', encoding='utf-8')

    # sprawdzenie czy json.dump został wywołany poprawnie
    mock_json_dump.assert_called_once()
    args, kwargs = mock_json_dump.call_args

    assert args[0] == test_data
    assert kwargs['indent'] == 4


@patch("utils.json.dump")
@patch("builtins.open", new_callable=mock_open)
def test_save_to_json_default_prefix(mock_file, mock_json_dump):
    """Testuje czy działa domyślny prefix."""
    data = []

    save_to_json(data)

    filename_arg = mock_file.call_args[0][0]
    assert filename_arg.startswith("scraped_brickeconomy_")