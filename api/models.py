"""
Models to store Vaccine & Trial Data

Setup Notes:
https://docs.sqlalchemy.org/en/13/orm/tutorial.html

On relationship with Base/Inheritance
https://docs.sqlalchemy.org/en/13/orm/inheritance.html#joined-table-inheritance
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


class Trial(Base):
    __tablename__ = 'trial'

    trial_id = Column(String, primary_key=True)
    title = Column(String)
    registry = Column(String)
    registration_date = Column(DateTime)
    start_date = Column(DateTime)
    recruitment_status = Column(String)


class Source(Base):
    __tablename__ = 'source'

    source_id = Column(Integer, primary_key=True)
    link = Column(String)


class ProductSource(Product):
    __tablename__ = 'productsource'

    source_id = Column(Integer, ForeignKey('source.source_id'))
    product_id = Column(Integer, ForeignKey('product.product_id'))


class Intervention(Base):
    __tablename__ = 'intervention'
    
    intervention_id = Column(Integer, primary_key=True)
    intervention_type = Column(String)
    description = Column(Text)


class ProductIntervention(Product):
    __tablename__ = 'productintervention'

    intervention_id = Column(Integer, ForeignKey('intervention.intervention_id'))
    product_id = Column(Integer, ForeignKey('product.product_id'))
    notes = Column(Text)


class TrialIntervention(Trial):
    __tablename__ = 'trialintervention'

    intervention_id = Column(Integer, ForeignKey('intervention.intervention_id'))
    trial_id = Column(String, ForeignKey('trial.trial_id'))
    notes = Column(Text)


class Sponsor(Base):
    __tablename__ = 'sponsor'

    sponsor_id = Column(Integer, primary_key=True)
    full_name = Column(String)
    short_name = Column(String)
    link = Column(String)


class ProductSponsor(Product):
    __tablename__ = 'productsponsor'

    sponsor_id = Column(Integer, ForeignKey('sponsor.sponsor_id'))
    product_id = Column(Integer, ForeignKey('product.product_id'))


class TrialSponsor(Trial):
    __tablename__ = 'trialsponsor'

    sponsor_id = Column(Integer, ForeignKey('sponsor.sponsor_id'))
    trial_id = Column(String, ForeignKey('trial.trial_id'))


class Funding(Base):
    __tablename__ = 'funding'

    funding_id = Column(Integer, primary_key=True)
    name = Column(String)
    link = Column(String)


class ProductFunding(Product):
    __tablename__ = 'productfunding'

    funding_id = Column(Integer, ForeignKey('funding.funding_id'))
    product_id = Column(Integer, ForeignKey('product.product_id'))


class TrialFunding(Trial):
    __tablename__ = 'trialfunding'

    funding_id = Column(Integer, ForeignKey('funding.funding_id'))
    trial_id = Column(String, ForeignKey('trial.trial_id'))


class Country(Base):
    __tablename__ = 'country'

    country_name = Column(String, primary_key=True)


class ProductCountry(Product):
    __tablename__ = 'productcountry'

    country_name = Column(String, ForeignKey('country.country_name'))
    product_id = Column(Integer, ForeignKey('product.product_id'))


class TrialCountry(Trial):
    __tablename__ = 'trialcountry'

    country_name = Column(String, ForeignKey('country.country_name'))
    trial_id = Column(String, ForeignKey('trial.trial_id'))


class Milestone(Base):
    __tablename__ = 'milestone'

    milestone_id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)


class ProductMilestone(Product):
    __tablename__ = 'productmilestone'

    milestone_id = Column(Integer, ForeignKey('milestone.milestone_id'))
    product_id = Column(Integer, ForeignKey('product.product_id'))


class TrialMilestone(Trial):
    __tablename__ = 'trialmilestone'

    milestone_id = Column(Integer, ForeignKey('milestone.milestone_id'))
    trial_id = Column(String, ForeignKey('trial.trial_id'))