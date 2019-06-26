import click

from schemy.graphql import GraphQl
from schemy.cmd.sync import sync
from schemy.renders import Type, TypeMethod
from schemy.utils.storage import Storage

import api.config as config


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

    types = {} # a list that has all the objs to render each type
    for query in queries:
        last_field = query.pop()
        # creates or gets the type instance to render later
        if last_field['type'] not in types:
            new_type = types[last_field['type']] = Type(last_field['type'])
        else:
            new_type = types[last_field['type']]

        method_name = last_field['field']
        relationship = False
        if not len(query):
            method_parent = 'Query'
        else:
            method_parent = query[-1]['type']
            relationship = True if query[-1]['list'] and last_field['list'] else False

        # create the method if the tuple parent, name doesn't exist
        if not new_type.get_method(method_name, method_parent):
            new_method = TypeMethod(method_name, new_type)
            new_method.parent = method_parent
            new_method.relationship = relationship
            new_method.list = last_field['list']
            new_method.args = last_field['args']
            new_method.nullable = last_field['nullable']
            new_type.add_method(new_method)

    root_dir = config.get('APP_ROOT_DIR')
    types_dir = config.get('APP_TYPES_DIR')
    # Render all types and save them
    for t in types.values():
        with Storage(root_dir + types_dir + '/' + t.name.lower() + '.py') as type_file:
            type_file.content = t.render() #saving just when assigning the content
        click.echo("Generating %s type class" % t.name)
