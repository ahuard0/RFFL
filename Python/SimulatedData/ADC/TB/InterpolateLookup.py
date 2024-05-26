import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('meas_adc_20231015.csv')

# Define the input values for interpolation/extrapolation
input_values = np.arange(-80, 6)  # From -80 dBm to +5 dBm

# Create a plot
plt.figure(figsize=(8, 6))

# Initialize a dictionary to store interpolated values
interpolated_data = {'Power': input_values}

# Plot and store interpolated data for CH1
output_values_CH1 = np.interp(input_values, df['Power'], df['CH1'], left=0, right=1022)
output_values_CH1 = np.round(output_values_CH1).astype(int)  # Round to the nearest integer
plt.plot(input_values, output_values_CH1, label='CH1')
interpolated_data['CH1'] = output_values_CH1

# Plot and store interpolated data for CH2
output_values_CH2 = np.interp(input_values, df['Power'], df['CH2'], left=0, right=1022)
output_values_CH2 = np.round(output_values_CH2).astype(int)  # Round to the nearest integer
plt.plot(input_values, output_values_CH2, label='CH2')
interpolated_data['CH2'] = output_values_CH2

# Plot and store interpolated data for CH3
output_values_CH3 = np.interp(input_values, df['Power'], df['CH3'], left=0, right=1022)
output_values_CH3 = np.round(output_values_CH3).astype(int)  # Round to the nearest integer
plt.plot(input_values, output_values_CH3, label='CH3')
interpolated_data['CH3'] = output_values_CH3

# Plot and store interpolated data for CH4
output_values_CH4 = np.interp(input_values, df['Power'], df['CH4'], left=0, right=1022)
output_values_CH4 = np.round(output_values_CH4).astype(int)  # Round to the nearest integer
plt.plot(input_values, output_values_CH4, label='CH4')
interpolated_data['CH4'] = output_values_CH4

# Set plot properties
plt.title('Voltage Gain Wiper Set to 15')
plt.xlabel('Power (dBm)')
plt.ylabel('ADC')  # Changed y-axis label
plt.grid(True)
plt.legend()

# Save the interpolated data to a CSV file
interpolated_df = pd.DataFrame(interpolated_data)
interpolated_df.to_csv('adc_table_20231015.csv', index=False)

# Show the plot
plt.show()
