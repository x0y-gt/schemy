import click

@click.group()
@click.option('-s', '--schema_path', default="api/schema.sdl", required=False, prompt='Path to schema', help='The relative path from the projects folder to schema.')
@click.pass_context
def sync(ctx, schema_path):
    ctx.obj = {
        'schema_path': schema_path
    }

from schemy.cmd.sync_models import models
from schemy.cmd.sync_types import types
from schemy.cmd.sync_factories import factories
