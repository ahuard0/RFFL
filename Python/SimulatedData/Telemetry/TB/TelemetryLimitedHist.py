import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Read the data from file
data_file = '../raw_telemetry_20230704.txt'

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
temp_threshold = 3*segment_mean
print("Segment Mean: ", segment_mean)
print("Temporary Threshold: ", temp_threshold)

# Calculate the mean and standard deviation of the noise using temporary threshold
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
output_file = 'data_limited_20230704.csv'

# Save the DataFrame to a CSV file
limited_data.to_csv(output_file, index=False)

# Print a message indicating the data has been saved
print(f"Limited data has been saved to {output_file}")

# Plot the histogram of the limited data
plt.figure(figsize=(10, 6))  # Create a new figure for the histogram
plt.hist(limited_data['signal_data'], bins=50, color='blue', alpha=0.7, label='Amplitude Histogram')

# Customize the chart
plt.xlabel('Magnitude')
plt.ylabel('Frequency')
plt.title('Signal points above threshold: ' + str(num_detected_points) + ' (' + str(num_det_pts_per_sec) + ' pts/sec)')

# Add the new threshold line to the plot
plt.axvline(x=threshold, color='r', linestyle='--', label='Threshold')

# Display the legend
plt.legend()

# Display the chart
plt.show()
