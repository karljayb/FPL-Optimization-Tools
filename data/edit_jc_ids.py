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

