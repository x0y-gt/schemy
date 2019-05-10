import click
from schemy.schema import Schema
from schemy.cmd.sync import sync
from schemy.utils.map_schema_types import map_schema_types

from pprint import pprint


@sync.command()
@click.pass_context
def models(ctx):
    schema = Schema(ctx.obj['schema_path']).load()
    types = map_schema_types(schema)
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

