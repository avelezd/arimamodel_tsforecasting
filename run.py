import sys, getopt
from utils.mylogsetup import logfilesetup
from utils.h5tools import get_cell_series, get_stationarytest_tsclassification
import pandas
    

logger = logfilesetup(__file__)

if __name__ == "__main__":
    
    logger.info('BOF')
    inpath = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:",["inpath="])
    except getopt.GetoptError:
        print('usage: run.py -i <input file>')

    for opt, arg in opts:
        if opt == '-h':
            print('usage: run.py -i <input file>')
            sys.exit()
        elif opt in ('-i','--inpath'):
            inpath = arg

    if not inpath:
        # inpath = '../00_datasets/shampoo.csv'
        print('parameters required. try again.')
        sys.exit()

    # get_file_by_channel(inpath)
    # dfchannel = pandas.read_csv(inpath)
    
    # for nucell in range(0,10):
    #     breakpoint()
    #     srcol = pandas.Series(data=dfchannel[1:, nucell])
    #     plot_timeseries_data(dfchannel)
    # get_cell_series(inpath, 0, 220, 210, 5) 
    get_stationarytest_tsclassification(inpath, 0)
    logger.info('EOF')

