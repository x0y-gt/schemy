"""Module to define the global setting of the API"""
from api import ROOT_DIR

APP = {
    'ROOT_DIR': ROOT_DIR,
    'MODELS_DIR': ROOT_DIR + '/model',
    'TYPES_DIR': ROOT_DIR + '/type',
    'FACTORIES_DIR': ROOT_DIR + '/database/factories'
}
