import logging
from datetime import datetime
from json import dumps as json_dumps


class GameLogger(object):
    def __init__(self, **kwargs):
        self.dictionary = kwargs

    def __str__(self):
        return '{}'.format(json_dumps(self.dictionary))


logging.basicConfig(level=logging.DEBUG, format='%(message)s')


def info(**kwargs): return logging.info(GameLogger(**kwargs))


def debug(**kwargs): return logging.debug(GameLogger(**kwargs))


def error(**kwargs): return logging.error(GameLogger(**kwargs))


def get_iso_time():
    return '{dt:%Y}-{dt:%m}-{dt:%d}T{dt:%H}:{dt:%M}:{dt:%S}.{dt:%f}'.format(dt=datetime.now())[:-3] + 'Z'
