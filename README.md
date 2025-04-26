# CSV Editor

This is a simple CSV editor application built with Streamlit. It allows users to load, view, search, create, update, and delete records in a CSV file.

## What it Does

The application provides a user interface to interact with a CSV file.
* It loads data from a specified CSV file (defaulting to `timeline.csv`).
* It displays the data in a searchable table.
* Users can search for records based on any field (key, value, or tags).
* It supports creating new records with unique keys.
* It allows updating existing records.
* It provides functionality to delete records.
* Changes are saved back to the CSV file.
* The CSV file uses a header row starting with '#' to indicate comments, and each data row is expected to have 'key', 'value', and 'tags' fields.

## How to Run

1.  **Save the code:** Save the provided Python code as `app.py`.
2.  **Install Streamlit:** If you haven't already, install Streamlit using pip:
    ```bash
    pip install streamlit
    ```
3.  **Run the application:** Open your terminal or command prompt, navigate to the directory where you saved `app.py`, and run the following command:
    ```bash
    streamlit run app.py
    ```
    This will open the application in your web browser.

## File Format

The application uses a simple CSV (Comma Separated Values) format with the following characteristics:

* The first line is a commented header row, starting with `#`, listing the field names: `#key,value,tags`.
* Each subsequent line represents a record with three fields: `key`, `value`, and `tags`.
* Fields containing commas or newlines are enclosed in double quotes (`"`).
* The `key` field is expected to be unique for each record.
* Malformed rows (those not starting with `#` and having fewer than 3 columns) will be skipped with a warning.
