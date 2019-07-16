import os

import click

from schemy.utils.package_name import package_name


CONTEXT_SETTINGS = dict(
    default_map={},
    obj={
        'project_path': '',
        'schema_path': '',
        'project_name': '',
    }
)

@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def main(ctx):
    setup_path = os.path.join(os.getcwd(), 'setup.py')
    if os.path.isfile(setup_path):
        name = package_name(setup_path)
        project_path = os.path.join(os.getcwd(), name)
        schema_path = os.path.join(project_path, 'schema.sdl')
        if os.path.isfile(schema_path):
            ctx.obj['project_path'] = project_path
            ctx.obj['schema_path'] = schema_path
            ctx.obj['project_name'] = name

    click.echo('Schemy executing...')
