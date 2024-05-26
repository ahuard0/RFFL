import random
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

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

# Set temporary threshold for noise calculation
segment_mean = np.mean(segment_magnitude)
temp_threshold = 3*segment_mean
print("Segment Mean: ", segment_mean)
print("Temporary Threshold: ", temp_threshold)

# Calculate the mean and standard deviation of the noise using temporary threshold
noise_data = [x for x in segment_magnitude if x <= temp_threshold]
noise_mean = np.mean(noise_data)
noise_std = np.std(noise_data)

# Calculate the new threshold based on the mean of noise plus 3 standard deviations
threshold = noise_mean + 3 * noise_std

# Separate the signal from the noise
lower_noise_data = [x for x in segment_magnitude if x <= threshold]
signal_data = [x for x in segment_magnitude if x > threshold]

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
plt.xlabel('Magnitude')
plt.ylabel('Frequency')
plt.title('Signal points above threshold: ' + str(num_detected_points) + ' (' + str(num_det_pts_per_sec) + ' pts/sec)')

# Calculate the KDE of the lower noise part
sns.histplot(lower_noise_data, bins='auto', kde=True)
sns.histplot(signal_data, bins='auto', kde=False)

# Add the new threshold line to the plot
plt.axvline(x=threshold, color='r', linestyle='--', label='Threshold')

# Display the legend
plt.legend()

# Display the chart
plt.show()
