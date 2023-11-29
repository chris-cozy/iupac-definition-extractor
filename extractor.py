import pandas as pd
import json

def search(terms, json_file, csv_file):
    # Load the JSON data
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError as e:
        print(f"Error: File '{json_file}' not found.")
        raise e

    extracted_data = []

    # Search for terms and extract metadata
    for term in terms:
        for key, value in data['terms']['list'].items():
            if value['title'] == term:
                extracted_data.append({
                    'Title': value['title'],
                    'Status': value['status'],
                    'URL': value['url']
                })

    
    # Convert DataFrame to CSV file
    try:
        df = pd.DataFrame(extracted_data)
        df.to_csv(csv_file, index=False)
        print(f"CSV file '{csv_file}' created successfully.")
    except Exception as e:
        print(f"Error occurred while converting to CSV: {e}")

# Code to execute when the file is run directly
if __name__ == "__main__":
    input_json_file = 'goldbook_terms_2023_.json'
    output_csv_file = 'extracted_terms.csv'
    terms_to_extract = ['α (alpha), β (beta)', 'α-addition', 'α-decay', 'backbone']

    search(terms_to_extract, input_json_file, output_csv_file)
