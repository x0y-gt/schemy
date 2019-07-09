import click


CONTEXT_SETTINGS = dict(
    default_map={},
    obj={
        'project_path': ''
    }
)

@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def main(ctx, project_path=''):
    click.echo('Schemy executing...')
