import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
import html
import re

# Function to extract text between two specific symbols
# Params: Orginal text
# Output: Ordered list of extracted terms
def extract_between_custom_symbols(text, start_symbol, end_symbol):
    pattern = re.compile(re.escape(start_symbol) + '(.*?)' + re.escape(end_symbol))
    matches = pattern.findall(text)
    return matches

# Function to replace the IDs with the appropriate string
# Params: Original text, List of ordered sub_terms
# Output: Revised text with sub_terms inserted
def replace_with_list_items(text, replacement_list):
    pattern = re.compile(r'@(.*?)@')
    replaced_text = pattern.sub(lambda x: replacement_list.pop(0), text)
    return replaced_text

# Function to grab the term from the url
def id_to_term(id_list):
    sub_terms = [];
    for id in id_list:
        url = 'https://doi.org/10.1351/goldbook.' + id
        #print(url)
        try:
            response = requests.get(url)
            response.encoding = 'utf-8'  # Set the correct encoding

            if response.status_code == 200:

                html_content = response.text
                decoded_content = html.unescape(html_content)
                soup = BeautifulSoup(decoded_content, 'html.parser')

                element = soup.find('div', class_='panel-footer text-justify')
                dirty_term = element.get_text()

                clean_term = extract_between_custom_symbols(dirty_term, "'", "'")
                
                #print(clean_term)
                
                sub_terms.append(clean_term[0])
            else:
                print(f"Failed to fetch term for URL: {url}")
        except Exception as e:
            print(f"Error occurred while fetching term: {e}")
    return sub_terms

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
            
            definition = deftext_div.get_text()
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
                sub_term_ids = extract_between_custom_symbols(definition, "@", "@")
                print(sub_term_ids)
                sub_terms = id_to_term(sub_term_ids)
                print(sub_terms)
                subbed_definition = replace_with_list_items(definition, sub_terms)
                extracted_data.append({
                    'Title': value['title'],
                    'Status': value['status'],
                    'URL': value['url'],
                    'Definition': subbed_definition
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
