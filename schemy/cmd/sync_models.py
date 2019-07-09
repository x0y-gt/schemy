import os
from functools import reduce

import click

from schemy.graphql import GraphQl
from schemy.utils import gql2alchemy
from schemy.cmd.main import main
from schemy.renders import SAModel, SAColumn
from schemy.utils.storage import Storage


MODELS_DIR = 'model'

@main.command()
@click.pass_context
def sync_models(ctx):
    if not ctx.obj['schema_path'] and not ctx.obj['project_path']:
        click.echo('ERROR: this command must be executed from the root directory of a schemy API')
        return 1

    gql = GraphQl(ctx.obj['schema_path'])
    types = gql.map_types()

    #TODO to improve later to add the functionality
    #to create different types of models
    Model = SAModel
    Column = SAColumn

    datasources = {}
    type_name = None
    for type_name, type_metadata in types['objects'].items():
        model = Model(type_name)
        # adding the columns for the model
        for field_name, field_data in type_metadata['field'].items():
            field = Column(field_name, gql2alchemy(field_data['type']))
            model.add_column(field)

        # adding the relationships to the model
        for field_name, field_data in type_metadata['relationship'].items():
            #look for the relationship on the other object
            rel_object_type = field_data['type']
            func_filter_type = (lambda x, obj:
                                obj[1]['type'] == type_name and obj or x)
            rel_field_name, rel_field_data = reduce(
                func_filter_type,
                types['objects'][rel_object_type]['relationship'].items()
            )

            #many to many relationship, we need to create another model
            if field_data['list'] and rel_field_data['list']:
                type_1ft = type_name.title()
                type_2nd = rel_object_type.title()
                if type_1ft <= type_2nd:
                    link_model_name = '%s%s' % (type_1ft, type_2nd)
                else:
                    link_model_name = '%s%s' % (type_2nd, type_1ft)

                field = SAColumn(field_name, link_model_name)
                field.relationship = True
                field.backref = type_name.lower()
                model.add_relationship(field)

                # Create the link model if not already created
                if link_model_name not in datasources:
                    link_model = Model(link_model_name)
                    link_model.imports.append('from sqlalchemy.orm import relationship')

                    link_id1 = Column(type_name.lower(), type_name)
                    link_id1.pk = True
                    link_id1.fk = '%s.id' % type_name.lower()
                    link_id1.backref = field_name

                    link_id2 = Column(rel_object_type.lower(), rel_object_type)
                    link_id2.pk = True
                    link_id2.fk = '%s.id' % rel_object_type.lower()
                    link_id2.backref = rel_field_name

                    link_model.add_column(link_id1)
                    link_model.add_column(link_id2)

                    datasources[link_model_name] = link_model

            #one to many relationship, I'm the parent
            elif field_data['list']:
                field = SAColumn(field_name, gql2alchemy(field_data['type']))
                field.relationship = True
                model.add_relationship(field)

            #many to one relationship, I'm the child
            else:
                field = SAColumn(field_name, gql2alchemy(field_data['type']))
                field.fk = '%s.id' % rel_object_type.lower()
                field.backref = rel_field_name
                model.add_relationship(field)

        datasources[type_name] = model

    # Render all models and save them
    models_dir = os.path.join(ctx.obj['project_path'], MODELS_DIR)
    for ds in datasources.values():
        with Storage(os.path.join(models_dir, ds.name.lower() + '.py'), 'w') as ds_file:
            ds_file.content = ds.render() #auto saving
        click.echo("Generating %s data source class" % ds.name)
