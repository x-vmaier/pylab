# Pylab

Pylab is a Python command-line interface (CLI) tool for capturing and processing data from Rigol DS1000z oscilloscopes. It provides dedicated commands for directly reading oscilloscope data and for processing simulation/measurement data through a data pipeline.

## Installation

### Prerequisites

- **Python:** Version lower than 3.13
- **Hardware:** A Rigol DS1000z series oscilloscope with TCP/IP connectivity

### Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/x-vmaier/pylab.git
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
