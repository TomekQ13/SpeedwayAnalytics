from pandas import DataFrame
import json
from functools import wraps
from numpy import array, random, copy, where, argmax, max

class ObjectNotFittedException(Exception):
    pass

def require_fit(func):
    @wraps(func)
    def inner_func(self, *args, **kwargs):      
        try:
            getattr(self, '_fitted')
        except AttributeError:
            raise ObjectNotFittedException('Object is not fitted.')
            
        func(self, *args, **kwargs)

    return inner_func

class BinaryEncoder:
    
    def fit(self, data:DataFrame, columns:list):
        self.col_cats = {}
        for column in columns:
            self.col_cats[column] = data[column].unique().tolist()
        self._fitted = True

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

    def fit_transform(self, data:DataFrame, columns:list, delete_original:bool=True):
        self.fit(data, columns)
        self.transform(data, delete_original)

    @require_fit
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
        if columns:
            self.columns_fitted = columns
        if cities:
            self.cities_fitted = cities

        for column in self.columns_fitted:
            for city in self.cities_fitted:
                data.loc[data[column].str.contains(city), column] = city

        self._fitted = True        

    @require_fit
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

class ColDropper:
    def transform(self, data, columns):
        '''Wrapper around Pandas df.drop to unify pipeline processing'''
        data.drop(columns=columns, inplace=True)
        self.columns = columns
        self._fitted = True
        
    @require_fit
    def save(self, filename):
        '''Method to save the ColDropper.'''
        with open(filename, 'w') as f:
            f = json.dump(self.columns, f)

    def load(self, filename):
        '''Method to load the ColDropper.'''
        with open(filename) as f:
            self.columns = json.load(f)

class XYTrainTestSplitter:
    def transform(self, data:DataFrame, y_columns:list, seed=1234):
        '''Returns X_train, Y_train, X_test, Y_test in this order.'''

        random.seed(seed)
        data['splitter'] = random.random(size=len(data))

        Y = data.loc[:, y_columns + ['splitter']]
        X = data.loc[:, [x for x in data.columns if x not in y_columns]]

        Y_train = Y.loc[data['splitter'] < 0.75, :]
        Y_test = Y.loc[data['splitter'] >= 0.75, :]
        X_train = X.loc[data['splitter'] < 0.75, :]
        X_test = X.loc[data['splitter'] >= 0.75, :]

        Y_train.drop(columns=['splitter'], inplace=True)
        Y_test.drop(columns=['splitter'], inplace=True)
        X_train.drop(columns=['splitter'], inplace=True)
        X_test.drop(columns=['splitter'], inplace=True)

        return X_train, Y_train, X_test, Y_test

class PredictionTransformer:
    '''Transforms the prediction to points'''
    @staticmethod
    def transform(prediction_array):
        return_arr = copy(prediction_array)
        for arr in return_arr:
            sorted_arr = copy(arr)
            sorted_arr.sort()
            arr[where(arr == sorted_arr[3])] = 3
            arr[where(arr == sorted_arr[2])] = 2
            arr[where(arr == sorted_arr[1])] = 1
            arr[where(arr == sorted_arr[0])] = 0

        return_arr = return_arr.astype(int)

        return return_arr

    @staticmethod
    def transform_winner_only(prediction_array):
        prediction_array = where(prediction_array < 3, 0, prediction_array)
        return prediction_array
            

class Scorer:
    def score_heat(self, arr_pred:array, arr_Y_test:array):
        if (arr_pred == arr_Y_test).all():
            self.all_correct += 1
            self.winner_correct += 1
            return 'all correct'

        if argmax(arr_pred) == argmax(arr_Y_test) and max(arr_pred) == max(arr_Y_test) == 3:
            self.winner_correct +=1
            return 'winner correct'

        return 'incorrect'

    def score(self, pred, Y_test):
        if len(pred) != len(Y_test):
            raise Exception('Prediction and test matrix are of a different length.')
            
        self.all_correct = 0
        self.no_obs = len(pred)
        self.winner_correct = 0
        self.score_arr = []

        for heat in enumerate(pred):
            prediction = self.score_heat(heat[1], Y_test.iloc[heat[0], :].to_numpy().astype(int))
            self.score_arr.append(prediction)

        self.results = {
            'winner_correct_%': round(self.winner_correct/self.no_obs * 100, 4),
            'all_correct_%': round(self.all_correct/self.no_obs * 100, 4),
            'no_obs': self.no_obs,
            'winner_correct': self.winner_correct,
            'all_correct': self.all_correct
        }

        return self.results


            

    


        