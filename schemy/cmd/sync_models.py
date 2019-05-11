import click
from schemy.graphql.schema import Schema
from schemy.cmd.sync import sync

from pprint import pprint


@sync.command()
@click.pass_context
def models(ctx):
    schema = Schema(ctx.obj['schema_path'])
    types = schema.map_types()
    pprint(types)

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

