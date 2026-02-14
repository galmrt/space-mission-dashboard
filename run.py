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
    st.session_state.date_range = (default_start_date, default_end_date)
    st.session_state.reset_counter += 1

# Initialize session state
if 'date_range' not in st.session_state:
    st.session_state.date_range = (default_start_date, default_end_date)
if 'reset_counter' not in st.session_state:
    st.session_state.reset_counter = 0
       
with st.sidebar:
    # add header  
    st.header("Filters", divider=True, )
    # dropdown to select attributes
    selected_column = st.selectbox("Attribute: ", df.columns, index=0)
    # multiselect to select values
    selected_values = st.multiselect("Filter by: ", df[selected_column].unique(), placeholder="Filter by values")
    


# The widget itself – controlled by session state with dynamic key
    selected_range = st.date_input(
        "Select date range",
        value=[],
        min_value=default_start_date,
        max_value=default_end_date,
        key=f'date_range_widget_{st.session_state.reset_counter}'
    )
    
    # Sync back to session state
    if isinstance(selected_range, tuple) and len(selected_range) == 2:
        st.session_state.date_range = selected_range
        
    # Reset button
    st.button("Reset Date Range", on_click=reset_date_range)


# Filter rows based on selected values from the selected column
if selected_values:
    filtered_df = df[df[selected_column].isin(selected_values)]
else:
    filtered_df = df

# Date filter (using the controlled session state value)
start_date, end_date = st.session_state.date_range
filtered_df = filtered_df[(filtered_df["Date"] >= start_date) &
    (filtered_df["Date"] <= end_date)]

# Output dataframe which user can filter
st.header("Original Data")
st.dataframe(filtered_df, use_container_width=True)


    
# Basic Information 
with st.expander("Basic Information"):
    desc = df.describe(include='all')
    st.dataframe(desc.reindex(['unique', 'top', 'freq', 'min', 'max']), use_container_width=True)

