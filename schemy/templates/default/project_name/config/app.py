"""Module to define the global setting of the API"""
from {project_name} import ROOT_DIR
from {project_name} import ROOT_PACKAGE

APP = {
    'ROOT_DIR': ROOT_DIR,
    'ROOT_PACKAGE': ROOT_PACKAGE,
    'MODELS_DIR': ROOT_PACKAGE + '/models',
    'TYPES_DIR': ROOT_PACKAGE + '/types',
    'FACTORIES_DIR': ROOT_PACKAGE + '/database/factories',
    'SDL_PATH': ROOT_PACKAGE + '/schema.sdl',
}
