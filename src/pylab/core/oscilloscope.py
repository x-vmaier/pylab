import time
import click
import pyvisa
from rigol1000z import Rigol1000z, EWaveformMode


class OscilloscopeReader:
    def __init__(self, ip_address):
        self.instrument = None
        self.ip_address = ip_address
        resource_str = f"TCPIP0::{ip_address}::INSTR"

        try:
            rm = pyvisa.ResourceManager()
            self.instrument = rm.open_resource(resource_str)
            idn = self.instrument.query("*IDN?").strip()
            click.echo(f"Connected to instrument: {idn}")
        except pyvisa.errors.VisaIOError as e:
            raise Exception(f"Could not connect to '{resource_str}'\nDetails: {e}")
        except Exception as e:
            raise Exception(f"Failed to open resource '{resource_str}': {e}")

    def read_channels(self, start_channel, end_channel, autoscale=False, delay=0.5, screenshot_path='screenshot.png', csv_path='data.csv'):
        """Read data from the oscilloscope"""
        channels = list(range(start_channel, end_channel + 1))
        with Rigol1000z(self.instrument) as scope:
            if autoscale:
                try:
                    #scope.ieee488.reset()
                    scope.autoscale()
                except Exception as e:
                    raise Exception(f"Failed to autoscale scope: {e}")

            try:
                # scope.run()
                for ch in channels:
                    scope[ch].enabled = True
            except Exception as e:
                raise Exception(f"Error configuring scope: {e}")

            time.sleep(delay)  # Wait for waveform to stabilize
            
            # try:
            #     scope.stop()  # Stop scope for data capture
            # except Exception as e:
            #     raise Exception(f"Could not stop scope cleanly: {e}")
            
            try:
                scope.get_screenshot(screenshot_path)
            except Exception as e:
                raise Exception(f"Error capturing screenshot: {e}")
            
            try:
                scope.get_data(EWaveformMode.Raw, csv_path)
            except Exception as e:
                raise Exception(f"Error saving waveform data: {e}")

            try:
                scope.run()  # Resume scope
            except Exception as e:
                raise Exception(f"Could not resume scope cleanly: {e}")
