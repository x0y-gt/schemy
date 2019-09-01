from schemy.renders import Base

__all__ = ['TypeMethod']


class TypeMethod(Base): #pylint: disable=too-many-instance-attributes,too-few-public-methods
    """This class defines a method implementation for a type class"""

    METHOD = """    def {name}(self, {args}):{content}

"""

    def __init__(self, name):
        super(TypeMethod, self).__init__(name)
        self._method_name = ''
        self.parent = None
        self.type = None
        self.relationship = False
        self.args = {}
        self.list = False
        self.nullable = False
        self.resolve_type = False

        self._method_name = ''
        self._line_indentation = '\n' + (' ' * 8)
        self._code = []
        self._method_args = ['info']

    def _render_get_id(self):
        """Returns the code to render the methods when
        the parent is Query and returns the element by Id"""
        self._method_name = 'resolve_{name}'.format(name=self.name.lower())
        self._code.insert(0, '"""This method is to return an element by Id')
        self._code.insert(1, 'it is called from the root obj Query"""')
        self._code.insert(2, 'query = self.query()')
        self._code.append('return query.get(id)')

        self._method_args.insert(0, 'Query')
        self._method_args.append('id')

    def _render_with_args(self):
        """Returns the code to render the methods when
        the parent is Query and returns elements filter by args"""
        self._method_name = 'resolve_{name}'.format(name=self.name.lower())

        self._code.insert(0, '"""This method is to return elements filtered by')
        self._code.insert(1, 'the arguments defined in the root obj Query field')
        self._code.insert(2, 'WARNING: Assuming the arguments exists as foreign keys in')
        self._code.insert(3, 'defined fields, "Id" added as postfix to arguments used as keys"""')
        self._code.append('query = self.query()')

        filters = ['{name}Id={name}'.format(name=arg_name) for arg_name in self.args]

        self._code.append('query.filter_by({filters})'.format(filters=', '.join(filters)))
        self._code.append('return query.all()')

        self._method_args.insert(0, 'Query')
        self._method_args.extend(self.args)

    def _render_without_args(self):
        """Returns the code to render the methods when
        the parent is Query and returns elements filter by args"""
        self._method_name = 'resolve_{name}'.format(name=self.name.lower())

        self._code.insert(0, '"""This method is to return a list of elements')
        self._code.insert(1, 'from query defined in the root obj Query"""')
        self._code.append('query = self.query()')
        self._code.append('return query.all()')

        self._method_args.insert(0, 'Query')

    def _render_resolve_type(self):
        """Returns the code to render the methods when
        the parent is another obj different than the root obj Query"""
        self._method_name = 'resolve_type_{name}'.format(name=self.type.lower())

        self._code.append('return {}.{}'.format(self.parent.name, self.name))
        if self.relationship:
            # for many to many relationships
            self._code.insert(0, '"""This method resolves a many to many relationship')
            self._code.insert(1, 'with the type {parent}"""'.format(parent=self.type))
        elif self.list:
            # for many to one relationships
            self._code.insert(0, '"""This method resolves a many to one relationship')
            self._code.insert(1, 'with the type {parent}"""'.format(parent=self.type))
        else:
            self._code.insert(0, '"""This method resolves a one to many relationship')
            self._code.insert(1, 'with the type {parent}"""'.format(parent=self.type))

        self._method_args.insert(0, self.parent.name)

    def render(self):
        """Renders the current method choosing between 2 main different approaches
        - One are methods that resolves a field from the root Query obj
        - The others are methods that resolves a type"""

        if not self.resolve_type:
            #Render a resolve field from root(Query) method
            if len(self.args) == 1 and 'id' in self.args:
                # unique case when it needs to respond getting an element by Id
                self._render_get_id()
            elif self.args:
                # For queries that have arguments in the root obj Query
                self._render_with_args()
            else:
                # For queries that have doesn't have arguments in the root obj Query
                self._render_without_args()
        else:
            #Render a resolve type method
            self._render_resolve_type()

        return self.METHOD.format(
            name=self._method_name,
            args=', '.join(self._method_args),
            content=self._line_indentation + self._line_indentation.join(self._code)
        )
