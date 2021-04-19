import os
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from requests import post

from scraper.exceptions import ExpectedValueMissingException
from scraper.preprocess import rider_name

class Scraper:
    """Scrapes data about speedway matches"""
    def __init__(self, driver_path=None, log=True, api=True):
        if driver_path:
            self.path = driver_path
        else:
            self.path = Path(os.getcwd()) / 'chromedriver.exe'

        self.driver = webdriver.Chrome(self.path)
        self._log = log
        self._log_path = Path(os.getcwd())  / 'logs'
        self._api = api
        self._interface_api_url = os.environ.get('INTERFACE_API_URL')

        #init timestamp is used to access the log file with the same name each time the log method is called
        self._timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        
        

    def get(self, url):
        """Wrapper around selenium driver.get method. Takes an url as an argument"""
        self.driver.get(url)

    def close(self):
        """Wrapper around selenium driver.close method."""
        self.driver.close()

    def post_match(self, data):
        """Makes a POST request to API endpoint which adds a match to the database"""
        return post(self._interface_api_url + 'new_match', data)

    def post_heat(self, data):
        """Makes a POST request to API endpoint which adds a heat to the database"""
        return post(self._interface_api_url + 'new_heat', data)

    def log(self, text, filename='log', print=False):
        if self._log:                       
            final_filename =  self._timestamp + '_' + filename + '.txt'

            #the timestamp for the log line should be generated when the method is called
            timestamp_logfile = datetime.now().strftime('%H:%M:%S')

            with open(self._log_path / final_filename, 'a') as f:
                f.write(timestamp_logfile + ': ' + text + '\n')

            if print:
                print(timestamp_logfile + ': ' + text + '\n')
        

    def scrape_match_results(self, match_url):
        if not self.driver.current_url == match_url:
            self.driver.get(match_url)

        self.log(f'Started scraping match {match_url}')
        result_dict = {}
        result_dict['match_url'] = match_url

        #get the scores
        scores = self.driver.find_elements_by_class_name('match__header__score')
        if len(scores) != 2:
            raise ExpectedValueMissingException('The number of scraped scores is not equal to 2')
        else:
            result_dict['score_team_home'] = int(scores[0].text)
            self.log(f'home team score {scores[0].text}')
            result_dict['score_team_away'] = int(scores[1].text)
            self.log(f'away team score {scores[1].text}')

        #get team names
        names = self.driver.find_elements_by_class_name('match__header__points__col__header')
        if len(names) != 2:
            raise ExpectedValueMissingException('The number of scraped names is not equal to 2')
        else:
            home_team_name = names[0].text[0:names[0].text.find('\n')]
            result_dict['name_team_home'] = home_team_name
            self.log(f'home team name {home_team_name}')
            away_team_name = names[1].text[0:names[1].text.find('\n')]
            result_dict['name_team_away'] = away_team_name
            self.log(f'away team name {away_team_name}')

        #get match details
        match_info = self.driver.find_element_by_class_name('match__header__info').find_elements_by_tag_name('div')
        if len(match_info) != 4:
            raise ExpectedValueMissingException('The number of scraped match information is not equal to 4')
        else:
            result_dict['stadium'] = match_info[0].text
            result_dict['round'] = match_info[1].text
            result_dict['date'] = match_info[2].text[0:match_info[2].text.find(',')]
            result_dict['time'] = match_info[2].text[match_info[2].text.find(',') + 2:]

        # here needs to be an api call
        return result_dict
    
    def scrape_heat_results(self, match_url):
        if not self.driver.current_url == match_url:
            self.driver.get(match_url)
        
        self.log(f'Started scraping heats results for match {match_url}')
        results_list = []

        heats = self.driver.find_elements_by_class_name('match__heat')
        for heat in heats:            
            results_dict = {}

            #only heat number has to be selected - time and repeat heat are discarded
            match_heat_header = heat.find_element_by_class_name('match__heat__header').text
            results_dict['heat_number'] = int(match_heat_header[match_heat_header.find('BIEG') + 5:match_heat_header.find('BIEG') + 5 + 2])
            
            self.log(f"Heat number: {results_dict['heat_number']}")

            riders = heat.find_elements_by_tag_name('tr')

            property = riders[0].find_elements_by_tag_name('td')
            results_dict['a_rider'] = rider_name(property)
            self.log(f"A_rider: {results_dict['a_rider']}")
            results_dict['a_score'] = property[3].text
            self.log(f"A_score: {results_dict['a_score']}")
            
            property = riders[1].find_elements_by_tag_name('td')
            results_dict['b_rider'] = property[2].text
            self.log(f"B_rider: {results_dict['b_rider']}")
            results_dict['b_score'] = property[3].text
            self.log(f"B_score: {results_dict['b_score']}")
            
            property = riders[2].find_elements_by_tag_name('td')
            results_dict['c_rider'] = property[2].text
            self.log(f"C_rider: {results_dict['c_rider']}")
            results_dict['c_score'] = property[3].text
            self.log(f"C_score: {results_dict['c_score']}")
            
            property = riders[3].find_elements_by_tag_name('td')
            results_dict['d_rider'] = property[2].text
            self.log(f"D_rider: {results_dict['d_rider']}")
            results_dict['d_score'] = property[3].text
            self.log(f"D_score: {results_dict['d_score']}")


            results_list.append(results_dict)
            # here needs to be an api call
        
        return results_list 

    def prepare_matches_list(self, results_page):
        if not self.driver.current_url == results_page:
            self.driver.get(results_page)

        self.log(f'Starting to generate a list of the matches urls from url {results_page}')        
        matches = self.driver.find_elements_by_class_name('schedule-events__item')
        # here needs to be a check added for incomplete years in the future if this is a desired functionality
        return [match.find_element_by_tag_name('a').get_attribute('href') for match in matches]

    def scrape_year(self, year_results):
        for match in self.prepare_matches_list(year_results):
            self.scrape_match_results(match)
            self.scrape_heat_results(match)
            self.log(f'Scraping of match {match} finished.')




