from lxml import html
import requests
import re
import datetime
from dateutil import parser as dateparser
from math import ceil
from typing import NamedTuple, Generator
import random
from time import sleep

from grabber.config import *


class ReviewInfo(NamedTuple):
    review_id: str
    header: str
    text: str
    posted_date: datetime.datetime
    rating: float
    comment_count: int
    purchase_verified: bool
    is_vine: bool
    author: str


class ResourceUrlHandler:

    def get_product_url(self, asin: str, domain: str) -> str:
        main_page_url_pattern = self._get_url_pattern(domain, 'main')
        return main_page_url_pattern.format(domain, asin)

    @staticmethod
    def _get_url_pattern(domain: str, page_type: str) -> str:
        # todo: add pattern storing to db
        if page_type == 'main':
            return ResourceUrlPatterns.PRODUCT_PAGE
        if page_type == 'review':
            return ResourceUrlPatterns.REVIEW_PAGE

    def get_review_urls(self, asin: str, domain: str, review_total: int) -> Generator:
        review_url_pattern = self._get_url_pattern(domain, 'review')
        for page_number in range(int(ceil(review_total/REVIEW_PER_PAGE))):
            yield review_url_pattern.format(domain, asin, REVIEW_PER_PAGE, page_number + 1)


class BaseResourceParser:

    def __init__(self):
        self.user_agent = self._get_user_agent()

    @staticmethod
    def _get_user_agent():
        return random.choice(USER_AGENT_LIST)

    def get_product_general_info(self, page_url: str):
        page_content = self._get_page_content(page_url)
        product_price = ''.join(page_content.xpath(XPATH_PRODUCT_PRICE)).replace(',', '')
        product_name = ''.join(page_content.xpath(XPATH_PRODUCT_NAME)).strip()
        total_ratings = page_content.xpath(XPATH_AGGREGATE_RATING)
        review_count_total = int(page_content.xpath(XPATH_REVIEW_COUNT)[0].replace(',', ''))
        return {'ratings': self._format_total_rating(total_ratings),
                'review_count': review_count_total,
                'price': product_price,
                'name': product_name}

    def get_product_reviews(self, review_urls: Generator):
        review_list = []
        for page_url in review_urls:
            sleep(3)
            page_content = self._get_page_content(page_url)
            reviews = page_content.xpath(XPATH_REVIEW_SECTION)
            for review in reviews:
                review_list.append(self._get_review_info(review))
        return review_list

    # @staticmethod
    def _get_review_info(self, review):
        # print('id', self._get_review_id(review))
        # print('header', self._get_review_header(review))
        # print('text', self._get_review_text(review))
        # print('date', self._get_review_date(review))
        # print('rating', self._get_review_rating(review))
        # print('comment', self._get_review_comment(review))
        # print('purchase', self._is_purchase_verified(review))
        # print('vine', self._is_vine(review))
        # print('author', self._get_review_author(review))
        return ReviewInfo(review_id=self._get_review_id(review),
                          header=self._get_review_header(review),
                          text=self._get_review_text(review),
                          posted_date=self._get_review_date(review),
                          rating=self._get_review_rating(review),
                          comment_count=self._get_review_comment(review),
                          purchase_verified=self._is_purchase_verified(review),
                          is_vine=self._is_vine(review),
                          author=self._get_review_author(review))

    @staticmethod
    def _get_review_author(review):
        return ''.join(review.xpath(XPATH_AUTHOR_NAME))

    @staticmethod
    def _get_review_id(review):
        return review.attrib['id']

    @staticmethod
    def _get_review_header(review):
        return ''.join(review.xpath(XPATH_REVIEW_HEADER))

    @staticmethod
    def _get_review_rating(review):
        return int(''.join(review.xpath(XPATH_RATING)).strip()[0])

    @staticmethod
    def _get_review_text(review):
        return ''.join(review.xpath(XPATH_REVIEW_TEXT))

    @staticmethod
    def _get_review_date(review):
        try:
            review_date = dateparser.parse(''.join(review.xpath(XPATH_REVIEW_POSTED_DATE))).strftime('%d %b %Y')
        except:
            review_date = None
        return review_date

    @staticmethod
    def _get_review_comment(review):
        try:
            review_comments = int(re.sub('[A-Za-z]', '', ''.join(review.xpath(XPATH_REVIEW_COMMENTS))).strip())
        except:
            review_comments = None
        return review_comments

    @staticmethod
    def _is_purchase_verified(review):
        try:
            verified = bool(review.xpath(XPATH_PURCHASE))
        except:
            verified = None
        return verified

    @staticmethod
    def _is_vine(review):
        raw_badges_row_text = review.xpath(XPATH_BADGES_ROW)
        vine_text = vine_review
        return vine_text in raw_badges_row_text

    # def _get_author_rating(self, domain: str, page_url: str):
    #     full_page_url = 'https://{}{}'.format(domain, page_url)
    #     page_content = self._get_page_content(full_page_url)

    def _get_page_content(self, page_url: str):
        headers = {'User-Agent': self.user_agent}
        page = requests.get(page_url, headers=headers, verify=False)
        return html.fromstring(page.text)

    @staticmethod
    def _format_total_rating(total_ratings: list):
        rating_dict = {}
        for ratings in total_ratings:
            extracted_rating = ratings.xpath(XPATH_SINGLE_RATING)
            if extracted_rating:
                rating_key = extracted_rating[0]
                raw_raing_value = extracted_rating[1]
                rating_value = raw_raing_value
                if rating_key:
                    rating_dict.update({rating_key: rating_value})
        return rating_dict


class JapanResourceParser(BaseResourceParser):

    DOMAIN = 'Resource.co.jp'

    @staticmethod
    def _get_review_date(review):
        try:
            review_date = re.findall(r"[\d']+", ''.join(review.xpath(XPATH_REVIEW_POSTED_DATE)))
            review_date.reverse()
            review_date = ' '.join(review_date)
            review_date = dateparser.parse(review_date).strftime('%d %b %Y')
        except:
            review_date = None
        return review_date


class DeutschlandResourceParser(BaseResourceParser):

    DOMAIN = 'Resource.de'

    @staticmethod
    def _get_review_date(review):
        try:
            review_date = ''.join(review.xpath(XPATH_REVIEW_POSTED_DATE))
            review_date = re.search(r"(\w{2} )(\d{1,2})(\.* )(\w*)( )(\d{4})", review_date).groups()[1::2]
            review_date = ' '.join(review_date)
        except:
            review_date = None
        return review_date


class MexicaResourceParser(BaseResourceParser):

    DOMAIN = 'Resource.com.mx'

    @staticmethod
    def _get_review_date(review):
        try:
            review_date = ''.join(review.xpath(XPATH_REVIEW_POSTED_DATE))
            review_date = re.search(r"(\w{2} )(\d{1,2})( de )(\w*)( de )(\d{4})", review_date).groups()[1::2]
            review_date = ' '.join(review_date)
        except:
            review_date = None
        return review_date


class ChanaResourceParser(JapanResourceParser, BaseResourceParser):

    DOMAIN = 'Resource.cn'


class FranceResourceParser(DeutschlandResourceParser, BaseResourceParser):

    DOMAIN = 'Resource.fr'


class ItaliResourceParser(DeutschlandResourceParser, BaseResourceParser):

    DOMAIN = 'Resource.it'


class NiderlandResourceParser(DeutschlandResourceParser, BaseResourceParser):

    DOMAIN = 'Resource.nl'


class BrazilResourceParser(MexicaResourceParser, BaseResourceParser):

    DOMAIN = 'Resource.com.br'
