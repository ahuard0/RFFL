# Import the ADC and difference table conversion classes from their respective modules
from ADC.ADC_Table import ADCTable
from DiffTable.DifferenceTable import DifferenceTable

# Input AoA value
input_aoa = -15.0  # Replace with your desired AoA value

if input_aoa > 0:
    ultimate_ch = 3
    penultimate_ch = 4
else:
    ultimate_ch = 4
    penultimate_ch = 3

# Define ultimate power level in dBm
ultimate_power = -44.5  # Replace with your desired ultimate power level

# Step 2: Get Delta dB from AOA
adc_table = ADCTable()
diff_table = DifferenceTable(r'..\DiffTable\diff_table_20231015.csv')

# Convert input AoA to channel difference
diff_dB = diff_table.convert_aoa_to_diff(input_aoa)

# Calculate the penultimate power level
penultimate_power = ultimate_power - abs(diff_dB)

# Step 4: Convert Channel Difference to ADC Value
# Find the ADC values for the ultimate power level
adc_values_ultimate = adc_table.convert_dbm_to_adc(ultimate_power, ultimate_ch)

# Find the ADC values for the penultimate power level
adc_values_penultimate = adc_table.convert_dbm_to_adc(penultimate_power, penultimate_ch)

print(f"Input AoA: {input_aoa} degrees")
print(f"Ultimate Power Level (dBm): {ultimate_power}, ADC Value: {adc_values_ultimate}")
print(f"Penultimate Power Level (dBm): {penultimate_power}, ADC Value: {adc_values_penultimate}")
