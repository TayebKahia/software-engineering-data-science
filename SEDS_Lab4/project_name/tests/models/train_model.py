import csv
from src.models.row_2_list import row_to_list # Import the function to be tested
import pytest

# Load your dataset from the CSV file
dataset = []
with open('house_price.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)  
    for row in csvreader:
        dataset.append(row)

print(dataset)
# Test if the function correctly handles rows with missing values
# Parametrize the test function to iterate through each row in the dataset

@pytest.mark.parametrize("input_row", dataset)
def test_row_to_list_with_missing_values(input_row):
    input_string = ' '.join(input_row)  # Convert list to a  string 
    output_list = row_to_list(input_string)  
    
    # Check if any value is empty (indicating a missing value)
    assert all(value.strip() != "" for value in output_list), \
        f"Row contains missing values: {output_list}"
