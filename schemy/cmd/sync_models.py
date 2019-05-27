import click
from functools import reduce
from schemy.config import MODELS_DIR
from schemy.graphql import GraphQl
from schemy.utils import gql2alchemy
from schemy.cmd.sync import sync
from schemy.renders import SAModel, SAColumn
from schemy.utils.storage import Storage

@sync.command()
@click.pass_context
def models(ctx):
    gql = GraphQl(ctx.obj['schema_path'])
    types = gql.map_types()

    #TODO to improve later to add the functionality to create different types of models
    Model = SAModel
    Column = SAColumn

    models = {}
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
            rel_field_name, rel_field_data = reduce(
                lambda x, obj: obj[1]['type']==type_name and obj or x,
                types['objects'][rel_object_type]['relationship'].items()
            )

            #many to many relationship, we need to create another model
            if field_data['list'] and rel_field_data['list']:
                o1 = type_name.title()
                o2 = rel_object_type.title()
                if o1 <= o2:
                    link_model_name = '%s%s' % (o1, o2)
                else:
                    link_model_name = '%s%s' % (o2, o1)

                field = SAColumn(field_name, link_model_name)
                field.relationship = True
                field.backref = type_name.lower()
                model.add_relationship(field)

                # Create the link model if not already created
                if link_model_name not in models:
                    link_model = Model(link_model_name)

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

                    models[link_model_name] = link_model

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

        models[type_name] = model

    # Render all models and save them
    for model in models.values():
        with Storage(MODELS_DIR + '/' + model.name.lower() + '.py') as model_file:
            model_file.content = model.render() #saving just when assigning the content
        click.echo("Generating %s model class" % model.name)
