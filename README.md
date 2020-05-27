# ARIMA Model for Time Series Forecasting 

This repository contains an implementation code of the tutorial (How to Create an ARIMA Model for Time Series Forecasting in Python)[https://machinelearningmastery.com/arima-for-time-series-forecasting-with-python/] explanation.

ARIMA is an acronym that stands for AutoRegressive Integrated Moving Average.

## Shampoo Sales Dataset
This dataset describes the monthly number of sales of shampoo over a 3 year period.

### plot\_shampoosales
It is an example of loading the Shampoo Sales dataset with Pandas with a custom function to parse the date-time field. The dataset is baselined in an arbitrary year, in this case 1900. The data is also plotted as a time series with the month along the x-axis and sales figures on the y-axis.

**TODO**:
* *what is stationarity? check link (Stationarity and differencing)[https://otexts.com/fpp2/stationarity.html]*

### shampoosales\_autocorrelation
This is a quick look at an autocorrelation plot of the time series. This is also built-in to Pandas. It plots the autocorrelation for a large number of lags in the time series.

**TODO**:

* what does mean the statemen? "there is a positive correlation with the first 10-to-12 lags that is perhaps significant for the first 5 lags. A good starting point for the AR parameter of the model may be 5."*




