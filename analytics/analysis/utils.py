from pandas import DataFrame
import json
from functools import wraps

class ObjectNotFittedException(Exception):
    pass

def require_fit(func):
    def inner_func(obj, *args):        
        try:
            a = obj.col_cats
        except AttributeError:
            raise ObjectNotFittedException('Object is not fitted.')
            
        func(*args)

    return inner_func

class BinaryEncoder:
    
    def fit(self, data:DataFrame, columns:list):
        self.col_cats = {}
        for column in columns:
            self.col_cats[column] = data[column].unique().tolist()

    @require_fit
    def transform(self, data:DataFrame):

        pass

    def fit_transform(self, data:DataFrame, columns:list):
        self.fit(data, columns)
    
        pass



    @require_fit
    def save(self, filename:str):
        ''' Method to save the encoder. Filename must be txt'''
        if not self.col_cats:
            raise ObjectNotFittedException('Object is not fitted.')

        with open(filename, 'w') as f:
            json.dump(self.col_cats, f)

    def load(self, filename):
        self.col_cats = json.load(filename)