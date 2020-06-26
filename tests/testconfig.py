import logging


logging.basicConfig(
    filename='testlog.log', 
    level=logging.INFO, 
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S %z',
    disable_existing_loggers=True
    )

def get_logger(name):
    return logging.getLogger(name)