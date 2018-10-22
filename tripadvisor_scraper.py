'''
    A script to scrape restaurant reviews from tripadvisor.com or tripadvisor.com using Selenium.

    Author:     Ryan Buchmeier <rwbleo@gmail.com>
    License:    MIT

    Installation:
        - Install `selenium` and `pandas` using pip
        - Install PhantomJS or get Chrome- or Firefox webdriver binaries and add them to your PATH (see http://selenium-python.readthedocs.io/installation.html#drivers)

    Usage as library:
        ```
            from tripadvisor_scraper import TripadvisorScraper
            scraper = TripadvisorScraper(engine='chrome')
            reviews = scraper.fetch_reviews('<some_url_here>', 10)
            scraper.close()
        ```

    Command-line usage:
        $ python3 tripadvisor_scraper.py -e chrome -n 10 -o my_reviews.csv https://www.tripadvisor.com/Restaurant_Review-g187289-d7595215-Reviews-Dom_Grill_Kitchen_Bar-Karlsruhe_Baden_Wurttemberg.html
'''

import argparse
import datetime
import locale
import logging
import re
import sys
import time

import pandas as pd
from selenium import webdriver
from selenium.common import exceptions

URL_PATTERN = 'http(s)?:\/\/.?(www\.)?tripadvisor\.com\/Restaurant_Review.*' #TODO: Fix

class Review():
    def __init__(self, id, date, title, user, text, language):
        self.id = id
        self.date = date
        self.title = title
        self.user = user
        self.text = text
        self.language = language


class TripadvisorScraper():
    def __init__(self, engine='chrome'):
        self.locale_backup = locale.getlocale()[0]
        self.lookup = {}

        if engine == 'chrome':
            self.driver = webdriver.Chrome()
        elif engine == 'firefox':
            self.driver = webdriver.Firefox()
        elif engine == 'phantomjs':
            self.driver = webdriver.PhantomJS()
        else:
            logging.warning('Engine {} not supported. Defaulting to PhantomJS.'.format(engine))
            self.driver = webdriver.PhantomJS()

        self.i18n = {
            'more_btn': 'More',
            'date_format': '%B %d, %Y'
        }

    def _parse_page(self, language):
        reviews = []
        try:
            self.driver.find_element_by_xpath('//span[contains(., "{}") and @class="taLnk ulBlueLinks"]'.format(self.i18n['more_btn'])).click()
        except:
            pass

        time.sleep(2)  # TODO

        review_elements = self.driver.find_elements_by_class_name('reviewSelector')
        for e in review_elements:
            try:
                id = e.get_attribute('id')
                date = e.find_element_by_class_name('ratingDate').get_attribute('title')
                date = datetime.datetime.strptime(date, self.i18n['date_format'])
                title = e.find_element_by_class_name('quote').find_element_by_tag_name('a').find_element_by_class_name('noQuotes').text
                try:
                    user = e.find_element_by_class_name('memberOverlayLink').get_attribute('id')
                    user = user[4:user.index('-')]
                except:
                    user = None
                text = e.find_element_by_class_name('partial_entry').text.replace('\n', '')

                if id in self.lookup:
                    logging.warning('Fetched review {} twice.'.format(r.id))
                else:
                    self.lookup[id] = True
                    reviews.append(Review(id, date, title, user, text, language))
            except:
                logging.warning('Couldn\'t fetch review.') #TODO: This could be any error. Could be a false negative.
                pass

        return reviews


    def get_languages(self):
        try:
            self.driver.find_element_by_xpath("//div[@class='prw_rup prw_filters_detail_language ui_column separated is-3']//div[@class='taLnk']").click()
            lans = self.driver.find_elements_by_xpath("//div[@class='more-options']/*")
        except exceptions.NoSuchElementException as e:
            lans = self.driver.find_elements_by_xpath("//div[@class='prw_rup prw_filters_detail_language ui_column separated is-3']//div[@class='choices is-shown-at-tablet']/*")
            # self.driver.find_element_by_link_text('More languages').click()

        # Below line worked at one point I think? Doesn't as of last testing (Sept 6, 2018)
        # lans = self.driver.find_elements_by_xpath("//ul[@class='langs']/*")
        # lans = [lan for lan in lans if lan.find_element_by_class_name('filterLabel').text != '']
        # lans_text = [lan.find_element_by_class_name('filterLabel').text for lan in lans]
        # lans_input = [lan.find_element_by_class_name('toggle').find_element_by_class_name('filterInput') for lan in lans]
        lan_text = [l.get_attribute("data-tracker") for l in lans]
        lans = [lan.find_element_by_class_name('label') for lan in lans]
        lans[0].click() #TODO: Find a better way to close the modal/popup
        time.sleep(2)
        return lan_text

    def click_language_at_index(self, index):
        self.driver.execute_script("window.scrollTo(0,0)") #Always run this at beginning of page
        try:
            self.driver.find_element_by_xpath("//div[@class='prw_rup prw_filters_detail_language ui_column separated is-3']//div[@class='taLnk']").click()
            lans = self.driver.find_elements_by_xpath("//div[@class='more-options']/*")
        except exceptions.NoSuchElementException as e:
            lans = self.driver.find_elements_by_xpath("//div[@class='prw_rup prw_filters_detail_language ui_column separated is-3']//div[@class='choices is-shown-at-tablet']/*")
            # self.driver.find_element_by_link_text('More languages').click()

        # Below line worked at one point I think? Doesn't as of last testing (Sept 6, 2018)
        # lans = self.driver.find_elements_by_xpath("//ul[@class='langs']/*")
        # lans = [lan for lan in lans if lan.find_element_by_class_name('filterLabel').text != '']
        # lans_text = [lan.find_element_by_class_name('filterLabel').text for lan in lans]
        # lans_input = [lan.find_element_by_class_name('toggle').find_element_by_class_name('filterInput') for lan in lans]
        lans = [lan.find_element_by_class_name('label') for lan in lans]
        lans[index].click()

    def fetch_reviews(self, url, max_reviews=None, as_dataframe=True):
        self.lookup = {}
        reviews = []
        if not max_reviews: max_reviews = sys.maxsize
        locale.setlocale(locale.LC_TIME, 'en_US')

        #TODO: Fix
        # if not is_valid_url(url): return logging.warning('Tripadvisor URL not valid.')
        self.driver.get(url)

        time.sleep(2)  # TODO

        languages = self.get_languages()

        for i, language in enumerate(languages):
            if i == 0:
                continue
            self.click_language_at_index(i)
            while len(reviews) < max_reviews:
                reviews += self._parse_page(language)
                logging.info('Fetched a total of {} reviews by now.'.format(len(reviews)))
                next_button_container = self.driver.find_element_by_class_name('next')
                if 'disabled' in next_button_container.get_attribute('class'):
                    break
                next_button_container.click()

            locale.setlocale(locale.LC_TIME, self.locale_backup)
            reviews = reviews[:max_reviews]
        if as_dataframe:
            return pd.DataFrame.from_records([r.__dict__ for r in reviews]).set_index('id', drop=True)
        return reviews

    def close(self):
        self.driver.quit()

def is_valid_url(url): #TODO: Fix
    return re.compile(URL_PATTERN).match(url)

def get_id_by_url(url): #TODO: Fix
    if not is_valid_url(url): return None
    match = re.compile('.*Restaurant_Review-g\d+-(d\d+).*').match(url)
    if match is None: return None
    return match.group(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape restaurant reviews from tripadvisor.com')
    parser.add_argument('url', help='URL to a Tripadvisor restaurant page')
    parser.add_argument('-o', '--out', dest='outfile', help='Path for output CSV file', default='reviews.csv')
    parser.add_argument('-n', dest='max', help='Maximum number of reviews to fetch', default=sys.maxsize, type=int)
    parser.add_argument('-e', '--engine', dest='engine', help='Driver to use', choices=['phantomjs', 'chrome', 'firefox'], default='chrome')
    args = parser.parse_args()

    scraper = TripadvisorScraper(engine=args.engine)
    df = scraper.fetch_reviews(args.url, args.max)
    print('Successfully fetched {} reviews.'.format(len(df.index)))
    import os
    file_exists = not os.path.isfile(args.outfile)
    df.to_csv(args.outfile, mode='a', header=file_exists)
    scraper.close()

