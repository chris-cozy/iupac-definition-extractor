# iupac-definition-extractor

The IUPAC Definition Extractor is a Python tool designed to search and extract definitions from a JSON file containing IUPAC (International Union of Pure and Applied Chemistry) terminology. This tool utilizes user-defined terms to locate corresponding entries within the JSON dataset and generates a CSV file containing relevant metadata.

## Features
- **Search Functionality**: Allows users to specify terms of interest to search within the provided JSON file.
- **Data Extraction**: Retrieves metadata such as title, status, and URL associated with the specified terms.
- **CSV Generation**: Creates a structured table in CSV format containing extracted data for easy access and integration into various applications.
- **Error Handling**: Provides error messages in case of file loading or conversion issues for seamless troubleshooting.

## Usage
### Inputs
- **JSON File**: A JSON file containing IUPAC terminology (goldbook_terms_2023_.json in this example).
- **Output CSV File**: A CSV file where extracted data will be saved (extracted_terms.csv in this example).
- **Terms to Extract**: Specify the terms of interest within the terms_to_extract list in the code.
### Running the Program (Windows using Python Venv)
```
git clone https://github.com/chris-cozy/iupac-definition-extractor.git
cd iupac-definition-extractor
python -m venv extractor_env
source extractor_env/Scripts/activate
pip install -r requirements_versions.txt
python extractor.py
```
Ensure to modify the `input_json_file`, `output_csv_file`, and `terms_to_extract` variables within the `extractor.py` script according to your requirements.

## Testing
The script includes a set of tests using Python's unittest module to ensure its functionality:
### Running Tests
1. Entered the virtual environment being used if not in use already.
```
source extractor_env/Scripts/activate
```
2. Execute the following command:
```
python -m unittest test_extractor.py
```
### Test Cases
- **Test valid data**: Checks if the search function generates the expected CSV file with valid data.
- **Test invalid JSON file**: Verifies if the function raises a FileNotFoundError when an invalid JSON file is provided.
- **Clean up**: Removes temporary files created during testing to maintain cleanliness.

## Contributing
Contributions to enhance functionality, improve code quality, or address issues are welcome! Please fork the repository, create a new branch, and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
