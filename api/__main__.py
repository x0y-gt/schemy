import sys
import click
# Remove schemy dir from sys path, it interfere when loading graphql
# sys.path = [d for d in sys.path if d != 'schemy']

@click.group()
def schemy():
  click.echo('Schemy command line tool')

from schemy.cmd.sync import sync
from schemy.cmd.seed import seed

schemy.add_command(sync)
schemy.add_command(seed)

schemy()
