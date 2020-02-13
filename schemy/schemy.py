import inspect

from graphql.execution import default_field_resolver
from graphql.type.definition import get_named_type, GraphQLScalarType

#from schemy import Query, Response
from schemy.graphql import GraphQl
from schemy.utils import load_modules
from schemy.types import BaseType


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
        self._resolver = (lambda s:\
                          lambda root, info, **args: s.resolve_type(root, info, **args) #pylint: disable=unnecessary-lambda
                         )(self)
        self._types = {}
        self.bootstrap()

    def bootstrap(self):
        """Loads default middlewares like logging and extra stuff"""
        pass

    def build(self, sdl_path: str = None):
        """Parse and builds a GraphQl Schema File"""
        path = sdl_path if sdl_path else self.sdl_path
        if not self.graphql:
            gql = GraphQl(path)
            gql.build()
            self.graphql = gql

        #pre-load types
        self._types = self._load_types()

        return self

    def schema(self):
        if self.graphql:
            return self.graphql.schema
        return None

    def get_resolver(self):
        return self._resolver

    def resolve_type(self, root, info, **args):
        """This method resolves each field of each type
        If it's a scalar then the default resolver(from the graphql package) is executed,
        if not, we look for a method in our defined types"""
        return_type = get_named_type(info.return_type)
        # if return type is scalar then resolve with default resolver
        if isinstance(return_type, GraphQLScalarType):
            return default_field_resolver(root, info, **args)

        # Looking for the type in charge to resolve the query/mutation
        if info.parent_type.name == 'Query' or info.parent_type.name == 'Mutation':
            type_name = return_type.name
        else:
            type_name = info.parent_type.name

        type_class = self.get_type(type_name)
        value = None
        if type_class:
            type_instance = type_class(self.datasource)

            # Look for same field name as defined in the Query or Mutation root objects
            if info.parent_type.name == 'Query':
                prefix = 'resolve_'
                field_name = info.field_name.lower()
            elif info.parent_type.name == 'Mutation':
                prefix = 'resolve_mutation_'
                field_name = info.field_name.lower()
            else:
                prefix = 'resolve_type_'
                field_name = return_type.name.lower()
            field_name = '{prefix}{name}'.format(
                prefix=prefix,
                name=field_name
            )

            # find and execute the resolver
            if hasattr(type_instance, field_name):
                try:
                    query_resolver = getattr(type_instance, field_name)
                    #if info.parent_type.name == 'Query':
                    #    value = query_resolver(**args)
                    #else:
                    value = query_resolver(root, info, **args)
                    del type_instance
                    #self.datasource.session.commit()
                except:
                    self.datasource.session.rollback()
                    raise
            else:
                print('log.warning: resolver {type_name}.{field_name} not found'.format(
                    type_name=type_class.__name__,
                    field_name=field_name
                ))

        return value

    def get_type(self, type_):
        """Return a Type module if exists, None overwise"""
        type_name = type_.lower()
        return self._types[type_name] if type_name in self._types else None

    def _load_types(self):
        """Load all the types into the _types property"""
        types = {}
        mods = load_modules(self.types_path + '/*.py')
        for type_ in mods:
            type_name = type_.__name__.split('.')[-1]
            for name, object_ in inspect.getmembers(type_, inspect.isclass):
                if (object_.__name__ != 'BaseType'
                        and issubclass(object_, BaseType)
                        and name.lower() == type_name.lower()):
                    # get just the module name, without the package
                    key = type_.__name__.split('.')[-1]
                    types[key] = object_

        return types
