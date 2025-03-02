import time
import click
import pyvisa
import questionary
import pandas as pd
from Rigol1000z import Rigol1000z, EWaveformMode


def list_tcpip_resources() -> list:
    """
    Query the VISA resource manager for all TCPIP instruments.

    Returns:
        A list of resource strings that contain 'TCPIP'.
    """
    try:
        rm = pyvisa.ResourceManager()
        resources = rm.list_resources()
        tcpip_resources = [res for res in resources if "TCPIP" in res]
        return tcpip_resources
    except Exception as e:
        click.echo(f"Error listing VISA resources: {e}")
        return []


def select_instrument_resource() -> str:
    """
    List available TCPIP VISA resources and let the user select one,
    or allow manual entry if none is found.

    Returns:
        A VISA resource string (e.g. "TCPIP0::172.16.62.9::INSTR")
    """
    tcpip_resources = list_tcpip_resources()
    if not tcpip_resources:
        click.echo("No VISA TCPIP instruments found")
        ip = questionary.text("Enter instrument IP manually:").ask()
        return f"TCPIP0::{ip}::INSTR"

    selected = questionary.select(
        "Select an instrument:",
        choices=tcpip_resources + ["Enter manually"]
    ).ask()

    if selected == "Enter manually":
        ip = questionary.text("Enter instrument IP manually:").ask()
        return f"TCPIP0::{ip}::INSTR"

    return selected


def setup_instrument(resource_str: str) -> pyvisa.resources.Resource:
    """
    Open the VISA resource and verify the connection by querying its ID.

    Args:
        resource_str: The VISA resource string.

    Returns:
        The VISA instrument resource.

    Raises:
        SystemExit: If the connection to the instrument fails.
    """
    rm = pyvisa.ResourceManager()
    try:
        instrument = rm.open_resource(resource_str)
        idn = instrument.query("*IDN?").strip()
        click.echo(f"Connected to instrument: {idn}")
        return instrument
    except pyvisa.errors.VisaIOError as e:
        click.echo(
            f"Error: Could not connect to resource '{resource_str}'\n{e}")
        exit(1)
    except Exception as e:
        click.echo(
            f"Unexpected error while opening resource '{resource_str}': {e}")
        exit(1)


def configure_scope(scope: Rigol1000z,
                    channels: list,
                    autoscale: bool = True) -> None:
    """
    Reset and configure the oscilloscope for measurement.

    Args:
        scope: The Rigol1000z interface instance.
        channels: List of channel numbers to enable.
        autoscale: If True, reset and autoscale the scope.
    """
    if autoscale:
        try:
            scope.ieee488.reset()
            scope.autoscale()
        except Exception as e:
            click.echo(f"Warning: Failed to autoscale scope: {e}")

    try:
        scope.run()
        for ch in channels:
            scope[ch].enabled = True
    except Exception as e:
        click.echo(f"Error configuring scope: {e}")
        exit(1)


def capture_data(scope: Rigol1000z,
                 screenshot_path: str,
                 data_path: str,
                 acquisition_delay: float = 0.5) -> None:
    """
    Capture a screenshot and waveform data from the oscilloscope.

    Args:
        scope: The Rigol1000z interface instance.
        screenshot_path: File path for the screenshot.
        data_path: File path for waveform data.
        acquisition_delay: Delay before capture (seconds).
    """
    time.sleep(acquisition_delay)  # Wait for waveform to stabilize
    try:
        scope.stop()  # Stop scope for data capture
    except Exception as e:
        click.echo(f"Warning: Could not stop scope cleanly: {e}")

    click.echo(f"Capturing screenshot to {screenshot_path} ...")
    try:
        scope.get_screenshot(screenshot_path)
    except Exception as e:
        click.echo(f"Error capturing screenshot: {e}")
        exit(1)

    click.echo(f"Saving waveform data to {data_path} ...")
    try:
        scope.get_data(EWaveformMode.Raw, data_path)
    except Exception as e:
        click.echo(f"Error saving waveform data: {e}")
        exit(1)

    try:
        scope.run()  # Resume run mode
    except Exception as e:
        click.echo(f"Warning: Could not resume scope run mode: {e}")
    click.echo("Data capture complete")


def create_table(csv_path: str, tex_path: str) -> None:
    """
    Create a LaTeX table from a CSV file.

    Args:
        csv_path (str): Path to the input CSV file.
        tex_path (str): Path to the output LaTeX file.

    Raises:
        SystemExit: If reading the CSV or writing the LaTeX file fails.
    """
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        click.echo(f"Error reading CSV file '{csv_path}': {e}")
        exit(1)
    try:
        latex_code = df.to_latex(
            index=False, caption="Captured Waveform Data", label="tab:waveform")
        with open(tex_path, "w") as f:
            f.write(latex_code)
        click.echo(f"LaTeX file created successfully at '{tex_path}'.")
    except Exception as e:
        click.echo(f"Error writing LaTeX file '{tex_path}': {e}")
        exit(1)


def create_plot(csv_path: str, tex_path: str) -> None:
    """
    Create a LaTeX plot from a CSV file.

    Args:
        csv_path (str): Path to the input CSV file.
        tex_path (str): Path to the output LaTeX file.

    Raises:
        SystemExit: If writing the LaTeX file fails.
    """
    latex_template = r"""
\documentclass{article}
\usepackage{pgfplots}
\usepackage[utf8]{inputenc}
\pgfplotsset{compat=1.18}
\begin{document}

\begin{tikzpicture}
    \begin{axis}[
            width=0.8\textwidth,
            height=0.7\textwidth,
            xlabel={Time (s)},
            ylabel={Value},
            title={Plot from CSV Data},
            grid=major
        ]
        \addplot table [mark=none, col sep=comma] {{{csv_file}}};
        \addlegendentry{Data}
    \end{axis}
\end{tikzpicture}

\end{document}
    """
    latex_code = latex_template.replace("{{csv_file}}", csv_path)
    try:
        with open(tex_path, "w") as f:
            f.write(latex_code)
        click.echo(f"LaTeX plot file created successfully at '{tex_path}'.")
    except Exception as e:
        click.echo(f"Error writing LaTeX file '{tex_path}': {e}")
        exit(1)


def create_latex(csv_path: str, tex_path: str, tex_type: str) -> None:
    if tex_type == "plot":
        create_plot(csv_path, tex_path)
    elif tex_type == "table":
        create_table(csv_path, tex_path)
    else:
        click.echo(f"Unsupported tex-type: {tex_type}")


@click.command()
@click.option('--ip', type=str, help='VISA resource string or instrument IP address')
@click.option('--start-channel', type=int, help='Starting channel number (default: 1)')
@click.option('--end-channel', type=int, help='Ending channel number (default: 2)')
@click.option('--screenshot', type=str, help='Screenshot file path (default: ./screenshot.png)')
@click.option('--data', type=str, help='Waveform data file path (default: ./waveform.csv)')
@click.option('--tex', type=str, help='LaTeX output file path (default: ./output.tex)')
@click.option('--tex-type', type=str, help='Type of display in the LaTeX file')
@click.option('--delay', type=float, help='Acquisition delay in seconds (default: 0.5)')
@click.option('--autoscale', type=bool, help='Autoscale scope axes (default: True)')
@click.option('--interactive/--no-interactive', default=True,
              help='Run interactively to prompt for missing values (default: interactive)')
def capture(ip, start_channel, end_channel, screenshot, data, tex, tex_type, delay, autoscale, interactive):
    """
    CLI tool to capture a screenshot and waveform data from a Rigol DS1000z oscilloscope.

    You can supply all options via command-line arguments or run interactively.
    """
    # If interactive mode is enabled, prompt for any missing values using Questionary
    if interactive:
        if not ip:
            ip = select_instrument_resource()
        else:
            if not ip.startswith("TCPIP"):
                ip = f"TCPIP0::{ip}::INSTR"
        if not start_channel:
            start_channel = int(questionary.text(
                "Enter starting channel number:", default="1").ask())
        if not end_channel:
            end_channel = int(questionary.text(
                "Enter ending channel number:", default="2").ask())
        if not screenshot:
            screenshot = questionary.text(
                "Enter screenshot file path:", default="./screenshot.png").ask()
        if not data:
            data = questionary.text(
                "Enter waveform data file path:", default="./waveform.csv").ask()
        if not tex:
            tex = questionary.text(
                "Enter LaTeX file path for plotting:", default="./plot.tex").ask()
        if not tex_type:
            tex_type = questionary.select(
                "Select the type of LaTeX output:",
                choices=["plot", "table"]
            ).ask()
        if delay is None:
            delay = float(questionary.text(
                "Enter acquisition delay in seconds:", default="0.5").ask())
        if autoscale is None:
            autoscale_answer = questionary.select("Autoscale scope axes?",
                                                  choices=["Yes", "No"]).ask()
            autoscale = (autoscale_answer == "Yes")
    else:
        # Use defaults if not provided
        ip = ip or ""
        start_channel = start_channel or 1
        end_channel = end_channel or 2
        screenshot = screenshot or "./screenshot.png"
        data = data or "./waveform.csv"
        tex = tex or "./output.tex"
        tex_type = tex_type or "plot"
        delay = delay if delay is not None else 0.5
        autoscale = autoscale if autoscale is not None else True

    channels = list(range(start_channel, end_channel + 1))
    click.echo(f"Enabling channels: {channels}")

    instrument = setup_instrument(ip)
    with Rigol1000z(instrument) as scope:
        configure_scope(scope, channels, autoscale)
        capture_data(scope,
                     screenshot_path=screenshot,
                     data_path=data,
                     acquisition_delay=delay)
        create_latex(csv_path=data, tex_path=tex, tex_type=tex_type)


if __name__ == '__main__':
    capture()
