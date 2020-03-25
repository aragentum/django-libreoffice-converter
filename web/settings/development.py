from .common import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'console_formatter': {
            'format': '[%(asctime)s]:[%(process)d] | [%(levelname)s] | %(name)-15s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console_formatter'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'web.api': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}
