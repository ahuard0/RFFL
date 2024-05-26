import random
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from ADC.ADCTable import ADCTable

# Read the data from file
data_file = 'data_20230704.txt'

magnitude = []

with open(data_file, 'r') as file:
    for line in file:
        line = line.strip()
        if line:
            _, m = line.split(',')
            magnitude.append(int(m))

# Determine the time range for the segment (5 seconds wide)
segment_duration = 5000  # 5 seconds in milliseconds
start_index = random.randint(0, len(magnitude) - segment_duration)
segment_magnitude = magnitude[start_index:start_index + segment_duration]

# Convert ADC to dBm
adc_table = ADCTable()
adc_value_U = segment_magnitude  # Replace with your ADC value
channel = 1  # Replace with the desired channel (1, 2, 3, or 4)
chan_power_dBm = adc_table.convert_adc_to_dbm(adc_value_U, channel)

# Convert dBm to milliwatts
segment_magnitude = [10 ** (value / 10.0) for value in chan_power_dBm]

# Set temporary threshold for noise calculation
segment_mean = np.mean(segment_magnitude)
temp_threshold = 3*segment_mean
print("Segment Mean: ", segment_mean)
print("Temporary Threshold: ", temp_threshold)
print("Number of Sample Points: ", np.size(segment_magnitude))

# Calculate the mean and standard deviation of the noise using temporary threshold
noise_data = [x for x in segment_magnitude if x <= temp_threshold]
noise_mean = np.mean(noise_data)
noise_std = np.std(noise_data)

# Calculate the new threshold based on the mean of noise plus 3 standard deviations
threshold = noise_mean + 3 * noise_std

# Separate the signal from the noise
lower_noise_data = [x for x in segment_magnitude if x <= threshold]
signal_data = [x for x in segment_magnitude if x > threshold]

# Convert milliwatts back to dBm
segment_magnitude = 10 * np.log10(segment_magnitude)
noise_mean = 10 * np.log10(noise_mean)
noise_std = 10 * np.log10(noise_std)
threshold = 10 * np.log10(threshold)
lower_noise_data = 10 * np.log10(lower_noise_data)
signal_data = 10 * np.log10(signal_data)

# Print the calculated mean, standard deviation, and the new threshold
print("Mean of noise:", noise_mean)
print("Standard deviation of noise:", noise_std)
print("New threshold:", threshold)

# Count the number of detected points above the threshold
num_detected_points = len(signal_data)
num_det_pts_per_sec = num_detected_points / (segment_duration / 1000)
print("Number of detected points above the threshold:", num_detected_points)
print("Detected points per second:", num_det_pts_per_sec)

# Plot the histogram with KDE and upper samples
sns.histplot(segment_magnitude, bins='auto', kde=False)

# Customize the chart
plt.xlabel('RX Power (dBm)')
plt.ylabel('Count')
plt.title('Detected above threshold: ' + str(num_det_pts_per_sec) + ' pts/sec')

# Calculate the KDE of the lower noise part
sns.histplot(signal_data, bins='auto', kde=False, alpha=0.25)

# Add the new threshold line to the plot
plt.axvline(x=threshold, color='r', linestyle='--', label='$3\sigma$ Threshold')

# Display the legend
plt.legend()

# Display the chart
plt.subplots_adjust(bottom=0.2)
plt.show()
