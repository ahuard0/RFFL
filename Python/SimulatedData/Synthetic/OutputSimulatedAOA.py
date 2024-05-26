def process_csv(input_file, output_file):
    with open(input_file, 'r') as file:
        # Read the CSV file and parse it into rows
        rows = file.readlines()

        # Remove the header row
        header_removed_rows = rows[1:]

        # Remove the first column of each row and replace newlines with spaces
        modified_rows = [','.join(row.strip().split(',')[1:]) for row in header_removed_rows]

        # Combine all modified rows into a single string
        modified_data = '\n'.join(modified_rows)
        modified_data = modified_data.replace('\n', ', ')

    with open(output_file, 'w') as file:
        file.write(modified_data)

# Replace 'input.csv' and 'output.csv' with your input and output file paths
process_csv('synth_data_45deg_20240303.csv', 'synth_final_20240303.csv')

