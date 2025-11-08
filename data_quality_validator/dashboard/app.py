import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -------------------------------
# CONFIG
# -------------------------------
OUTPUT_DIR = Path("data/output/")
st.set_page_config(page_title="Data Quality Dashboard", page_icon="🧠", layout="wide")

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_master_summary():
    path = OUTPUT_DIR / "master_summary.csv"
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame(columns=["file", "issues", "invalid_rows", "score"])

@st.cache_data
def load_invalid_data(file_name):
    path = OUTPUT_DIR / f"{file_name}_invalid.csv"
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame(columns=["row_no", "column", "error", "value"])

@st.cache_data
def load_summary(file_name):
    path = OUTPUT_DIR / f"{file_name}_summary.csv"
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame(columns=["issues"])

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("Configuration")
st.sidebar.markdown("Select a file to view detailed results:")

master_df = load_master_summary()

if master_df.empty:
    st.warning("No validation results found. Run the validator first.")
    st.stop()

file_names = [Path(f).stem for f in master_df["file"]]
selected_file = st.sidebar.selectbox("Choose File", file_names)

# -------------------------------
# DASHBOARD LAYOUT
# -------------------------------
st.title("Data Quality Validation Dashboard")

# Overall summary metrics
col1, col2, col3 = st.columns(3)
overall_score = round(master_df["score"].mean(), 2)
total_files = len(master_df)
total_invalid_rows = master_df["invalid_rows"].sum()

col1.metric("Total Files Validated", total_files)
col2.metric("Total Invalid Rows", total_invalid_rows)
col3.metric("Overall Data Quality Score", overall_score)

# -------------------------------
# SCORE DISTRIBUTION
# -------------------------------
st.subheader("File-wise Data Quality Scores")
fig = px.bar(master_df, x="file", y="score", color="score", text="score",
             color_continuous_scale="Tealgrn", title="File-wise Data Quality Score")
st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# SELECTED FILE DETAILS
# -------------------------------
st.markdown("---")
st.header(f"Detailed Report — {selected_file}")

summary_df = load_summary(selected_file)
invalid_df = load_invalid_data(selected_file)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Column-Level Summary")
    if summary_df.empty:
        st.info("No issues found for this file.")
    else:
        st.dataframe(summary_df, use_container_width=True)

with col2:
    st.subheader("Invalid Records (Row-Level)")
    if invalid_df.empty:
        st.info("All records valid.")
    else:
        st.dataframe(invalid_df, use_container_width=True, height=400)

# -------------------------------
# INVALID RECORDS VISUALIZATION
# -------------------------------
if not invalid_df.empty:
    st.subheader("Most Frequent Error Columns")
    top_columns = invalid_df["column"].value_counts().reset_index()
    top_columns.columns = ["Column", "Error Count"]
    fig2 = px.bar(top_columns, x="Column", y="Error Count", color="Error Count",
                  title="Columns with Most Errors", color_continuous_scale="Reds")
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.caption("© 2025 Aditya Kumar | Data Quality Validator | Streamlit Dashboard")
