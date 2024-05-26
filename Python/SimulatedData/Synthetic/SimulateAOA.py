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
from datetime import datetime

import numpy as np
import pandas as pd

from ADC.ADC_Table import ADCTable
from DiffTable.DifferenceTable import DifferenceTable
from Telemetry.Telemetry import Telemetry

# -----------------------------------------------------------------------
# Open the telemetry file
# -----------------------------------------------------------------------

str_date_now = datetime.now().strftime('%Y%m%d')  # Get today's date

# Read the data from file
data_file = '../Telemetry/raw_telemetry_20230704.txt'

telemetry_obj = Telemetry(data_file)  # Create an instance of the Telemetry class

# Create a DataFrame with signal_indices and signal_data
limited_data = telemetry_obj.getLimitedSampleDataFrame()

print("Segment Mean: ", telemetry_obj.segment_mean)
print("Temporary Threshold: ", telemetry_obj.temp_threshold)
print("Mean of noise:", telemetry_obj.noise_mean)
print("Standard deviation of noise:", telemetry_obj.noise_std)
print("New threshold:", telemetry_obj.threshold)

# Count the number of detected points above the threshold
num_detected_points = len(limited_data.get('signal_data'))
num_det_pts_per_sec = num_detected_points / (telemetry_obj.segment_duration / 1000)
print("Number of detected points above the threshold:", num_detected_points)
print("Detected points per second:", num_det_pts_per_sec)

# -----------------------------------------------------------------------
# Group the telemetry into clusters, then process by cluster
# -----------------------------------------------------------------------
clusters_unique, colors_clusters_unique, clusters_all = telemetry_obj.getClusteredSample(limited_data)

# Read the difference table
file_path = "../DiffTable/diff_table_45deg_20231126.csv"  # Difference Table file path
diff_table = DifferenceTable(file_path)  # Create an instance of the DifferenceTable class

# Read the ADC lookup table
adc_table = ADCTable()

# aoa_values_azi = [-20, -5, 30]  # AOA values in degrees (Azi)
# aoa_values_el = [-10, -5, 15]  # AOA values in degrees (El)
# aoa_values_azi = [0]  # AOA values in degrees (Azi)
# aoa_values_el = [0]  # AOA values in degrees (El)
aoa_values_azi = [5]  # AOA values in degrees (Azi)
aoa_values_el = [-1]  # AOA values in degrees (El)

# Define an empty dictionary to store ADC values for each cluster
cluster_adc_values = {}

for cluster_id, color in zip(clusters_unique, colors_clusters_unique):

    # -----------------------------------------------------------------------
    # Convert Cluster ADC Values to an Ultimate Power Level
    # -----------------------------------------------------------------------

    cluster_points = limited_data[clusters_all == cluster_id]
    adc_values = cluster_points['signal_data'].tolist()  # Convert to a list for comparison
    t_values = cluster_points['signal_indices'].tolist()

    # Simulate AOA (select a random AOA value from the provided AOA values)
    random_index = random.randint(0, len(aoa_values_azi) - 1)
    aoa_azi = aoa_values_azi[random_index]
    aoa_el = aoa_values_el[random_index]

    # Determine which channel is the ultimate and penultimate based on AOA
    azi_ultimate_channel = 2 if aoa_azi > 0 else 1
    azi_penultimate_channel = 1 if azi_ultimate_channel == 2 else 2
    el_ultimate_channel = 3 if aoa_el > 0 else 4
    el_penultimate_channel = 4 if el_ultimate_channel == 3 else 3

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
    azi_delta_db_value = float(diff_table.convert_aoa_to_diff([aoa_azi])[0])
    el_delta_db_value = float(diff_table.convert_aoa_to_diff([aoa_el])[0])

    # Calculate the power level of the penultimate channel using the Delta dB value
    azi_penultimate_power_values = [value - abs(azi_delta_db_value) for value in azi_power_values_ultimate]
    el_penultimate_power_values = [value - abs(el_delta_db_value) for value in el_power_values_ultimate]

    std_deviation = 0.2  # Standard deviation in dB
    # std_deviation = 0  # Standard deviation in dB (noiseless)

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
        'CH1_ADC': azi_adc_values_ultimate if azi_ultimate_channel == 1 else azi_adc_values_penultimate,
        'CH2_ADC': azi_adc_values_ultimate if azi_ultimate_channel == 2 else azi_adc_values_penultimate,
        'CH3_ADC': el_adc_values_ultimate if el_ultimate_channel == 3 else el_adc_values_penultimate,
        'CH4_ADC': el_adc_values_ultimate if el_ultimate_channel == 4 else el_adc_values_penultimate
    })

    # Concatenate the cluster telemetry with the original telemetry
    telemetry = pd.concat([telemetry, cluster_telemetry])

telemetry = telemetry.sort_values('t_index')

# Save the original telemetry to a CSV file if needed
telemetry.to_csv('synth_data_45deg_'+str_date_now+'.csv', index=False)
