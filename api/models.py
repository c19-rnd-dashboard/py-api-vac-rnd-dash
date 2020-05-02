"""
Models to store Vaccine & Trial Data

Setup Notes:
https://docs.sqlalchemy.org/en/13/orm/tutorial.html

On relationship with Base/Inheritance
https://docs.sqlalchemy.org/en/13/orm/inheritance.html#joined-table-inheritance
"""

from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()

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
from sqlalchemy.orm import relationship


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
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
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
    code = Column(String)


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
    current_status = Column(String)
    phase = Column(String)
    condition_or_disease = Column(String)
    product_type = Column(String)
    trial_id = Column(String)
    num_sites = Column(String)
    site_locations = Column(Text)
    sources = Column(String)


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

    trial_id = Column(String, primary_key=True, nullable=False, default=id_default)
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

    productmilestones = relationship('ProductMilestone', back_populates='milestone')

class ProductMilestone(Base):
    __tablename__ = "productmilestone"
    _class_name = 'ProductMilestone'

    link_id = Column(Integer, primary_key=True)
    milestone_id = Column(Integer, ForeignKey("milestone.milestone_id"))
    product_id = Column(Integer, nullable=False)
    date_start = Column(DateTime, nullable=True)
    milestone_status = Column(String, nullable=True)

    milestone = relationship('Milestone', back_populates='productmilestones')


class Sponsor(Base):
    __tablename__ = 'sponsor'
    _class_name = 'Sponsor'

    sponsor_id = Column(String, primary_key=True)
    sponsor_name = Column(String)

    products = relationship('ProductSponsor', back_populates='sponsor')


class ProductSponsor(Base):
    __tablename__ = 'productsponsor'
    _class_name = 'ProductSponsor'

    link_id = Column(Integer, primary_key=True)
    sponsor_id = Column(String, ForeignKey('sponsor.sponsor_id'))
    product_id = Column(Integer)

    sponsor = relationship('Sponsor', back_populates='products')




#######################
### Adv Data Models ###
#######################

"""
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
    name = Column(String)
    link = Column(String)


class ProductSource(Product):
    __tablename__ = 'productsource'

    link_id = Column(Integer, primary_key=True) 
    source_id = Column(Integer, ForeignKey('source.source_id'))
    product_id = Column(Integer, ForeignKey('product.product_id'))


class TrialSource(Trial):
    __tablename__ = 'trialsource'

    link_id = Column(Integer, primary_key=True) 
    source_id = Column(Integer, ForeignKey('source.source_id'))
    trial_id = Column(String, ForeignKey('trial.trial_id'))


class Intervention(Base):
    __tablename__ = 'intervention'
    
    intervention_id = Column(Integer, primary_key=True)
    intervention_type = Column(String)
    description = Column(Text)


class ProductIntervention(Product):
    __tablename__ = 'productintervention'

    link_id = Column(Integer, primary_key=True) 
    intervention_id = Column(Integer, ForeignKey('intervention.intervention_id'))
    product_id = Column(Integer, ForeignKey('product.product_id'))
    description = Column(Text)


class TrialIntervention(Trial):
    __tablename__ = 'trialintervention'

    link_id = Column(Integer, primary_key=True) 
    intervention_id = Column(Integer, ForeignKey('intervention.intervention_id'))
    trial_id = Column(String, ForeignKey('trial.trial_id'))
    description = Column(Text)


class Sponsor(Base):
    __tablename__ = 'sponsor'

    sponsor_id = Column(Integer, primary_key=True)
    full_name = Column(String)
    short_name = Column(String)
    link = Column(String)


class ProductSponsor(Product):
    __tablename__ = 'productsponsor'

    link_id = Column(Integer, primary_key=True) 
    sponsor_id = Column(Integer, ForeignKey('sponsor.sponsor_id'))
    product_id = Column(Integer, ForeignKey('product.product_id'))


class TrialSponsor(Trial):
    __tablename__ = 'trialsponsor'

    link_id = Column(Integer, primary_key=True) 
    sponsor_id = Column(Integer, ForeignKey('sponsor.sponsor_id'))
    trial_id = Column(String, ForeignKey('trial.trial_id'))


class Funding(Base):
    __tablename__ = 'funding'

    funding_id = Column(Integer, primary_key=True)
    name = Column(String)
    link = Column(String)


class ProductFunding(Product):
    __tablename__ = 'productfunding'

    link_id = Column(Integer, primary_key=True) 
    funding_id = Column(Integer, ForeignKey('funding.funding_id'))
    product_id = Column(Integer, ForeignKey('product.product_id'))


class TrialFunding(Trial):
    __tablename__ = 'trialfunding'

    link_id = Column(Integer, primary_key=True) 
    funding_id = Column(Integer, ForeignKey('funding.funding_id'))
    trial_id = Column(String, ForeignKey('trial.trial_id'))


class ProductCountry(Product):
    __tablename__ = 'productcountry'

    link_id = Column(Integer, primary_key=True) 
    country_name = Column(String, ForeignKey('country.country_name'))
    product_id = Column(Integer, ForeignKey('product.product_id'))


class TrialCountry(Trial):
    __tablename__ = 'trialcountry'

    link_id = Column(Integer, primary_key=True) 
    country_name = Column(String, ForeignKey('country.country_name'))
    trial_id = Column(String, ForeignKey('trial.trial_id'))


class Milestone(Base):
    __tablename__ = 'milestone'

    milestone_id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)


class ProductMilestone(Product):
    __tablename__ = 'productmilestone'

    link_id = Column(Integer, primary_key=True) 
    milestone_id = Column(Integer, ForeignKey('milestone.milestone_id'))
    product_id = Column(Integer, ForeignKey('product.product_id'))


class TrialMilestone(Trial):
    __tablename__ = 'trialmilestone'

    link_id = Column(Integer, primary_key=True) 
    milestone_id = Column(Integer, ForeignKey('milestone.milestone_id'))
    trial_id = Column(String, ForeignKey('trial.trial_id'))
"""
