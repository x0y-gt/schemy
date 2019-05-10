from graphql import build_schema
from schemy.config import ROOT_DIR

__all__ = ['Schema']

class Schema:
    def __init__(self, schema_path):
        self.sdl = None
        self.sdl_path = ROOT_DIR + '/' + schema_path

    def load(self):
        with open(self.sdl_path, 'r') as f:
            self.SDL=f.read()
            f.close()

        return build_schema(self.SDL)
