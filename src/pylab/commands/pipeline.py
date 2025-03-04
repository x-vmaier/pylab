import click
from pylab.core.pipeline_processor import PipelineProcessor


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
    """Run a data processing pipeline with simulation and measurement data"""
    click.echo(f"Running pipeline with simulation data from: {sim}")
    click.echo(f"Using measurement data from: {meas}")

    click.echo("=== Data Pipeline Run ===")
    click.echo("Configuration:")
    click.echo(f"  - Simulation file: {sim}")
    click.echo(f"  - Measurement file {meas}")
    click.echo(f"  - Event threshold: {trigger}")
    click.echo(f"  - Smoothing: {'enabled' if smooth else 'disabled'}")
    click.echo(f"  - Plotting: {'enabled' if plot else 'disabled'}")

    try:
        processor = PipelineProcessor()
        processor.run(sim_file=sim, meas_file=meas,trigger=trigger, smooth=smooth)
        processor.save()

        if plot:
            processor.generate_plots()
            click.secho("Plots generated successfully", fg='green', bold=True)

        click.secho("Pipeline completed successfully", fg='green', bold=True)
    except Exception as e:
        click.secho(f"Error during pipeline execution: {e}", fg='red', bold=True)
