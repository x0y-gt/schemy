import click
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

    for type_name, type_metadata in types['objects'].items():
        model = SAModel(type_name)
        for field_name, field_data in type_metadata['field'].items():
            field = SAColumn(field_name)
            field.set_type(gql2alchemy(field_data['type']))
            model.add_column(field)

        for field_name, field_data in type_metadata['relationship'].items():
            field = SAColumn(field_name)
            field.set_type(gql2alchemy(field_data['type']))
            if field_data['list']:
                field.set_relationship()
            model.add_column(field)
        print(model.render())


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

