import os
import logging


def initialize_logging():
    path_current_directory = os.path.dirname(__file__)
    log_file_path = os.path.join(path_current_directory, 'logs.log')

    # Logging configuration
    logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
                        datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG, filename=log_file_path)
    logger = logging.getLogger("main")

initialize_logging()
