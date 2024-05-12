import pandas as pd

def sort_and_group_csv(input_filename, output_filename):
    # Load the data from CSV
    df = pd.read_csv(input_filename)
    
    # Sorting by 'Pulse' and then by 'Source Node'
    sorted_df = df.sort_values(by=['Source Node', 'Pulse'])
    
    # Save the sorted data back to a new CSV file
    sorted_df.to_csv(output_filename, index=False)
    print("Data has been sorted and saved to", output_filename)

# Example usage
sort_and_group_csv('ByzantineAuth.csv', 'SortedByzantineAuth.csv')
