import string
from datetime import datetime

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def generateDifferenceTable(pattern_diff_file_path="./HFSS/Pattern Difference 45 deg Offset.csv") -> string:
    df = pd.read_csv(pattern_diff_file_path, header=None)  # Read the CSV file into a DataFrame without specifying column names
    str_date_now = datetime.now().strftime('%Y%m%d')  # Get today's date

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

    # Define a range for the middle portion
    # noinspection PyTypeChecker
    range_start = min(min_point, max_point)
    # noinspection PyTypeChecker
    range_end = max(min_point, max_point)

    # Extract the middle portion of the curve
    truncated_azimuth = azimuth[range_start:range_end + 1]
    truncated_power_diff = power_diff[range_start:range_end + 1]

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
    lookup_table.to_csv('diff_table_45deg_' + str_date_now + '.csv', index=False, header=False)

    # Plot the truncated curve in red
    plt.plot(truncated_azimuth, truncated_power_diff, 'r', label="Lookup Table", linewidth=4)

    # Show the legend
    plt.legend()

    # Show the updated plot
    plt.grid(True)
    plt.show()

    return pattern_diff_file_path


class DifferenceTable:
    def __init__(self, file_path):
        # Read the CSV file into a DataFrame with column names
        self.lookup_table = pd.read_csv(file_path, names=['Azimuth (deg)', 'Power Difference (dB)'])

    def convert_diff_to_aoa(self, delta_dB: list) -> list:
        """
        Convert a given channel power difference (dB) to the corresponding azimuth angle (degrees).

        Args:
            delta_dB (float): The channel power difference in dB.

        Returns:
            float: The azimuth angle in degrees.
        """
        sorted_lookup_table = self.lookup_table.sort_values(by='Power Difference (dB)')

        diff_vector = sorted_lookup_table['Power Difference (dB)'].astype(float)
        angle_vector = sorted_lookup_table['Azimuth (deg)'].astype(float)

        aoa_deg = np.interp(delta_dB, diff_vector, angle_vector)
        return aoa_deg.tolist()

    def convert_aoa_to_diff(self, angle: list) -> list:
        """
        Convert a given azimuth angle (degrees) to the corresponding channel power difference (dB).

        Args:
            angle (float): The azimuth angle in degrees.

        Returns:
            float: The channel power difference in dB.
        """
        sorted_lookup_table = self.lookup_table.sort_values(by='Azimuth (deg)')

        diff_vector = sorted_lookup_table['Power Difference (dB)'].astype(float)
        angle_vector = sorted_lookup_table['Azimuth (deg)'].astype(float)

        diff = np.interp(angle, angle_vector, diff_vector)
        return diff.tolist()


def main():
    file_path = generateDifferenceTable()

    # Create an instance of the AoaDiffConverter class
    diff_table = DifferenceTable(file_path)

    # Example usage of the conversion functions:
    # Convert from power difference to azimuth
    diff_dB = [-5.0, 100, 0.0]

    azimuth_angle = diff_table.convert_diff_to_aoa(diff_dB)
    print(f"Power difference of {diff_dB} dB corresponds to an azimuth angle of {azimuth_angle} degrees.")

    # Convert from azimuth to power difference
    power_difference = diff_table.convert_aoa_to_diff(azimuth_angle)
    print(f"An azimuth angle of {azimuth_angle} degrees corresponds to a power difference of {power_difference} dB.")


if __name__ == "__main__":
    main()
