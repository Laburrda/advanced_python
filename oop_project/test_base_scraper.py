import pytest
from base_scraper import BaseScraper


def test_open_and_close_browser():
    """Sprawdza, czy scraper w ogóle się uruchamia i zamyka bez błędu."""
    scraper = BaseScraper(headless=True)

    assert scraper.driver is not None

    scraper.close()


def test_get_soup_real_website():
    """Pobiera prawdziwą stronę (example.com) i sprawdza tytuł."""
    scraper = BaseScraper(headless=True)

    try:
        soup = scraper.get_soup("https://example.com", wait_time=1)

        title = soup.find("h1").text
        assert title == "Example Domain"

    finally:
        scraper.close()