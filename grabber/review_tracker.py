import sqlalchemy as sa
from sqlalchemy.orm import Session
from typing import Dict, List
from datetime import datetime
from collections import defaultdict
from grabber.graber import BaseResourceParser, ResourceUrlHandler, ReviewInfo
import copy

from db.db import Product, Review, get_db_session


class ResourceReviewTracker:

    def __init__(self, product_identity: str, domain_list: List[str],
                 rating_list: List[int]):
        self.product_identity = product_identity
        self.domain_list = domain_list
        self.rating_list = rating_list
        self.new_reviews_dict = {}
        self.review_dict = {}
        self._handler()

    def _handler(self):
        db_reviews = self._get_db_reviews()
        Resource_reviews = self._get_resource_reviews()
        self._compare_reviews(db_reviews, Resource_reviews)
        self._filter_with_rating()

    def _filter_with_rating(self):
        filtered_review_dict = {}
        for domain in self.new_reviews_dict.keys():
            for review in self.new_reviews_dict[domain]:
                if review.rating in self.rating_list:
                    filtered_review_list = filtered_review_dict.get(domain, [])
                    filtered_review_list.append(review)
                    filtered_review_dict[domain] = filtered_review_list
        self.review_dict = copy.deepcopy(filtered_review_dict)

    def _compare_reviews(self, db_reviews: Dict[str, Dict[str, int]],
                         Resource_reviews: Dict[str, List[ReviewInfo]]):
        for domain in Resource_reviews.keys():
            Resource_domain_reviews = Resource_reviews[domain]
            db_domain_reviews = db_reviews.get(domain)
            if db_domain_reviews is None:
                self.new_reviews_dict[domain] = Resource_domain_reviews
            else:
                for Resource_review in Resource_domain_reviews:
                    db_review_rating = \
                        db_domain_reviews.get(Resource_review.review_id)
                    if db_review_rating != Resource_review.rating:
                        review_list = self.new_reviews_dict.get(domain, [])
                        review_list.append(Resource_review)
                        self.new_reviews_dict[domain] = review_list

    def _get_resource_reviews(self):
        Resource_url_handler = ResourceUrlHandler()

        review_dict = {}
        for domain in self.domain_list:
            Resource_parcer = self._get_parcer(domain)()
            product_main_url = \
                Resource_url_handler.get_product_url(self.product_identity,
                                                   domain)
            review_count = \
                Resource_parcer.get_product_general_info(product_main_url)['review_count']
            review_urls = \
                Resource_url_handler.get_review_urls(self.product_identity, domain, review_count)
            review_list = Resource_parcer.get_product_reviews(review_urls)
            review_dict[domain] = review_list
        return review_dict

    @staticmethod
    def _get_parcer(domain):
        for subclass in BaseResourceParser.__subclasses__():
            if domain == subclass.DOMAIN:
                return subclass
        return BaseResourceParser


    def _get_db_reviews(self):
        session = get_db_session()
        review_obj_list = session.query(Review).filter(sa.and_(Review.product == self._get_product_db_id(),
                                                               Review.domain.in_(self.domain_list))).all()
        return self._transform_db_review(review_obj_list)

    @staticmethod
    def _transform_db_review(review_obj_list: List[Review]):
        review_dict = infinity_deep_dict()
        for review in review_obj_list:
            review_dict[review.domain][review.review_id] = review.rating
        return review_dict

    def _get_product_db_id(self):
        session = get_db_session()
        product_obj = session.query(Product).filter(Product.product_id == self.product_identity).one_or_none()
        if product_obj is not None:
            self.product_pk = product_obj.id
        else:
            self._create_product(session)
            product_obj = session.query(Product).filter(Product.product_id == self.product_identity).one_or_none()
            self.product_pk = product_obj.id
        return self.product_pk

    def _create_product(self, session: Session):
        session.add(Product(product_id=self.product_identity,
                            checked_at=None))
        session.commit()

    def save_new_review(self):
        session = get_db_session()
        for domain in self.new_reviews_dict:
            for review in self.new_reviews_dict[domain]:
                db_review = session.query(Review).filter(sa.and_(Review.domain == domain,
                                                                 Review.review_id == review.review_id,
                                                                 Review.product == self.product_pk)).one_or_none()
                if db_review is not None:
                    db_review.rating = review.rating
                else:
                    session.add(Review(product=self.product_pk,
                                       domain=domain,
                                       review_id=review.review_id,
                                       rating=review.rating))
        product = session.query(Product).filter(Product.id == self.product_pk).one()
        product.checked_at = datetime.now()
        session.commit()


def infinity_deep_dict():
    return defaultdict(infinity_deep_dict)
