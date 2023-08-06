from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer 
from regression_model.config_base.core_test import config
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
import numpy as np

profit_pipe = Pipeline([
                        # ('dropping_columns',ColumnTransformer(remainder= 'passthrough',transformers=[('drop_columns','drop',[config.model_config.drop_feature])])),
                        ('missing_values',SimpleImputer(missing_values=np.nan, strategy='median')),
                        ('estimator',LinearRegression())
])