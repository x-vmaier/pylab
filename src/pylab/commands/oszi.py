import click


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
    from pylab.implementations.oszi import oszi_read_impl
    oszi_read_impl(ip_address, start_channel, end_channel, autoscale, screenshot, waveform, delay)


@oszi.command()
def list():
    from pylab.implementations.oszi import oszi_list_impl
    oszi_list_impl()
