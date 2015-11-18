# -*- coding: utf-8 -*-
from pkgutil import get_data

from itertools import chain
from functools import wraps
from yaml import load as load_yaml

from .utils import Registry

"""
:mod:`dateparser`'s parsing behavior can be configured like below

*``PREFER_DAY_OF_MONTH``* defaults to ``current`` and can have ``first`` and ``last`` as values::

    >>> from dateparser.conf import settings
    >>> from dateparser import parse
    >>> parse(u'December 2015')
    datetime.datetime(2015, 12, 16, 0, 0)
    >>> settings.update('PREFER_DAY_OF_MONTH', 'last')
    >>> parse(u'December 2015')
    datetime.datetime(2015, 12, 31, 0, 0)
    >>> settings.update('PREFER_DAY_OF_MONTH', 'first')
    >>> parse(u'December 2015')
    datetime.datetime(2015, 12, 1, 0, 0)

*``PREFER_DATES_FROM``* defaults to ``current_period`` and can have ``past`` and ``future`` as values.
Assuming current date is June 16, 2015::

    >>> from dateparser.conf import settings
    >>> from dateparser import parse
    >>> parse(u'March')
    datetime.datetime(2015, 3, 16, 0, 0)
    >>> settings.update('PREFER_DATES_FROM', 'future')
    >>> parse(u'March')
    datetime.datetime(2016, 3, 16, 0, 0)

*``SKIP_TOKENS``* is a ``list`` of tokens to discard while detecting language. Defaults to ``['t']`` which skips T in iso format datetime string.e.g. ``2015-05-02T10:20:19+0000``.
This only works with :mod:`DateDataParser` like below:

    >>> settings.update('SKIP_TOKENS', ['de'])  # Turkish word for 'at'
    >>> from dateparser.date import DateDataParser
    >>> DateDataParser().get_date_data(u'27 Haziran 1981 de')  # Turkish (at 27 June 1981)
    {'date_obj': datetime.datetime(1981, 6, 27, 0, 0), 'period': 'day'}
"""


class SettingsRegistry(Registry):

    @classmethod
    def get_key(cls, *args, **kwargs):
        if not args and not kwargs:
            return 'default'

        keys= sorted(['%s-%s' % (key, str(kwargs[key])) for key in kwargs])
        return ''.join(keys)


class Settings(object):

    __metaclass__ = SettingsRegistry

    _attributes = []
    _default = True

    def __init__(self, **kwargs):
        """
        Settings are now loaded using the data/settings.yaml file.
        """
        self.updateall(
            chain(self.get_settings_from_yaml().items(),
            kwargs.items())
        )

    def get_settings_from_yaml(self):
        data = get_data('data', 'settings.yaml')
        data = load_yaml(data)
        return data.pop('settings', {})

    def updateall(self, iterable):
        for key, value in iterable:
            self._attributes.append(key)
            setattr(self, key, value)

    def replace(self, **kwds):
        for x in self._attributes:
            kwds.setdefault(x, getattr(self, x))
        kwds['_default'] = False

        return self.__class__(**kwds)


settings = Settings()


def apply_settings(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'settings' in kwargs:
            if isinstance(kwargs['settings'], dict):
                kwargs['settings'] = settings.replace(**kwargs['settings'])
            elif isinstance(kwargs['settings'], Settings):
                kwargs['settings'] = kwargs['settings']
            else:
                raise TypeError("settings can only be either dict or instance of Settings class")
        else:
            kwargs['settings'] = settings
        return f(*args, **kwargs)
    return wrapper
