# ARIMA: Autoregressive Integrated Moving Average

An ARIMA, which stands for AutoRegressive Integrated Moving Average, model can be created using an `ARIMA(p,d,q)` model within `statsmodels` library. We will be using an alternative library `pmdarima`, which allows us to automatically search for optimal ARIMA parameters, within a specified range. More specifically, we will be using `auto_arima` function within `pmdarima` to automatically discover the optimal parameters for an ARIMA model. This function wraps `ARIMA` and `SARIMAX` models of `statsmodels` library, that correspond to non-seasonal and seasonal model space, respectively.

In an ARIMA model there are 3 parameters that are used to help model the major aspects of a times series: seasonality, trend, and noise. These parameters are:

* `p` is the parameter associated with the auto-regressive aspect of the model, which incorporates past values.
* `d` is the parameter associated with the integrated part of the model, which effects the amount of differencing to apply to a time series.
* `q` is the parameter associated with the moving average part of the model.,
If our data has a seasonal component, we use a seasonal ARIMA model or `ARIMA(p,d,q)(P,D,Q)m`. In that case, we have an additional set of parameters: `P`, `D`, and `Q` which describe the autoregressive, differencing, and moving average terms for the seasonal part of the ARIMA model, and `m` refers to the number of periods in each season.


## Data

Bitcoin downloaded form trading.com


