"""Module to define the global setting of the API"""
from api import ROOT_DIR
from api import ROOT_PACKAGE

APP = {
    'ROOT_DIR': ROOT_DIR,
    'ROOT_PACKAGE': ROOT_PACKAGE,
    'MODELS_DIR': ROOT_PACKAGE + '/model',
    'TYPES_DIR': ROOT_PACKAGE + '/type',
    'FACTORIES_DIR': ROOT_PACKAGE + '/database/factories'
}
