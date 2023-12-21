import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
import html
import re
import os
import csv

def sanitize_term(term):
    """
    Sanitizes a term by removing leading/trailing whitespaces and special characters.

    Args:
    - term (str): The term to be sanitized.

    Returns:
    - str: Sanitized term.
    """
    return term.strip()

def extract_between_custom_symbols(text, start_symbol, end_symbol):
    """
    Extracts text between specified start and end symbols from a given text.

    Args:
    - text (str): The original text containing the desired content.
    - start_symbol (str): The starting symbol to identify the beginning of the content to extract.
    - end_symbol (str): The ending symbol to identify the end of the content to extract.

    Returns:
    - list: Ordered list of extracted terms between the specified symbols.
    """
    pattern = re.compile(re.escape(start_symbol) + '(.*?)' + re.escape(end_symbol))
    return pattern.findall(text)

def replace_with_list_items(text, replacement_list):
    """
    Replaces placeholders in the text with items from a given list.

    Args:
    - text (str): The original text containing placeholders.
    - replacement_list (list): List of items to replace the placeholders in the text.

    Returns:
    - str: Revised text with placeholders replaced by items from the list.
    """
    pattern = re.compile(r'@(.*?)@')
    return pattern.sub(lambda x: replacement_list.pop(0), text)

def id_to_term(json_file, id_list):
    """
    Retrieves subterm names from a provided JSON file based on a list of IDs.

    Args:
    - json_file (str): Path to the JSON file containing term metadata.
    - id_list (list): List of IDs used to retrieve subterm names.

    Returns:
    - list: List of extracted subterm names corresponding to the provided IDs.
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError as e:
        print(f"Error: File '{json_file}' not found.")
        raise e
    
    sub_terms = []
    for id in id_list:
        subterm_name = data['terms']['list'][id]['title']
        print(subterm_name)  # Printing the subterm name for demonstration
        sub_terms.append(subterm_name)

    return sub_terms

def get_definition(url):
    """
    Fetches the definition from a given URL (IUPAC website).

    Args:
    - url (str): The URL from which the definition is to be fetched.

    Returns:
    - str or None: Extracted definition text if successful, otherwise None.
    """
    # Validate URL format
    if not url.startswith('https://doi.org/'):
        print("Error: Invalid URL format.")
        return None
    
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            decoded_content = html.unescape(response.text)
            soup = BeautifulSoup(decoded_content, 'html.parser')
            deftext_div = soup.find('div', class_='deftext')
            if deftext_div:
                return deftext_div.get_text().strip()
            else:
                print("Error: Definition not found in the retrieved content.")
                return None
        else:
            print(f"Failed to fetch definition for URL: {url}")
    except Exception as e:
        print(f"Error occurred while fetching definition: {e}")
    return None

def search(terms, json_file, csv_file):
    """
    Searches for terms in a JSON file, extracts metadata, and creates a CSV file with extracted data.

    Args:
    - terms (list): List of terms to search for in the JSON data.
    - json_file (str): Path to the JSON file containing term metadata.
    - csv_file (str): Path to the CSV file to be created with extracted data.

    Returns:
    - None
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError as e:
        print(f"Error: File '{json_file}' not found.")
        raise e

    extracted_data = []
    for term in terms:
        for value in data['terms']['list'].values():
            if value['title'] == term:
                definition = get_definition(value['url'])
                sub_term_ids = extract_between_custom_symbols(definition, "@", "@")
                sub_terms = id_to_term(json_file, sub_term_ids)
                subbed_definition = replace_with_list_items(definition, sub_terms)
                extracted_data.append({
                    'Title': value['title'],
                    'Status': value['status'],
                    'URL': value['url'],
                    'Definition': subbed_definition
                })

    try:
        df = pd.DataFrame(extracted_data)
        df.to_csv(csv_file, index=False)
        print(f"CSV file '{csv_file}' created successfully.")
    except Exception as e:
        print(f"Error occurred while converting to CSV: {e}")


if __name__ == "__main__":
    input_json_file = 'goldbook_terms_2023_.json'
    if not os.path.isfile(input_json_file):
        print(f"Error: File '{input_json_file}' does not exist.")
        exit()

    if not os.access(input_json_file, os.R_OK):
        print(f"Error: No read permissions for file '{input_json_file}'.")
        exit()

    input_csv_file = 'input_terms.csv'
    terms_to_extract = []

    if not os.path.isfile(input_csv_file):
        print(f"Error: File '{input_csv_file}' does not exist.")
        exit()

    if not os.access(input_csv_file, os.R_OK):
        print(f"Error: No read permissions for file '{input_csv_file}'.")
        exit()

    try:
        with open(input_csv_file, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if len(row) > 0:
                    term = sanitize_term(row[0])
                    terms_to_extract.append(term)
    except FileNotFoundError as e:
        print(f"Error: File '{input_csv_file}' not found.")
        raise e

    output_csv_file = 'extracted_terms.csv'
    if os.path.exists(output_csv_file):
        if not os.access(output_csv_file, os.W_OK):
            print(f"Error: No write permissions for file '{output_csv_file}'.")
            exit()
    search(terms_to_extract, input_json_file, output_csv_file)
