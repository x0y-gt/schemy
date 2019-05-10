import sys
import click
# Remove schemy dir from sys path
sys.path = [d for d in sys.path if d != 'schemy']

@click.group()
def schemy():
  click.echo('Schemy command line tool')

from schemy.cmd.sync import sync

schemy.add_command(sync)

schemy()
