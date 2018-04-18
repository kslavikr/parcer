from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa
from typing import Optional


Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'
    id = sa.Column(sa.Integer, primary_key=True)
    product_id = sa.Column(sa.String(100), nullable=False)
    checked_at = sa.Column(sa.DateTime, nullable=True)

    def __init__(self, product_id: str, checked_at: Optional[sa.DateTime]):
        self.product_id = product_id
        self.checked_at = checked_at


class Review(Base):
    __tablename__ = 'review'
    id = sa.Column(sa.Integer, primary_key=True)
    product = sa.Column(sa.Integer, nullable=True)
    domain = sa.Column(sa.String(100), nullable=False)
    review_id = sa.Column(sa.String(100), nullable=False)
    rating = sa.Column(sa.Integer, nullable=True)

    def __init__(self,
                 product: str,
                 domain: str,
                 review_id: str,
                 rating: int):
        self.product = product
        self.domain = domain
        self.review_id = review_id
        self.rating = rating


def get_db_engine(db_path: str = 'sqlite:///{}/review_db.db3'.format(Path(__file__).parent)):
    return sa.create_engine(db_path)


def get_db_session(engine: Engine = get_db_engine()):
    session_maker = sessionmaker(bind=engine)
    return session_maker()
