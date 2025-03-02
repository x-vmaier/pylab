# Pyrigol

Pyrigol is a Python command-line interface (CLI) tool that allows you to capture data from a Rigol DS1000z oscilloscope. The tool can automatically configure the oscilloscope, capture both waveform data and a screenshot, and output LaTeX-compatible files for generating plots or tables from the captured data.

## Installation

### Prerequisites

Before using Pyrigol, you need the following dependencies:

- Python < 3.13
- A Rigol DS1000z series oscilloscope with TCP/IP connectivity

### Dependencies

Create a virtual environment first:

```bash
python -m venv ./venv
```

Activate it with:

```bash
venv/Scripts/activate  # Windows
source venv/bin/activate  # macOS/Linux
```

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

You can run the Pyrigol CLI tool with the following options:

```bash
python pyrigol.py [options]
```

### Options

- `--ip`: (Optional) VISA resource string or IP address of the oscilloscope (e.g., `TCPIP0::192.168.1.100::INSTR`). If not provided, you will be prompted to enter it interactively.
- `--start-channel`: (Optional) The starting channel number (default: 1).
- `--end-channel`: (Optional) The ending channel number (default: 2).
- `--screenshot`: (Optional) File path to save the screenshot (default: `./screenshot.png`).
- `--data`: (Optional) File path to save the waveform data (default: `./waveform.csv`).
- `--tex`: (Optional) File path for LaTeX output (default: `./output.tex`).
- `--tex-type`: (Optional) Type of LaTeX output ("plot" or "table").
- `--delay`: (Optional) Acquisition delay in seconds before capturing (default: 0.5).
- `--autoscale`: (Optional) Whether to autoscale the oscilloscope (default: `True`).
- `--interactive/--no-interactive`: (Optional) Run interactively to prompt for missing values (default: `interactive`).

### Interactive Mode

In interactive mode, if any arguments are missing, you will be prompted to provide values. This allows you to configure the oscilloscope and capture data dynamically.

## LaTeX Output

Pyrigol can generate LaTeX-compatible files for displaying captured data either as a plot or a table:

- **Plot**: A LaTeX file for plotting the waveform data using `pgfplots`.
- **Table**: A LaTeX file for displaying the waveform data in a table format.

### Example LaTeX Output (Plot)

```latex
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
        \addplot table [mark=none, col sep=comma] {{{discharge_curve.csv}}};
        \addlegendentry{Data}
    \end{axis}
\end{tikzpicture}

\end{document}
```

## Contributing

Feel free to fork the repository, report issues, or submit pull requests to contribute.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- This project uses the [Rigol1000z Python package](https://github.com/AlexZettler/Rigol1000z) for communicating with the Rigol DS1000z oscilloscope.
- The LaTeX code for generating plots is based on the `pgfplots` package.
