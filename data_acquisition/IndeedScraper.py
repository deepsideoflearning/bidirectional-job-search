from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
from bs4 import BeautifulSoup
import os
import shutil
import csv

base_url = 'https://www.indeed.com'
driver_path = '/home/kyle/Downloads/chromedriver'


class IndeedScraper:

    def __init__(self, job_title, key_words, location='', starting_page=1, radius='Exact location only'):
        """
        Args:
             job_title: string, title used when searching for jobs on indeed.com
             key_words: list of strings, key words that should be in the job titles to help remove ads
             location: string, location used when searching for jobs on indeed.com
             starting_page: int, page number which the user wants to start on
             radius: str, maximum distance in miles from given location that a job can be
                                the string 'Exact location only' is the default value,
                                and other values can only be 5, 10, 15, 25, 50, 100
        """

        self.job_title = job_title
        self.location = location
        self.page_number = starting_page
        self.key_words = key_words
        try:
            self.radius = int(radius)
        except ValueError:
            # Only executes if default value is given
            self.radius = radius

        try:
            self.driver = webdriver.Chrome(executable_path=driver_path)
            self.load_page(base_url)
        except WebDriverException:
            raise RuntimeError("Driver Unable to connect")

        # Starting at the correct page immediately
        if self.page_number > 1:
            # Formatting the title and url for the website
            self.load_page()

    def search_jobs(self):

        # Finding text fields to enter job title and location
        what = self.driver.find_element_by_id('text-input-what')
        where = self.driver.find_element_by_id('text-input-where')

        # Clearing any entries that might be there
        what.send_keys(Keys.CONTROL, 'a', Keys.DELETE)
        where.send_keys(Keys.CONTROL, 'a', Keys.DELETE)

        # Entering in given data
        what.send_keys(self.job_title)
        where.send_keys(self.location)

        # Clicking the search button
        find_jobs_button = self.driver.find_element_by_class_name('icl-Button--primary')
        find_jobs_button.click()

        self.driver.minimize_window()

        # Setting the radius to the given distance
        if self.location:
            select_radius = Select(self.driver.find_element_by_id('distance_selector'))
            if type(self.radius) == int:
                select_radius.select_by_visible_text(f'within {self.radius} miles')
            elif type(self.radius) == str:
                select_radius.select_by_visible_text(self.radius)

    def next_page(self):
        # Attempts to call the next page
        try:
            # Ensuring this is the correct page
            current_url = self.driver.current_url
            if current_url not in base_url+self.get_url():
                self.load_page()

            # Following the next_button link
            next_button = self.driver.find_element_by_link_text('Next »')
            next_html = next_button.get_attribute('outerHTML')
            soup = BeautifulSoup(next_html, 'html.parser')
            next_url = soup.a['href']
            self.load_page(base_url+next_url)
            return True
        except NoSuchElementException:
            return False

    def get_data(self):
        # Restarting the driver periodically ensures the browser doesn't crash
        if self.page_number % 10 == 0:
            self.restart_driver()

        links = self.driver.find_elements_by_class_name('title')
        page_data = []

        for i, link in enumerate(links):
            posting_data = {}

            # I need to do this round about method because utilizing
            # click() will crash the webdriver due to a bug while clicking
            # on any hyperlinked text
            try:
                links = self.driver.find_elements_by_class_name('title')
                # If the list is empty, there was an issue getting back to the postings page
                if not links:
                    self.load_page()
                    links = self.driver.find_elements_by_class_name('title')
            except WebDriverException:
                # Only happens when the driver has crashed and needs to be restarted
                self.restart_driver()
                links = self.driver.find_elements_by_class_name('title')

            try:
                soup = BeautifulSoup(links[i].get_attribute('outerHTML'), 'html.parser')
            except IndexError:
                continue

            posting_title = soup.text.rstrip().lstrip().lower()
            # Moving onto the next link if the title doesn't contain an appropriate key word
            if all(key_word not in posting_title for key_word in self.key_words):
                continue
                
            # Saving Title data
            posting_data['Title'] = posting_title

            url = soup.a['href']
            # Saving url data
            posting_data['Url'] = base_url + url
            
            # Loading the job posting
            self.load_page(base_url+url)

            if base_url not in self.driver.current_url:
                # If this executes, the driver has left indeed due to following some recommended
                # job postings. This also indicates the end of the page, so I can just return
                # all of the data collected
                self.page_number += 1
                self.driver.execute_script("window.history.go(-1)")
                return page_data

            # Getting the rest of the data from each Job posting
            posting_soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            try:
                posting_data['Description'] = posting_soup.find('div', {'id': 'jobDescriptionText'}).text
            except AttributeError:
                # Going back to the main page
                self.driver.execute_script("window.history.go(-1)")
                continue

            # Due to inconsistent formatting, this is the only spot where the company
            # name is reliably kept on the postings. The company name might not be
            # relevant, but it could give insight like company size later on
            try:
                company_location = (
                    posting_soup.find('div', {'class': 'jobsearch-InlineCompanyRating'})
                                .text
                                .split('-')
                )
            except AttributeError:
                # Going back to the main page
                self.driver.execute_script("window.history.go(-1)")
                continue

            # If there wasn't a '-' in this location, only the location was specified
            if len(company_location) > 1:
                # The company needs more cleaning than the location due to reviews possibly existing
                company = company_location[0]
                if 'reviews' in company:
                    company = company.replace('reviews', '')
                company = company.rstrip('0123456789.,- ')
                posting_data['Company'] = company

                posting_data['Location'] = company_location[1]
            else:
                posting_data['Location'] = company_location[0]
                posting_data['Company'] = None

            # Going back to the main page
            self.driver.execute_script("window.history.go(-1)")

            page_data.append(posting_data)
            del posting_data

        self.page_number += 1

        return page_data

    def restart_driver(self):
        # Attempting to close an already open window
        try:
            self.close()
        except WebDriverException:
            # The window has already closed due to some other reason, so I can move on
            pass

        self.driver = webdriver.Chrome(executable_path=driver_path)
        self.driver.minimize_window()
        self.load_page()

    def get_url(self):
        """Creates the url for the indeed website from the class attributes
        Returns:
            url: string, the formatted url for the website
        """
        # Formatting the title and url for the website
        f_title = self.job_title.replace(' ', '+')
        f_location = self.location.replace(' ', '+')
        f_location = f_location.replace(',', '%2C')
        f_page_number = (self.page_number - 1) * 10
        f_radius = self.radius
        if type(self.radius) == str:
            f_radius = 0

        if self.location:
            url = f'/jobs?q={f_title}&l={f_location}&' \
                f'radius={f_radius}&start={f_page_number}'
        else:
            url = f'/jobs?q={f_title}&radius={self.radius}&' \
                f'start={f_page_number}'

        return url

    def close(self):
        self.driver.close()

    def load_page(self, url='default'):
        """Loads the page of the given url
        Args:
            url: string, url which needs to be loaded. If no url is given, then the url
                        will be created from the class attributes and base_url
        """
        if url == 'default':
            url = base_url + self.get_url()
        count = 0
        # Loads page, but if it fails, then it will try again
        while count < 10:
            try:
                self.driver.refresh()
                self.driver.get(url)
                return
            except TimeoutException:
                pass
            count += 1

        self.restart_driver()


if __name__ == '__main__':
    starting_page = 19
    key_words = ['scientist', 'research', 'engineer', 'analyst', 'data']
    s = IndeedScraper('Data Scientist', key_words=key_words, starting_page=starting_page, location='Chicago')

    count = starting_page

    # A starting page greater than 1 assumes data has already
    # been collected for previous pages
    if starting_page <= 1:
        s.search_jobs()
        # Removing the directory if it exists
        try:
            shutil.rmtree('./raw_data')
        except FileNotFoundError:
            pass

        os.mkdir('./raw_data')

    while True:
        data = s.get_data()
        try:
            keys = data[0].keys()
        except IndexError:
            # If this error occurs, the page was full of ads and
            # no data is returned and we move onto the next page
            res = s.next_page()
            if not res:
                break

            print(f'No data on page {count}')
            count += 1

            continue

        with open('./raw_data/job_postings.csv', 'a') as file:
            dict_writer = csv.DictWriter(file, keys)
            if count == 1:
                dict_writer.writeheader()
            dict_writer.writerows(data)

        del data

        print(f'Finished with page {count}')
        count += 1

        res = s.next_page()

        if not res:
            break

    # I don't need the scraper anymore
    s.close()

