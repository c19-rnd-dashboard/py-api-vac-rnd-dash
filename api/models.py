"""
Models to store Vaccine & Trial Data

Setup Notes:
https://docs.sqlalchemy.org/en/13/orm/tutorial.html

On relationship with Base/Inheritance
https://docs.sqlalchemy.org/en/13/orm/inheritance.html#joined-table-inheritance
"""

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Float,
    Text,
    Boolean,
    UniqueConstraint,
    ForeignKeyConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()


### Helper Functions ##

def to_dict(inst, cls):
    """
    Convert the sql alchemy query result to a clean python dictionary.
    """
    convert = dict()
    # add your coversions for things like datetime's
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(
                    convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return d

#######################
### New Data Models ###
#######################


class Country(Base):
    __tablename__ = 'country'
    _class_name = 'Country'

    name = Column(String, primary_key=True)
    alpha2 = Column(String)
    alpha3 = Column(String)


class ProductRaw(Base):
    __tablename__ = "productraw"
    _class_name = 'ProductRaw'

    product_id = Column(Integer, primary_key=True)
    preferred_name = Column(String)
    chemical_name = Column(String)
    brand_name = Column(String)
    intervention_type = Column(String)
    indication = Column(String)
    molecule_type = Column(String)
    therapeutic_approach = Column(String)
    repurposed = Column(String)
    countries = Column(Text)
    country_codes = Column(Text)
    other_partners = Column(Text)
    notes = Column(Text)
    status = Column(String)
    current_stage = Column(String)
    phase = Column(String)
    accepts_healthy_subjects = Column(String)
    condition_or_disease = Column(String)
    trial_id = Column(String)
    num_sites = Column(String)
    sources = Column(String)
    study_start_date = Column(DateTime, nullable=True)
    primary_completion_date = Column(DateTime, nullable=True)
    study_completion_date = Column(DateTime, nullable=True)

    @property
    def json(self):
        return to_dict(self, self.__class__)


class TrialRaw(Base):
    __tablename__ = "trialraw"
    _class_name = 'TrialRaw'

    @staticmethod
    def id_default(context):
        new_id = hash(context.get_current_parameters()["title"])
        # print(new_id)  # DEBUG
        return new_id

    trial_id = Column(String, primary_key=True,
                      nullable=False, default=id_default)
    preferred_name = Column(String)
    title = Column(String)
    registry = Column(String)
    registration_date = Column(DateTime)
    enrollment_date = Column(DateTime)
    start_date = Column(DateTime)
    study_type = Column(String)
    phase = Column(String)
    recruitment_status = Column(String)
    target_enrollment = Column(String)
    intervention_type = Column(String)
    intervention = Column(Text)
    sponsors = Column(Text)
    countries = Column(Text)
    country_codes = Column(Text)
    data_reference = Column(String)
    data_source = Column(String)
    results_link = Column(String)
    inferred_product = Column(String)

    def to_json(self):
        return {
            "trial_id": self.trial_id,
            "title": self.title,
            "registry": self.registry,
            "registration_date": self.registration_date,
            "enrollment_date": self.enrollment_date,
            "start_date": self.start_date,
            "recruitment_status": self.recruitment_status,
            "intervention_type": self.intervention_type,
            "intervention": self.intervention,
            "sponsors": self.sponsors,
            "countries": self.countries,
            "country_codes": self.country_codes,
            "data_reference": self.data_reference,
            "data_source": self.data_source,
            "results_link": self.results_link,
            "phase_num": self.get_phase_num(self.phase),
            "phase": self.phase,
        }

    def get_phase_num(self, phase):
        nums = [int(i) for i in phase if i.isdigit()]
        if len(nums) == 0:
            if "applicable" in phase:
                return None
            else:
                return 0
        else:
            return max(nums)


class Milestone(Base):
    __tablename__ = "milestone"
    _class_name = 'Milestone'

    milestone_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String)

    productmilestones = relationship(
        'ProductMilestone', back_populates='milestone')


class ProductMilestone(Base):
    __tablename__ = "productmilestone"
    _class_name = 'ProductMilestone'

    link_id = Column(Integer, primary_key=True)
    milestone_id = Column(Integer, ForeignKey("milestone.milestone_id"))
    product_id = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=True)
    status = Column(String, nullable=True)

    milestone = relationship('Milestone', back_populates='productmilestones')


class Sponsor(Base):
    __tablename__ = 'sponsor'
    _class_name = 'Sponsor'

    sponsor_id = Column(String, primary_key=True)
    sponsor_name = Column(String)

    products = relationship('ProductSponsor', back_populates='sponsor')

    @property
    def json(self):
        return to_dict(self, self.__class__)


class ProductSponsor(Base):
    __tablename__ = 'productsponsor'
    _class_name = 'ProductSponsor'

    link_id = Column(Integer, primary_key=True)
    sponsor_id = Column(String, ForeignKey('sponsor.sponsor_id'))
    product_id = Column(Integer)

    sponsor = relationship('Sponsor', back_populates='products')

    @property
    def json(self):
        return to_dict(self, self.__class__)


class SiteLocation(Base):
    __tablename__ = 'sitelocation'
    _class_name = 'SiteLocation'

    site_location_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)

    products = relationship('ProductSiteLocation', back_populates='sitelocation')

    @property
    def json(self):
        return to_dict(self, self.__class__)



class ProductSiteLocation(Base):
    __tablename__ = 'productsitelocation'
    _class_name = 'ProductSiteLocation'

    link_id = Column(Integer, primary_key=True)
    site_location_id = Column(String, ForeignKey('sitelocation.site_location_id'))
    product_id = Column(Integer)

    sitelocation = relationship('SiteLocation', back_populates='products')

    @property
    def json(self):
        return to_dict(self, self.__class__)
