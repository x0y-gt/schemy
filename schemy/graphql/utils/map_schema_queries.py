from graphql import get_named_type
from schemy.graphql.utils.map_schema_types import map_schema_types

from pprint import pprint

__all__ = ["map_schema_resolvers"]

def map_schema_queries(schema, base='Query'):
    """Returns a list that contains all the path queries from a base object like Query of Mutation

    :param base: can be Query or Mutation

    This is used to build a list of resolvers for a graphQl schema
    Example of return:
    [
    [{'field': 'publisher', 'list': False, 'nullable': True, 'type': 'Publisher', args: {}},
     {'field': 'books', 'list': True, 'nullable': True, 'type': 'Book', args: {}},
     {'field': 'authors', 'list': True, 'nullable': True, 'type': 'Author', args: {}}],
    ...
    [{'field': 'books', 'list': True, 'nullable': True, 'type': 'Book', args: {}},
     {'field': 'publisher', 'list': False, 'nullable': True, 'type': 'Publisher', args: {}}]
    ]
    """
    types = map_schema_types(schema, [])

    stack = []
    queries = _map_query_path(types['objects'], types['objects'][base], stack)
    #map arguments to root fields
    for query in queries:
        # root field if it only has one field in the path
        if len(query) == 1:
            query[0]['args'] = _get_args(schema.query_type.fields, query[0]['field'])

    return queries

def _map_query_path(types, base_type, stack):
    """Recursive function to get a list of all path queries"""
    queries = []
    for field_name, field in base_type['relationship'].items():
        # if it's a field that leave us to another type then...
        if field['type'] in types.keys():
            #add this query path
            queries.append([{'field':field_name, 'args':{}, **field}])

            # if the field type is not already in the stack, this is to avoid an infinite recursion
            if field['type'] not in stack:
                stack.append(field['type'])
                sub_queries = _map_query_path(types, types[field['type']], stack)
                stack.pop()
                # prepend current query path to the returned queries
                queries += [[{'field':field_name, 'args':{}, **field}] + sub_query for sub_query in sub_queries]

    return queries

def _get_args(fields, field):
    args = {}
    if field in fields and len(fields[field].args):
        args = [{arg_name: get_named_type(arg.type).name} for arg_name, arg in fields[field].args.items()]

    return args
