from graphql import graphql_sync, format_error
from graphql.execution.execute import default_field_resolver

#from schemy import Query, Response
from schemy.graphql import GraphQl

from pprint import pprint


class Schemy:
    """This is the framework's main class.
    Basically it loads a graphql schema, process graphql queries that connects
    with resolvers in "Type" classes and returns the response"""

    def __init__(self):
        self.graphql = GraphQl()
        self.bootstrap()

    def bootstrap(self):
        """Loads default middlewares like logging"""
        pass

    def build(self, sdl_path:str):
        """Parse and builds a GraphQl Schema File"""
        self.graphql.build(sdl_path)
        return self

    #def handle(self, query: Query) -> Response:
    def handle(self):
        query = """{
            book(id: "1") {
                name
                publisher {
                    name
                }
            }
        }"""
        root = None
        context = {}
        variables = {}
        result = graphql_sync(self.graphql.schema, query, root,
                              context, variables)
                              #field_resolver=field_resolver,
                              #middleware=[LogMiddleware('logware')])
        pprint(result)

    def resolve(self):
        pass
