"""
Models to store Vaccine & Trial Data

Setup Notes:
https://docs.sqlalchemy.org/en/13/orm/tutorial.html
"""

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy import \
    (Column, Integer, String, ForeignKey, DateTime, Float, Text,
        Boolean, UniqueConstraint, ForeignKeyConstraint)
from sqlalchemy.orm import relationship


###################
### Data Models ###
###################

class Product(Base):
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True)
    preferred_name = Column(String)
    chemical_name = Column(String)
    brand_name = Column(String)
    repurposed = Column(Boolean)
    notes = Column(Text)

class Source(Base):
    __tablename__ = 'source'

    source_id = Column(Integer, primary_key=True)
    name = Column(String)
    link = Column(String)

    product_id = Column(Integer, ForeignKey('product.product_id'))