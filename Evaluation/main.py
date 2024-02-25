import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def start():
    # Load data from Excel spreadsheet
    df = pd.read_excel('Evaluation_Data.xlsx')

    # Get unique azimuth and range values
    azimuths = np.deg2rad(df['Azimuth']).unique()
    ranges = df['Range'].unique()
    error = df['Error']

    # Create meshgrid for r and theta
    theta, r = np.meshgrid(azimuths, ranges)

    # Reshape error vector to match the shape of r and theta meshgrid
    error_reshaped = error.values.reshape(theta.shape)

    # Create a polar plot
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

    # Plot the data with colormap 'magma'
    c = ax.pcolormesh(theta, r, error_reshaped, cmap='magma', shading='auto', vmin=0, vmax=10)

    # Add a colorbar
    plt.colorbar(c, ax=ax, label='Intensity')

    # Set azimuth ticks every 5 degrees
    ax.set_xticks(np.deg2rad(np.arange(-35, 36, 5)))

    # Hide the tick lines but keep the tick marks visible
    ax.tick_params(axis='both', which='both', length=5, width=0)

    # Set labels
    ax.set_xlabel('Azimuth (degrees)')
    ax.set_ylabel('Range (meters)')

    # Adjust the plot to have a fan shape
    ax.set_thetamin(-35)
    ax.set_thetamax(35)

    # Set radial limit to 1 meter
    ax.set_ylim(0, 5)  # Adjust the range limit according to your data range

    # Hide radial axes beyond r < 1
    ax.spines['polar'].set_visible(False)

    # Show the plot
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start()
