from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BaseScraper:
    def __init__(self, headless: bool = False) -> None:
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")

        if headless:
            options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=options)

    def get_soup(self, url: str, wait_time: int = 5) -> BeautifulSoup:
        """Pobiera stronę i zwraca obiekt BeautifulSoup."""
        self.driver.get(url)
        sleep(wait_time)
        html = self.driver.page_source
        return BeautifulSoup(html, "html.parser")

    def close(self):
        """Zamyka przeglądarkę."""
        self.driver.quit()