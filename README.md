# Streamlit CSV Editor

The Streamlit CSV Editor is a web-based application built with Python and Streamlit to manage CSV files containing historical events or similar data. It provides a user-friendly interface for **Create, Read, Update, Delete (CRUD)** operations, search functionality, and navigation, with a focus on handling quoted data fields. The application is designed to work with a specific CSV format, featuring a commented header and fully quoted fields, and is optimized for ease of use and data integrity.

## Table of Contents
- [Features](#features)
- [CSV File Format](#csv-file-format)
- [Installation](#installation)
- [Operation](#operation)
  - [Launching the Application](#launching-the-application)
  - [User Interface](#user-interface)
  - [Modes and Actions](#modes-and-actions)
  - [Navigation](#navigation)
  - [Search](#search)
  - [Clipboard Support](#clipboard-support)
- [Programmer's Reference](#programmers-reference)
  - [Code Structure](#code-structure)
  - [Key Functions](#key-functions)
  - [Session State](#session-state)
  - [Error Handling](#error-handling)
  - [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Features
- **CRUD Operations**: Create, read, update, and delete records in a CSV file.
- **Search**: Case-insensitive search across all fields (`key`, `value`, `tags`).
- **Navigation**: Move through records using Up, Down, Home, and End buttons.
- **Clipboard Support**: Copy the current record to the clipboard with quoted fields.
- **Quoted Data Handling**: Supports fully quoted fields in the CSV file, displaying them without quotes in the UI.
- **Commented Header**: Skips `#`-prefixed header lines when loading and includes them when saving.
- **Responsive UI**: Streamlit-based interface with sections for status, menu, current record, search, and record list.
- **Immediate File Updates**: Changes are saved to the CSV file instantly upon completion of create, update, or delete actions.
- **Form Behavior**: Creation and update forms disappear immediately after adding or canceling.
- **Error Handling**: Displays errors in the UI for file access issues, malformed data, or invalid inputs.

## CSV File Format
The application is designed to work with a specific CSV file format, typically named `timeline.csv`. The file structure is as follows:

- **Commented Header**: The first line is a comment starting with `#`, typically `# key,value,tags`, which is ignored when loading and included when saving.
- **Fields**: Each data row contains three fields: `key`, `value`, and `tags`.
  - **`key`**: A unique, quoted string (e.g., a date like `"1775-04-19"` or a term like `"ablution"`).
  - **`value`**: A quoted string, potentially long, describing the event or definition (e.g., `"Revolutionary War begins..."`).
  - **`tags`**: A quoted, comma-separated list of tags with spaces after commas (e.g., `"#RevolutionaryWar, #Revolution, #Independence"`).
- **Quoting**: All fields are enclosed in double quotes (`"`) to ensure data integrity, especially for fields containing commas or special characters.
- **Example**:
  ```csv
  # key,value,tags
  "1775-04-19","Revolutionary War begins with the Battles of Lexington and Concord, sparking armed conflict between Britain and the American colonies.","#RevolutionaryWar, #Revolution, #Independence"
  "1773-12-16","Boston Tea Party: Colonists dump tea into Boston Harbor to protest British taxation without representation.","#BostonTeaParty, #Revolution, #Taxation"
  "1776-7-4","Declaration of Independence adopted, marking the founding of America as a sovereign nation.","#FoundingOfAmerica, #Independence, #Revolution"
  "1810-5-1","TONA passes Congress (Senate 19-5, House 87-3). Needs 13 of 17 states to ratify.","#TONA, #Legislation"
