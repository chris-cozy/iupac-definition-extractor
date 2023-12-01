import pandas as pd
import json
import requests
from bs4 import BeautifulSoup


# Function to find nested divs with class 'term'
def find_nested_terms(element):
    terms = []
    if element.name == 'div' and 'term' in element.get('class', []):
        terms.append(element.text)  # Do whatever you want with the found div element
    for child in element.children:
        print(child)
        if child.name == 'div' and 'term' in child.get('class', []):
            terms.append(child.text)  # Do whatever you want with the found div element
        if child.name is not None:
            child_terms = find_nested_terms(child)
            for term in child_terms:
                terms.append(term)
    return terms

def get_definition(url):
    # Perform web scraping to extract the definition from the IUPAC website
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Assuming the definition is inside a specific HTML tag or class
            outer_div = soup.find('div', class_='deftext')  # Update this according to HTML structure
            terms = find_nested_terms(outer_div)
            for term in terms:
                print(term)
            definition = outer_div.get_text()
            #print(definition)
            return definition.strip()
        else:
            print(f"Failed to fetch definition for URL: {url}")
    except Exception as e:
        print(f"Error occurred while fetching definition: {e}")
    return None


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
                definition = get_definition(value['url']) # Fetch definition using the URL
                extracted_data.append({
                    'Title': value['title'],
                    'Status': value['status'],
                    'URL': value['url'],
                    'Definition': definition
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
