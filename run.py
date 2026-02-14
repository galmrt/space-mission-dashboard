import streamlit as st
import pandas as pd
import plotly as plt
import numpy as np
from src import data_processing as dp






st.set_page_config(
    page_title="Space Mission Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Space Mission Dataset Dashboard")
st.write("""
This dashboard provides an overview of space missions from 1957 to 2023. The data is sourced from a public dataset and includes information about the company, mission status, and launch date. The dashboard provides various visualizations to help you understand the data.
""")


# load the data
df = dp.load_data()

default_start_date = df["Date"].min()
default_end_date = df["Date"].max()

def reset_date_range():
    if 'date_range_widget' in st.session_state:
        del st.session_state['date_range_widget']
    st.session_state.date_range = (default_start_date, default_end_date)
    
    
with st.sidebar:
    # add header  
    st.header("Filters", divider=True, )
    # dropdown to select attributes
    selected_column = st.selectbox("Attribute: ", df.columns, index=0)
    # multiselect to select values
    selected_values = st.multiselect("Filter by: ", df[selected_column].unique(), placeholder="Filter by values")
    
    # Initialize date range in session state
    if 'date_range' not in st.session_state:
        st.session_state.date_range = (default_start_date, default_end_date)

    # date range - use default or session state value
    selected_range = st.date_input(
        "Select a date range",
        help="Choose your start and end dates",
        value=st.session_state.date_range,
        key='date_range_widget'
    )
    
    st.button("Reset Date Range", on_click=reset_date_range)

    # Update session state if both dates are selected
    if isinstance(selected_range, tuple) and len(selected_range) == 2:
        st.session_state.date_range = selected_range
    else:
        st.session_state.date_range = (default_start_date, default_end_date)


# Filter rows based on selected values from the selected column
if selected_values:
    filtered_df = df[df[selected_column].isin(selected_values)]
else:
    filtered_df = df

filtered_df = filtered_df[(filtered_df["Date"] >= st.session_state.date_range[0]) & (filtered_df["Date"] <= st.session_state.date_range[1])]

# Output dataframe which user can filter
st.header("Original Data")
st.dataframe(filtered_df, use_container_width=True)


    
# Basic Information 
with st.expander("Basic Information"):
    desc = df.describe(include='all')
    st.dataframe(desc.reindex(['unique', 'top', 'freq', 'min', 'max']), use_container_width=True)

