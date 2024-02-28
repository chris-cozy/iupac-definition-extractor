# iupac-definition-extractor

The IUPAC Definition Extractor is a Python tool designed to search and extract definitions from a JSON file containing IUPAC (International Union of Pure and Applied Chemistry) terminology. This tool utilizes user-defined terms to locate corresponding entries within the JSON dataset and generates a CSV file containing the terms' relevant metadata.

## Features

- **Search Functionality**: Allows users to specify terms of interest, in the form of a csv file, to search within the provided JSON file.
- **Data Extraction**: Retrieves metadata such as title, status, IUPAC URL, and definition associated with the specified terms.
- **CSV Generation**: Creates a structured table in CSV format containing extracted data for easy access and integration into various applications.
- **Error Handling**: Provides error messages in case of file loading or conversion issues for seamless troubleshooting.

## Usage

### Inputs

- **JSON File**: A JSON file containing IUPAC terminology (goldbook_terms_2023_.json in this use case).
- **Output CSV File**: A CSV file where extracted data will be saved (extracted_terms.csv in this example).
- **Input CSV File**: The terms of interest will be in csv format, in the first column, with one term per row.

### Running the Program (Windows using Python Venv)

```
git clone https://github.com/chris-cozy/iupac-definition-extractor.git
cd iupac-definition-extractor
python -m venv extractor_env
extractor_env/Scripts/activate
pip install -r requirements_versions.txt
python extractor.py
```

Ensure to create the `input_terms.csv` file containing the terms of interest, before running the program. Format this file to use a single column, with each unique term on a separate row.

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

- **Test extract between custom symbols**: This test checks whether the function correctly extracts text between specified start and end symbols from a given text.
- **Test replace with list items**: This test verifies that the function correctly replaces placeholders in the text with items from a given replacement list.
- **Test id to term**: This test checks whether the function retrieves terms from the source JSON file based on the provided list of IDs.
- **Test get definition**: This test verifies the functionality of fetching definitions from URLs, including the proper retrieval and extraction of definition text.


## Contributing

Contributions to enhance functionality, improve code quality, or address issues are welcome! Please fork the repository, create a new branch, and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
