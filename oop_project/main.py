from BE_scraper import ScrapBrickEconomy

tabs = ['4-plus', 'ahsoka', 'andor', 'battlefront', 'book-parts', 'boost', 'buildable-figures',
          'comiccon', 'diorama-collection', 'employee-gift', 'episode-i', 'episode-ii', 'episode-iii',
          'episode-iv', 'episode-v', 'episode-vi', 'exclusive-minifigs', 'galaxys-edge', 'helmet-collection',
          'jedi-fallen-order', 'legends', 'master-builder-series', 'mechs', 'microfighters', 'miscellaneous',
          'original-content', 'planet-set', 'promotional', 'rebels', 'rebuild-the-galaxy', 'resistance', 
          'rogue-one', 'seasonal', 'skeleton-crew', 'solo', 'starship-collection', 'technic', 'the-bad-batch',
          'the-book-of-boba-fett', 'the-clone-wars', 'the-force-awakens', 'the-last-jedi', 'the-mandalorian',
          'the-old-republic', 'the-rise-of-skywalker', 'ultimate-collector-series', 'value-packs', 'young-jedi-adventures']

def main():
    obj = ScrapBrickEconomy(tabs)
    
    try:
        data = obj.scrape()
        obj.write_json(data)        
    finally:
        obj.close()

if __name__ == '__main__':
    main()

