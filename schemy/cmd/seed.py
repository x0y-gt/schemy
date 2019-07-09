import click

#from api.database.factories import seed as seed_api

from schemy.cmd.main import main

@main.command()
@click.pass_context
def seed(ctx):
    click.echo('Seeding database')
    #seed_api()
