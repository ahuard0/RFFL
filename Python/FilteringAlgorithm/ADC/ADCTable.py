class ADCTable:
    # Constants for the channel formulas
    CHANNEL_FORMULAS = {
        1: (16.468, 1155.3),
        2: (16.461, 1145.5),
        3: (16.272, 1131.4),
        4: (16.014, 1121)
    }

    def __init__(self):
        pass

    def convert_adc_to_dbm(self, adc_values: list, channel_num: int) -> list:
        """
        Convert ADC value to power in dBm for the specified channel.

        Args:
            adc_values (list): The ADC values to be converted.
            channel_num (int): The channel (1, 2, 3, 4) for which to apply the conversion formula.

        Returns:
            list: The powers in dBm.
        """
        if channel_num not in self.CHANNEL_FORMULAS:
            raise ValueError("Invalid channel. Choose from 1, 2, 3, or 4.")

        adc_values = [min(value, 1023) for value in adc_values]  # Limit to 1023
        adc_values = [max(value, 0) for value in adc_values]  # Limit to 0

        slope, intercept = self.CHANNEL_FORMULAS[channel_num]
        powers_dbm = [(adc_value - intercept) / slope for adc_value in adc_values]  # Convert each ADC value to power in dBm

        return powers_dbm

    def convert_dbm_to_adc(self, powers_dbm: list, channel_num: int) -> list:
        """
        Convert ADC value to power in dBm for the specified channel.

        Args:
            powers_dbm (list): The power values in dBm to be converted.
            channel_num (int): The channel (1, 2, 3, 4) for which to apply the conversion formula.

        Returns:
            list: adc_values: The ADC values returned.
        """
        if channel_num not in self.CHANNEL_FORMULAS:
            raise ValueError("Invalid channel. Choose from 1, 2, 3, or 4.")

        max_power_dBm = float(self.convert_adc_to_dbm([1023], channel_num)[0])
        min_power_dBm = float(self.convert_adc_to_dbm([0], channel_num)[0])

        powers_dbm = [min(value, max_power_dBm) for value in powers_dbm]
        powers_dbm = [max(value, min_power_dBm) for value in powers_dbm]

        slope, intercept = self.CHANNEL_FORMULAS[channel_num]
        adc_values = [slope * power_dbm + intercept for power_dbm in powers_dbm]  # Convert each power in dBm to ADC values
        return adc_values


def test_adc_conversion():
    # Create an instance of ADCTableConverter
    adc_table = ADCTable()

    # Example usage:
    adc_value_U = [1000, 511, 437]  # Replace with your ADC value
    channel = 1  # Replace with the desired channel (1, 2, 3, or 4)

    power_value_dbm = adc_table.convert_adc_to_dbm(adc_value_U, channel)
    print(f"Power in dBm for channel {channel}: {power_value_dbm} dBm")

    adc_value_U_returned = adc_table.convert_dbm_to_adc(power_value_dbm, channel)
    print(f"ADC value for channel {channel}: {adc_value_U_returned} U")


if __name__ == "__main__":
    test_adc_conversion()
