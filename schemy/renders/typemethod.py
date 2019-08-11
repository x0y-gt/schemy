from schemy.renders import Base

__all__ = ['TypeMethod']


METHOD = """    def {name}(self, {args}):{content}

"""

class TypeMethod(Base):
    """This class defines a method implementation for a type class"""

    def __init__(self, name, Type):
        super(TypeMethod, self).__init__(name)
        self._method_name = ''
        self.parent = None
        self.parent_field = None
        self.type = Type
        self.relationship = False
        self.args = {}
        self.list = False
        self.nullable = False
        self.line_indentation = '\n' + (' ' * 8)

    def _render_get_id(self, code, args):
        """Returns the code to render the methods when
        the parent is Query and returns the element by Id"""
        self._method_name = 'resolve_{name}'.format(name=self.name.lower())
        code.insert(0, '"""This method is to return an element by Id')
        code.insert(1, 'the method is called from the root obj Query"""')
        code.insert(2, 'query = self.query()')
        args.insert(0, 'Query')
        code.append('return query.get(id)')
        args.append('id')
        return code, args

    def _render_with_args(self, code, args):
        """Returns the code to render the methods when
        the parent is Query and returns elements filter by args"""
        self._method_name = 'resolve_{name}'.format(name=self.name.lower())
        code.insert(0, '"""This method is to return elements filtered by')
        code.insert(1, 'the arguments(if any) defined in the root obj Query"""')
        code.insert(2, 'query = self.query()')
        args.insert(0, 'Query')
        if self.args:
            filters = []
            for arg_name, arg_type in self.args.items():
                args.append(arg_name)
                filters.append('{name} = {name}'.format(name=arg_name))
            if filters:
                code.append('query.filter_by({filters})'\
                            .format(filters=', '.join(filters)))
        code.append('return query.all()')
        return code, args

    def _render_other_parent(self, code, args):
        """Returns the code to render the methods when
        the parent is another obj different than the root obj Query"""
        self._method_name = 'resolve_type_{name}'\
                            .format(name=self.parent.lower())
        args.insert(0, self.type.name)
        code.append('return {}.{}'.format(self.type.name, self.parent_field))

        if self.relationship:
            # for many to many relationships
            code.insert(0, '"""This method is resolve a many to many relationship')
            code.insert(1, 'with the type {parent}"""'.format(parent=self.parent))
        elif self.list:
            # for many to one relationships
            code.insert(0, '"""This method is resolve a many to one relationship')
            code.insert(1, 'with the type {parent}"""'.format(parent=self.parent))
        else:
            code.insert(0, '"""This method is resolve a one to many relationship')
            code.insert(1, 'with the type {parent}"""'.format(parent=self.parent))

        return code, args

    def render(self):
        code = []
        args = ['info'] # method default arguments

        if self.parent == 'Query' and len(self.args) == 1 and 'id' in self.args:
            # unique case when it needs to respond getting an element by Id
            code, args = self._render_get_id(code, args)
        else:
            if self.parent == 'Query':
                # For queries that have arguments in the root obj Query
                code, args = self._render_with_args(code, args)
            else:
                # for queries from another objs
                code, args = self._render_other_parent(code, args)

        return METHOD.format(
            name=self._method_name,
            args=', '.join(args),
            content=self.line_indentation + self.line_indentation.join(code)
        )
