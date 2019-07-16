import os

import click

from schemy.cmd.main import main
from schemy.utils.storage import Storage


TEMPLATES_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    '..',
    'templates'
))
DIR_MODE = 0o755

@main.command()
@click.argument('name')
@click.argument('directory', default='')
@click.option('--template', default='default')
@click.pass_context
def new_project(ctx, name, directory, template):
    """Generates a new schemy project with the given name"""
    project_name = name #TODO - Verify name

    # Define the project directory
    cwd = os.getcwd()
    project_directory = os.path.join(cwd, directory if directory else project_name)
    if os.path.exists(project_directory):
        click.echo(
            "ERROR: The directory %s already exists, can't create new project" % project_directory
        )
        return 1
    click.echo('Creating project directory')
    os.mkdir(project_directory, mode=DIR_MODE)

    click.echo('Creating project structure...')
    template_directory = os.path.join(TEMPLATES_DIR, template)
    with click.progressbar(os.walk(template_directory)) as template_files:
        for dirpath, _subdirs, files in template_files:
            # Create each directory in the template, except the root dir already created
            _, current_dirpath = dirpath.split(template)
            new_dirpath = project_directory
            if current_dirpath:
                new_dirpath = os.path.join(
                    project_directory,
                    current_dirpath if current_dirpath[0] != '/' else current_dirpath[1:]
                )
                new_dirpath = new_dirpath.replace('project_name', project_name)
                os.mkdir(new_dirpath, mode=DIR_MODE)

            # Create each file in the template, replacing the project_name var
            if files:
                for file in files:
                    source_path = os.path.join(dirpath, file)
                    dest_path = os.path.join(new_dirpath, file)
                    with Storage(source_path, 'r') as source, Storage(dest_path, 'x') as dest:
                        # TODO change to a templating engine
                        dest.content = source.content.replace('{project_name}', project_name)

    click.echo('Now you can build your api in {}'.format(project_directory))
    click.echo('You can execute commands from there using: /> python {} CMD'.format(project_name))
    click.echo('Done.')
