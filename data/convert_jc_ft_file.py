import pandas as pd

# Read the files
ftvamps_df = pd.read_csv('ftvamps.csv')
jc_model_df = pd.read_csv('jc_fanteam_model_38420984309834.csv')
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