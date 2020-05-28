#-----------------------------------------------------------------------------
# Script name:  arima_shampoo.py
# Description:  Group of methods to analyze the time series of shampoo sales.
# Creation date:26/05/2020
# Last update:  26/05/2020
# Author:       avelezd
#------------------------------------------------------------------------------
import sys, getopt

from pandas import read_csv
from pandas import datetime
from pandas import DataFrame
from statsmodels.tsa.arima_model import ARIMA
from matplotlib import pyplot
from pandas.plotting import autocorrelation_plot
from sklearn.metrics import mean_squared_error

def parser(x):
	return datetime.strptime('190'+x, '%Y-%m')

def plot_shampoosales(inpath):
    """
    The data is also plotted as a time series with the month along the x-axis and sales figures on the y-axis.
    """
    series = read_csv(inpath, header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
    # print(series.head())
    series.plot()
    pyplot.show()

def shampoosales_autocorrelation(inpath):
    """
    The code below plots the autocorrelation for a large number of lags in the time series.
    """
    series = read_csv(inpath, header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
    autocorrelation_plot(series)
    pyplot.show()

def fitarima_sales(inpath):
    """
    We will fit an ARIMA model to the entire Shampoo Sales dataset and review the residual errors.
    """
    series = read_csv(inpath, header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)

    # fit model
    #-----------
    # we fit an ARIMA(5,1,0) model. 
    # This sets the lag value to 5 for autoregression, 
    # uses a difference order of 1 to make the time series stationary, 
    # and uses a moving average model of 0.
    model = ARIMA(series, order=(5,1,0))
    model_fit = model.fit(disp=0)
    
    print('Model fit summary')
    print(model_fit.summary())
    
    # plot residual errors
    residuals = DataFrame(model_fit.resid)
    residuals.plot()
    pyplot.show()
    residuals.plot(kind='kde')
    pyplot.show()
    
    print('Residual errors')
    print(residuals.describe())

def arima4casting_simple(inpath):
    series = read_csv(inpath, header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
    X = series.values
    size = int(len(X) * 0.66)
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
    	model = ARIMA(history, order=(5,1,0))
    	model_fit = model.fit(disp=0)
    	output = model_fit.forecast()
    	yhat = output[0]
    	predictions.append(yhat)
    	obs = test[t]
    	history.append(obs)
    	print('predicted=%f, expected=%f' % (yhat, obs))
    error = mean_squared_error(test, predictions)
    print('Test MSE: %.3f' % error)
    # plot
    pyplot.plot(test)
    pyplot.plot(predictions, color='red')
    pyplot.show()

if __name__ == "__main__":
    
    inpath = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:",["inpath="])
    except getopt.GetoptError:
        print('usage: arima_shampoo.py -i <input file>')

    for opt, arg in opts:
        if opt == '-h':
            print('usage: arima_shampoo.py -i <input file>')
            sys.exit()
        elif opt in ('-i','--inpath'):
            inpath = arg

    if not inpath:
        # inpath = '../00_datasets/shampoo.csv'
        print('parameters required. try again.')
        sys.exit()
    
    # plot_shampoosales(inpath)
    # shampoosales_autocorrelation(inpath)
    # fitarima_sales(inpath)
    arima4casting_simple(inpath)

