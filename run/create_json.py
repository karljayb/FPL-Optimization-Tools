import requests
import sys
import json
import subprocess
from subprocess import Popen, DEVNULL

def save_json_from_url(url, filename):
    # Fetch the JSON data from the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for unsuccessful requests
    
    # Save the entire JSON data to a file with correct encoding
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(response.json(), file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    json_filename = '../run/bootstrap-static.json'
    
    # Fetch and save the JSON data
    save_json_from_url(url, json_filename)
    print(f"Data saved to {json_filename}")
    
    if len(sys.argv) > 1:
        ff_format = sys.argv[1]
    else:
        print("No ff_format argument provided")

    if 'ftvamps' in ff_format:
        script_path = 'ft_player_updates.py'
        subprocess.run(['python', script_path], check=True)
    elif 'sdtvamps' in ff_format:
        script_path = 'sdt_player_updates.py'
        subprocess.run(['python', script_path], check=True)

