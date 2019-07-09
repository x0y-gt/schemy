import os
import importlib.util

import click

from schemy.cmd.main import main

@main.command()
@click.pass_context
def seed(ctx):
    if not ctx.obj['schema_path'] and not ctx.obj['project_path']:
        click.echo('ERROR: this command must be executed from the root directory of a schemy API')
        return 1

    module_path = os.path.join(ctx.obj['project_path'], 'database', 'factories', 'seed.py')
    spec = importlib.util.spec_from_file_location("seed", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    print(dir(module))

    click.echo('Seeding database')
    #seed_api()
