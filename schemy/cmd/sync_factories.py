import os
import inspect
from functools import reduce

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
    if not ctx.obj['schema_path'] and not ctx.obj['project_path']:
        click.echo('ERROR: this command must be executed from the root directory of a schemy API')
        return 1

    gql = GraphQl(ctx.obj['schema_path'])
    types = gql.map_types()

    factories = {}
    type_name = None
    factories_dir = os.path.join(ctx.obj['project_path'], FACTORIES_DIR)
    factories_base = ctx.obj['project_name'] + '.database.factories'
    code = ['\ndef seed():']
    for type_name, type_metadata in types['objects'].items():
        factory = Factory(type_name)
        # adding columns definitions
        for field_name, field_data in type_metadata['field'].items():
            field = FactoryColumn(field_name, field_data['type'])
            factory.add_column(field)

        # adding the relationships to the factory
        many_to_many = False
        for field_name, field_data in type_metadata['relationship'].items():
            #look for the relationship on the other object
            rel_object_type = field_data['type']
            func_filter_type = (lambda x, obj:
                                obj[1]['type'] == type_name and obj or x)
            rel_field_name, rel_field_data = reduce(
                func_filter_type,
                types['objects'][rel_object_type]['relationship'].items()
            )

            #many to many relationship, we need to create another factory
            if field_data['list'] and rel_field_data['list']:
                many_to_many = True
                type_1ft = type_name.title()
                type_2nd = rel_object_type.title()
                if type_1ft <= type_2nd:
                    link_factory_name = '%s%s' % (type_1ft, type_2nd)
                else:
                    link_factory_name = '%s%s' % (type_2nd, type_1ft)

                field = FactoryColumn(field_name)
                field.one_to_many = '{base}.{factory}.{factory_class}'.format(
                    base=factories_base,
                    factory=link_factory_name.lower(),
                    factory_class=link_factory_name + 'Factory'
                )
                field.backref = type_name.lower()
                factory.add_relationship(field)

                # Create the link factory if not already created
                if link_factory_name not in factories:
                    link_factory = Factory(link_factory_name)

                    link_1 = FactoryColumn(type_name.lower())
                    link_1.many_to_one = type_1ft
                    link_1.backref = field_name + '=[]'

                    link_2 = FactoryColumn(rel_object_type.lower())
                    link_2.many_to_one = type_2nd
                    link_2.backref = rel_field_name + '=[]'

                    link_factory.add_column(link_1)
                    link_factory.add_column(link_2)

                    factories[link_factory_name] = link_factory
                    code.append("    from PACKAGE_NAME.database.factories.{name} import {factory}Factory".format(
                        name=link_factory_name.lower(),
                        factory=link_factory_name
                    ))
                    code.append("    {name}Factory.create_batch(randint(0,3))".format(
                        name=link_factory_name
                    ))
                    code.append('    datasource.session.commit()')

            #one to many relationship, I'm the parent
            elif field_data['list']:
                field = FactoryColumn(field_name)
                field.one_to_many = "{base}.{factory}.{factory_class}".format(
                    base=factories_base,
                    factory=rel_object_type.lower(),
                    factory_class=rel_object_type + 'Factory'
                )
                field.backref = rel_field_name
                factory.add_relationship(field)

            #many to one relationship, I'm the child, backref
            else:
                field = FactoryColumn(field_name)
                field.many_to_one = rel_object_type
                factory.add_relationship(field)

        factories[type_name] = factory
        # Call the factories if they're not related by many to many
        if not many_to_many:
            code.append("    from PACKAGE_NAME.database.factories.{name} import {factory}Factory".format(
                name=type_name.lower(),
                factory=type_name
            ))
            code.append("    {name}Factory.create_batch(randint(0,3))".format(
                name=type_name
            ))
            code.append('    datasource.session.commit()')

    # Render all models and save them
    for f in factories.values():
        with Storage(os.path.join(factories_dir, f.name.lower() + '.py'), 'w') as f_file:
            f_file.content = f.render(project_name=ctx.obj['project_name']) #auto saving
        click.echo("Generating %s data source class" % f.name)

    code.insert(0, 'from PACKAGE_NAME.model import datasource')
    code.insert(0, 'from random import randint')
    code.append("\nif __name__ == '__main__':")
    code.append("    seed()")
    with Storage(os.path.join(factories_dir, 'seed.py'), 'w') as f_main:
        f_main.content = '\n'.join(code).replace('PACKAGE_NAME', ctx.obj['project_name'])
    click.echo("Updating seed command")
