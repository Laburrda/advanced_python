from brick_scraper import BrickEconomyScraper
from utils import save_to_json

tabs = ['4-plus', 'ahsoka', 'andor', 'battlefront', 'book-parts', 'boost', 'buildable-figures',
          'comiccon', 'diorama-collection', 'employee-gift', 'episode-i', 'episode-ii', 'episode-iii',
          'episode-iv', 'episode-v', 'episode-vi', 'exclusive-minifigs', 'galaxys-edge', 'helmet-collection',
          'jedi-fallen-order', 'legends', 'master-builder-series', 'mechs', 'microfighters', 'miscellaneous',
          'original-content', 'planet-set', 'promotional', 'rebels', 'rebuild-the-galaxy', 'resistance', 
          'rogue-one', 'seasonal', 'skeleton-crew', 'solo', 'starship-collection', 'technic', 'the-bad-batch',
          'the-book-of-boba-fett', 'the-clone-wars', 'the-force-awakens', 'the-last-jedi', 'the-mandalorian',
          'the-old-republic', 'the-rise-of-skywalker', 'ultimate-collector-series', 'value-packs', 'young-jedi-adventures']


def main():
    print("Starting scraper...")
    scraper = BrickEconomyScraper(tabs)

    try:
        data = scraper.run()
        save_to_json(data)
    except KeyboardInterrupt:
        print("\nScraping interrupted by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        scraper.close()
        print("Driver closed.")


if __name__ == '__main__':
    main()