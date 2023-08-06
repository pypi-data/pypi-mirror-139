from __future__ import annotations

from typing import Union

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

X_TYPE = Union[pd.Series, pd.DataFrame]


class TruncateTransformer(BaseEstimator, TransformerMixin):
    """Truncate data.

    Leave only a specific number of past weeks.
    """

    def __init__(self, full_weight_weeks: int, truncate: bool = True) -> None:
        self.truncate = truncate
        self.full_weight_weeks = full_weight_weeks

    def fit(self, X: X_TYPE, y: pd.Series = None) -> TruncateTransformer:
        return self

    def transform(self, X: X_TYPE) -> X_TYPE:
        if self.truncate and self.full_weight_weeks > 0:
            return X[X.index > X.index.max() - pd.DateOffset(weeks=self.full_weight_weeks, days=1)]
        else:
            return X

    @staticmethod
    def inverse_transform(X: X_TYPE) -> X_TYPE:
        return X
