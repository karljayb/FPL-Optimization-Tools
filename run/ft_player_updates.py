import json
import csv

# Define the mapping from 'Pos' to 'element_type'
POS_TO_ELEMENT_TYPE = {
    'G': 1,  # Goalkeeper
    'D': 2,  # Defender
    'M': 3,  # Midfielder
    'F': 4   # Forward
}


def read_csv(file_path):
    updates = {}
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        # Print the fieldnames to check for discrepancies
        # print("CSV Fieldnames:", reader.fieldnames)
        for row in reader:
            id_value = row.get('ID', '').strip()
            bv_value = row.get('BV', '').strip()
            pos_value = row.get('Pos', '').strip()
            if id_value and bv_value and pos_value:
                bv_value = float(bv_value) * 10
                pos_to_type = POS_TO_ELEMENT_TYPE.get(pos_value)
                if pos_to_type is not None:
                    updates[id_value] = {'bv': bv_value, 'element_type': pos_to_type}
    return updates

def update_json(json_file_path, updates):
    with open(json_file_path, mode='r', encoding='utf-8') as file:
        data = json.load(file)
    
    elements_updated = 0
    for element in data.get('elements', []):
        id_value = str(element.get('id'))
        if id_value in updates:
            update_info = updates[id_value]
            # Update now_cost if it differs
            if element['now_cost'] != int(update_info['bv']):
                element['now_cost'] = int(update_info['bv'])
                print(f"Updated now_cost for ID {id_value} to {element['now_cost']}")
            # Update element_type if it differs
            if element['element_type'] != update_info['element_type']:
                element['element_type'] = update_info['element_type']
                print(f"Updated element_type for ID {id_value} to {element['element_type']}")
            elements_updated += 1
    
    # Save the updated JSON data
    with open(json_file_path, mode='w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    
    print(f"Total elements updated: {elements_updated}")

if __name__ == '__main__':
    json_filename = '../run/bootstrap-static.json'
    csv_file_path = '../data/ftvamps.csv'
    
    
    # Read the CSV and get updates
    updates = read_csv(csv_file_path)
    # print("Updates read from CSV:", updates)
    
    # Update the JSON file
    update_json(json_filename, updates)
    print(f"JSON file updated based on CSV data.")
