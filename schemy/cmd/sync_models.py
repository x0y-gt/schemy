import click
from functools import reduce
from schemy.graphql.schema import Schema
from schemy.graphql.types import gql2alchemy
from schemy.cmd.sync import sync
from schemy.classes.samodel import SAModel
from schemy.classes.sacolumn import SAColumn

from pprint import pprint

@sync.command()
@click.pass_context
def models(ctx):
    schema = Schema(ctx.obj['schema_path'])
    types = schema.map_types()

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

                if link_model_name not in models:
                    link_model = Model(link_model_name)
                    link_id1 = '%sId' % type_name.lower()
                    link_id2 = '%sId' % rel_object_type.lower()
                    link_model.add_column(Column(link_id1, 'Integer'))
                    link_model.add_column(Column(link_id2, 'Integer'))

                    models[link_model_name] = link_model
            #one to many relationship, I'm the parent
            elif field_data['list']:
                field = SAColumn(field_name, gql2alchemy(field_data['type']))
                field.relationship = True
                model.add_column(field)
            #many to one relationship, I'm the child
            else:
                field = SAColumn(field_name, gql2alchemy(field_data['type']))
                field.fk = True
                field.backref = rel_field_name
                model.add_column(field)

        models[type_name] = model

    # Render all models
    for m in models.values(): print(m.render())

    #for name, model in types.items():
    #    filepath = ROOT_DIR + "/model/" + name.lower() + ".py"
    #    if (os.path.isfile(filepath)):
    #        click.echo("Omitting %s model, file already exists" % name)
    #    else:
    #        click.echo("Generating %s model class" % name)
    #        _save_dotpy(
    #            filepath,
    #            model.render()
    #        )

