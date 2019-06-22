import os
ROOT_DIR = os.path.abspath(os.getcwd())
ROOT_PACKAGE = __package__

from .config import config

__all__ = [
    'ROOT_DIR',
    'ROOT_PACKAGE',
    'config'
]
