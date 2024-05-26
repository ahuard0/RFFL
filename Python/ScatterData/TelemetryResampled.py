import random
import matplotlib.pyplot as plt
import pandas as pd

# Read the data from file
data_file = 'data_20230704.txt'

time = []
magnitude = []

with open(data_file, 'r') as file:
    for line in file:
        line = line.strip()
        if line:
            t, m = line.split(',')
            time.append(int(t))
            magnitude.append(int(m))

# Determine the time range for the segment (5 seconds wide)
segment_duration = 5000  # 5 seconds in milliseconds
max_start_time = max(time) - segment_duration
start_time = random.randint(min(time), max_start_time)
end_time = start_time + segment_duration

# Find the indices of the data points within the segment time range
indices = [i for i, t in enumerate(time) if start_time <= t <= end_time]
segment_time = [time[i] for i in indices]
segment_magnitude = [magnitude[i] for i in indices]

# Create a DataFrame from the segment data
segment_df = pd.DataFrame({'timestamp': segment_time, 'magnitude': segment_magnitude})

# Convert 'timestamp' column to datetime
segment_df['timestamp'] = pd.to_datetime(segment_df['timestamp'], unit='ms')

# Aggregate values by taking the maximum of duplicate timestamps
aggregated_df = segment_df.groupby('timestamp').max().reset_index()

# Extract the aggregated timestamps and magnitudes
aggregated_time = aggregated_df['timestamp'].tolist()
aggregated_magnitude = aggregated_df['magnitude'].tolist()

# Resample the data to 1-second intervals and calculate statistics
resampled_df = segment_df.set_index('timestamp').resample('1S').agg({
    'magnitude': ['mean', 'min', 'max', 'median', 'sum', 'std', 'var', 'count']
})

# Print the table of statistics
print(resampled_df)

# Save the table of statistics to a text file
output_file = "stats_" + data_file
resampled_df.to_csv(output_file, sep='\t', index=True)  # Set index=True to include timestamp in output file

# Plot the line chart for the segment using the aggregated data
plt.plot(aggregated_time, aggregated_magnitude, '-')

# Customize the chart
plt.xlabel('Time')
plt.ylabel('Magnitude')
plt.title('Line Chart of Random Segment (5 seconds)')
plt.grid(True)

# Display the chart
plt.show()
