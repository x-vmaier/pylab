import click
from pylab.commands.oszi import oszi
from pylab.commands.pipeline import pipeline


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """PyLab - Laboratory Automation CLI Tool."""
    pass


cli.add_command(oszi)
cli.add_command(pipeline)
