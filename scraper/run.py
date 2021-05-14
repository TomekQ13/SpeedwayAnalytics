from scraper.scrape import Scraper

scraper = Scraper()
years = [str(x) for x in range(2007, 2021)]
try:
    for year in years:
        scraper.scrape_year(f'https://speedwayekstraliga.pl/terminarz-i-wyniki/?y={year}')
        scraper.log(f'Finished year {year}')
finally:
    scraper.close()