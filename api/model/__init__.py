import inspect

from sqlalchemy.ext.declarative import declarative_base
import api.config as config

from schemy.datasource import Datasource
from schemy.utils import load_modules

__all__ = [
    'datasource',
    'Base',
]

datasource = Datasource(config.get('DATABASE_CONNECTION'))
Base = declarative_base() #(cls=DeferredReflection)

def load_models():
    modules = load_modules(config.get('APP_MODELS_DIR') + '/*.py')
    for module in modules:
        #Getting the module objects to get the Model Class
        for _name, object_ in inspect.getmembers(module, inspect.isclass):
            if issubclass(object_, Base): # and object_.__module__ == module_path:
                globals()[object_.__name__] = object_

#pre-import all models to avoid dependencies problems
load_models()
