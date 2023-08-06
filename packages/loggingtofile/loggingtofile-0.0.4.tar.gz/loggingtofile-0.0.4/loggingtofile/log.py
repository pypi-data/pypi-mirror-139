import logging
import os

logger = None

def initialize(logging_file_name):
    logger = logging.getLogger()
    logger.setLevel(level=logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

    file_handler = logging.FileHandler(logging_file_name)
    file_handler.setLevel(level=logging.INFO)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

def createfilename():
    filelist = os.listdir("./")
    logging_index = 0
    logging_file_name = 'logging_'+str(logging_index)+'.log'
    while (logging_file_name in filelist):
        logging_index += 1
        logging_file_name = 'logging_' + str(logging_index) + '.log'
    return logging_file_name


def print(*infos):
    global logger
    if (type(logger) == type(None)):
        logging_file_name = createfilename()
        logger = initialize(logging_file_name)
    format_output = ""
    for item in infos:
        format_output += '{}'.format(item)
        format_output += '    '
    logger.info(format_output)





