import random
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

# Set the number of data points
num_data_points = 1000

# Set the range for azimuth and elevation
azimuth_range = (-45, 45)
elevation_range = (-45, 45)

# Define the cluster centers
cluster_centers = [(-20, 5), (5, 0), (30, -2)]

# Set the standard deviation for narrowing the clusters
std_deviation = 2  # Change this value to adjust the cluster width

# Generate the dataset
dataset = []
for i in range(num_data_points):
    time_ms = round(i * 2.3)  # Time in milliseconds

    # Choose a random cluster center
    center = random.choice(cluster_centers)
    center_azimuth, center_elevation = center

    # Add random noise to the cluster center coordinates
    azimuth = random.gauss(center_azimuth, std_deviation)
    elevation = random.gauss(center_elevation, std_deviation)

    # Ensure the generated values are within the specified ranges
    azimuth = max(min(azimuth, azimuth_range[1]), azimuth_range[0])
    elevation = max(min(elevation, elevation_range[1]), elevation_range[0])

    dataset.append((azimuth, elevation))

# Extract the x and y coordinates from the dataset
x = [point[0] for point in dataset]
y = [point[1] for point in dataset]

# Save the dataset to a text file
output_file = 'Telemetry/TB/scatter_data.txt'  # Specify the desired output file name

with open(output_file, 'w') as file:
    for point in dataset:
        azimuth, elevation = point
        file.write(f"{azimuth},{elevation}\n")

# Plot the scatter plot
fig, ax = plt.subplots()
ax.scatter(x, y)
ax.set_xlabel('Azimuth (degrees)')
ax.set_ylabel('Elevation (degrees)')
ax.set_title('Scatter Plot of Telemetry Data')
ax.grid(True)

# Add confidence interval ellipses for each cluster
for center in cluster_centers:
    ellipse = Ellipse(center, 2 * std_deviation, 2 * std_deviation,
                      edgecolor='r', facecolor='none', linestyle='--')
    ax.add_patch(ellipse)

plt.show()
