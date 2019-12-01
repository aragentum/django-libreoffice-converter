from abc import ABCMeta


class Service(object):
    """
    Abstract class for inheritance singleton service.
    """
    __metaclass__ = ABCMeta

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
