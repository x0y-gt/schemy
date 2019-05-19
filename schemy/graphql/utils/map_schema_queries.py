from schemy.graphql.utils.map_schema_types import map_schema_types

__all__ = ["map_schema_resolvers"]

def map_schema_queries(schema, base='Query'):
    """Returns a list that contains all the path queries from a base object like Query of Mutation

    This is used to build a list of resolvers for a graphQl schema
    Example of return:
    [
    [{'field': 'publisher', 'list': False, 'nullable': True, 'type': 'Publisher'},
     {'field': 'books', 'list': True, 'nullable': True, 'type': 'Book'},
     {'field': 'authors', 'list': True, 'nullable': True, 'type': 'Author'}],
    ...
    [{'field': 'books', 'list': True, 'nullable': True, 'type': 'Book'},
     {'field': 'publisher', 'list': False, 'nullable': True, 'type': 'Publisher'}]
    ]
    """
    types = map_schema_types(schema, [])

    stack = []
    queries = _map_query_path(types['objects'], types['objects'][base], stack)
    return queries

def _map_query_path(types, base_type, stack):
    """Recursive function to get a list of all path queries"""
    queries = []
    for field_name, field in base_type['relationship'].items():
        # if it's a field that leave us to another type then...
        if field['type'] in types.keys():
            #add this query path
            queries.append([{'field':field_name, **field}])

            # if the field type is not already in the stack, this is to avoid an infinite recursion
            if field['type'] not in stack:
                stack.append(field['type'])
                sub_queries = _map_query_path(types, types[field['type']], stack)
                stack.pop()
                queries += [[{'field':field_name, **field}] + sub_query for sub_query in sub_queries]

    return queries
