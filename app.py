#!/usr/bin/env python3
"""
Knowledge App: A Streamlit application for managing key-value records with tags.

Features:
- Loads and saves data to/from a CSV file
- Provides a data editor interface for managing records
- Validates for duplicate keys
- Displays status information including filename and record count
"""

import csv
import pandas as pd
import streamlit as st

DEFAULT_FILENAME: str = "timeline.csv"
FIELDS: list[str] = ["key", "value", "tags"]

def load_csv(filename: str) -> list[dict[str, str]]:
    '''
    Load CSV file from disk into a list of dictionaries.
    
    Args:
        filename: Path to the CSV file to load
        
    Returns:
        List of dictionaries where each dictionary represents a record with keys:
        "key", "value", and "tags"
        
    Notes:
        - Skips rows starting with '#' (comments)
        - Skips malformed rows that don't have exactly 3 columns
        - Creates a new file with header if the file doesn't exist
    '''
    data: list[dict[str, str]] = []
    try:
        with open(filename, mode="r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f, quoting=csv.QUOTE_ALL)
            for row in reader:
                if row and row[0].startswith("#"):
                    continue
                if len(row) == 3:
                    data.append({"key": row[0], "value": row[1], "tags": row[2]})
                else:
                    st.warning(f"Skipping malformed row: {row}")
    except FileNotFoundError:
        with open(filename, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(["# key,value,tags"])
    return data

def save_csv(filename: str, data: list[dict[str, str]]) -> None:
    '''
    Save data to a CSV file on disk.
    
    Args:
        filename: Path to the CSV file to save to
        data: List of dictionaries where each dictionary represents a record
        
    Notes:
        - Writes a comment header line starting with '#'
        - Quotes all fields and escapes special characters
    '''
    with open(filename, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(["# key,value,tags"])
        for record in data:
            writer.writerow([record["key"], record["value"], record["tags"]])

def main() -> None:
    '''
    Main application function that manages the Streamlit interface.
    
    Features:
    - Initializes session state for data, filename, and status message
    - Displays a status bar with filename, record count, and status messages
    - Provides a save button that persists changes to disk
    - Shows an editable table of key-value-tag records
    - Validates for duplicate keys when editing data
    
    The interface includes:
    - A status bar showing current file and record count
    - A save button (💾) to persist changes
    - An editable data table with columns: Key, Value, Tags
    '''
    if "data" not in st.session_state:
        st.session_state.data = load_csv(DEFAULT_FILENAME)
    if "last_filename" not in st.session_state:
        st.session_state.last_filename = DEFAULT_FILENAME
    if "status_message" not in st.session_state:
        st.session_state.status_message = ""

    # Status Bar with save button
    status_text = f"{st.session_state.last_filename} | {len(st.session_state.data)}"
    if st.session_state.status_message:
        status_text += f" | {st.session_state.status_message}"

    col1, col2 = st.columns([8, 1])
    with col1:
        st.markdown(f"""
            <div style="font-family: monospace; margin: 0; padding: 0.5rem 1rem; background: #f0f2f6;">
                {status_text}
            </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("💾", help="Save"):
            save_csv(st.session_state.last_filename, st.session_state.data)
            st.session_state.status_message = "Saved"
            st.rerun()

    st.markdown("""
        <style>
        [data-testid="stTable"] th:nth-child(1),
        [data-testid="stTable"] td:nth-child(1) {
            text-align: right !important;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.session_state.data:
        df = pd.DataFrame(st.session_state.data)
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            key="data_editor",
            use_container_width=True,
            column_config={
                "key": st.column_config.TextColumn("Key", required=True),
                "value": st.column_config.TextColumn("Value"),
                "tags": st.column_config.TextColumn("Tags")
            }
        )
        new_data = edited_df.to_dict("records")
        keys = [record["key"] for record in new_data]
        if len(keys) != len(set(keys)):
            st.session_state.status_message = "Error: Duplicate keys"
            st.rerun()
        else:
            st.session_state.data = new_data
    else:
        st.write("No records")

if __name__ == "__main__":
    main()
