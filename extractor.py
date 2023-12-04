import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
import html


# Function to find nested divs with class 'term'
def find_nested_terms(element):
    if element is None:
        return  # If the element is None, exit the function

    if element.name == 'div' and 'term' in element.get('class', []):
        print(element.text)  # If element is a term
    for child in element.children:
        if child.name is not None:
            find_nested_terms(child)


def get_definition(url):
    # Perform web scraping to extract the definition from the IUPAC website
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'  # Set the correct encoding

        if response.status_code == 200:

            html_content = response.text
            decoded_content = html.unescape(html_content)
            soup = BeautifulSoup(decoded_content, 'html.parser')

            deftext_div = soup.find('div', class_='deftext')  # Update this according to HTML structure
            find_nested_terms(deftext_div)
            
            definition = deftext_div.get_text()

            print(definition)
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
