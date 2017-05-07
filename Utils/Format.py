import datetime
from json import dumps as json_dumps


def p_json(**kwargs):
    return '{}'.format(json_dumps(kwargs))


def current_time():
    return '{dt:%H}:{dt:%M}:{dt:%S}'.format(dt=datetime.datetime.now())
