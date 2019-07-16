import sys
import os
#changing the syspath to search for schemy modules in its parent folder
#if sys.path[0] == 'schemy':
#    sys.path[0] = os.path.abspath('./schemy/..')

import click

from schemy.cmd.main import main

from schemy.cmd.sync_models import sync_models
from schemy.cmd.sync_types import sync_types
from schemy.cmd.sync_factories import sync_factories
from schemy.cmd.seed import seed
from schemy.cmd.new_project import new_project

def run():
    sys.exit(main()) #pylint: disable=no-value-for-parameter

if __name__ == '__main__':
    run()
