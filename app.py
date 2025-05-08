#!/usr/bin/env python3
"""
Timeline App: A Streamlit application for managing key-value records with tags.
"""
import csv
import pandas as pd
import streamlit as st


DEFAULT_FILENAME: str = "timeline.csv"
FIELDS: list[str] = ["key", "value", "tags"]


def load_csv(filename: str) -> list[dict[str, str]]:
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
    with open(filename, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(["# key,value,tags"])
        for record in data:
            writer.writerow([record["key"], record["value"], record["tags"]])


def main() -> None:
    if "data" not in st.session_state:
        st.session_state.data = load_csv(DEFAULT_FILENAME)
    if "last_filename" not in st.session_state:
        st.session_state.last_filename = DEFAULT_FILENAME
    if "status_message" not in st.session_state:
        st.session_state.status_message = ""

    try:
        # Status Bar - completely flat inline version
        status_line = st.empty()
        status_text = f"Filename: {st.session_state.last_filename} | Lines: {len(st.session_state.data)}"
        if st.session_state.status_message:
            status_text += f" | {st.session_state.status_message}"
            st.session_state.status_message = ""
        status_line.markdown(f"""
            <div style="font-family: monospace; margin: 0; padding: 0;">
                {status_text}
            </div>
        """, unsafe_allow_html=True)

        # Menu
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Save"):
                save_csv(st.session_state.last_filename, st.session_state.data)
                st.session_state.status_message = "Saved"
                st.rerun()
        with col2:
            if st.button("Quit"):
                st.stop()
        with col3:
            if st.button("Reload"):
                st.session_state.data = load_csv(st.session_state.last_filename)
                st.session_state.status_message = "Reloaded"
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

    except Exception as e:
        st.session_state.status_message = f"Error: {str(e)}"
        st.rerun()


if __name__ == "__main__":
    main()
