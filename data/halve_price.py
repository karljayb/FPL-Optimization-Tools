import pandas as pd
import os

# Define the filename
filename = 'sdtvamps.csv'

# Check if the file exists
if not os.path.isfile(filename):
    raise FileNotFoundError(f"{filename} not found in the current directory.")

# Load the CSV file into a DataFrame
df = pd.read_csv(filename)

# Check if columns D and E exist (by index)
if len(df.columns) < 5:
    raise ValueError("The CSV file must have at least 5 columns.")

# Columns D and E are indexed as 3 and 4 (0-based indexing)
# Halve the values in columns D and E
df.iloc[:, 3] = df.iloc[:, 3] / 2
df.iloc[:, 4] = df.iloc[:, 4] / 2

# Save the modified DataFrame to a new CSV file
df.to_csv('sdtvamps_modified.csv', index=False)

print("The values in columns D and E have been halved and saved to 'sdtvamps_modified.csv'.")
