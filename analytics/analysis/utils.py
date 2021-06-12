from pandas import DataFrame
import json
from functools import wraps

class ObjectNotFittedException(Exception):
    pass

def require_fit(func, check):
    def inner_func(self, *args, **kwargs):      
        try:
            getattr(self, check)
        except AttributeError:
            raise ObjectNotFittedException('Object is not fitted.')
            
        func(self, *args, **kwargs)

    return inner_func

class BinaryEncoder:
    
    def fit(self, data:DataFrame, columns:list):
        self.col_cats = {}
        for column in columns:
            self.col_cats[column] = data[column].unique().tolist()

    @require_fit('col_cats')
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

    @require_fit('col_cats')
    def save(self, filename:str):
        '''Method to save the encoder. Filename must be txt'''
        if not self.col_cats:
            raise ObjectNotFittedException('Object is not fitted.')

        with open(filename, 'w') as f:
            f = json.dump(self.col_cats, f)

    def load(self, filename):
        '''Method to load the encoder.'''
        with open(filename) as f:
            self.col_cats = json.load(f)

class CityExtractor:
    def __init__(self):
        self.columns_fitted = ['name_team_home', 'name_team_away']
        self.cities_fitted = ['Bydgoszcz', 'Rzeszów', 'Wrocław', 'Leszno', 'Toruń',
         'Częstochowa', 'Tarnów', 'Gorzów', 'Zielona Góra', 'Rybnik', 'Ostrów', 'Lublin', 'Grudziądz', 'Gdańsk', 'Gniezno']

    def transform(self, data, columns=None, cities=None):
        if not columns:
            self.colums_fitted = columns
        if not cities:
            self.cities_fitted = cities

        for column in self.colums_fitted:
            for city in self.cities_fitted:
                data.loc[data[column].str.contains(city), column] = city
        return data

    @require_fit('columns')
    def save(self, filename):
        '''Method to save the CityExtractor.'''
        dict_to_save = {
            'cities': self.cities_fitted,
            'columns': self.colums_fitted
        }
        with open(filename, 'w') as f:
            f = json.dump(self.col_cats, f)

    def load(self, filename):
        '''Method to load the CityExtractor.'''
        with open(filename) as f:
            load_dict = json.load(f)

        self.colums_fitted = load_dict['columns']
        self.cities_fitted = load_dict['cities']