# Analiza Rynku LEGO Star Wars & Scraper

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Selenium](https://img.shields.io/badge/Selenium-Web_Scraping-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![AGH](https://img.shields.io/badge/AGH-Advanced_Python-brown)

To repozytorium zawiera zestaw narzędzi do pobierania (scrapowania), przetwarzania i analizy danych rynkowych zestawów **LEGO Star Wars** z serwisu [BrickEconomy](https://www.brickeconomy.com/). Projekt obejmuje własny scraper (w wersji funkcyjnej oraz obiektowej), pipeline czyszczenia danych oraz interaktywny dashboard w Streamlit.

> **Kontekst:** Projekt został zrealizowany w ramach przedmiotu **Zaawansowane Programowanie w Pythonie** na kierunku Informatyka i Ekonometria (Studia Magisterskie) na **AGH w Krakowie**.

---

## Zespół Projektowy

Projekt został zrealizowany przez 4-osobowy zespół z podziałem na kluczowe moduły systemu:

### Maciej Laburda – Core Scraping & Logic
**Rola:** Stworzenie podstawowego mechanizmu pobierania danych (podejście funkcyjne) oraz logiki sterującej procesem scrapowania.
* **Kluczowe pliki:** `be_scraper_lib.py` (podejście funkcyjne), `main.py` (logika sterująca)
* **Zadania:**
    * Konfiguracja środowiska **Selenium** i sterowników przeglądarki.
    * Implementacja funkcji `fetch_soup` do parsowania HTML przez **BeautifulSoup**.
    * Logika nawigacji po podstronach (subthemes) i zarządzanie zapisem surowych danych.

### Bartosz Sermak – Refaktoryzacja OOP & Testy
**Rola:** Refactoryzacja kodu poprzez wprowadzenie programowania obiektowego, modularyzację oraz testy (QA).
* **Kluczowe pliki:** `brick_scraper.py`, `base_scraper.py`, `exceptions.py`, `utils.py`, `test_brick_scraper.py`
* **Zadania:**
    * Refaktoryzacja monolitycznego kodu do postaci modułowej i klasowej (`BrickEconomyScraper` dziedziczące po `BaseScraper`).
    * Wydzielenie logiki pomocniczej (`utils.py`) i obsługi błędów (`exceptions.py`).
    * Implementacja walidacji i metod czyszczących dane wejściowe.
    * Przygotowanie testów jednostkowych w **pytest** (mockowanie WebDrivera, testy parsowania).

### Jakub Koperdowski – Data Engineering & Cleaning
**Rola:** Transformacja surowych danych JSON do formatu analitycznego oraz czyszczenie zbioru danych (ETL).
* **Kluczowe pliki:** `create_df.ipynb`, `clean_BE_df.parquet`
* **Zadania:**
    * Implementacja klasy `LoadJson` do efektywnego wczytywania danych.
    * Czyszczenie danych: konwersja walut, typów danych, obsługa braków i niespójności.
    * Eksport do formatów `.parquet` i `.xlsx` na potrzeby analizy.

### Grzegorz Stańczyk – Data Analysis & Visualization
**Rola:** Warstwa prezentacji danych, analiza eksploracyjna (EDA) oraz budowa interaktywnego dashboardu.
* **Kluczowe pliki:** `streamlit_app.py`, `create_charts.ipynb`
* **Zadania:**
    * Stworzenie aplikacji webowej w **Streamlit** z interaktywnymi filtrami (wiek zestawu, liczba elementów, minifigurki, cena).
    * Opracowanie wizualizacji (**Seaborn**, **Matplotlib**): analiza wartości rynkowej w czasie, rozkład liczby minifigurek, liczebność premier w poszczególnych latach oraz dostępność w sklepach (Amazon, eBay, etc.).
    * Przeprowadzenie wstępnej analizy statystycznej (EDA) (korelacje, wykresy gęstości zmiennych).

---

## Struktura Plików

### 1. Pobieranie Danych (Scraping - Refactored OOP)
* **`main.py`**: Punkt startowy aplikacji. Uruchamia proces scrapowania dla zdefiniowanych kategorii.
* **`base_scraper.py`**: Klasa bazowa obsługująca instancję Selenium WebDriver.
* **`brick_scraper.py`**: Główna logika biznesowa scrapowania serwisu BrickEconomy.
* **`utils.py`**: Funkcje pomocnicze (np. parsowanie walut, zapis do pliku).
* **`exceptions.py`**: Definicje własnych wyjątków (np. `ValidationError`).
* **`BE_scraper.py`**: (Legacy) Pierwotna implementacja funkcyjna.

### 2. Przetwarzanie Danych
* **`create_df.ipynb`**: Notebook Jupyter do czyszczenia danych i konwersji JSON -> Parquet/Excel.
* **`clean_BE_df.parquet` / `clean_BE_df.xlsx`**: Gotowe zbiory danych.
* **`scraped_brickeconomy_final.json`**: Przykładowy zrzut surowych danych.

### 3. Analiza i Aplikacja
* **`streamlit_app.py`**: Kod źródłowy dashboardu analitycznego.
* **`create_charts.ipynb`**: Notebook z analizą eksploracyjną (EDA).
