#-----------------------------------------------------------------------------
# Script name:  arima_model.py
# Description:  Group of methods to analyze the time series.
# Creation date:29/05/2020
# Last update:  29/05/2020
# Author:       avelezd
#------------------------------------------------------------------------------
import sys, getopt
import h5py
import numpy
import pandas
from matplotlib import pyplot

def plot_timeseries_data(series):
    series.plot()
    pyplot.show()

def _get_h5fcontent(h5filepath):
    '''Extracts data from h5file and change format to numpy array'''
    print('_get_h5fcontent')
    h5file = h5py.File(h5filepath, 'r')
    keys = list(h5file.keys())
    a_group_key = list(h5file.keys())[0]

    h5data = list(h5file[a_group_key])
    h5data = [h5data[0:]]
    h5data = numpy.stack(h5data,axis=0)

    print('Data from HDF5 file extracted')
    return h5data

def _get_tsrows(nublock, h5content, nuchannel, nurows, nucols):
    
    print('_get_tsrows')
    nucount_cells = 1
    tsrow = numpy.zeros([1,(nurows*nucols)+1], dtype = int)
    
    tsrow[0,0] = nublock
    # print('start for loop')
    for rowidx in range(0,nurows):
        # print('row: %s'%rowidx)
        for colidx in range(0,nucols):
            # print('row: %s - col: %s'%(rowidx, colidx))
            # breakpoint()
            tsrow[0,nucount_cells] = h5content[0,nublock,rowidx,colidx,nuchannel]
            nucount_cells += 1
            # print('cell number: %s'%nucount_cells)
    
    # breakpoint()
    # tsrow[rowidx,colidx] = array2print[0, nublock, rowidx, colidx, nuchannel]
    # print('valor fila: ', tsrow)
    # print('extraction ok')
    return tsrow

def get_tsdatastructure(h5fpath, nuchannel):
    print('get_tsdatastructure')
    h5content = _get_h5fcontent(h5fpath)
    nutime = 288 # 5 minutes block times
    nurows = 495 # height
    nucols = 436 # width
    tsrows = numpy.empty([1, (nurows*nucols)+1], dtype = int)

    # breakpoint()
    
    for blockidx in range(0, nutime):
        tsrows =numpy.vstack((tsrows, _get_tsrows(blockidx, h5content, nuchannel, nurows, nucols)))
        print('block: %s complete'%blockidx)

    return tsrows

if __name__ == "__main__":
    inpath = nuchannel = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:c:",["inpath=", "nuchannel="])
    except getopt.GetoptError:
        print('usage: arima_model.py -i <input file> -c <channel>')

    for opt, arg in opts:
        if opt == '-h':
            print('usage: arima_model.py -i <input file> -c <channel>')
            sys.exit()
        elif opt in ('-i','--inpath'):
            inpath = arg
        elif opt in ('-c','--nuchannel'):
            nuchannel = arg

    if not inpath or not nuchannel:
        # inpath = '../00_datasets/shampoo.csv'
        print('parameters required. try again.')
        sys.exit()
    
    tsdataset = get_tsdatastructure(inpath, int(nuchannel))
    # breakpoint() 
    # numpy.savetxt("map_channel{0}.csv".format(nuchannel), tsdataset,
    #               delimiter=',')
    
    # breakpoint()
    cellserie = pandas.DataFrame(
        data=tsdataset[1:,1:] #,
        # index=tsdataset[1:,0],
        # columns=['nublock'] + list(range(1, 495*436))
    )

    cellserie.to_csv('serie_cell200.csv')
    # plot_timeseries_data(cellserie)

