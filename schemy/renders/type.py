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
        self.imports = ['from schemy import BaseType']
        self.methods = []
        self.datasource_name = name.title() + 'Model'
        self.imports.append('from api.models import ' + self.datasource_name)

    def add_method(self, method:TypeMethod):
        """Adds a new method defined with the TypeMethod class"""
        if method.parent == 'Query':
            self.methods.insert(0, method)
        else:
            self.methods.append(method)
        return self

    def add_import(self, module):
        """Adds a new method defined with the TypeMethod class"""
        self.imports.append(module)
        return self

    def get_method(self, name, parent):
        """Returns the class of a method if it exists
        It's identified by the name|parent pair"""
        methods = [m for m in self.methods if name == m.name and parent == m.parent]
        return methods[0] if methods else None

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
