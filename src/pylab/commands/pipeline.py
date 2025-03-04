import click


@click.group()
def pipeline():
    """Data pipeline commands."""
    pass


@pipeline.command()
@click.option('-s', '--sim', type=click.Path(exists=True), required=True, help='Simulation data file.')
@click.option('-m', '--meas', type=click.Path(exists=True), required=True, help='Measurement channels file.')
@click.option('-t', '--trigger', type=float, default=0.01, help='Threshold for event detection.')
@click.option('-f', '--smooth', default=True, help='Apply smoothing before calculating derivative.')
@click.option('-p', '--plot', is_flag=True, help='Generate plots from the data.')
def run(sim, meas, trigger, smooth, plot):
    from pylab.implementations.pipeline import pipeline_run_impl
    pipeline_run_impl(sim, meas, trigger, smooth, plot)