import inspect

from graphql import graphql_sync, format_error
from graphql.execution import default_field_resolver
from graphql.type.definition import get_named_type, GraphQLScalarType

#from schemy import Query, Response
from schemy.graphql import GraphQl
from schemy.utils import load_modules
from schemy.type import BaseType

from pprint import pprint


class Schemy:
    """This is the framework's main class.
    Basically it loads a graphql schema, process graphql queries that connects
    with resolvers in "Type" classes and returns the response"""

    def __init__(self, sdl_path):
        self.sdl_path = sdl_path
        self.types_path = './types'
        self.datasource = None
        self.graphql = None
        # define the resolver func as a lambda to have a reference to self
        # so we can have an easy access to the defined types
        self.resolver = (lambda s:\
                         lambda root, info, **args: s.resolve_type(root, info, **args)
                         )(self)
        self._types = {}
        self.bootstrap()

    def bootstrap(self):
        """Loads default middlewares like logging and extra stuff"""
        pass

    def build(self, sdl_path:str=None):
        """Parse and builds a GraphQl Schema File"""
        path = sdl_path if sdl_path else self.sdl_path
        if not self.graphql:
            gql = GraphQl(path)
            gql.build()
            self.graphql = gql

        #pre-load types
        self._types = self._load_types(self.types_path)

        return self

    #def handle(self, query: Query) -> Response:
    def handle(self, query):
        root = None
        context = {}
        variables = {}
        result = graphql_sync(
            self.graphql.schema,
            query,
            root,
            context,
            variables,
            field_resolver=self.resolver
        )
        #middleware=[LogMiddleware('logware')])
        return result

    def resolve_type(self, root, info, **args):
        """This method resolves each field of each type
        If it's a scalar then the default resolver(from the graphql package) is executed,
        if not, we look for a method in our defined types"""
        return_type = get_named_type(info.return_type)
        # if return type is scalar then resolve with default resolver
        if isinstance(return_type, GraphQLScalarType):
            return default_field_resolver(root, info, **args)

        return_type_name = return_type.name
        type_class = self.get_type(return_type_name)
        value = None
        if type_class:
            type_instance = type_class(self.datasource)

            # Look for same field name as defined in the Query root object
            if info.parent_type.name == 'Query':
                prefix = 'resolve_'
                field_name = '{prefix}{name}'.format(prefix=prefix, name=info.field_name)
            else:
                prefix = 'resolve_type_'
                field_name = '{prefix}{name}'.format(prefix=prefix, name=info.parent_type.name.lower())

            # find and execute the resolver
            if hasattr(type_instance, field_name):
                query_resolver = getattr(type_instance, field_name)
                #if info.parent_type.name == 'Query':
                #    value = query_resolver(**args)
                #else:
                value = query_resolver(root, info, **args)
                del type_instance
            else:
                print('log.warning: resolver {type_name}.{field_name} not found'.format(
                    type_name=type_class.__name__,
                    field_name=field_name
                ))

        return value

    def get_type(self, type_):
        """Return a Type module if exists if not, None"""
        type_name = type_.lower()
        return self._types[type_name] if type_name in self._types else None

    def _load_types(self, types_path):
        """Load all the types into the _types property"""
        types = {}
        mods = load_modules(types_path + '/*.py')
        for type_ in mods:
            for _name, object_ in inspect.getmembers(type_, inspect.isclass):
                if object_.__name__ != 'BaseType' and issubclass(object_, BaseType):
                    key = type_.__name__.split('.')[-1] # get just the module name, without the package
                    types[key] = object_

        return types
