"""
BOT configuration.
"""
import logging.config as logger
import os

# Discord token.
DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

# Mysql configuration.
MYSQL_CONFIG = {
    'host': os.environ.get('MYSQL_HOST', 'localhost'),
    'port': int(os.environ.get('MYSQL_PORT', '3306')),
    'db': os.environ.get('MYSQL_DATABASE', 'neeble'),
    'user': os.environ.get('MYSQL_USER', 'neeble'),
    'password': os.environ.get('MYSQL_PASSWORD', 'neeble'),
}

# Define the log level
LOGLEVEL = os.environ.get('LOGLEVEL', 'info').upper()

# Configuração do logging.
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': LOGLEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'logfile': {
            'level': LOGLEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/tmp/neeble.log',
            'maxBytes': 50000,
            'backupCount': 9,
            'formatter': 'default',
        },
    },
    'loggers': {
        '': {
            'level': LOGLEVEL,
            'handlers': ['console', 'logfile'],
            'propagate': False,
        },
        'neeble': {
            'level': LOGLEVEL,
            'handlers': ['console', 'logfile'],
            'propagate': False,
        },
    },
}

logger.dictConfig(LOGGING_CONFIG)
