import time
from datetime import datetime

import logging
import coloredlogs

def get_local_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
class Logger(object):
    _instance = None

    @classmethod
    def get_logger(cls, level='INFO', write_to_file=False, log_path='/tmp/log-{}'.format(get_local_time())):
        if cls._instance:
            return cls._instance
        write_to_file = write_to_file
        if write_to_file:
            if not log_path:
                raise ValueError("Argument [log_path] cannot be None when write_to_file is True")
            else:
                log_path = log_path
        logger = logging.getLogger(__name__)
        logger.setLevel(level)
        # fhandler = logging.FileHandler(log_path)
        handler = logging.StreamHandler()
        handler.setLevel(level)
        fmt = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        coloredlogs.install(fmt=fmt, level=level, logger=logger)
        cls._instance = logger
        return cls._instance
    
class PerformanceProfile:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f'\033[1;34mPERFORMANCE PROFILE: \033[1;36m{self.name}\033[1;34m took \033[1;36m{time.time() - self.start:.2f}\033[1;34m seconds\033[0m')

default_logger = Logger().get_logger()

if __name__ == '__main__':
    ...