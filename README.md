# STREAMLIT CSV EDITOR

The Streamlit CSV Editor is a web-based application built with Python and Streamlit for managing CSV files containing structured data, such as historical events. It provides a user-friendly interface for Create, Read, Update, Delete (CRUD) operations, case-insensitive search, navigation, and clipboard support. The application handles a CSV file (default: `timeline.csv`) with a commented header (`# key,value,tags`) and fully quoted fields, displaying fields without outer quotes in the UI for a cleaner appearance. It ensures data integrity with unique keys, immediate file updates, and robust error handling.

## TABLE OF CONTENTS
* [Features](#features)
* [Installation](#installation)
* [Operation](#operation)
  * [Launching the Application](#launching-the-application)
  * [User Interface](#user-interface)
  * [Modes and Actions](#modes-and-actions)
  * [Navigation](#navigation)
  * [Search](#search)
  * [Clipboard Support](#clipboard-support)
* [Programmer's Reference](#programmers-reference)
  * [Code Structure](#code-structure)
  * [Key Functions](#key-functions)
  * [Session State](#session-state)
  * [Error Handling](#error-handling)
  * [Dependencies](#dependencies)
* [Contributing](#contributing)
* [License](#license)

## FEATURES
* **CRUD Operations:** Create, read, update, and delete records in a CSV file.
* **Search:** Case-insensitive search across key, value, and tags fields.
* **Navigation:** Move through records using Up, Down, Home, and End buttons.
* **Clipboard Support:** Copy the current record to the clipboard with quoted fields.
* **Quoted Data Handling:** Supports fully quoted fields in the CSV, displaying them without quotes in the UI (e.g., `1775-04-19` instead of `"1775-04-19"`).
* **Commented Header:** Skips `# key,value,tags` header when loading and includes it when saving.
* **Form Behavior:** Creation and update forms disappear immediately after adding or canceling.
* **Immediate File Updates:** Changes are saved to the CSV instantly upon create, update, or delete actions.
* **Responsive UI:** Streamlit-based interface with Status Bar, Menu, Current Record, Search, and List sections.
* **Error Handling:** Displays errors for file access, malformed data, or invalid inputs (e.g., duplicate or empty keys).
* **Reload Option:** Reverts to the last saved state by reloading the CSV.

## INSTALLATION

### Prerequisites
* **Python:** Version 3.8 or later (tested with 3.12.3).
* **Operating System:** Compatible with Windows, macOS, and Linux (tested on Linux Mint, kernel 6.8.0-57-generic).
* **Dependencies:** `streamlit` (version 1.38.0 or later recommended).

### Steps
1.  **Save the Code:**
    * Save the Python code as `app.py` in your project directory.
    * Optionally, rename it (e.g., `csv_editor.py`), updating references as needed.
2.  **Clone the Repository (if using a repository):**
    ```bash
    git clone [https://github.com/your-username/streamlit-csv-editor.git](https://github.com/your-username/streamlit-csv-editor.git)
    ```
    ```bash
    cd streamlit-csv-editor
    ```
3.  **Set Up a Virtual Environment (recommended):**
    ```bash
    python -m venv venv
    ```
    ```bash
    source venv/bin/activate # On Windows: venv\Scripts\activate
    ```
4.  **Install Dependencies:**
    ```bash
    pip install streamlit
    ```
5.  **Prepare the CSV File:**
    * Place a CSV file (e.g., `timeline.csv`) in the project directory with a commented header (`# key,value,tags`) and quoted fields (`key`, `value`, `tags`).
    * If no file exists, the application creates one with the header.
6.  **Verify Installation:**
    * Confirm Python version:
        ```bash
        python --version
        ```
    * Check Streamlit:
        ```bash
        pip show streamlit
        ```

## OPERATION

### Launching the Application
* Run the application using the command:
    ```bash
    streamlit run app.py
    ```
* This starts a local web server, typically at `http://localhost:8501`.
* Open the URL in a web browser to access the interface.

### User Interface
The UI is divided into five sections:
1.  **Status Bar:**
    * Displays:
        * **Mode:** Current mode (read/search, create, update, delete).
        * **Filename:** The CSV file being edited (default: `timeline.csv`).
        * **Lines:** Total number of records.
        * **Matches:** Number of records matching the search query.
        * **Current Line:** Index of the displayed record (1-based; 0 if none).
2.  **Menu:**
    * Buttons for actions: Create (c), Update (u), Delete (d), Save (s), Quit (q), Search (s).
3.  **Current Record:**
    * Shows the selected record’s key, value, and tags without quotes or a form/prompt for create/update/delete.
4.  **Search:**
    * A text input for filtering records.
5.  **List:**
    * A table of records matching the search, displayed without quotes.

### Modes and Actions
* **Read/Search (Default):**
    * View records, search, navigate, or copy to clipboard.
    * Search matches any part of key, value, or tags case-insensitively.
* **Create:**
    * Shows a form to enter key, value, and tags.
    * Validates: key must be non-empty and unique.
    * On Add Record: Saves to the CSV with quoted fields, hides the form, and switches to read/search.
    * On Cancel: Hides the form without saving, reverting to read/search.
* **Update:**
    * Shows a form pre-filled with the current record’s data.
    * Validates: key must be non-empty and unique (if changed).
    * On Update Record: Saves changes with quoted fields, hides the form, and switches to read/search.
    * On Cancel: Hides the form without saving, reverting to read/search.
* **Delete:**
    * Shows a confirmation prompt.
    * On Confirm Delete: Removes the record, updates the CSV, hides the prompt, and switches to read/search.
    * On Cancel: Hides the prompt without changes.
* **Save:** Saves the current data to the CSV with quoted fields.
* **Quit:** Stops the application.
* **Reload:** Reloads the CSV to revert to the last saved state.

### Navigation
* **Up/Down:** Move through the record list, updating the Current Record.
* **Home/End:** Jump to the first or last record.
* Buttons are disabled at list boundaries.
* **Note:** Streamlit’s web nature prevents keyboard navigation; buttons simulate arrow keys.

### Search
* Enter a term in the Search input (e.g., `Revolution`).
* Empty search shows all records.
* Matches appear in the List, with the first match in the Current Record.

### Clipboard Support
* In read/search, click `Copy to Clipboard` to copy the current record.
* Copied text includes quotes (e.g., `Key: "1775-04-19"\nValue: "..."\nTags: "#RevolutionaryWar, #Revolution, #Independence"`).

## PROGRAMMER'S REFERENCE

### Code Structure
The application is in a single file, `app.py`, with:
* **Imports:** Standard libraries (`csv`, `os`), Streamlit, typing utilities.
* **Constants:**
    * `DEFAULT_FILENAME`: `timeline.csv`.
    * `FIELDS`: `["key", "value", "tags"]`.
* **Functions:** Manage CSV operations, search, and clipboard.
* **Main Function:** Handles UI and interactions.
* **Entry Point:** Runs `main()` with error handling.

### Key Functions
* `load_csv(filename: str) -> List[Dict[str, str]]`:
    * Loads the CSV, skipping `# key,value,tags` lines.
    * Strips quotes for internal storage.
    * Creates a new file with `# key,value,tags` if none exists.
    * Skips malformed rows (fewer than three columns) with a UI warning.
* `save_csv(filename: str, data: List[Dict[str, str]])`:
    * Saves data, quoting all fields (`csv.QUOTE_ALL`).
    * Includes the commented header.
* `search_data(data: List[Dict[str, str]], search_str: str) -> List[Dict[str, str]]`:
    * Filters records case-insensitively.
* `copy_to_clipboard(text: str)`:
    * Uses JavaScript to copy text.
* `main()`:
    * Initializes session state, renders UI, handles actions.

### Session State
Streamlit’s `st.session_state` manages:
* `data`: List of record dictionaries.
* `mode`: Current mode (read/search, create, update, delete).
* `search_str`: Search term.
* `current_line`: Selected record index (0-based; -1 if none).
* `filtered_data`: Records matching the search.
* `last_filename`: Tracks filename changes.

### Error Handling
* **File Operations:** `Try-except` blocks catch file errors, shown via `st.error`.
* **Data Validation:** Rejects duplicate or empty keys with `st.error`.
* **Malformed Rows:** Skipped with `st.warning`.
* **Main Function:** Catches unexpected errors for UI display.

### Dependencies
* **Standard Libraries:**
    * `csv`: CSV handling.
    * `os`: File operations.
* **External:**
    * `streamlit`: UI and session state.
        * Install: `pip install streamlit` (1.38.0+).

## CONTRIBUTING
Contributions are welcome! To contribute:
1.  Fork the repository.
2.  Create a feature branch:
    ```bash
    git checkout -b feature/your-feature
    ```
3.  Commit changes:
    ```bash
    git commit -m "Add your feature"
    ```
4.  Push to the branch:
    ```bash
    git push origin feature/your-feature
    ```
5.  Open a pull request.
Include tests and update README.

## License
[Consider adding a license section here, e.g., MIT, Apache 2.0, etc.]
