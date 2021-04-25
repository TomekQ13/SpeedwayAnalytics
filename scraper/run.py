from scraper.scrape import Scraper

scraper = Scraper()
try:
    scraper.scrape_year('https://speedwayekstraliga.pl/terminarz-i-wyniki/?y=2020')
finally:
    scraper.close()