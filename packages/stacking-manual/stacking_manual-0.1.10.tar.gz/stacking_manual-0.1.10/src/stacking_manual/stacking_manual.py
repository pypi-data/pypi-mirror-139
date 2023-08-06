import pandas as pd
from sklearn import dummy

class StackingManual:
    """
    use fit and predict method for manually stacked model (combining multiple models on user specified columns) 
    You manual assign which model to use based on one of the column values    
    """
   
    def fit(self, models_dict: dict, X:pd.DataFrame, y:pd.Series, split_col:str, fit_params:dict={}):
        """
        model_dict: dictionary of {key:value}, with key being an entry found in split_col and value being an sklearn style model
        X: dataframe used to train models
        y: series of targets
        split_col: string, name of column in X used to manually assign model 
        fit_params: optional, nested dictionary of {key:{key:value}}, with first key being entry found in split_col and value being a dict of params to pass to fit function
        """
        X_tmp = X.copy()
        X_tmp['target_col'] = y
        dfs = [X_tmp[X_tmp[split_col]==value] for value in X_tmp[split_col].unique()]
        self.models = {}
        
        for index, df in X_tmp.groupby(split_col, as_index=False):
            try:
                tmp_model = models_dict[index]
                if fit_params.get(index):
                    self.models[index] = tmp_model.fit(df.drop(columns=['target_col']), df['target_col'], **fit_params.get(index))
                else:
                    self.models[index] = tmp_model.fit(df.drop(columns=['target_col']), df['target_col'])
            except:
                self.models[index] = dummy.DummyClassifier().fit(df.drop(columns=['target_col']), df['target_col'])
        self.split_col = split_col
        
        return self.models
            
    def predict(self, X: pd.DataFrame) -> pd.Series:
        """
        X: datafame used to predict
        """
        output_list = []
        for index, df in X.groupby(self.split_col, as_index=False):
            df_tmp = df.copy()
            df_tmp['prd_target_col'] = self.models[index].predict(df)
            output_list = output_list + [df_tmp]
        output = pd.concat(output_list)
        output = output.loc[X.index, 'prd_target_col']
        return output