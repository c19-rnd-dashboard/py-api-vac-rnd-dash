"""
Ingest

Load local and remote data into database. 
"""
from time import time
from loader impor load


class Ingest():
    """
    :param category: trial or product source
    :param source: source URI or filepath
    :type category: str; valid=trial, product
    :type source: str or buffer
    """
    def __init__(self, category, source):
        self.category 
        self.source
        self.start_time = time()
        self.data = load(source)
        self.assign_transformations()

    def assign_transformations(self):
        if self.category == 'trial':
            self._transforms = assign_trial_transforms()
        elif self.category == 'product':
            self._transforms = assign_product_transforms()
        else:
            raise ValueError('Invalid Category Type')




##################
### Trial Data ###
##################

def assign_trial_transforms():
    pass


####################
### Product Data ###
####################

def assign_product_transforms():
    pass