from graphql import build_schema
from schemy.config import ROOT_DIR
from schemy.graphql.utils.map_schema_types import map_schema_types
from pprint import pprint

__all__ = ['Schema']

class Schema:
    def __init__(self, schema_path):
        self.sdl = None
        self.schema = None
        self.sdl_path = ROOT_DIR + '/' + schema_path
        self.load()

    def load(self):
        self.schema = None
        try:
            with open(self.sdl_path, 'r') as f:
                self.sdl = f.read()
                self.schema = build_schema(self.sdl)
                f.close()
        except OSError:
            raise OSError('GraphQl Schema file not found')
        except TypeError:
            raise TypeError('The GraphQl Schema is not valid')

        return self.schema

    def map_types(self):
        if self.schema:
            return map_schema_types(self.schema)
        else:
            raise TypeError('Schema is empty, you must load a valid schema')
