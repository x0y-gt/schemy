from schemy.renders import Base
from schemy.renders.typemethod import TypeMethod

__all__ = ['Type']


class Type(Base):
    """This class defines a schema type to render type classes"""
    CLASS = """{imports}

__all__ = ['{name}']


class {name}(BaseType):

    DATASOURCE = {datasource}

{methods}
"""

    def __init__(self, name):
        super(Type, self).__init__(name)
        self.imports = ['from schemy.types import BaseType']
        self.methods = []
        self.datasource_name = name.title() + 'Model'
        self.imports.append('from api.models import ' + self.datasource_name)

    def add_method(self, method:TypeMethod):
        self.methods.append(method)
        return self

    def render(self):
        methods = ''

        for m in self.methods:
            methods += m.render()

        return self.CLASS.format(
                imports='\n'.join(self.imports),
                name=self.name,
                datasource=self.datasource_name,
                methods= methods
            )
