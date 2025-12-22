import json
from datetime import datetime


def parse_currency(price_str: str) -> float:
    """Konwertuje string z ceną (np. '$1,234.56') na float."""
    # Usuwamy 'Retail ', 'Value ' i inne prefiksy, bierzemy drugą część
    parts = price_str.split(' ')
    if len(parts) < 2:
        return 0.0

    raw_price = parts[1]

    # Usuwamy znak dolara i przecinki
    clean_price = raw_price.replace('$', '').replace(',', '')

    try:
        return float(clean_price)
    except ValueError:
        return 0.0


def save_to_json(data: list, filename_prefix: str = 'scraped_brickeconomy') -> None:
    """Zapisuje dane do pliku JSON z sygnaturą czasową."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{filename_prefix}_{timestamp}.json"

    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

    print(f"Dane zapisano do pliku: {file_name}")