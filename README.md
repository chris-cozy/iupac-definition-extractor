# iupac-definition-extractor

This Python program serves to extract definitions from the IUPAC key-value store by searching through a JSON file based on user-defined terms. Utilizing Pandas, it generates a table and exports the retrieved definitions into a downloadable CSV format. This tool facilitates easy access to IUPAC terminology.

The IUPAC Term Extractor is a Python tool designed to search and extract definitions from a JSON file containing IUPAC (International Union of Pure and Applied Chemistry) terminology. This tool utilizes user-defined terms to locate corresponding entries within the JSON dataset and generates a CSV file containing relevant metadata.

## Features
- **Search Functionality**: Allows users to specify terms of interest to search within the provided JSON file.
- **Data Extraction**: Retrieves metadata such as title, status, and URL associated with the specified terms.
- **CSV Generation**: Creates a structured table in CSV format containing extracted data for easy access and integration into various applications.
- **Error Handling**: Provides error messages in case of file loading or conversion issues for seamless troubleshooting.

## Installation
1. Clone this repository to your local machine
```
git clone https://github.com/your-username/iupac-term-extractor.git
```
2. Install the required dependencies
```
pip install pandas
```

## Usage
### Inputs
- **JSON File**: A JSON file containing IUPAC terminology (goldbook_terms_2023_.json in this example).
- **Output CSV File**: A CSV file where extracted data will be saved (extracted_terms.csv in this example).
- **Terms to Extract**: Specify the terms of interest within the terms_to_extract list in the code.
### Running the Program
```
python iupac_extractor.py
```
Ensure to modify the `input_json_file`, `output_csv_file`, and `terms_to_extract` variables within the `iupac_extractor.py` script according to your requirements.

## Contributing
Contributions to enhance functionality, improve code quality, or address issues are welcome! Please fork the repository, create a new branch, and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.