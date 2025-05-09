#!/usr/bin/env python3
"""
Knowledge App: A Streamlit application for managing key-value records with tags.
"""

import csv
import re
import pandas as pd
import streamlit as st

DEFAULT_FILENAME: str = "melon.csv"
FIELDS: list[str] = ["key", "value", "tags"]

def load_csv(filename: str) -> list[dict[str, str]]:
    '''Load CSV file from disk into a list of dictionaries.'''
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
    '''Save data to a CSV file on disk.'''
    with open(filename, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(["# key,value,tags"])
        for record in data:
            writer.writerow([record["key"], record["value"], record["tags"]])
    st.session_state.status_message = f"Saved to {filename}"
    st.session_state.last_filename = filename

def main() -> None:
    '''Main application function.'''
    # Initialize session state
    if "data" not in st.session_state:
        st.session_state.data = load_csv(DEFAULT_FILENAME)
    if "last_filename" not in st.session_state:
        st.session_state.last_filename = DEFAULT_FILENAME
    if "status_message" not in st.session_state:
        st.session_state.status_message = ""
    if "force_reload" not in st.session_state:
        st.session_state.force_reload = False
    if "filtered_data" not in st.session_state:
        st.session_state.filtered_data = []

    # Handle forced reload
    if st.session_state.force_reload:
        st.session_state.data = load_csv(st.session_state.last_filename)
        st.session_state.status_message = f"Reloaded from {st.session_state.last_filename}"
        st.session_state.force_reload = False
        st.rerun()

    # Sidebar Menu
    with st.sidebar:
        st.title("Menu")
        st.subheader("File Operations")
        
        # Create a tight row for buttons
        button_row = st.columns([1, 1, 2])  # Adjust widths as needed
        
        with button_row[0]:
            if st.button("💾", help="Save to current file"):
                save_csv(st.session_state.last_filename, st.session_state.data)
                st.session_state.force_reload = True
        
        with button_row[1]:
            if st.button("🔄", help="Reload from disk"):
                st.session_state.force_reload = True
        
        with button_row[2]:
            if st.button("💾❓", help="Save As [new file name]"):
                new_filename = st.text_input("New filename:", value=st.session_state.last_filename)
                if new_filename and st.button("Confirm Save"):
                    if not new_filename.endswith('.csv'):
                        new_filename += '.csv'
                    save_csv(new_filename, st.session_state.data)
                    st.session_state.force_reload = True

        st.divider()
        st.subheader("Current File")
        st.write(f"Filename: {st.session_state.last_filename}")
        st.write(f"Records: {len(st.session_state.data)}")
        
        if st.session_state.status_message:
            st.info(st.session_state.status_message)

    # Main content area
    st.title("Knowledge App")
    
    # Search functionality
    with st.expander("🔍 Search Options", expanded=True):
        search_mode = st.radio(
            "Search Mode",
            ["Basic", "Regex"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        search_term = st.text_input("Search term", "")
        
        if search_term:
            if search_mode == "Basic":
                st.session_state.filtered_data = [
                    item for item in st.session_state.data
                    if search_term.lower() in item["key"].lower()
                    or search_term.lower() in item["value"].lower()
                ]
            elif search_mode == "Regex":
                try:
                    st.session_state.filtered_data = [
                        item for item in st.session_state.data
                        if re.search(search_term, item["key"], re.IGNORECASE)
                        or re.search(search_term, item["value"], re.IGNORECASE)
                    ]
                except re.error:
                    st.error("Invalid regular expression pattern")
                    st.session_state.filtered_data = st.session_state.data
        else:
            st.session_state.filtered_data = st.session_state.data
    
    if st.session_state.filtered_data:
        df = pd.DataFrame(st.session_state.filtered_data)
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
        st.write("No records matching search criteria")

if __name__ == "__main__":
    main()
