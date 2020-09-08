# ARIMA Model for Time Series Forecasting 

This repository contains an implementation code of the tutorial [How to Create an ARIMA Model for Time Series Forecasting in Python](https://machinelearningmastery.com/arima-for-time-series-forecasting-with-python/) explanation.

ARIMA is an acronym that stands for AutoRegressive Integrated Moving Average.

## Shampoo Sales Dataset
This dataset describes the monthly number of sales of shampoo over a 3 year period.

### plot\_shampoosales
It is an example of loading the Shampoo Sales dataset with Pandas with a custom function to parse the date-time field. The dataset is baselined in an arbitrary year, in this case 1900. The data is also plotted as a time series with the month along the x-axis and sales figures on the y-axis.

**TODO**:
* *what is stationarity? check link [Stationarity and differencing](https://otexts.com/fpp2/stationarity.html)*

### shampoosales\_autocorrelation
This is a quick look at an autocorrelation plot of the time series. This is also built-in to Pandas. It plots the autocorrelation for a large number of lags in the time series.

**TODO**:

* *what does mean the statemen? "there is a positive correlation with the first 10-to-12 lags that is perhaps significant for the first 5 lags. A good starting point for the AR parameter of the model may be 5."*

### fitarima\_sales
We fit an ARIMA(5,1,0) model. This sets the lag value to 5 for autoregression, uses a difference order of 1 to make the time series stationary, and uses a moving average model of 0.

When fitting the model, a lot of debug information is provided about the fit of the linear regression model. We can turn this off by setting the disp argument to 0.

we get a line plot of the residual errors, suggesting that there may still be some trend information not captured by the model.

we get a density plot of the residual error values, suggesting the errors are Gaussian, but may not be centered on zero.

The distribution of the residual errors is displayed. The results show that indeed there is a bias in the prediction (a non-zero mean in the residuals).

### arima4casting\_simple
Prints the prediction and expected value each iteration.We can also calculate a final mean squared error score (MSE) for the predictions, providing a point of comparison for other ARIMA configurations.
A line plot is created showing the expected values (blue) compared to the rolling forecast predictions (red). We can see the values show some trend and are in the correct scale.

The model could use further tuning of the p, d, and maybe even the q parameters.

## Configuring an ARIMA Model

The classical approach for fitting an ARIMA model is to follow the [Box-Jenkins Methodology](https://en.wikipedia.org/wiki/Box%E2%80%93Jenkins_method).

This is a process that uses time series analysis and diagnostics to discover good parameters for the ARIMA model.

In summary, the steps of this process are as follows:

* **Model Identification.** Use plots and summary statistics to identify trends, seasonality, and autoregression elements to get an idea of the amount of differencing and the size of the lag that will be required.
* **Parameter Estimation.** Use a fitting procedure to find the coefficients of the regression model.
* **Model Checking.** Use plots and statistical tests of the residual errors to determine the amount and type of temporal structure not captured by the model.

The process is repeated until either a desirable level of fit is achieved on the in-sample or out-of-sample observations (e.g. training or test datasets).

The process was described in the classic 1970 textbook on the topic titled Time Series Analysis: Forecasting and Control by George Box and Gwilym Jenkins. An updated 5th edition is now available if you are interested in going deeper into this type of model and methodology.

Given that the model can be fit efficiently on modest-sized time series datasets, grid searching parameters of the model can be a valuable approach.
