import os

LOGGING = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
			'stream': 'ext://sys.stdout',
		},
		'file': {
			'class': 'logging.handlers.RotatingFileHandler',
			'level': 'INFO',
			'formatter': 'standard',
			'filename': './logs/api.log',
			'mode': 'a',
			'maxBytes': 1024*1024*25, # 25MB,
			'backupCount': 5,
		},
		'slack': {
            'class': 'slack_logger.SlackHandler',
            'level': 'ERROR',
			'formatter': 'standard',
            'url': os.getenv('SLACK_WEBHOOK', None),
            'username':'Logger',
        },
    },
    'loggers': {
        'api': {  # default logger
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
    }
}
