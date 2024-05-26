# SimulateAOA
#   This script will simulate received ADC values for the ultimate (CH3) and penultimate (CH4) channels.
#   The script starts by opening real telemetry data, which are received ADC values for the ultimate channel.
#   The ultimate channel is the channel with the highest received power at a point in time, followed by the penultimate
#   channel, which will have the 2nd highest power level received.  This telemetry will be grouped into clusters
#   simulating TMDA.  Next, the clusters in ADC unitless values will be converted to a received power level using a
#   lookup table.  This will be the power received by the ultimate channel.  The cluster will be randomly assigned one
#   of three available AOA values. Depending on the AOA value assigned, the channel power difference will be determined
#   using a difference table, which is a lookup table that relates the AOA to the channel power difference between the
#   channels.  For example, the difference table relates the subtraction of the CH3 and CH4 power levels to the AOA.
#   Based on AOA, determine if the ultimate channel is CH3 or CH4.  Next, the power level of the penultimate channel is
#   determined by subtracting the channel power difference from the difference table based on AOA.  The penultimate
#   power level is then related back to ADC unitless values using the ADC lookup table.  Finally, present the data in
#   the original for of the telemetry, but include both ultimate and penultimate ADC values.

import random
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, fcluster

from ADC.ADC_Table import ADCTable
from DiffTable.DifferenceTable import DifferenceTable

# -----------------------------------------------------------------------
# Open the telemetry file
# -----------------------------------------------------------------------

# Read the data from file
data_file = '../../Telemetry/raw_telemetry_20230704.txt'

magnitude = []
indices = []

with open(data_file, 'r') as file:
    for line in file:
        line = line.strip()
        if line:
            ind, m = line.split(',')
            indices.append(int(ind))
            magnitude.append(int(m))

# Determine the time range for the segment (10 seconds wide)
segment_duration = 10000  # 10 seconds in milliseconds
start_index = random.randint(0, len(magnitude) - segment_duration)
segment_magnitude = magnitude[start_index:start_index + segment_duration]
segment_indices = indices[start_index:start_index + segment_duration]

# Set temporary threshold for noise calculation
segment_mean = np.mean(segment_magnitude)
temp_threshold = 3 * segment_mean
print("Segment Mean: ", segment_mean)
print("Temporary Threshold: ", temp_threshold)

# Calculate the mean and standard deviation of the noise using the temporary threshold
noise_data = [x for x in segment_magnitude if x <= temp_threshold]
noise_indices = [ind for ind, x in zip(segment_indices, segment_magnitude) if x <= temp_threshold]
noise_mean = np.mean(noise_data)
noise_std = np.std(noise_data)

# Calculate the new threshold based on the mean of noise plus 3 standard deviations
threshold = noise_mean + 3 * noise_std

# Separate the signal from the noise
lower_noise_data = [x for x in segment_magnitude if x <= threshold]
lower_noise_indices = [ind for ind, x in zip(segment_indices, segment_magnitude) if x <= threshold]
signal_data = [x for x in segment_magnitude if x > threshold]
signal_indices = [ind for ind, x in zip(segment_indices, segment_magnitude) if x > threshold]

# Print the calculated mean, standard deviation, and the new threshold
print("Mean of noise:", noise_mean)
print("Standard deviation of noise:", noise_std)
print("New threshold:", threshold)

# Count the number of detected points above the threshold
num_detected_points = len(signal_data)
num_det_pts_per_sec = num_detected_points / (segment_duration / 1000)
print("Number of detected points above the threshold:", num_detected_points)
print("Detected points per second:", num_det_pts_per_sec)

# Create a DataFrame with signal_indices and signal_data
limited_data = pd.DataFrame({'signal_indices': signal_indices, 'signal_data': signal_data})

# Define the output file name
output_file = '../../Telemetry/TB/data_limited_20231119.csv'

# Save the DataFrame to a CSV file
limited_data.to_csv(output_file, index=False)

# Print a message indicating the data has been saved
print(f"Limited data has been saved to {output_file}")

# -----------------------------------------------------------------------
# Group the telemetry into clusters
# -----------------------------------------------------------------------

# Perform hierarchical clustering to group data based on signal indices
linkage_matrix = linkage(limited_data[['signal_indices']], method='ward')

# Define the threshold for cutting the dendrogram
cut_threshold = 200  # Adjust this threshold as needed

# Cut the dendrogram to form clusters based on the threshold
clusters = fcluster(linkage_matrix, cut_threshold, criterion='distance')

# Define colors for each cluster
colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']

# Scatter plot points, color-coded by cluster
unique_clusters = np.unique(clusters)
n_clusters = len(unique_clusters)
cluster_colors = sns.color_palette('hsv', n_clusters)

for cluster_id, color in zip(unique_clusters, cluster_colors):
    cluster_points = limited_data[clusters == cluster_id]
    plt.scatter(cluster_points['signal_indices'], cluster_points['signal_data'], color=color, alpha=0.7,
                label=f'Cluster {cluster_id}')

# -----------------------------------------------------------------------
# Process by Cluster
# -----------------------------------------------------------------------

# Read the difference table
file_path = "../../DiffTable/HFSS/Difference Table 45 deg Offset.csv"  # Difference Table file path
diff_table = DifferenceTable(file_path)  # Create an instance of the DifferenceTable class

# Read the ADC lookup table
adc_table = ADCTable()

# aoa_values_azi = [-5, 5, 0, -10]  # AOA values in degrees (Azi)
# aoa_values_el = [-1, -3, 5, -5]  # AOA values in degrees (El)
aoa_values_azi = [0]  # AOA values in degrees (Azi)
aoa_values_el = [0]  # AOA values in degrees (El)

# Define an empty dictionary to store ADC values for each cluster
cluster_adc_values = {}

for cluster_id, color in zip(unique_clusters, cluster_colors):

    # -----------------------------------------------------------------------
    # Convert Cluster ADC Values to an Ultimate Power Level
    # -----------------------------------------------------------------------

    cluster_points = limited_data[clusters == cluster_id]
    adc_values = cluster_points['signal_data'].tolist()  # Convert to a list for comparison
    t_values = cluster_points['signal_indices'].tolist()

    # Simulate AOA (select a random AOA value from the provided AOA values)
    random_index = random.randint(0, len(aoa_values_azi) - 1)
    aoa_azi = aoa_values_azi[random_index]
    aoa_el = aoa_values_el[random_index]

    # Determine which channel is the ultimate and penultimate based on AOA
    azi_ultimate_channel = 4 if aoa_azi > 0 else 3
    azi_penultimate_channel = 3 if azi_ultimate_channel == 4 else 4
    el_ultimate_channel = 1 if aoa_el > 0 else 2
    el_penultimate_channel = 2 if el_ultimate_channel == 1 else 1

    # Find the Power values for the ultimate channel by interpolating ADC values
    azi_power_values_ultimate = list()
    el_power_values_ultimate = list()
    azi_adc_values_ultimate = list()
    el_adc_values_ultimate = list()
    t_index = list()
    for adc_value_U, t in zip(adc_values, t_values):
        azi_power_value_dbm = adc_table.convert_adc_to_dbm([adc_value_U], azi_ultimate_channel)
        el_power_value_dbm = adc_table.convert_adc_to_dbm([adc_value_U], el_ultimate_channel)
        azi_power_values_ultimate.extend(azi_power_value_dbm)
        el_power_values_ultimate.extend(el_power_value_dbm)
        azi_adc_values_ultimate.extend([adc_value_U])
        el_adc_values_ultimate.extend([adc_value_U])
        t_index.append(t)

    # -----------------------------------------------------------------------
    # Get Delta dB from Difference Table and Generate Penultimate
    # -----------------------------------------------------------------------

    # Get the Delta dB value from the Difference Table corresponding to the AOA
    azi_delta_db_value = float(diff_table.convert_diff_to_aoa([aoa_azi])[0])
    el_delta_db_value = float(diff_table.convert_diff_to_aoa([aoa_el])[0])

    # Calculate the power level of the penultimate channel using the Delta dB value
    azi_penultimate_power_values = [value - abs(azi_delta_db_value) for value in azi_power_values_ultimate]
    el_penultimate_power_values = [value - abs(el_delta_db_value) for value in el_power_values_ultimate]

    # std_deviation = 0.2  # Standard deviation in dB
    std_deviation = 0  # Standard deviation in dB

    # Add Gaussian noise to the data
    azi_noisy_penultimate_power_values = [value + np.random.normal(0, std_deviation) for value in azi_penultimate_power_values]
    el_noisy_penultimate_power_values = [value + np.random.normal(0, std_deviation) for value in el_penultimate_power_values]
    azi_penultimate_power_values = azi_noisy_penultimate_power_values
    el_penultimate_power_values = el_noisy_penultimate_power_values

    # Find the ADC values for the penultimate channel by interpolating Power values
    azi_adc_values_penultimate = adc_table.convert_dbm_to_adc(azi_penultimate_power_values, azi_penultimate_channel)
    el_adc_values_penultimate = adc_table.convert_dbm_to_adc(el_penultimate_power_values, el_penultimate_channel)

    # Store the ADC values, AOA, ultimate and penultimate channel information, and power values
    cluster_data = {
        'cluster_id': cluster_id,
        'color': color,
        't_index': t_index,
        'aoa_azi': aoa_azi,
        'aoa_el': aoa_el,
        'azi_delta_db_value': azi_delta_db_value,
        'el_delta_db_value': el_delta_db_value,
        'azi_ultimate_channel': azi_ultimate_channel,
        'azi_penultimate_channel': azi_penultimate_channel,
        'el_ultimate_channel': el_ultimate_channel,
        'el_penultimate_channel': el_penultimate_channel,
        'azi_power_values_ultimate': azi_power_values_ultimate,
        'azi_adc_values_ultimate': azi_adc_values_ultimate,
        'el_power_values_ultimate': el_power_values_ultimate,
        'el_adc_values_ultimate': el_adc_values_ultimate,
        'azi_penultimate_power_values': azi_penultimate_power_values,
        'azi_adc_values_penultimate': azi_adc_values_penultimate,
        'el_penultimate_power_values': el_penultimate_power_values,
        'el_adc_values_penultimate': el_adc_values_penultimate
    }

    # Add the cluster data to the dictionary
    cluster_adc_values[cluster_id] = cluster_data

# Initialize an empty DataFrame to store the original telemetry
telemetry = pd.DataFrame()

# Loop through each cluster and add the telemetry data
for cluster_id, cluster_data in cluster_adc_values.items():
    t_index = cluster_data['t_index']
    azi_adc_values_ultimate = cluster_data['azi_adc_values_ultimate']
    azi_adc_values_penultimate = cluster_data['azi_adc_values_penultimate']
    el_adc_values_ultimate = cluster_data['el_adc_values_ultimate']
    el_adc_values_penultimate = cluster_data['el_adc_values_penultimate']
    azi_ultimate_channel = cluster_data['azi_ultimate_channel']
    el_ultimate_channel = cluster_data['el_ultimate_channel']

    # Round the ADC values to the nearest integer
    azi_adc_values_penultimate = list(map(int, map(round, azi_adc_values_penultimate)))
    el_adc_values_penultimate = list(map(int, map(round, el_adc_values_penultimate)))

    # Create a DataFrame for the current cluster
    cluster_telemetry = pd.DataFrame({
        't_index': t_index,
        'CH1_ADC': el_adc_values_ultimate if el_ultimate_channel == 1 else el_adc_values_penultimate,
        'CH2_ADC': el_adc_values_ultimate if el_ultimate_channel == 2 else el_adc_values_penultimate,
        'CH3_ADC': azi_adc_values_ultimate if azi_ultimate_channel == 3 else azi_adc_values_penultimate,
        'CH4_ADC': azi_adc_values_ultimate if azi_ultimate_channel == 4 else azi_adc_values_penultimate
    })

    # Concatenate the cluster telemetry with the original telemetry
    telemetry = pd.concat([telemetry, cluster_telemetry])

telemetry = telemetry.sort_values('t_index')

# Save the original telemetry to a CSV file if needed
telemetry.to_csv('synth_data_20231119.csv', index=False)
