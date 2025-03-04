import click
import pyvisa
from ..core.oscilloscope import OscilloscopeReader
from ..utils.helpers import list_tcpip_resources, validate_ip_address


@click.group()
def oszi():
    """Oscilloscope interaction commands."""
    pass


@oszi.command()
@click.argument('ip_address')
@click.option('-c', '--start-channel', type=int, default=1, help='Starting channel number.')
@click.option('-e', '--end-channel', type=int, default=1, help='Ending channel number.')
@click.option('-a', '--autoscale', is_flag=True, help='Enable autoscaling.')
@click.option('-s', '--screenshot', type=str, default='./screenshot.png', help='Screenshot file path.')
@click.option('-w', '--waveform', type=str, default='./waveform.csv', help='Waveform data file path.')
@click.option('-d', '--delay', type=float, default=0.5, help='Acquisition delay in seconds.')
def read(ip_address, start_channel, end_channel, autoscale, screenshot, waveform, delay):
    """Read data from an oscilloscope at the specified IP address"""
    if not validate_ip_address(ip_address):
        click.secho(f"{ip_address} is not a valid IP address", fg='red', bold=True)
        exit(1)

    click.echo("=== Oscilloscope Data Read ===")
    click.echo(f"Target IP: {ip_address}")

    click.echo("Configuration:")
    click.echo(f"  - Channels: {start_channel} to {end_channel}")
    click.echo(f"  - Autoscaling {'enabled' if autoscale else 'disabled'}")
    click.echo(f"  - Screenshot path: {screenshot}")
    click.echo(f"  - Waveform path: {waveform}")
    click.echo(f"  - Acquisition delay: {delay}s")

    try:
        reader = OscilloscopeReader(ip_address)
        reader.read_channels(start_channel, end_channel, autoscale, delay)
        reader.save_screenshot(screenshot)
        reader.save_waveform(waveform)

        click.secho("Data successfully read from oscilloscope", fg='green', bold=True)
    except Exception as e:
        click.secho(f"Error during oscilloscope read: {e}", fg='red', bold=True)


@oszi.command()
def list():
    """List all available TCPIP instrument resources"""
    try:
        tcpip_resources = list_tcpip_resources()
        if not tcpip_resources:
            click.echo("No TCPIP instruments found on the network")
            return

        click.echo("Available TCPIP Instruments:")
        for res in tcpip_resources:
            click.echo(f"{res}")

    except pyvisa.VisaIOError as e:
        click.secho(f"VISA connection error: {e}", fg='red', bold=True)
    except Exception as e:
        click.secho(f"Unexpected error: {e}", fg='red', bold=True)
