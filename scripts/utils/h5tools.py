#-----------------------------------------------------------------------------
# Script name:  h5tools.py
# Description:  Tools to get data from HDF5 files.
# Creation date:09/07/2020
# Last update:  09/07/2020
# Author:       avelezd
#------------------------------------------------------------------------------
import h5py
import numpy
import pandas
import logging
from matplotlib import pyplot
from matplotlib.colors import ListedColormap

import math

## ADF test - Stationary times series
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

logger = logging.getLogger(__name__)

NUBLOCKS = 288 # 5 minutes block times
NUROWS = 495 # map height
NUCOLS = 436 # map width

def plot_timeseries_data(series):
    logger.info('running plot...')
    series.plot()
    pyplot.show()

def _get_h5fcontent(h5filepath):
    '''Extracts data from h5file and change format to numpy array'''
    logger.info('get content file {}'.format(h5filepath))

    h5file = h5py.File(h5filepath, 'r')
    keys = list(h5file.keys())
    a_group_key = list(h5file.keys())[0]

    h5data = list(h5file[a_group_key])
    h5data = [h5data[0:]]
    h5data = numpy.stack(h5data,axis=0)

    logger.info('Data from HDF5 file extracted OK')
    return h5data

def _get_tsrows(nublock, h5content, nuchannel, nurows, nucols):
    # logger.info('_get_tsrows')

    nucount_cells = 1
    tsrow = numpy.zeros([1,(nurows*nucols)+1], dtype = int)
    
    tsrow[0,0] = nublock
    # logger.info('start for loop')
    for rowidx in range(0,nurows):
        # logger.info('row: %s'%rowidx)
        for colidx in range(0,nucols):
            # logger.info('row: %s - col: %s'%(rowidx, colidx))
            # breakpoint()
            tsrow[0,nucount_cells] = h5content[0,nublock,rowidx,colidx,nuchannel]
            nucount_cells += 1
            # logger.info('cell number: %s'%nucount_cells)
    
    # breakpoint()
    # logger.info('extraction OK')
    return tsrow

def _get_file_name(h5path):
    namelist = h5path.split('/')
    return namelist[-1]

def get_file_by_channel(h5path):
    
    logger.info('get files from {}'.format(h5path))
    
    filename = _get_file_name(h5path)
    h5content = _get_h5fcontent(h5path)

    tsrows = numpy.empty([1, (NUROWS*NUCOLS)+1], dtype = int)
    
    for nuchannel in range(0,3):
        logger.info('channel {}'.format(nuchannel))

        for blockidx in range(0, NUBLOCKS):
            tsrows =numpy.vstack((
                tsrows, 
                _get_tsrows(
                    blockidx, 
                    h5content,
                    nuchannel, 
                    NUROWS, 
                    NUCOLS
                )))
            logger.info('block {}'.format(blockidx))
    
        logger.info('Data extracted, writing file...')
        outfile = 'output/ch{0}_{1}.csv'.format(nuchannel, filename.replace('.h5',''))
        
        dfchannel = pandas.DataFrame(data = tsrows[1:,1:])
        dfchannel.to_csv(outfile)
        logger.info('file {} created OK!'.format(outfile))

    logger.info('Files by channel OK')

def get_cell_series(h5path, nuchannel, nurow, nucol, step):
    
    h5content = _get_h5fcontent(h5path)

    
    # Creates a zeros array
    ts = numpy.zeros(NUBLOCKS, dtype = int)
    
    # breakpoint()
    for nuidx in range(0, step):

        # fill the array
        for nublock in range(0, NUBLOCKS):
            ts[nublock] = h5content[0, nublock, nucol, nurow, nuchannel]

        # Convert array to series to plot
        tserie = pandas.Series(data=ts)
    
        # plot the time series
        plot_timeseries_data(tserie)

        # Dickey-Fuller test
        # breakpoint()
        adf_result = adfuller(tserie)
        
        print('ADF Statistics: %f'%adf_result[0])
        print('p-value: %f'%adf_result[1])
        print('Critical values:')
        for key, value in adf_result[4].items():
            print('\t%s: %.3f'%(key, value))

        if adf_result[0] < adf_result[4]['5%']:
            print('Rejected H0 - Time Series is Stationary')
            tserie.to_csv('output/series_ch0_20180622/stationary/{0}.csv'.format())
        else:
            print('Failed to reject H0 - Time Series is Non-Stationary')

        nurow += step
        nucol += step

def plotsaveframe(frame2plot, custcmap, nuchannel, outpath):
    '''Plot an image and pops up a window to show it, the image is saved after close de window'''    
    fig = pyplot.figure(figsize=(NUROWS, NUCOLS))
    pyplot.imshow(frame2plot, cmap=custcmap)
    pyplot.axis('off')
    pyplot.title('Stationarity distribution channel {0}'.format(nuchannel))

    pyplot.show()
    fig.savefig('%s/samplemap_ch%s.png'%(outpath, nuchannel))
    pyplot.close(fig)


def get_stationarytest_tsclassification(h5path, nuchannel):
    h5content = _get_h5fcontent(h5path)

    h5filename = _get_file_name(h5path)
    h5filename_root = h5filename.replace('_100m_bins.h5','')
    outpath = '../datasets/output/'

    # Creates a zeros array
    ts = numpy.zeros(NUBLOCKS, dtype = int)

    # Creates an empty frame to classify stationarity
    framearray = numpy.zeros([NUROWS, NUCOLS], dtype = int)

    logger.info('Extracting time series')
    nucount = 0
    isstationary = 0 # {0:"NA", 1:"stationary", 2:"nonstationary"}

    for nurow in range(0, NUROWS):
        for nucol in range(0, NUCOLS):
            for nublk in range(0, NUBLOCKS):
                ts[nublk] = h5content[0, nublk, nurow, nucol, nuchannel]
        
            logger.info('\nts {0}, nurow {1}, nucol {2}'.format(nucount, nurow, nucol))
            tserie = pandas.Series(data=ts)
            adf_result = adfuller(tserie)
            
            if math.isnan(adf_result[0]):
                logger.info('nan - valores fijos en cero (0)')
                isstationary = 0
                tserie.to_csv('{0}/nan/{1}_ch{2}_{3}.csv'.format(outpath
                                                                  ,h5filename_root
                                                                  ,nuchannel
                                                                  ,nucount
                                                                 ), header=False)
            elif adf_result[0] < adf_result[4]['5%']:
                logger.info('stationary')
                isstationary = 1
                tserie.to_csv('{0}/stationary/{1}_ch{2}_{3}.csv'.format(outpath
                                                                     ,h5filename_root
                                                                     ,nuchannel
                                                                     ,nucount
                                                                    ), header=False)
            else:
                logger.info('non-stationary')
                isstationary = 2
                tserie.to_csv('{0}/nonstationary/{1}_ch{2}_{3}.csv'.format(outpath
                                                                        ,h5filename_root
                                                                        ,nuchannel
                                                                        ,nucount
                                                                       ), header=False)
            nucount+=1
            framearray[nurow, nucol] = isstationary

    return framearray
