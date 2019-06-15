import glob
from os.path import isfile
from importlib import import_module

def load_modules(modules_path):
    """It imports all the modules inside a path
    e.g.
    this is usefull to pre-load all the models"""
    modules = []
    for module in glob.glob(modules_path):
        if isfile(module) and not module.endswith('__init__.py'):
            module_path = module[:-3].replace('/', '.')
            modules.append(import_module(module_path))

    return modules
