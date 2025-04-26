import streamlit as st
import csv
import os
import pandas as pd

DEFAULT_FILENAME = "timeline.csv"
FIELDS = ["key", "value", "tags"]

def load_csv(filename):
    data = []
    try:
        with open(filename, "r", newline="") as f:
            reader = csv.reader(f, quoting=csv.QUOTE_ALL)
            for row in reader:
                if row and row[0].startswith("#"):
                    continue
                if len(row) == 3:
                    data.append({"key": row[0], "value": row[1], "tags": row[2]})
                else:
                    st.warning(f"Skipping malformed row: {row}")
    except FileNotFoundError:
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(["# key,value,tags"])
    return data

def save_csv(filename, data):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(["# key,value,tags"])
        for record in data:
            writer.writerow([record["key"], record["value"], record["tags"]])

def main():
    if "data" not in st.session_state:
        st.session_state.data = load_csv(DEFAULT_FILENAME)
    if "last_filename" not in st.session_state:
        st.session_state.last_filename = DEFAULT_FILENAME

    try:
        # Status Bar
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Filename: {st.session_state.last_filename}")
        with col2:
            st.write(f"Lines: {len(st.session_state.data)}")

        # Menu
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Save"):
                save_csv(st.session_state.last_filename, st.session_state.data)
                st.success("File saved!")
        with col2:
            if st.button("Quit"):
                st.stop()
        with col3:
            if st.button("Reload"):
                st.session_state.data = load_csv(st.session_state.last_filename)
                st.rerun()

        # Inject CSS for column alignment
        st.markdown("""
            <style>
            /* Right-align the 'key' column (first column) */
            [data-testid="stTable"] th:nth-child(1),
            [data-testid="stTable"] td:nth-child(1) {
                text-align: right !important;
            }
            /* Ensure 'value' and 'tags' columns (second and third) are left-aligned */
            [data-testid="stTable"] th:nth-child(2),
            [data-testid="stTable"] td:nth-child(2),
            [data-testid="stTable"] th:nth-child(3),
            [data-testid="stTable"] td:nth-child(3) {
                text-align: left !important;
            }
            </style>
        """, unsafe_allow_html=True)

        # List with Inline Editing
        if st.session_state.data:
            # Convert to DataFrame for st.data_editor
            df = pd.DataFrame(st.session_state.data)
            # Allow inline editing
            edited_df = st.data_editor(
                df,
                num_rows="dynamic",  # Allow adding/deleting rows
                key="data_editor",
                use_container_width=True,
                column_config={
                    "key": st.column_config.TextColumn("Key", required=True),
                    "value": st.column_config.TextColumn("Value"),
                    "tags": st.column_config.TextColumn("Tags")
                }
            )
            # Update data with edited values
            new_data = edited_df.to_dict("records")
            # Validate unique keys
            keys = [record["key"] for record in new_data]
            if len(keys) != len(set(keys)):
                st.error("All keys must be unique")
            else:
                st.session_state.data = new_data
        else:
            st.write("No records")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
