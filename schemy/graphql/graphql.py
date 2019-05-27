from os.path import abspath

from graphql import build_schema

from schemy.graphql.utils import map_schema_types, map_schema_queries

__all__ = ['GraphQl']


class GraphQl:
    def __init__(self, sdl_path:str = None):
        self.sdl = None
        self.schema = None
        self.sdl_path = sdl_path
        if self.sdl_path:
            self.build()

    def build(self, sdl_path=None):
        self.schema = None
        if not sdl_path:
            sdl_path = self.sdl_path
        try:
            filepath = abspath(sdl_path)
            with open(filepath, 'r') as f:
                self.sdl = f.read()
                self.schema = build_schema(self.sdl)
                f.close()
        except OSError:
            raise OSError('GraphQl Schema file not found')
        except TypeError:
            raise TypeError('The GraphQl Schema is not valid')

        return self.schema

    def map_types(self, ignore=['Query', 'Mutation']):
        if self.schema:
            return map_schema_types(self.schema, ignore)
        else:
            raise TypeError('Schema is empty, you must load a valid schema')

    def map_queries(self, base='Query'):
        if self.schema:
            return map_schema_queries(self.schema, base)
        else:
            raise TypeError('Schema is empty, you must load a valid schema')
