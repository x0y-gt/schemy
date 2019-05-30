import click

from schemy.graphql import GraphQl
from schemy.cmd.sync import sync
from schemy.renders import Type, TypeMethod
from schemy.utils.storage import Storage

from pprint import pprint
import sys

@sync.command()
@click.pass_context
def types(ctx):
    """This command creates classes that represents GraphQl types
    each class has the necesarry methods to resolve the fields from
    the schema

    There are 4 query types that each type can resolve:
    - get type from root
    - get type from another type
    - get a list of type from root
    - get a list of type from another type
    """
    gql = GraphQl(ctx.obj['schema_path'])
    queries = gql.map_queries()
    pprint(queries)

    types = {} # a list that has all the objs to render each type
    for query in queries:
        last_field = query.pop()
        # creates or gets the type instance to render later
        if last_field['type'] not in types:
            new_type = types[last_field['type']] = Type(last_field['type'])
        else:
            new_type = types[last_field['type']]

        # The case when the parent object is Query
        if not len(query):
            new_method = TypeMethod(last_field['field'])
            new_method.parent = 'Query'
            new_method.list = last_field['list']
            new_method.args = last_field['args']
            new_method.nullable = last_field['nullable']
            #print(last_field['type']+'.get(query)'+str(last_field['args']))
            new_type.add_method(new_method)
        # The case then the parent object is another type obj
        #else:
        #    #pprint(query[-1])
        #    if last_field['list']:
        #        new_type.add_list_getter(
        #                last_field['field'],
        #                parent=query[-1]['type'],
        #                nullable=last_field['nullable']
        #            )
        #        #print(last_field['type']+'.list('+query[-1]['type']+')')
        #    else:
        #        new_type.add_getter(
        #                last_field['field'],
        #                parent=query[-1]['type'],
        #                nullable=last_field['nullable']
        #            )
                #print(last_field['type']+'.get('+query[-1]['type']+')')

    pprint(types)
    for t in types.values():
        print(t.render())
    sys.exit()
