from __future__ import annotations

from typing import List

import pandas as pd
from statsmodels.regression.linear_model import OLS
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.tsatools import add_trend

from hcl_model.model_base import ModelBase


class SARIMAXModel(ModelBase):
    """
    SARIMAX model

    Wrapper around `statsmodels implementation
    <http://www.statsmodels.org/stable/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html#statsmodels.tsa.statespace.sarimax.SARIMAX>`_.

    See documentation of `statsmodels.tsa.statespace.sarimax.SARIMAX`
    """

    def __init__(
        self,
        order: tuple = (0, 0, 0),
        seasonal_order: tuple = (0, 0, 0, 0),
        trend: str = "c",
        enforce_stationarity: bool = True,
    ) -> None:
        self.order = order
        self.seasonal_order = seasonal_order
        self.trend = trend
        self.enforce_stationarity = enforce_stationarity

    def _fit(self, **kwargs) -> None:
        self.y_train_ = self._remove_trend(self.y_train_)
        self.fit_results_ = SARIMAX(
            self.y_train_,
            exog=self.x_train_,
            order=self.order,
            seasonal_order=self.seasonal_order,
            enforce_stationarity=self.enforce_stationarity,
        ).fit(disp=False)

    def _predict(
        self, num_steps: int, X: pd.DataFrame = None, quantile_levels: List[float] = None, num_simulations: int = None
    ) -> pd.DataFrame:
        return (
            self.fit_results_.get_forecast(steps=num_steps, exog=X)
            .predicted_mean.rename(self._get_endog_name())
            .to_frame()
            .rename_axis(index=self.y_train_.index.name)
        )

    def _simulate(self, num_steps: int, num_simulations: int, X: pd.DataFrame = None, **kwargs) -> pd.DataFrame:
        self.y_train_ = self._remove_trend(self.y_train_)
        sim_model = SARIMAX(
            pd.Series(index=X.index, dtype=float),
            exog=X,
            order=self.order,
            seasonal_order=self.seasonal_order,
            enforce_stationarity=self.enforce_stationarity,
        )
        sim_model = sim_model.filter(params=self.fit_results_.params)
        # TODO: check simulation output for different model. I am not sure it is correct without initial_sate.
        return pd.DataFrame({i: sim_model.simulate(num_steps) for i in range(num_simulations)})

    def _get_aic(self) -> float:
        return self.fit_results_.aic

    def _get_fitted_values(self) -> pd.Series:
        return self.fit_results_.fittedvalues

    def _get_residuals(self) -> pd.Series:
        return self.fit_results_.resid

    def _compute_prediction_quantiles(
        self, num_steps: int, quantile_levels: List[float] = None, X: pd.DataFrame = None, **kwargs
    ) -> pd.DataFrame:
        forecast = self.fit_results_.get_forecast(steps=num_steps, exog=X)
        out = dict()
        for alpha, q_name in zip(quantile_levels, self.get_quantile_names(quantile_levels)):
            if alpha < 50:
                out[q_name] = forecast.conf_int(alpha=2 * alpha / 100).iloc[:, 0]
            else:
                out[q_name] = forecast.conf_int(alpha=2 * (100 - alpha) / 100).iloc[:, 1]
        return pd.DataFrame(out).rename_axis(index=self.y_train_.index.name)

    def _remove_trend(self, endog: pd.Series) -> pd.Series:
        if self.trend == "n":
            return endog
        else:
            name = endog.name
            trend = add_trend(self.y_train_, trend=self.trend, prepend=False)
            self.trend_fit_ = OLS(endog, trend.iloc[:, 1:]).fit()
            endog -= self.trend_fit_.fittedvalues
            return endog.rename(name)

    def _add_trend(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.trend == "n":
            return df
        else:
            exog = add_trend(
                pd.concat([self.y_train_, df[self.y_train_.name]]),
                trend=self.trend,
                prepend=False,
                has_constant="add",
            )
            return df.apply(lambda x: x + self.trend_fit_.predict(exog.iloc[-df.shape[0] :, 1:]))
