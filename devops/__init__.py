import sys

from loguru import logger

config = {
    'handlers': [
        {
            'sink'      : sys.stdout,
            'format'    : '<green>{time:YYYY:MM:DD HH:mm:ss.SSS}</green> [<level>{level}</level>] <level><n>{message}</n></level>',
            'colorize'  : True
        }
    ]
}
logger.configure(**config)