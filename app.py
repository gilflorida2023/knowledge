#!/usr/bin/env python3
"""
Knowledge App: A Streamlit application for managing key-value records with tags.

Features:
- Loads and saves data to/from a CSV file
- Provides a data editor interface for managing records
- Validates for duplicate keys
- Displays status information including filename and record count
- Includes a sidebar menu with save options
"""

import csv
import pandas as pd
import streamlit as st

DEFAULT_FILENAME: str = "timeline.csv"
FIELDS: list[str] = ["key", "value", "tags"]

def load_csv(filename: str) -> list[dict[str, str]]:
    '''
    Load CSV file from disk into a list of dictionaries.
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
    '''
    with open(filename, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(["# key,value,tags"])
        for record in data:
            writer.writerow([record["key"], record["value"], record["tags"]])
    st.session_state.status_message = f"Saved to {filename}"
    st.session_state.last_filename = filename

def main() -> None:
    '''
    Main application function that manages the Streamlit interface.
    '''
    if "data" not in st.session_state:
        st.session_state.data = load_csv(DEFAULT_FILENAME)
    if "last_filename" not in st.session_state:
        st.session_state.last_filename = DEFAULT_FILENAME
    if "status_message" not in st.session_state:
        st.session_state.status_message = ""

    # Sidebar Menu
    with st.sidebar:
        st.title("Menu")
        st.subheader("File Operations")
        
        # Save options
        if st.button("💾 Save to Current File", help="Save to current file"):
            save_csv(st.session_state.last_filename, st.session_state.data)
            st.rerun()
        
        if st.button("💾 Save As...", help="Save to a new file"):
            new_filename = st.text_input("New filename:", value=st.session_state.last_filename)
            if new_filename and st.button("Confirm Save"):
                if not new_filename.endswith('.csv'):
                    new_filename += '.csv'
                save_csv(new_filename, st.session_state.data)
                st.rerun()
        
        st.divider()
        st.subheader("Current File")
        st.write(f"Filename: {st.session_state.last_filename}")
        st.write(f"Records: {len(st.session_state.data)}")
        
        if st.session_state.status_message:
            st.info(st.session_state.status_message)

    # Main content area
    st.title("Knowledge App")
    
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
