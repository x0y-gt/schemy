import inspect

from schemy.datasources import BaseModel as Base
from schemy.helpers import load_modules

from customers.app import api

__all__ = [
    'Base',
]

def load_models():
    modules = load_modules(api.models_path + '/*.py')
    for module in modules:
        #Getting the module objects to get the Model Class
        for _name, object_ in inspect.getmembers(module, inspect.isclass):
            if issubclass(object_, Base): # and object_.__module__ == module_path:
                globals()[object_.__name__] = object_

#pre-import all models to avoid dependencies problems
load_models()
