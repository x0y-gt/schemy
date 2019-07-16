import click

from schemy.cmd.main import main

from schemy.cmd.sync_models import sync_models
from schemy.cmd.sync_types import sync_types
from schemy.cmd.sync_factories import sync_factories
from schemy.cmd.seed import seed
from schemy.cmd.new_project import new_project

if __name__ == '__main__':
    main() #pylint: disable=no-value-for-parameter
