import click
from pylab.core.pipeline_processor import PipelineProcessor

def pipeline_run_impl(sim, meas, trigger, smooth, plot):
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
