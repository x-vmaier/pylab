import os
import pandas as pd
import matplotlib.pyplot as plt
from ..utils.helpers import align_datasets_on_event, interpolate_simulation


class PipelineProcessor:
    def __init__(self):
        self.sim_file = None
        self.meas_file = None
        self.sim_data = None
        self.meas_data = None

    def run(self, sim_file, meas_file, trigger, smooth):
        """Process simulation and measurement data"""
        self.sim_file = sim_file
        self.meas_file = meas_file

        self.sim_data = pd.read_excel(sim_file, skiprows=1, names=['X', 'Y'])
        self.meas_data = pd.read_csv(meas_file, delimiter=',', header=None, names=['X', 'Y'])

        self.meas_data, self.sim_data = align_datasets_on_event(self.meas_data, self.sim_data, trigger, smooth=smooth)
        self.sim_data = interpolate_simulation(self.sim_data, self.meas_data)

    def save(self):
        """ Save the processed simulation and measurement data to CSV files"""
        
        # Extract filename without extension
        sim_output_file = os.path.splitext(os.path.basename(self.sim_file))[0]
        meas_output_file = os.path.splitext(os.path.basename(self.meas_file))[0]

        self.sim_data.to_csv(f"processed_{sim_output_file}.csv", index=False, header=False)
        self.meas_data.to_csv(f"processed_{meas_output_file}.csv", index=False, header=False)

    def generate_plots(self):
        """Plots the measurement data and the simulation data"""
        if self.meas_data is None or self.sim_data is None:
            raise Exception("Failed to generate plot: Data is missing")

        plt.figure(figsize=(10, 6))
        plt.plot(self.meas_data['X'], self.meas_data['Y'],label="Measurements", color='b', linestyle='-')
        plt.plot(self.sim_data['X'], self.sim_data['Y'],label="Interpolated Simulation", color='r', linestyle='--')
        plt.xlabel('X Value')
        plt.ylabel('Y Value')
        plt.title('Pipeline Output')
        plt.legend()
        plt.show()
