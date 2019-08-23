import os

import click

from schemy.graphql import GraphQl
from schemy.cmd.main import main
from schemy.renders import Factory
from schemy.renders import FactoryColumn
from schemy.utils.storage import Storage

FACTORIES_DIR = 'database/factories'


@main.command()
@click.pass_context
def sync_factories(ctx):
    """Iterate over all the types defined in the schema to generate factories for each
    type to them be able to generate dummy data"""
    if not ctx.obj['schema_path'] and not ctx.obj['project_path']:
        click.echo('ERROR: this command must be executed from the root directory of a schemy API')
        return 1

    gql = GraphQl(ctx.obj['schema_path'])
    types = gql.map_types()

    factories = {}
    factories_dir = os.path.join(ctx.obj['project_path'], FACTORIES_DIR)
    #factories_base = ctx.obj['project_name'] + '.database.factories'
    code = []
    for type_name, type_metadata in types['objects'].items():
        factory = Factory(type_name)
        add_to_seed = True

        # adding columns definitions
        for field_name, field_data in type_metadata['field'].items():
            field = FactoryColumn(field_name, field_data['type'])
            factory.add_column(field)

        # adding relationships definitions to the factory
        for field_name, field_data in type_metadata['relationship'].items():
            #look for the relationship on the other object
            rel_object_type = field_data['type']
            rels = list(filter(
                lambda rel: rel[1]['type'] == type_name,
                types['objects'][rel_object_type]['relationship'].items()
            ))
            if rels:
                rel_field_name, rel_field_data = rels[0]
            else:
                #We can't generate models if the objects doesn't have a reference to each other
                click.echo('ABORTING: Missing reference to type {} from type {}'
                           .format(type_name, rel_object_type))
                return 1

            field = FactoryColumn(field_name, type_name)
            field.backref = rel_field_name
            if field_data['list'] and rel_field_data['list']:
                #many to many relationship, we need to create another factory
                add_to_seed = False
                field.many_to_many = rel_object_type
            elif field_data['list']:
                #one to many relationship, I'm the parent
                field.one_to_many = rel_object_type
            elif rel_field_data['list']:
                #many to one relationship, I'm the child
                add_to_seed = False
                field.many_to_one = rel_object_type
            else:
                #one to one
                add_to_seed = False
                field.one_to_one = rel_object_type
            factory.add_relationship(field)

        factories[type_name] = factory
        # Call the factories if they're not related by many to many
        if add_to_seed:
            code.append("\n    from PACKAGE_NAME.database.factories.{name} import {factory}Factory".format(
                name=type_name.lower(),
                factory=type_name
            ))
            loop = """    for _ in range(randint(2, 5)):
        {factory}Factory.create()
        factories.stack = {{'_owner':{{}}}}"""
            code.append(loop.format(factory=type_name))
            code.append('    datasource.session.commit()')

    # Render all factories and save them
    for factory in factories.values():
        with Storage(os.path.join(factories_dir, factory.name.lower() + '.py'), 'w') as f_file:
            f_file.content = factory.render(project_name=ctx.obj['project_name']) #auto saving
        click.echo("Generating %s data source class" % factory.name)

    #
    code.insert(0, 'from PACKAGE_NAME.model import datasource')
    code.insert(1, 'from random import randint')
    code.insert(2, 'import PACKAGE_NAME.database.factories as factories')
    code.insert(3, '\ndef seed():')
    code.insert(4, '\n    factories.init()')
    code.append("\nif __name__ == '__main__':")
    code.append("    seed()")
    with Storage(os.path.join(factories_dir, 'seed.py'), 'w') as f_main:
        f_main.content = '\n'.join(code).replace('PACKAGE_NAME', ctx.obj['project_name'])
    click.echo("Updating seed command")
