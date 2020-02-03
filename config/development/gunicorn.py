import multiprocessing

# base config
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count()
timeout = 120

# development config
reload = True
