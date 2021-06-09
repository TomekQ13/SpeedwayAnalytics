from pandas import DataFrame

class BinaryEncoder:
    
    def fit(self, data:DataFrame, columns:list):
        self.col_cats = {}
        for column in columns:
            self.col_cats[column] = data[column].unique().tolist()
        
        
    def fit_transform(self, data:DataFrame, columns:list):
        self.fit(data, columns)
    
        pass

    def save(self):
        pass

    def load():
        pass