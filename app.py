#!/usr/bin/env python3
"""
Knowledge App: A Streamlit application for managing key-value records with tags.
"""

import csv
from collections import defaultdict
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
    if "duplicates_reported" not in st.session_state:
        st.session_state.duplicates_reported = False
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(st.session_state.data)

    # Handle forced reload
    if st.session_state.force_reload:
        st.session_state.data = load_csv(st.session_state.last_filename)
        st.session_state.df = pd.DataFrame(st.session_state.data)
        st.session_state.status_message = f"Reloaded from {st.session_state.last_filename}"
        st.session_state.force_reload = False
        st.rerun()

    # Main content area
    st.title("Knowledge App")
    
    if not st.session_state.data:
        st.write("No records found")
    else:
        # Display data editor
        edited_df = st.data_editor(
            st.session_state.df,
            num_rows="dynamic",
            key="data_editor",
            use_container_width=True,
            column_config={
                "key": st.column_config.TextColumn("Key", required=True),
                "value": st.column_config.TextColumn("Value"),
                "tags": st.column_config.TextColumn("Tags")
            }
        )
        
        # Check for duplicate keys
        new_data = edited_df.to_dict("records")
        keys = [record["key"] for record in new_data]

        if len(keys) != len(set(keys)):
            key_indices = defaultdict(list)
            for idx, key in enumerate(keys):
                key_indices[key].append(idx + 1)  # 1-based record numbers
            duplicates = {k: v for k, v in key_indices.items() if len(v) > 1}
            # Print to console and show sidebar error exactly once
            if not st.session_state.duplicates_reported:
                print("\n=== DUPLICATE KEYS DETECTED ===")
                for key, records in sorted(duplicates.items()):
                    print(f"Key: '{key}' appears in records: {', '.join(map(str, records))}")
                print("===============================\n")
                st.session_state.duplicates_reported = True
                st.session_state.show_duplicate_error = True
                st.rerun()  # Force update to show sidebar error
        else:
            st.session_state.data = new_data
            st.session_state.df = pd.DataFrame(new_data)
            st.session_state.duplicates_reported = False

    # Sidebar Menu
    with st.sidebar:
        #st.divider()
        st.subheader("Current File")
        st.write(f"Filename: {st.session_state.last_filename}")
        st.write(f"Records: {len(st.session_state.data)}")
        if st.session_state.status_message:
            st.info(st.session_state.status_message)

if __name__ == "__main__":
    main()
