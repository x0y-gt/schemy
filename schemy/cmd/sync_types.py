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
        field = query.pop()
        field_name = field['field']
        field_type = field['resolves_type']

        relationship = False
        if not query:
            #if query is empty at this point, then we are dealing with a "resolve field" case
            type_name = field_type #'Query'
        else:
            #else we are dealing with a "resolve type" case
            type_name = field['type']
            relationship = bool(query[-1]['list'] and field['list'])

        # create and get the type instance to render
        if type_name not in types:
            types[type_name] = Type(type_name)
        type_ = types[type_name]

        # create the method if it doesn't exist
        if not type_.get_method(field_name):
            new_method = TypeMethod(field_name)
            new_method.type = field_type
            new_method.relationship = relationship
            new_method.list = field['list']
            new_method.args = field['args']
            new_method.nullable = field['nullable']
            #Render a resolve type method if not query from root
            new_method.resolve_type = bool(query)
            type_.add_method(new_method)


    types_dir = os.path.join(ctx.obj['project_path'], TYPES_DIR)
    # Render all types and save them
    for type_ in types.values():
        with Storage(os.path.join(types_dir, type_.name.lower() + '.py'), 'w') as type_file:
            type_file.content = type_.render(package_name=ctx.obj['project_name']) #auto saving
        click.echo("Generating %s type class" % type_.name)

    return 0
