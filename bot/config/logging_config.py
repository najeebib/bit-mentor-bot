import logging
import logging.config
import os

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, 'app.log')

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',  # Change to INFO to suppress DEBUG messages
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': log_file_path,
            'formatter': 'standard',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'encoding': 'utf8'
        },
        'console': {
            'level': 'INFO',  # Change to INFO to suppress DEBUG messages
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'httpx': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False
        },
        'telegram': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False
        },
    }
}
