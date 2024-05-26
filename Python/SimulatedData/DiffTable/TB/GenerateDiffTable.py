import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define the file path
file_path = "../HFSS/pattern_diff_45deg_20231119.csv"

# Read the CSV file into a DataFrame without specifying column names
df = pd.read_csv(file_path, header=None)

# Extract data from columns
azimuth = df[0]  # Assuming the azimuth is in the first column
power_diff = df[1]  # Assuming the power difference is in the second column

# Create a plot
plt.figure(figsize=(10, 6))
plt.plot(azimuth, power_diff, label="Pattern Difference")
plt.title("HFSS Simulation Results")
plt.xlabel("Azimuth Angle (degrees)")
plt.ylabel("Channel Power Difference (dB)")

# Find the minimum and maximum values
min_value = np.min(power_diff)
max_value = np.max(power_diff)

# Find the indices of the minimum and maximum values
min_point = np.where(power_diff == min_value)[0][0]
max_point = np.where(power_diff == max_value)[0][0]

# Calculate the midpoint between the minimum and maximum points
midpoint = (min_point + max_point) // 2

# Define a range for the middle portion
# noinspection PyTypeChecker
range_start = min(min_point, max_point)
# noinspection PyTypeChecker
range_end = max(min_point, max_point)

# Extract the middle portion of the curve
truncated_azimuth = azimuth[range_start:range_end+1]
truncated_power_diff = power_diff[range_start:range_end+1]

# Check if the truncated curve is monotonic
truncated_power_diff = truncated_power_diff.reset_index(drop=True)
truncated_azimuth = truncated_azimuth.reset_index(drop=True)
if len(truncated_power_diff) >= 2:
    is_monotonic_increasing = True
    is_monotonic_decreasing = True

    try:
        for i in range(len(truncated_power_diff) - 1):
            if truncated_power_diff[i] > truncated_power_diff[i + 1]:
                is_monotonic_increasing = False
            if truncated_power_diff[i] < truncated_power_diff[i + 1]:
                is_monotonic_decreasing = False
    except Exception as e:
        print("error: ", e)

    if is_monotonic_increasing or is_monotonic_decreasing:
        print("The truncated curve is monotonic.")
    else:
        print("The truncated curve is not strictly monotonic.")
else:
    print("The truncated curve contains less than 2 data points, so monotonicity cannot be determined.")


# Create a DataFrame for the lookup table
lookup_table = pd.DataFrame({
    'Azimuth': truncated_azimuth,
    'Power Difference (dB)': truncated_power_diff
})

# Save the lookup table to a CSV file
lookup_table.to_csv('diff_table_45deg_20231119.csv', index=False, header=False)

# Plot the truncated curve in red
plt.plot(truncated_azimuth, truncated_power_diff, 'r', label="Lookup Table", linewidth=4)

# Show the legend
plt.legend()

# Show the updated plot
plt.grid(True)
plt.show()
