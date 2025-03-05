# Pylab

Pylab is a Python command-line interface (CLI) tool for capturing and processing data from Rigol DS1000z oscilloscopes. It provides dedicated commands for directly reading oscilloscope data and for processing simulation/measurement data through a data pipeline.

## Installation

### Prerequisites

- **Python:** Version lower than 3.13
- **Hardware:** A Rigol DS1000z series oscilloscope with TCP/IP connectivity

### Steps

1. **Clone the Repository:**

   ```bash
   git clone --recurse-submodules https://github.com/x-vmaier/pylab.git
   ```

2. **Navigate to the Project Directory:**

   ```bash
   cd pylab
   ```

3. **Install the Module:**

   Use pip to install the project:

   ```bash
   python -m pip install .
   ```

## Usage

Pylab organizes commands into distinct groups:

### Oscilloscope Commands (`oszi`)

- **Read Data:**  
  Connect to an oscilloscope and capture data.

  ```bash
  pylab oszi read <ip_address> [OPTIONS]
  ```

  **Options:**

  - `-c, --start-channel INTEGER`  
    Starting channel number (default: 1)
  - `-e, --end-channel INTEGER`  
    Ending channel number (default: 1)
  - `-a, --autoscale`  
    Enable autoscaling
  - `-s, --screenshot TEXT`  
    Screenshot file path (default: `./screenshot.png`)
  - `-w, --waveform TEXT`  
    Waveform data file path (default: `./waveform.csv`)
  - `-d, --delay FLOAT`  
    Acquisition delay in seconds (default: 0.5)

- **List Instruments:**  
  List all available TCP/IP instrument resources.

  ```bash
  pylab oszi list
  ```

### Pipeline Commands (`pipeline`)

- **Run Data Pipeline:**  
  Process simulation and measurement data.

  ```bash
  pylab pipeline run [OPTIONS]
  ```

  **Options:**

  - `-s, --sim PATH`  
    Simulation data file (Excel format; required)
  - `-m, --meas PATH`  
    Measurement data file (CSV format; required)
  - `-t, --trigger FLOAT`  
    Threshold for event detection (default: 0.01)
  - `-f, --smooth BOOLEAN`  
    Apply smoothing before calculating the derivative (default: True)
  - `-p, --plot`  
    Generate plots from the data

For more detailed help with each command, run:

```bash
pylab [COMMAND] --help
```

## Contributing

Contributions are welcome! Please feel free to fork the repository, report issues, or submit pull requests. Ensure you follow the project’s coding style.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- This project uses the [Rigol1000z Python package](https://github.com/AlexZettler/Rigol1000z) for communication with Rigol DS1000z oscilloscopes.
