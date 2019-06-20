import os
ROOT_DIR = os.path.abspath(os.getcwd()) + '/api'

from .config import config

__all__ = [
    'ROOT_DIR',
    'config'
]
