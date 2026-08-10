import streamlit as st
import pandas as pd

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Dataset Upload",
    page_icon="📂",
    layout="wide"
)

# ==========================================
# HEADER
# ==========================================

st.title("Dataset Upload & Dynamic Preview")

st.caption(
    "Upload a CSV or JSON dataset and explore it instantly."
)

st.divider()

# ==========================================
# FILE UPLOAD
# ==========================================

uploaded_file = st.file_uploader(
    "Upload your dataset",
    type=["csv", "json"],
    help="Supported formats: CSV and JSON"
)

# ==========================================
# NO FILE UPLOADED
# ==========================================

if uploaded_file is None:

    st.info(
        "Upload a CSV or JSON file to begin."
    )

    st.stop()

# ==========================================
# READ UPLOADED FILE
# ==========================================

try:

    if uploaded_file.name.lower().endswith(".csv"):

        df = pd.read_csv(uploaded_file)

    elif uploaded_file.name.lower().endswith(".json"):

        df = pd.read_json(uploaded_file)

    else:

        st.error(
            "Unsupported file type. "
            "Please upload a CSV or JSON file."
        )

        st.stop()

except Exception:

    st.error(
        "Could not read this file. "
        "Check the format and try again."
    )

    st.stop()

# ==========================================
# EMPTY DATASET
# ==========================================

if df.empty:

    st.warning(
        "Uploaded file is empty."
    )

    st.stop()

# ==========================================
# SUCCESS MESSAGE
# ==========================================

st.success(
    f"Loaded: {uploaded_file.name} "
    f"({len(df):,} rows, {len(df.columns):,} columns)"
)   