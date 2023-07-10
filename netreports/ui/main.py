"""Main entrypoint for the Streamlit UI."""
import streamlit as st
import pandas as pd
import json
import requests

st.title("NetReports")


@st.cache_data
def load_report():
    response = requests.get("http://localhost:8080/reports/ports/")
    return response.json()


data = load_report()
df = pd.DataFrame.from_records(data["results"])

st.dataframe(df, hide_index=True)
