from datetime import datetime

from be_scraper_lib import scrape_tabs, write_json


def main() -> None:
    # Przykładowe podstrony (subthemes)
    tabs = [
        "the-mandalorian",
        "the-clone-wars",
    ]

    data = scrape_tabs(tabs)

    # Nazwa pliku z datą (żeby nie nadpisywać)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"scraped_brickeconomy_{stamp}.json"

    write_json(data, file_name)
    print(f"Saved: {file_name}")


if __name__ == "__main__":
    main()
