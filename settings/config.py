"""
BOT configuration.
"""
import logging.config as logger
import os

from sqlalchemy import create_engine

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

SQLACHEMY = create_engine(
    'mysql://%s:%s@%s:%s/%s' % (
        os.environ.get('MYSQL_USER', 'neeble'),
        os.environ.get('MYSQL_PASSWORD', 'neeble'),
        os.environ.get('MYSQL_HOST', 'localhost'),
        int(os.environ.get('MYSQL_PORT', '3306')),
        os.environ.get('MYSQL_DATABASE', 'neeble'),
    )
)

# Define the log level
LOGLEVEL = os.environ.get('LOGLEVEL', 'info').upper()

# Logging custom config.
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

## INSTRUCTIONS ON SETTING UP PERMISSIONS:
# Permissions are now granular, more than one distinct role
# can execute the commands, whatever roles are inside the
# comma-separated lists can execute their respective commands
# Commands with empty lists will grant execution privileges to everyone
PERMISSIONS = {
    'dq' : ['BotMan'],
    'v' : ['Operador', 'BotMan']
}

OW_API_CONFIG = {
    'api_id' : os.environ.get('OPENWEATHER_API_TOKEN', 'no'),
    'wh_url' : 'https://api.openweathermap.org/data/2.5/weather?q=<CITY>&units=metric&appid=<API_ID>'
}

# Tuple of image type on image links.
# e.g: https://cdn.discordapp.com/attachments/720808802340962357/988542480981061702/cat.jpeg
# e.g: https://cdn.discordapp.com/attachments/720808802340962357/988542480981061702/unknow.png
IMAGE_TYPES = (
    '.jpeg',
    '.jpg',
    '.png',
    '.mp4',
    '.gif',
)
