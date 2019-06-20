import os
import inspect

from schemy.utils import Singleton
from schemy.utils import load_modules

class Config(dict, metaclass=Singleton):
    """Class to load the API configuration"""
    __data = {}

    def __init__(self, root_pkg):
        """Load all the configuration into the instance"""
        super().__init__()
        config_dir = os.path.join(root_pkg, 'config')
        self.__load_config(config_dir)

    def __load_config(self, config_dir):
        """This method loads all the configuration files in the config package
        for each module try to load a constant with the modules name
        containing a dict with configuration data, then it adds a prefix for
        every key in the dict
        for example:
        # file app.py
        APP = {'SECRET': '#$%47#$%'}
        ---
        would convert to:   APP_SECRET
        and save it to its __data class property"""
        modules = load_modules(config_dir + '/*.py')
        for module in modules:
            config_const_name = inspect.getmodulename(module.__file__).upper()
            if hasattr(module, config_const_name):
                data = getattr(module, config_const_name)
                prefix = config_const_name + '_'
                self.__data.update(
                    {prefix + k: v for (k, v) in data.items()}
                )

    def __getitem__(self, key):
        return self.__data[key]

    def __setitem__(self, key, value):
        self.__data[key] = value

    def __delitem__(self, key):
        del self.__data[key]

    def __contains__(self, key):
        return key in self.__data

    def __len__(self):
        return len(self.__data)

    def __repr__(self):
        return repr(self.__data)
