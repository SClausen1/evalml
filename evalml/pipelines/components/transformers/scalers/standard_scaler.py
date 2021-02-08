import pandas as pd
from sklearn.preprocessing import StandardScaler as SkScaler
from woodwork.logical_types import Integer

from evalml.pipelines.components.transformers import Transformer
from evalml.utils import (
    _convert_to_woodwork_structure,
    _convert_woodwork_types_wrapper,
    _retain_custom_types_and_initalize_woodwork
)


class StandardScaler(Transformer):
    """Standardize features: removes mean and scales to unit variance."""
    name = "Standard Scaler"
    hyperparameter_ranges = {}

    def __init__(self, random_state=0, **kwargs):
        parameters = {}
        parameters.update(kwargs)

        scaler = SkScaler(**parameters)
        super().__init__(parameters=parameters,
                         component_obj=scaler,
                         random_state=random_state)

    def transform(self, X, y=None):
        X_ww = _convert_to_woodwork_structure(X)
        X = _convert_woodwork_types_wrapper(X_ww.to_dataframe())
        X_t = self._component_obj.transform(X)
        X_t_df = pd.DataFrame(X_t, columns=X.columns, index=X.index)
        return _retain_custom_types_and_initalize_woodwork(X_ww, X_t_df, to_ignore=[Integer])

    def fit_transform(self, X, y=None):
        return self.fit(X, y).transform(X, y)
