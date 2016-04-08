# see http://docs.gunicorn.org/en/latest/configure.html#configuration-file

from os import getenv


bind = '0.0.0.0:8000'
workers = getenv('WSGI_NUM_WORKERS', 2)
errorlog = '-'
loglevel = getenv('WSGI_LOG_LEVEL', 'warning')
