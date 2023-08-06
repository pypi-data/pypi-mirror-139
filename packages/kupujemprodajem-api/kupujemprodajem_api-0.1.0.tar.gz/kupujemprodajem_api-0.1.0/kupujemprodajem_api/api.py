import json
import lxml
import os
import requests

from bs4 import BeautifulSoup
from requests.compat import quote_plus
from requests.compat import urljoin

from .models import Advertisment

from .exceptions import LoginError


class KupujemprodajemAPI:
    def __init__(self, email, password):
        self.session = requests.Session()
        self.session.headers.update({
            'X-Prototype-Version': '1.7',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Kp-Signature': 'c8da3299e366aff6c51aeea2dc5a443c7c88046a'})
        self.main_url = 'https://www.kupujemprodajem.com'
        self.category_information = None
        self.subcategory_information = None

        self.choosen_category_id = None
        self.choosen_subcategory_id = None

        self.email = email
        self.password = password

    @property
    def is_logged(self):
        # TODO: This method needs to be extended
        # Add exensive checks to verify that user is logged. 
        return self._is_logged()

    def login(self):
        login_path = '/api/web/v1/auth/login'
        login_url = urljoin(self.main_url, login_path)
        data = {'email': self.email, 'password': self.password}

        self.session.post(login_url, data=data)
        if not self.is_logged:
            raise LoginError

    def info(self):
        pass

    def upvotes(self):
        info_path = '/review.php?action=list&data[page]=1&data[ad_kind]=all&data[user_type]=all&data[rate]=positive'
        info_url = urljoin(self.main_url, info_path)

        r = self.session.get(info_url)
        html = BeautifulSoup(r.text, 'lxml')

        votes_positive = html.find_all('span', {'class': 'reviews-thumbs__thumb-number'})[0].text

        return votes_positive

    def downvotes(self):
        info_path = '/review.php?action=list&data[page]=1&data[ad_kind]=all&data[user_type]=all&data[rate]=negative'
        info_url = urljoin(self.main_url, info_path)

        r = self.session.get(info_url)
        html = BeautifulSoup(r.text, 'lxml')

        votes_negative = html.find_all('span', {'class': 'reviews-thumbs__thumb-number'})[1].text

        return votes_negative

    def post_ad(self, Ad):

        # tries to get request data, if data not valid then returns None
        ad_data = Ad.get_data()



    # utils

    def _get_category_information(self):
        category_path = '/ajax_functions.php?action=get_categories&data[active]=yes'
        category_url = urljoin(self.main_url, category_path)

        data = self.session.get(category_url)

        category_information = json.loads(data)

        '''Create a dictionary with Key (id) : Value (Category Name)

        Since we have to use ID-s instead of category names, we create a dictionary
        with key-values matches of id-s and category names.

        Returns:
            Key-Value matches with id:category_name
                dict
        '''
        self.category_information = category_information
        return category_information

    def _get_subcategory_information(self, category):
        '''Create a dictionary with Key (id) : Value (Category Name)

        Since we have to use ID-s instead of subcategory names, we create a dictionary
        with key-values matches of id-s and subcategory names.

        Important difference is that we need a category id as an input, because each category
        has many different subcategories.

        Returns:
                Key-Value matches with id:subcategory_name
                        dict
        '''
        return subcategory_information

    def _is_working(self):
        '''Check does site work

        checks if site is works with status code or similar
        by using checking status codes of the requests and other 
        techniques, to see if our requests are blocked by a security system

        returns: True - if works, False if it doesn't work
        '''

    def _is_logged(self):
        '''Check if user is logged in

        By visiting certain restricted pages that are only available
        to people that are logged in their account and by checking if
        we are blocked we verify if we are logged in or not.

        Returns:
                        If Logged in: True , if not: raise LoginError
                        bool or LoginError
        '''

        welcome_path = '/user.php?action=welcome'
        welcome_url = urljoin(self.main_url, welcome_path)
        r = self.session.get(welcome_url)

        if r.url == welcome_url:
            return True

        raise LoginError

    @staticmethod
    def search():
        pass
        # return results