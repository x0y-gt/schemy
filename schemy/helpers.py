import sys
import os
import glob
import inspect
from importlib import import_module

from schemy.types import BaseType

__all__ = [
	'get_root_path',
	'resolve_path',
	'load_modules',
	'load_module',
	'intersec',
]


def intersec(defaults, dic):
    """Merges two dictionaries, the intention is to override the defaults"""
    new_dict = {**defaults, **dict(dic)}
    return {k:new_dict[k] for k in new_dict if k in defaults}


def get_root_path(import_name):
    """Returns the path to a package or cwd if that cannot be found.  This
    returns the path of a package or the folder that contains a module.
    """
    # Module already imported and has a file attribute.  Use that first.
    mod = sys.modules.get(import_name)
    if not mod:
        __import__(import_name)
        mod = sys.modules[import_name]

    if mod and hasattr(mod, "__file__"):
        return os.path.dirname(os.path.abspath(mod.__file__))

    raise Exception('No root path can be found for the provided package name %s' % import_name)


def resolve_path(dir_path, root_path):
    """Given a directory returns its absolute path,
    tries to resolve the path if its relative to the root path
    """
    if not dir_path:
        return None

    if os.path.isabs(dir_path):
        return dir_path

    return os.path.abspath(os.path.join(root_path, dir_path))


def load_type(module_path):
    """Given a filename tries to load the type class"""
    types = {}
    module = '.'.join(module_path[:-3].split('/')[-3:])

    mod = import_module(module)
    mod_name = mod.__name__.split('.')[-1]
    for name, object_ in inspect.getmembers(mod, inspect.isclass):
        if (object_.__name__ != 'BaseType'
                and issubclass(object_, BaseType)
                and name.lower() == mod_name.lower()):
            # get just the module name, without the package
            return object_

    return None


def load_modules(modules_path):
    """It imports all the modules inside a path
    e.g.
    usefull to pre-load all the modules from an __init__ file"""
    modules = []
    for module in glob.glob(modules_path):
        if os.path.isfile(module) and not module.endswith('__init__.py'):
            # remove .py, take just the 3 last words assuming the first is the package name
            # and change the / for .
            module_path = '.'.join(module[:-3].split('/')[-3:])
            modules.append(import_module(module_path))

    return modules
