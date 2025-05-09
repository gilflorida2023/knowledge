# Knowldege App

This is a Streamlit application for managing key-value records with tags. It provides a web interface to load, edit, and save records in a CSV file.

## How to Run

Follow these steps to set up and run the application:

1.  Create a Python virtual environment:
    ```bash
    python3 -m venv venv
    ```
2.  Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```
3.  Install the required dependencies (assuming you have a `requirements.txt` file):
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```

## Application Description

The Knowledge App allows users to manage data stored in a CSV file named `timeline.csv`. The application provides an interactive interface using Streamlit where users can view, edit, add, and delete records. The data is displayed in a table format, enabling inline editing. The application handles loading data from the CSV, skipping commented lines, and saving the modified data back to the file. It also includes basic validation to ensure that keys are unique.

## CSV File Organization

The application uses a CSV file (`timeline.csv`) to store the records. The file is organized with the following columns:

* **key**: A unique identifier for the record.
* **value**: The main content or value associated with the key.
* **tags**: Tags or labels associated with the record.

The first line of the CSV file is expected to be a commented header: `# key,value,tags`. Subsequent lines contain the data records, with each line representing a single record with values for 'key', 'value', and 'tags', separated by commas.
