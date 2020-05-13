import inspect
import os
import asyncio

from aiohttp import web
from aiohttp_graphql import GraphQLView
import aiohttp_cors
from graphql.execution import default_field_resolver
from graphql.type.definition import get_named_type, is_leaf_type
from dotenv import load_dotenv

#from schemy import Query, Response
from schemy.graphql import GraphQl
from schemy.types import BaseType
from schemy.config import Config
from schemy.logging import create_logger
from schemy.helpers import get_root_path, resolve_path, load_type
from schemy.datasources import Datasource


class Schemy:
    """This is the framework's main class.
    Basically it loads a graphql schema, process graphql queries that connects
    with resolvers in "Type" classes and returns the response"""

    # Absolute path location to where to find the .env file
    # Schemy also tries to look for the filename from the API_DOTENV environment variable
    dotenv_filename = None

    # Location relative to the root path or absolute to where the config files are
    config_path = './config'

    # Location relative to the root path or absolute to where the models are
    models_path = './models'

    # Location relative to the root path or absolute to where the types are
    types_path = './types'

    # Location relative to the root path or absolute to where the services are
    services_path = './services'

    # Location relative to the root path or absolute to where the inputs are
    inputs_path = './inputs'

    # Location relative to the root path or absolute to where the factories are
    factories_path = './database/factories'

    # Absolute location of the package in the filesystem
    root_path = None

    # dict with the default values for the config
    default_config = {
        'API_ENV': 'local',             #local|stage|prod
        'API_PORT': 7777,
        'API_GRAPHQL_PATH': '/graphql',
        'API_CORS': False,
        'API_SCHEMA_FILENAME': './schema.sdl',
        'DATABASE_CONNECTION': None,
        'LOGGING': {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
                },
            },
            'handlers': {
                'default': {
                    'level': 'DEBUG',
                    'formatter': 'standard',
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stdout',
                },
                'file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'INFO',
                    'formatter': 'standard',
                    'filename': './logs/api.log',
                    'mode': 'a',
                    'maxBytes': 1024*1024*25, # 25MB,
                    'backupCount': 5,
                },
                'slack': {
                    'class': 'slack_logger.SlackHandler',
                    'level': 'ERROR',
                    'formatter': 'standard',
                    'url': os.getenv('SLACK_WEBHOOK', None),
                    'username':'Logger',
                },
            },
            'loggers': {
                'api': {  # default logger
                    'handlers': ['default'],
                    'level': 'DEBUG',
                    'propagate': False
                },
            }
        }
    }

    # instance to the graphql obj
    graphql = None

    # Datasource for access the DB
    datasource = None

    def __init__(self, api_name):
        """Basically this init resolves all the paths and core variables need it for the
        execution of the api, the most important to resolve:
        - The root path based on the api name(basically the name package name)
        - The .env file
        - The config files to resolve all the other important paths
        """
        self.api_name = api_name

        # Call a helper to get us the root path
        self.root_path = get_root_path(self.api_name)

        # load variables from dotenv if available
        self._load_dotenv()

        # load config files
        self.config = self.load_config()

        # resolving classes paths
        self.models_path = resolve_path(self.models_path, self.root_path)
        self.types_path = resolve_path(self.types_path, self.root_path)
        self.services_path = resolve_path(self.services_path, self.root_path)
        self.inputs_path = resolve_path(self.inputs_path, self.root_path)
        self.factories_path = resolve_path(self.factories_path, self.root_path)

        # define the resolver func as a lambda to have a reference to self
        # so we can have an easy access to the defined types
        #self._resolver = (lambda s:\
        #                  lambda root, info, **args: s.resolve_type(root, info, **args) #pylint: disable=unnecessary-lambda
        #                 )(self)
        self.bootstrap()


    def bootstrap(self):
        """Define directories, middlewares, config and logger"""
        if 'DATABASE_CONNECTION' in self.config:
            # setup datasource using sqlalchemy
            self.datasource = Datasource(self.config.get('DATABASE_CONNECTION'))

        self.logger = create_logger(self.config.get('LOGGING'))


    def _load_dotenv(self):
        """Load the variables from .env if file available
        """
        if not self.dotenv_filename:
            self.dotenv_filename = resolve_path(os.getenv('API_DOTENV', None), self.root_path)
            if not self.dotenv_filename:
                #Try to guess the filepath
                self.dotenv_filename = resolve_path('../.env', self.root_path)

        if os.path.isfile(self.dotenv_filename):
            load_dotenv(dotenv_path=self.dotenv_filename)   #, override=True


    def load_config(self):
        """Creates the config obj based on the Config class.
        It looks for the config files in the config path relative to the root path
        """
        config_path = resolve_path(self.config_path, self.root_path)

        return Config(config_path, self.default_config)


    def build(self):
        """Parse and builds a GraphQl Schema File"""
        if not self.graphql:
            sdl_path = resolve_path(self.config.get('API_SCHEMA_FILENAME'), self.root_path)
            gql = GraphQl(sdl_path)
            gql.build()
            self.graphql = gql

        return self


    def schema(self):
        """return the instance of the graqhql schema"""
        if self.graphql:
            return self.graphql.schema
        return None


    async def resolve_type(self, root, info, **args):
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

        if not resolver_class and not is_leaf_type(graphql_type_to_return):
            msg = 'resolver class %s not found' % resolver_class.__name__
            self.logger.warning(msg)
            raise Exception(msg)

		# instantiate class and get method resolver name
        resolver_class_instance = resolver_class(self.datasource)
        resolver_method_name = self._get_resolver_method(
            graphql_type_to_return,
            graphql_parent_type,
            info.field_name
        )

        # find and execute the resolver
        if not hasattr(resolver_class_instance, resolver_method_name):
            if is_leaf_type(graphql_type_to_return):
                return default_field_resolver(root, info, **args)

            msg = 'resolver method %s.%s not found' % (
                resolver_class.__name__,
                resolver_method_name
            )
            self.logger.warning(msg)
            raise Exception(msg)

        try:
            query_resolver = getattr(resolver_class_instance, resolver_method_name)
            if asyncio.iscoroutinefunction(query_resolver):
                respose = await query_resolver(root, info, **args)
            else:
                respose = query_resolver(root, info, **args)

            del resolver_class_instance
            return respose
            #self.datasource.session.commit()
        except Exception as e:
            self.logger.error(str(e), exc_info=True)
            if self.datasource:
                self.datasource.session.rollback()
            raise


    def _get_resolver_class(self, root, return_type, parent_type):
        """Return a Type module if exists, None overwise"""

        # Looking for the resolver class in charge to resolve the query/mutation
        if root and not is_leaf_type(return_type):
            resolver_class_name = return_type.name.lower()
        else:
            # the one to resolve is always the parent when I'm now quering from the root
            # or I'm a scalar
            resolver_class_name = parent_type.name.lower()

        resolver_class = load_type(os.path.join(self.types_path, resolver_class_name) + '.py')

        return resolver_class if resolver_class else None


    def _get_resolver_method(self, return_type, parent_type, field_name):
        """Returns the name of the method to be called in order to resolve the query
        :returns: string
        """
        # Look for same field name as defined in the Query or Mutation root objects
        if is_leaf_type(return_type):
            prefix = 'resolve_field_'
            resolver_method = field_name.lower()
        elif parent_type.name == 'Query':
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


    async def _resolver(self, root, info, **args):
        """Async resolver wrapper"""
        return await self.resolve_type(root, info, **args)


    def wsgi_app(self):
        """This method defines all the necesarry to be called from the wsgi"""
        self.build()
        app = web.Application()

        # configure route
        GraphQLView.attach(
            app,
            schema=self.schema(),
            field_resolver=self._resolver,
            batch=True,
            graphiql=True
        )

        if self.config.get('API_CORS', False):
            # enable CORS
            cors = aiohttp_cors.setup(app, defaults={
                "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers=("X-Custom-Server-Header",),
                    allow_headers=("X-Requested-With", "Content-Type"),
                    max_age=3600,
                )
            })
            #get_route = app.router.add_route('GET', '/graphql', handler, name='graphql')
            #post_route = app.router.add_route('POST', '/graphql', handler, name='graphql')

            #cors.add(get_route)
            #cors.add(post_route)

        return app


    def __call__(self):
        """The WSGI server calls the Flask application object as the
        WSGI application."""
        return self.wsgi_app()
