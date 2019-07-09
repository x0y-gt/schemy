import os

import click

from schemy.graphql import GraphQl
from schemy.cmd.main import main
from schemy.renders import Type, TypeMethod
from schemy.utils.storage import Storage


TYPES_DIR = 'type'

@main.command()
@click.pass_context
def sync_types(ctx):
    """This command creates classes that represents GraphQl types
    each class has the necesarry methods to resolve the fields from
    the schema
There are 4 query types that each type can resolve:
    - get type from root
    - get type from another type
    - get a list of type from root
    - get a list of type from another type
    """
    if not ctx.obj['schema_path'] and not ctx.obj['project_path']:
        click.echo('ERROR: this command must be executed from the root directory of a schemy API')
        return 1

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

    types_dir = os.path.join(ctx.obj['project_path'], TYPES_DIR)
    # Render all types and save them
    for t in types.values():
        with Storage(os.path.join(types_dir, t.name.lower() + '.py'), 'w') as type_file:
            type_file.content = t.render() #saving just when assigning the content
        click.echo("Generating %s type class" % t.name)
