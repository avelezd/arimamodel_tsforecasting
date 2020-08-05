import logging # log generation
import datetime
    
def logfilesetup(logname):
    
    # Create logger
    # breakpoint() 
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # File Handler which logs even degug messages
    d = datetime.datetime.today()
    d = d.strftime('%Y%m%d')
    
    _LOG_FILEPATH_ = "logs/"
    _LOG_INFO_FILENAME_ = "%s_%s.log"%(d,(logname.replace('.py','')))
    
    fh = logging.FileHandler(_LOG_FILEPATH_ + _LOG_INFO_FILENAME_)
    fh.setLevel(logging.INFO)

    # Console Handler with higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    
    # Create formater and add it to handlers
    _LOG_FORMAT_ = "[%(asctime)s] %(levelname)5s %(message)s (%(filename)s:%(funcName)s():%(lineno)s)"
    formatter = logging.Formatter(_LOG_FORMAT_)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    # breakpoint()
    
    return logger

