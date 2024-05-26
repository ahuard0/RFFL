import random

import numpy
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import linkage, fcluster


def plotClusteredSample(limited_data: DataFrame, clusters_unique: numpy.ndarray, color_clusters_unique: list, clusters_all: numpy.ndarray) -> None:
    """
    Plot clustered sample points based on hierarchical clustering.

    Args:
        limited_data (pd.DataFrame): DataFrame containing signal indices and data for clustering.
        clusters_all (numpy.ndarray): Array containing all cluster assignments for each data point.
        clusters_unique (numpy.ndarray): Array containing unique cluster assignments.
        color_clusters_unique (list): List of colors for visualizing unique clusters.

    Returns:
        None

    Notes:
        - The function iterates over unique clusters and plots points color-coded by cluster.
        - The cluster assignments and colors are provided by the hierarchical clustering results.
    """
    for cluster_id, color in zip(clusters_unique, color_clusters_unique):
        cluster_points = limited_data[clusters_all == cluster_id]
        plt.scatter(cluster_points['signal_indices'], cluster_points['signal_data'], color=color, alpha=0.7,
                    label=f'Cluster {cluster_id}')

    # Set labels and title
    plt.xlabel('Index')
    plt.ylabel('Magnitude')
    plt.title('Clustered Sample Points')
    plt.show()


class Telemetry:
    def __init__(self, file_path='raw_telemetry_20230704.txt'):
        """
        Initializes an instance of Telemetry with data from a specified file.

        Args:
            file_path (str, optional): The path to the telemetry data file. Defaults to '../raw_telemetry_20230704.txt'.
        """
        self.clusters_all = None
        self.colors_clusters_unique = None
        self.n_clusters_unique = None
        self.clusters_unique = None
        self.limited_data = None
        self.segment_duration = None
        self.noise_std = None
        self.noise_mean = None
        self.sigma = None
        self.temp_threshold = None
        self.segment_mean = None
        self.data_file_path = file_path
        self.magnitude = []
        self.indices = []
        self.threshold = None
        with open(self.data_file_path, 'r') as file:  # Read the data from file
            for line in file:
                line = line.strip()
                if line:
                    ind, m = line.split(',')
                    self.indices.append(int(ind))
                    self.magnitude.append(int(m))

    def getRandomSample(self, segment_duration_ms=10000.0) -> tuple:
        """
        Retrieve a random sample of telemetry data.

        Args:
            segment_duration_ms (float, optional): time range for the segment.  Defaults to 10000.0.

        Returns:
            tuple: Two lists - one for magnitude and one for indices.
        """
        segment_duration_index = round(segment_duration_ms)  # Round segment_duration_ms to the nearest integer for indexing
        self.segment_duration = segment_duration_index

        start_index = random.randint(0, len(self.magnitude) - segment_duration_index)
        segment_magnitude = self.magnitude[start_index:start_index + segment_duration_index]
        segment_indices = self.indices[start_index:start_index + segment_duration_index]
        return segment_magnitude, segment_indices

    def calcThreshold(self, segment_magnitude: list, sigma=3.0) -> float:
        """
        Calculate the threshold for noise rejection.

        Args:
            segment_magnitude (list): segment magnitude data
            sigma (float): number of standard deviations for noise rejection thresholding

        Returns:
            float: the threshold for noise rejection
        """
        # Set temporary threshold for noise calculation
        self.segment_mean = np.mean(segment_magnitude)
        self.temp_threshold = 3 * self.segment_mean
        self.sigma = sigma

        # Calculate the mean and standard deviation of the noise using the temporary threshold
        noise_data = [x for x in segment_magnitude if x <= self.temp_threshold]
        self.noise_mean = np.mean(noise_data)
        self.noise_std = np.std(noise_data)

        # Calculate the new threshold based on the mean of noise plus 3 standard deviations
        self.threshold = self.noise_mean + sigma * self.noise_std
        return self.threshold

    def getLimitedSample(self, segment_duration_ms=10000.0, sigma=3.0) -> tuple:
        """
        Retrieves a limited sample of telemetry data based on a specified segment duration and sigma value.

        Args:
            segment_duration_ms (float, optional): Time range for the segment in milliseconds. Defaults to 10000.0.
            sigma (float, optional): The number of standard deviations to use in threshold calculation. Defaults to 3.0.

        Returns:
            tuple: A tuple containing two lists - signal data and corresponding indices.
                   - signal_data (list): The subset of magnitude data above the calculated threshold.
                   - signal_indices (list): The corresponding indices for the signal data.

        Note:
            This method internally uses the getRandomSample and calcThreshold methods to generate the limited sample.
        """
        segment_magnitude, segment_indices = self.getRandomSample(segment_duration_ms)
        threshold = self.calcThreshold(segment_magnitude, sigma)

        # Separate the signal from the noise
        signal_data = [x for x in segment_magnitude if x > threshold]
        signal_indices = [ind for ind, x in zip(segment_indices, segment_magnitude) if x > threshold]

        limited_data = signal_data, signal_indices
        return limited_data

    def getLimitedSampleDataFrame(self, segment_duration_ms=10000.0, sigma=3.0) -> DataFrame:
        """
        Retrieves a limited sample of telemetry data and returns it as a DataFrame.

        Args:
            segment_duration_ms (float, optional): Time range for the segment in milliseconds. Defaults to 10000.0.
            sigma (float, optional): The number of standard deviations to use in threshold calculation. Defaults to 3.0.

        Returns:
            pd.DataFrame: A DataFrame containing the limited sample data.
                          Columns:
                          - 'signal_indices': The indices corresponding to the signal data.
                          - 'signal_data': The subset of magnitude data above the calculated threshold.

        Note:
            This method internally uses the getLimitedSample method to generate the limited sample.
        """
        signal_data, signal_indices = self.getLimitedSample(segment_duration_ms, sigma)
        self.limited_data = pd.DataFrame({'signal_indices': signal_indices, 'signal_data': signal_data})
        return self.limited_data

    def getClusteredSample(self, limited_data: DataFrame, cluster_cut_threshold=200) -> tuple:
        """
        Perform hierarchical clustering on a DataFrame and return information about the resulting clusters.

        Args:
            limited_data (pd.DataFrame): DataFrame containing signal indices for clustering.
            cluster_cut_threshold (float, optional): The distance threshold for cutting the dendrogram to form clusters.
                                                      Adjust this threshold as needed. Defaults to 200.

        Returns:
            tuple: A tuple containing information about the clusters.
                   - clusters_unique (numpy.ndarray): An array containing unique cluster assignments.
                   - colors_clusters_unique (list): A list of colors for visualizing unique clusters.
                   - clusters_all (numpy.ndarray): An array containing all cluster assignments for each data point.

        Notes:
            - The hierarchical clustering is performed using the 'ward' method.
            - The resulting clusters are determined based on the distance criterion using the cut_threshold.
            - Cluster information includes unique cluster assignments, colors for visualization, and all cluster assignments.
        """
        linkage_matrix = linkage(limited_data[['signal_indices']], method='ward')  # Perform hierarchical clustering to group data based on signal indices
        cut_threshold = cluster_cut_threshold  # Define the threshold for cutting the dendrogram, adjust this threshold as needed
        self.clusters_all = fcluster(linkage_matrix, cut_threshold, criterion='distance')  # Cut the dendrogram to form clusters based on the threshold

        # Scatter points, color-coded by cluster
        self.clusters_unique = np.unique(self.clusters_all)
        self.n_clusters_unique = len(self.clusters_unique)
        self.colors_clusters_unique = sns.color_palette('hsv', self.n_clusters_unique)

        return self.clusters_unique, self.colors_clusters_unique, self.clusters_all


def main():
    # -----------------------------------------------------------------------------------
    # Get Telemetry and Limit by Noise Thresholding (3 Sigma), then plot the result
    # -----------------------------------------------------------------------------------
    telemetry_obj = Telemetry()  # Create an instance of the Telemetry class

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

    # -----------------------------------------------------------------------------------
    # Cluster the limited telemetry, then plot the result
    # -----------------------------------------------------------------------------------
    clusters_unique, colors_clusters_unique, clusters_all = telemetry_obj.getClusteredSample(limited_data)
    plotClusteredSample(limited_data, clusters_unique, colors_clusters_unique, clusters_all)


if __name__ == "__main__":
    main()
