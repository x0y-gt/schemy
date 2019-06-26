import click

from api.database.factories import seed as seed_api

from schemy.cmd.sync import sync

@sync.command()
@click.pass_context
def seed(ctx):
    click.echo('Seeding database')
    seed_api()
