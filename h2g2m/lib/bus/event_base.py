from ctypes import ArgumentError
from h2g2m.models.base import DBSession
from pyramid.threadlocal import get_current_request


class Event(object):
    request = None
    DBSession = None

    def __init__(self, **kwargs):
        given = kwargs.keys()
        needed = [attr for attr in dir(self.__class__) if attr[0] != '_' and attr not in ['request', 'DBSession']]
        if not set(given) <= set(needed):
            raise ArgumentError('Event constructor was given %s and requires %s.' % (repr(given), repr(needed)))
        self.__dict__.update({k: self.__class__.__dict__[k] for k in needed})
        self.__dict__.update(kwargs)

        if not self.request:
            self.request = get_current_request()
        self.DBSession = DBSession
