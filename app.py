import streamlit as st
import csv
import os
from typing import List, Dict
from streamlit.components.v1 import html

# Default filename
DEFAULT_FILENAME = "timeline.csv"

# Schema
FIELDS = ["key", "value", "tags"]

# Load CSV file
def load_csv(filename: str) -> List[Dict[str, str]]:
    try:
        # If file doesn’t exist, create it with commented header
        if not os.path.exists(filename):
            with open(filename, 'w', newline='') as f:
                f.write('# ' + ','.join(FIELDS) + '\n')
            return []

        # Read file, skipping commented lines
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = []
            for row in reader:
                if row and not row[0].startswith('#'):  # Skip comments
                    if len(row) >= 3:  # Ensure row has enough columns
                        # Strip quotes from fields for internal storage
                        data.append({FIELDS[i]: row[i].strip('"') for i in range(3)})
                    else:
                        st.warning(f"Skipping malformed row: {row}")
            return data
    except Exception as e:
        st.error(f"Error loading CSV: {str(e)}")
        return []

# Save CSV file
def save_csv(filename: str, data: List[Dict[str, str]]):
    try:
        with open(filename, 'w', newline='') as csvfile:
            # Write commented header
            csvfile.write('# ' + ','.join(FIELDS) + '\n')
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            for record in data:
                writer.writerow([record[field] for field in FIELDS])
    except Exception as e:
        st.error(f"Error saving CSV: {str(e)}")

# Search records
def search_data(data: List[Dict[str, str]], search_str: str) -> List[Dict[str, str]]:
    if not search_str:
        return data
    search_str = search_str.lower()
    return [record for record in data if any(search_str in field.lower() for field in record.values())]

# Copy text to clipboard
def copy_to_clipboard(text):
    html(f"""
    <script>
    navigator.clipboard.writeText('{text.replace("'", "\\'").replace('\n', '\\n')}');
    </script>
    """)

# Main application
def main():
    st.title("CSV Editor")

    # Initialize session state
    if 'data' not in st.session_state:
        st.session_state.data = load_csv(DEFAULT_FILENAME)
    if 'mode' not in st.session_state:
        st.session_state.mode = 'read/search'
    if 'search_str' not in st.session_state:
        st.session_state.search_str = ""
    if 'current_line' not in st.session_state:
        st.session_state.current_line = 0 if st.session_state.data else -1
    if 'filtered_data' not in st.session_state:
        st.session_state.filtered_data = st.session_state.data

    # **SECTION: Filename Input**
    filename = st.text_input("Filename", value=DEFAULT_FILENAME)

    # Reload data if filename changes
    if st.session_state.get('last_filename') != filename:
        st.session_state.data = load_csv(filename)
        st.session_state.filtered_data = st.session_state.data
        st.session_state.current_line = 0 if st.session_state.filtered_data else -1
        st.session_state.last_filename = filename

    data = st.session_state.data
    mode = st.session_state.mode

    # **SECTION: SEARCH**
    search_str = st.text_input("Search", value=st.session_state.search_str)
    if search_str != st.session_state.search_str:
        st.session_state.search_str = search_str
        st.session_state.filtered_data = search_data(data, search_str)
        st.session_state.current_line = 0 if st.session_state.filtered_data else -1

    filtered_data = st.session_state.filtered_data
    current_line = st.session_state.current_line
    line_count = len(data)
    matches = len(filtered_data)

    # **SECTION: STATUS_BAR**
    st.write(f"Mode: {mode} | Filename: {filename} | Lines: {line_count} | Matches: {matches} | Current Line: {current_line + 1 if current_line >= 0 else 0}")

    # **SECTION: MENU**
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        if st.button("Create (c)"):
            st.session_state.mode = 'create'
    with col2:
        if st.button("Update (u)", disabled=current_line < 0):
            st.session_state.mode = 'update'
    with col3:
        if st.button("Delete (d)", disabled=current_line < 0):
            st.session_state.mode = 'delete'
    with col4:
        if st.button("Save (s)"):
            save_csv(filename, data)
            st.success("Saved!")
            st.session_state.mode = 'read/search'
    with col5:
        if st.button("Quit (q)"):
            st.stop()
    with col6:
        if st.button("Search (s)"):
            st.session_state.mode = 'read/search'

    # **SECTION: CURRENT_RECORD**
    if mode == 'create':
        with st.form(key='create_form'):
            new_key = st.text_input("Key")
            new_value = st.text_area("Value")
            new_tags = st.text_input("Tags")
            col_submit, col_cancel = st.columns(2)
            with col_submit:
                submit = st.form_submit_button("Add Record")
            with col_cancel:
                cancel = st.form_submit_button("Cancel")

            if submit:
                if not new_key:
                    st.error("Key cannot be empty.")
                elif any(record['key'] == new_key for record in data):
                    st.error("Key must be unique.")
                else:
                    data.append({"key": new_key, "value": new_value, "tags": new_tags})
                    save_csv(filename, data)
                    st.session_state.data = data
                    st.session_state.filtered_data = search_data(data, search_str)
                    st.session_state.current_line = 0 if st.session_state.filtered_data else -1
                    st.session_state.mode = 'read/search'
                    st.success("Record added.")
                    st.rerun()  # Force rerun to hide form immediately
            if cancel:
                st.session_state.mode = 'read/search'
                st.rerun()  # Force rerun to hide form immediately

    elif mode == 'update' and current_line >= 0:
        with st.form(key='update_form'):
            updated_key = st.text_input("Key", value=filtered_data[current_line]['key'])
            updated_value = st.text_area("Value", value=filtered_data[current_line]['value'])
            updated_tags = st.text_input("Tags", value=filtered_data[current_line]['tags'])
            col_submit, col_cancel = st.columns(2)
            with col_submit:
                submit = st.form_submit_button("Update Record")
            with col_cancel:
                cancel = st.form_submit_button("Cancel")
            if submit:
                if not updated_key:
                    st.error("Key cannot be empty.")
                else:
                    original_key = filtered_data[current_line]['key']
                    if updated_key != original_key and any(record['key'] == updated_key for record in data):
                        st.error("Key must be unique.")
                    else:
                        index = next(i for i, record in enumerate(data) if record['key'] == original_key)
                        data[index] = {"key": updated_key, "value": updated_value, "tags": updated_tags}
                        save_csv(filename, data)
                        st.session_state.data = data
                        st.session_state.filtered_data = search_data(data, search_str)
                        st.session_state.mode = 'read/search'
                        st.success("Record updated.")
                        st.rerun()  # Force rerun to hide form
            if cancel:
                st.session_state.mode = 'read/search'
                st.rerun()  # Force rerun to hide form

    elif mode == 'delete' and current_line >= 0:
        st.write(f"Delete Key: {filtered_data[current_line]['key']}?")
        col_confirm, col_cancel = st.columns(2)
        with col_confirm:
            if st.button("Confirm Delete"):
                original_key = filtered_data[current_line]['key']
                data[:] = [record for record in data if record['key'] != original_key]
                save_csv(filename, data)
                st.session_state.data = data
                st.session_state.filtered_data = search_data(data, search_str)
                st.session_state.current_line = min(current_line, len(filtered_data) - 1) if filtered_data else -1
                st.session_state.mode = 'read/search'
                st.success("Record deleted.")
                st.rerun()  # Force rerun to update UI
        with col_cancel:
            if st.button("Cancel"):
                st.session_state.mode = 'read/search'
                st.rerun()  # Force rerun to update UI

    else:  # read/search mode
        if current_line >= 0:
            # Display fields without outer quotes
            st.write("Key:", filtered_data[current_line]["key"])
            st.write("Value:", filtered_data[current_line]["value"])
            st.write("Tags:", filtered_data[current_line]["tags"])
        else:
            st.write("No record selected.")

    # **SECTION: LIST**
    if filtered_data:
        # Display records without outer quotes in the table
        st.dataframe([record for record in filtered_data], use_container_width=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("Up", disabled=current_line <= 0):
                st.session_state.current_line -= 1
        with col2:
            if st.button("Down", disabled=current_line >= len(filtered_data) - 1):
                st.session_state.current_line += 1
        with col3:
            if st.button("Home", disabled=current_line <= 0):
                st.session_state.current_line = 0
        with col4:
            if st.button("End", disabled=current_line >= len(filtered_data) - 1):
                st.session_state.current_line = len(filtered_data) - 1

        # Copy to clipboard in read/search mode (include quotes in copied text)
        if mode == 'read/search' and current_line >= 0:
            if st.button("Copy to Clipboard"):
                record = filtered_data[current_line]
                text = f'Key: "{record["key"]}"\nValue: "{record["value"]}"\nTags: "{record["tags"]}"'
                copy_to_clipboard(text)
                st.success("Copied to clipboard.")
    else:
        st.write("No records found.")

    # Revert/Reload option
    if st.button("Reload"):
        st.session_state.data = load_csv(filename)
        st.session_state.filtered_data = search_data(st.session_state.data, st.session_state.search_str)
        st.session_state.current_line = 0 if st.session_state.filtered_data else -1
        st.session_state.mode = 'read/search'
        st.success("Data reloaded.")
        st.rerun()  # Force rerun to update UI

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
