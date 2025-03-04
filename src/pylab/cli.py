import click
from .commands.oszi import oszi
from .commands.pipeline import pipeline


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """PyLab - Laboratory Automation CLI Tool."""
    pass


cli.add_command(oszi)
cli.add_command(pipeline)

if __name__ == '__main__':
    cli()
