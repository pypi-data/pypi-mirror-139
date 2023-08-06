from __future__ import annotations

from typing import Union

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from hcl_model.utils.smooth import smooth_series
from hcl_model.utils.string_enum import StringEnum

X_TYPE = Union[pd.Series, np.ndarray]


class CorrectOutliersMethodNames(StringEnum):
    nothing = "nothing"
    interpolate = "interpolate"
    trim = "trim"


class TargetOutlierCorrectionTransformer(BaseEstimator, TransformerMixin):
    """Target outlier correction."""

    def __init__(
        self,
        outlier_correction_method: CorrectOutliersMethodNames,
        six_sigma_multiplier: float,
        smoothing_window: int = 52,
        ewm_alpha: float = 0.1,
    ) -> None:
        self.six_sigma_multiplier = six_sigma_multiplier
        self.smoothing_window = smoothing_window
        self.ewm_alpha = ewm_alpha
        self.outlier_correction_method = outlier_correction_method

    def fit(self, X: X_TYPE, y: pd.Series = None) -> TargetOutlierCorrectionTransformer:
        return self

    def transform(self, X: X_TYPE) -> X_TYPE:
        if self.outlier_correction_method == CorrectOutliersMethodNames.nothing:
            return X
        else:
            if isinstance(X, np.ndarray):
                return self._correct_outliers(series=pd.Series(X.flatten())).values
            else:
                return self._correct_outliers(series=X)

    def _correct_outliers(self, series: pd.Series) -> pd.Series:
        is_too_high = self.get_idx_too_high(series=series)
        is_too_low = self.get_idx_too_low(series=series)
        series_corrected = series.copy()
        if sum(is_too_high) + sum(is_too_low) > 0:
            if self.outlier_correction_method == CorrectOutliersMethodNames.trim:
                series_corrected[is_too_low] = self.get_lower_limit(series=series)[is_too_low]
                series_corrected[is_too_high] = self.get_upper_limit(series=series)[is_too_high]
            elif self.outlier_correction_method == CorrectOutliersMethodNames.interpolate:
                series_corrected[is_too_low] = np.nan
                series_corrected[is_too_high] = np.nan
                series_corrected = series_corrected.interpolate()
            else:
                raise NotImplementedError
        return series_corrected.rename(series.name)

    def get_idx_too_high(self, series: pd.Series) -> pd.Series:
        return series > self.get_upper_limit(series=series)

    def get_idx_too_low(self, series: pd.Series) -> pd.Series:
        return series < self.get_lower_limit(series=series)

    def get_upper_limit(self, series: pd.Series) -> pd.Series:
        return self._get_smoothed_series(series=series) + self.six_sigma_multiplier * self._get_iqr_residuals(
            series=series
        )

    def get_lower_limit(self, series: pd.Series) -> pd.Series:
        return self._get_smoothed_series(series=series) - self.six_sigma_multiplier * self._get_iqr_residuals(
            series=series
        )

    def _get_iqr_residuals(self, series: pd.Series) -> float:
        residuals = series - self._get_smoothed_series(series=series)
        return residuals.quantile(q=0.75) - residuals.quantile(q=0.25)

    def _get_smoothed_series(self, series: pd.Series) -> pd.Series:
        return smooth_series(y=series, window=self.smoothing_window, quantile=0.5, ewm_alpha=self.ewm_alpha)
