## Project Team

The project was delivered by a 4-person team, with the key system modules divided among its members.

**Maciej Laburda – Core Scraping & Logic**
Role: Built the core data-collection mechanism (functional approach) and the logic that controls the scraping process.

* Key files: `be_scraper_lib.py` (functional approach), `main.py` (control logic)
* Tasks:
   * Configured the Selenium environment and browser drivers.
   * Implemented the `fetch_soup` function for parsing HTML with BeautifulSoup.
   * Implemented navigation logic across subpages (subthemes) and management of raw-data storage.

**Bartosz Sermak – OOP Refactoring & Testing**
Role: Refactored the code using object-oriented programming, modularized it, and handled testing (QA).

* Key files: `brick_scraper.py`, `base_scraper.py`, `exceptions.py`, `utils.py`, `test_brick_scraper.py`
* Tasks:
   * Refactored the monolithic code into a modular, class-based structure (`BrickEconomyScraper` inheriting from `BaseScraper`).
   * Extracted helper logic (`utils.py`) and error handling (`exceptions.py`).
   * Implemented validation and input-cleaning methods.
   * Wrote unit tests in pytest (WebDriver mocking, parsing tests).

**Jakub Koperdowski – Data Engineering & Cleaning**
Role: Transformed raw JSON data into an analytical format and cleaned the dataset (ETL).

* Key files: `create_df.ipynb`, `clean_BE_df.parquet`
* Tasks:
   * Implemented the `LoadJson` class for efficient data loading.
   * Cleaned the data: currency and data-type conversion, handling of missing values and inconsistencies.
   * Exported to `.parquet` and `.xlsx` formats for analysis.

**Grzegorz Stańczyk – Data Analysis & Visualization**
Role: Data presentation layer, exploratory data analysis (EDA), and building the interactive dashboard.

* Key files: `streamlit_app.py`, `create_charts.ipynb`
* Tasks:
   * Built a Streamlit web application with interactive filters (set age, number of pieces, minifigures, price).
   * Developed visualizations (Seaborn, Matplotlib): market value over time, distribution of minifigure counts, number of releases per year, and availability in stores (Amazon, eBay, etc.).
   * Carried out a preliminary statistical analysis (EDA): correlations and density plots of variables.

## File Structure

### 1. Data Collection (Scraping – Refactored OOP)

* `main.py`: Application entry point. Runs the scraping process for the defined categories.
* `base_scraper.py`: Base class that manages the Selenium WebDriver instance.
* `brick_scraper.py`: Main business logic for scraping the BrickEconomy website.
* `utils.py`: Helper functions (e.g., currency parsing, saving to file).
* `exceptions.py`: Definitions of custom exceptions (e.g., `ValidationError`).
* `BE_scraper.py`: (Legacy) Original functional implementation.

### 2. Data Processing

* `create_df.ipynb`: Jupyter notebook for data cleaning and JSON -> Parquet/Excel conversion.
* `clean_BE_df.parquet` / `clean_BE_df.xlsx`: Ready-to-use datasets.
* `scraped_brickeconomy_final.json`: Sample dump of raw data.

### 3. Analysis and Application

* `streamlit_app.py`: Source code of the analytical dashboard.
* `create_charts.ipynb`: Notebook with the exploratory data analysis (EDA).
