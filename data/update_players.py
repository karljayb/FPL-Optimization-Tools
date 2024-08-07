import pandas as pd
from unidecode import unidecode


# Read the CSV files
fpl_players = pd.read_csv('fpl_players.csv')
sdt_players = pd.read_csv('sdt players.csv', encoding='utf-8')
fanteam_players = pd.read_csv('Fanteam Players.csv')

# Function to remove accents
def remove_accents(name):
    if isinstance(name, str):
        return unidecode(name)
    return name

# Apply the remove_accents function to the relevant columns
sdt_players['First Name'] = sdt_players['First Name'].apply(remove_accents)
sdt_players['Last Name'] = sdt_players['Last Name'].apply(remove_accents)

# Match FPL_ID from fpl_players to sdt_players
sdt_players['FPL_ID'] = sdt_players['ID'].map(fpl_players.set_index('Code')['Id'])


# Move the FPL_ID column to the first position
cols = sdt_players.columns.tolist()
cols.insert(0, cols.pop(cols.index('FPL_ID')))
sdt_players = sdt_players[cols]

# Step 2: Copy Id from sdt_players to Fanteam Players
def match_player(row, sdt_df):
    # Check if Last Name is provided
    if pd.notna(row['Last Name']) and row['Last Name'] != '':
        # Create a boolean mask for rows where Last Name matches
        last_name_match = sdt_df['Last Name'] == row['Last Name']
    else:
        # If Last Name is empty, set last_name_match to all True
        last_name_match = pd.Series([True] * len(sdt_df))
    
    # Check if First Name is provided
    if pd.notna(row['First Name']) and row['First Name'] != '':
        # Create a boolean mask for rows where First Name matches
        first_name_match = sdt_df['First Name'] == row['First Name']
    else:
        # If First Name is empty, set first_name_match to all True
        first_name_match = pd.Series([True] * len(sdt_df))
    
    # Combine the conditions
    match = sdt_df[last_name_match & first_name_match]

    # if  match.empty:
    #     print(f"No match found for {row['First Name']} {row['Last Name']}")
    
    # Return the FPL_ID if a match is found, otherwise None
    return match['FPL_ID'].values[0] if not match.empty else None

fanteam_players['FPL_ID'] = fanteam_players.apply(lambda row: match_player(row, sdt_players), axis=1)


# Move the FPL_ID column to the first position
cols = fanteam_players.columns.tolist()
cols.insert(0, cols.pop(cols.index('FPL_ID')))
fanteam_players = fanteam_players[cols]

# Save the updated files
sdt_players.to_csv('sdt_players_updated.csv', index=False)
fanteam_players.to_csv('Fanteam_Players_updated.csv', index=False)

print("Process completed. Updated files have been saved.")


# Read the files
ftvamps_df = pd.read_csv('ftvamps.csv')
jc_model_df = pd.read_csv('jc_fanteam_model_RAW.csv')
ft_playerlist_df = pd.read_csv('Fanteam_Players_updated.csv')

# Rename columns in jc_model_df to match ftvamps_df
jc_model_df = jc_model_df.rename(columns={
    'Value': 'BV',
    '1_xMins': '1_xMins',
    '1_Pts': '1_Pts',
    '2_xMins': '2_xMins',
    '2_Pts': '2_Pts',
    '3_xMins': '3_xMins',
    '3_Pts': '3_Pts',
    '4_xMins': '4_xMins',
    '4_Pts': '4_Pts',
    '5_xMins': '5_xMins',
    '5_Pts': '5_Pts',
    '6_xMins': '6_xMins',
    '6_Pts': '6_Pts'
})

# Add SV column with values equal to BV
jc_model_df['SV'] = jc_model_df['BV']

# Replace team abbreviations with full names
jc_model_df['Team'] = jc_model_df['Team'].replace({
    'ARS': 'Arsenal',
    'AVL': 'Aston Villa',
    'BOU': 'Bournemouth',
    'BRE': 'Brentford',
    'BHA': 'Brighton',
    'CHE': 'Chelsea',
    'CRY': 'Crystal Palace',
    'EVE': 'Everton',
    'FUL': 'Fulham',
    'IPS': 'Ipswich',
    'LEI': 'Leicester',
    'LIV': 'Liverpool',
    'MCI': 'Man City',
    'MUN': 'Man Utd',
    'NEW': 'Newcastle',
    'FOR': "Nott'm Forest",
    'SOU': 'Southampton',
    'TOT': 'Spurs',
    'WHU': 'West Ham',
    'WOL': 'Wolves'
})

# Merge jc_model_df with ft_playerlist_df to update the ID column
jc_model_df = jc_model_df.merge(ft_playerlist_df[['ID', 'FPL_ID']], on='ID', how='left')

# Update the ID column with FPL_ID where available, and set ID to empty string if no match is found
jc_model_df['ID'] = jc_model_df['FPL_ID'].fillna('')

# Drop the FPL_ID column as it's no longer needed
jc_model_df = jc_model_df.drop(columns=['FPL_ID'])

# Find rows with empty ID
empty_id_rows = jc_model_df[(jc_model_df['ID'] == '') & (jc_model_df['total_pts'] >= 1)]
print("Rows with empty ID and total_pts >= 1:")
print(empty_id_rows)

# Reorder columns to match ftvamps_df
column_order = ['Pos', 'ID', 'Name', 'BV', 'SV', 'Team']
column_order += [f'{i}_{suffix}' for i in range(1, 13) for suffix in ['xMins', 'Pts']]
# Add missing columns with default values
for col in column_order:
    if col not in jc_model_df.columns:
        if col.endswith('_xMins') or col.endswith('_Pts'):
            jc_model_df[col] = 0  # Default value for missing xMins and Pts columns

# Reorder columns
jc_model_df = jc_model_df[column_order]

# Save the modified DataFrame to a new CSV file
jc_model_df.to_csv('jc_fanteam_model.csv', index=False)

print("File has been successfully modified and saved as 'jc_fanteam_model.csv'")



def compare_and_update_files_based_on_key(old_file, new_file, key_column):
    # Read the old and new CSV files
    old_df = pd.read_csv(old_file)
    new_df = pd.read_csv(new_file)
    
    # Print initial row counts for debugging
    # print(f"Initial rows in {old_file}: {len(old_df)}")
    # print(f"Initial rows in {new_file}: {len(new_df)}")

    # Identify rows to add to old_df (rows in new_df with key_column not in old_df)
    rows_to_add = new_df[~new_df[key_column].isin(old_df[key_column])]
    
    # Identify rows to remove from old_df (rows in old_df with key_column not in new_df)
    rows_to_remove = old_df[~old_df[key_column].isin(new_df[key_column])]

    # Print rows to add and remove for debugging
    # print(f"Rows to add to {old_file}:")
    # print(rows_to_add)
    # print(f"Rows to remove from {old_file}:")
    # print(rows_to_remove)

    # Update old_df by adding new rows and removing old rows
    updated_df = pd.concat([old_df, rows_to_add], ignore_index=True).drop(rows_to_remove.index)
    
    # Print final row count for debugging
    # print(f"Final rows in {old_file} after update: {len(updated_df)}")

    # Save the updated old_df back to the original old file
    updated_df.to_csv(old_file, index=False)
    # print(f"File '{old_file}' has been successfully updated.")

# File paths and key columns
files_and_keys = [
    ('fpl_players.csv', 'fpl_players NEW.csv', 'Id'),
    ('sdt players.csv', 'sdt players NEW.csv', 'ID'),
    ('Fanteam Players.csv', 'Fanteam Players NEW.csv', 'ID')
]

# Process each pair of files
for old_file, new_file, key_column in files_and_keys:
    compare_and_update_files_based_on_key(old_file, new_file, key_column)
