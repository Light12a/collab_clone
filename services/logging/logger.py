import os
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

# from pythonjsonlogger import jsonlogger

LOG_PATH = "log"

LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
}

DEFAULT_LEVEL = logging.INFO
LOG_PATH = "log"
# FORMATTER = jsonlogger.JsonFormatter(
#     "%(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s"
# )
FORMATTER = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s', "%Y-%m-%d %H:%M:%S")


def init_logging(log_path=LOG_PATH, console=False, level=DEFAULT_LEVEL, days_to_keep=3):
    """ init logging in db_service """

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    # root logger
    rlogger = logging.getLogger()
    rlogger.setLevel(DEFAULT_LEVEL)
    fp_rlogger = os.path.join(LOG_PATH, "collabos_backend.log")
    rhandler = TimedRotatingFileHandler(
        fp_rlogger, backupCount=days_to_keep, when="MIDNIGHT"
    )
    rhandler.setFormatter(FORMATTER)
    rlogger.addHandler(rhandler)

    # db logger
    db_logger = logging.getLogger("db")
    db_logger.propagate = False
    db_logger.setLevel(DEFAULT_LEVEL)
    filepath_db_logger = os.path.join(LOG_PATH, "db_query.log")
    db_handler = TimedRotatingFileHandler(
        filepath_db_logger, backupCount=days_to_keep, when="MIDNIGHT"
    )
    db_handler.setFormatter(FORMATTER)
    db_logger.addHandler(db_handler)

    # add new logging handler here base on db_logger

    if console:
        fmt2 = logging.Formatter("%(levelname)-8s %(message)s")
        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(fmt2)
        rlogger.addHandler(console)
        db_logger.addHandler(console)


def get(name, prefix=None, level=None):
    if prefix is not None:
        logger = logging.getLogger(prefix + name)
    else:
        logger = logging.getLogger(name)

    if level and level.lower() in LOG_LEVELS:
        logger.setLevel(LOG_LEVELS[level.lower()])
    else:
        logger.setLevel(DEFAULT_LEVEL)

    return logger


def backup_log(path):
    p = path
    count = 0
    d = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    while os.path.exists(p):
        p = "{}.{}_{}".format(path, d, count)
        count += 1
    if count > 0:
        os.rename(path, p)
