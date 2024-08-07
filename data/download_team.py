import browser_cookie3
import requests
import json

# Load cookies from Brave
cookies = browser_cookie3.brave()

# Define the URL you want to access
url = 'https://fantasy.premierleague.com/api/my-team/3161/'

# Make the request with the loaded cookies
response = requests.get(url, cookies=cookies)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    # Save the JSON data to a file
    with open('team.json', 'w') as file:
        json.dump(data, file, indent=4)
    print('Data saved to team.json')
else:
    print(f'Failed to retrieve data. Status code: {response.status_code}')
