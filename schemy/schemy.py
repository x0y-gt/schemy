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
        graphql_type_to_return = get_named_type(info.return_type)
        graphql_parent_type = info.parent_type

        #get the class in charge of resolve the current field
        resolver_class = self._get_resolver_class(
            not root,
            graphql_type_to_return,
            graphql_parent_type
        )

        if not resolver_class and not isinstance(graphql_type_to_return, GraphQLScalarType):
            print('log.warning: resolver class {type_name} not found'.format(
                type_name=resolver_class.__name__
            ))
            raise Exception('Resolver class does not exist')

        resolver_class_instance = resolver_class(self.datasource)
        resolver_method_name = self._get_resolver_method(
            graphql_type_to_return,
            graphql_parent_type,
            info.field_name
        )

        # find and execute the resolver
        if not hasattr(resolver_class_instance, resolver_method_name):
            if isinstance(graphql_type_to_return, GraphQLScalarType):
                return default_field_resolver(root, info, **args)

            print('log.warning: resolver {type_name}.{resolver_method} not found'.format(
                type_name=resolver_class.__name__,
                resolver_method=resolver_method_name
            ))
            raise Exception('Resolver not found')

        try:
            query_resolver = getattr(resolver_class_instance, resolver_method_name)
            return query_resolver(root, info, **args)
            #self.datasource.session.commit()
        except:
            self.datasource.session.rollback()
            raise

    def _get_resolver_class(self, root, return_type, parent_type):
        """Return a Type module if exists, None overwise"""

        # Looking for the resolver class in charge to resolve the query/mutation
        if root and not isinstance(return_type, GraphQLScalarType):
            resolver_class_name = return_type.name.lower()
        else:
            # the one to resolve is always the parent when I'm now quering from the root
            # or I'm a scalar
            resolver_class_name = parent_type.name.lower()

        return self._types[resolver_class_name] if resolver_class_name in self._types else None

    def _get_resolver_method(self, return_type, parent_type, field_name):
        """Returns the name of the method to be called in order to resolve the query
        :returns: string
        """
        # Look for same field name as defined in the Query or Mutation root objects
        if parent_type.name == 'Query' or isinstance(return_type, GraphQLScalarType):
            prefix = 'resolve_'
            resolver_method = field_name.lower()
        elif parent_type.name == 'Mutation':
            prefix = 'resolve_mutation_'
            resolver_method = field_name.lower()
        else:
            prefix = 'resolve_type_'
            resolver_method = return_type.name.lower()

        return '{prefix}{name}'.format(
            prefix=prefix,
            name=resolver_method
        )

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
