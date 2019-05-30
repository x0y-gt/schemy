from schemy.renders import Base

from pprint import pprint

__all__ = ['TypeMethod']


class TypeMethod(Base):
    """This class defines a method implementation for a type class"""
    METHOD = """    def {name}(parent, info{args}):
{content}

"""

    def __init__(self, name):
        super(TypeMethod, self).__init__(name)
        self.parent = None
        self.args = {}
        self.list = False
        self.nullable = False
        self.line_indentation = '\n' + (' ' * 8)

    def render(self):
        code = ['        query = self.query()']
        args = []

        if self.args and 'id' in self.args and len(self.args) == 1:
            code.append('return query.get(Id)')
            args.append('Id')
        else:
            if self.args:
                filters = []
                for arg_name, arg_type in self.args.items():
                    args.append(arg_name)
                    filters.append('{name} = {name}'.format(name=arg_name))
                code.append('query.filter_by({filters})'\
                        .format(filters=', '.join(filters)))

            if self.list:
                code.append('return query.all()')
            else:
                code.append('return query.first()')

        args_code = ', ' + args[0] if len(args) == 1 else ', '.join(args)
        return self.METHOD.format(
            name=self.name,
            args=args_code,
            content=self.line_indentation.join(code)
        )
