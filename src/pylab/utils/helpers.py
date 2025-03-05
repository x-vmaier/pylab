import click
import pyvisa
import ipaddress
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter


def list_tcpip_resources() -> list:
    """Query the VISA resource manager for all TCPIP instruments."""
    try:
        rm = pyvisa.ResourceManager()
        resources = rm.list_resources()
        tcpip_resources = [res for res in resources if "TCPIP" in res]
        return tcpip_resources
    except Exception as e:
        click.echo(f"Error listing VISA resources: {e}")
        return []


def validate_ip_address(ip_address):
    """Validate that the given string is a valid IP address."""
    try:
        ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        return False


def read_data(file_path, file_ext):
    """Helper function to read simulation or measurement data based on file extension."""
    if file_ext == '.xlsx':
        return pd.read_excel(file_path, skiprows=1, names=['X', 'Y'])
    elif file_ext == '.csv':
        return pd.read_csv(file_path, delimiter=',', header=None, names=['X', 'Y'])
    else:
        raise ValueError(f"Unsupported file extension: {file_ext}")


def shift_csv(data: pd.DataFrame, column_name: str, amount: float) -> pd.DataFrame:
    """Shifts the data in the specified column by the given amount and removes entries with negative values."""
    data[column_name] = data[column_name] - amount
    return data[data[column_name] >= 0]


def zero_x(data: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """Shifts the data in the specified column so that the first x-value becomes 0.0."""
    shift_amount = data[column_name].iloc[0]
    data[column_name] = data[column_name] - shift_amount
    return data


def smooth_data(data: pd.DataFrame, column_name: str, window_length: int, polyorder: int) -> np.ndarray:
    """Applies a Savitzky-Golay filter to smooth the data in the specified column."""
    return savgol_filter(data[column_name], window_length=window_length, polyorder=polyorder)


def calculate_derivative(data: pd.DataFrame, column_name: str,
                         smooth: bool = False, rel_threshold: float = 1e-2) -> np.ndarray:
    """Calculates the derivative (rate of change) of the data in the specified column."""
    values = data[column_name].values
    if smooth:
        smoothed_values = smooth_data(data, column_name, window_length=2000, polyorder=2)
        derivative = np.gradient(smoothed_values)
    else:
        derivative = np.gradient(values)

    # Calculate relative change between consecutive values
    relative_change = np.abs(np.diff(values)) / np.abs(values[:-1] + 1e-10)
    relative_change = np.append(relative_change, 0)

    # Zero out derivative where relative change is below the threshold (likely noise)
    derivative[relative_change < rel_threshold] = 0
    return derivative


def align_datasets_on_event(meas_data: pd.DataFrame, sim_data: pd.DataFrame, event_threshold: float,
                            smooth: bool = True, padding: float = 0.5) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Aligns measurement and simulation datasets based on the first significant event."""
    meas_derivative = calculate_derivative(meas_data, 'Y', smooth=smooth, rel_threshold=event_threshold)
    sim_derivative = calculate_derivative(sim_data, 'Y', smooth=smooth, rel_threshold=event_threshold)

    # Detect the first significant event for measurement data
    meas_event_indices = np.where(np.abs(meas_derivative) > event_threshold)[0]
    meas_event_index = meas_event_indices[0] if meas_event_indices.size > 0 else np.argmax(np.abs(meas_derivative))

    # Detect the first significant event for simulation data
    sim_event_indices = np.where(np.abs(sim_derivative) > event_threshold)[0]
    sim_event_index = sim_event_indices[0] if sim_event_indices.size > 0 else np.argmax(np.abs(sim_derivative))

    # Shift both datasets so that the event occurs at x = 0 + padding
    shift_amount_meas = meas_data['X'].iloc[meas_event_index] - padding
    shift_amount_sim = sim_data['X'].iloc[sim_event_index] - padding

    meas_data['X'] -= shift_amount_meas
    sim_data['X'] -= shift_amount_sim

    return meas_data, sim_data


def interpolate_simulation(sim_data: pd.DataFrame, meas_data: pd.DataFrame) -> pd.DataFrame:
    """Interpolates simulation data to match the x-values of the measurement data."""
    x_sim = sim_data['X'].values
    y_sim = sim_data['Y'].values
    x_meas = meas_data['X'].values
    y_sim_interp = np.interp(x_meas, x_sim, y_sim)
    return pd.DataFrame({'X': x_meas, 'Y': y_sim_interp})
