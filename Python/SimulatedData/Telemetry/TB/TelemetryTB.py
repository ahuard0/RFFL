from datetime import datetime
from matplotlib import pyplot as plt
from Telemetry.Telemetry import Telemetry

telemetry_obj = Telemetry('../raw_telemetry_20230704.txt')  # Create an instance of the Telemetry class

# Create a DataFrame with signal_indices and signal_data
limited_data = telemetry_obj.getLimitedSampleDataFrame()

# Get today's date
str_date_now = datetime.now().strftime('%Y%m%d')

# Define the output file name
output_file = './telemetry_limited_' + str_date_now + '.csv'

# Save the DataFrame to a CSV file
limited_data.to_csv(output_file, index=False)

# Print a message indicating the data has been saved
print(f"Limited data has been saved to {output_file}")

# Plot the original data as a line plot
plt.figure(figsize=(10, 6))
plt.plot(telemetry_obj.indices, telemetry_obj.magnitude, label='Original Data', color='blue', linewidth=2)

# Draw a horizontal line at the threshold for better visualization
plt.axhline(y=telemetry_obj.threshold, color='green', linestyle='--', label='Threshold')

# Plot the detected signal points as markers
plt.scatter(limited_data.get('signal_indices'), limited_data.get('signal_data'), label='Detected Signal', color='red', marker='o', s=50, zorder=10)

# Set labels and title
plt.xlabel('Index')
plt.ylabel('Magnitude')
plt.title('Original Data with Detected Signal Points')
plt.legend()

# Save the plot to a file if needed
plot_output_file = './telemetry_limited_' + str_date_now + '.png'
plt.savefig(plot_output_file)

# Show the plot
plt.show()