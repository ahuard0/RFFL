import random
import matplotlib.pyplot as plt

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

# Plot the line chart for the segment
plt.plot(segment_time, segment_magnitude, '-')

# Customize the chart
plt.xlabel('Time (ms)')
plt.ylabel('Magnitude')
plt.title('Line Chart of Random Segment (5 seconds)')
plt.grid(True)

# Display the chart
plt.show()
