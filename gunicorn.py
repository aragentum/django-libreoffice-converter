import multiprocessing

# Config
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count()
timeout = 120

# Development
loglevel = 'debug'
accesslog = '-'
errorlog = '-'

env = {
    'DJANGO_SETTINGS_MODULE': 'web.settings.development'
}
reload = True
