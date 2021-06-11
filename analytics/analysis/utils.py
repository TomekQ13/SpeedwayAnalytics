from pandas import DataFrame
import json
from functools import wraps

class ObjectNotFittedException(Exception):
    pass

def require_fit(func):
    def inner_func(self, *args, **kwargs):      
        try:
            a = self.col_cats
        except AttributeError:
            raise ObjectNotFittedException('Object is not fitted.')
            
        func(self, *args, **kwargs)

    return inner_func

class BinaryEncoder:
    
    def fit(self, data:DataFrame, columns:list):
        self.col_cats = {}
        for column in columns:
            self.col_cats[column] = data[column].unique().tolist()

    @require_fit
    def transform(self, data:DataFrame, delete_original:bool=True):
        for column in self.col_cats.keys():
            for value in self.col_cats[column]:
                col_name = (column + '_' + str(value))
                chars_to_replace = [(' ', '_')]
                for char in chars_to_replace:
                    col_name = col_name.replace(char[0], char[1])
                data[col_name] = (data[column] == str(value)).astype(int)
            if delete_original:
                data.drop(columns=[column], inplace=True)
        return data

    def fit_transform(self, data:DataFrame, columns:list, delete_original:bool=True):
        self.fit(data, columns)
        self.transform(data, delete_original)
        return data

    @require_fit
    def save(self, filename:str):
        ''' Method to save the encoder. Filename must be txt'''
        if not self.col_cats:
            raise ObjectNotFittedException('Object is not fitted.')

        with open(filename, 'w') as f:
            json.dump(self.col_cats, f)

    def load(self, filename):
        self.col_cats = json.load(filename)