import streamlit as st
import pandas as pd
from src import data_processing as dp
from src import visualizations as viz

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

df = dp.load_data()
default_start_date = df["Date"].min()
default_end_date = df["Date"].max()


def reset_date_range():
    st.session_state.date_range = (default_start_date, default_end_date)
    st.session_state.reset_counter += 1


if 'date_range' not in st.session_state:
    st.session_state.date_range = (default_start_date, default_end_date)
if 'reset_counter' not in st.session_state:
    st.session_state.reset_counter = 0

with st.sidebar:
    st.header("Filters", divider=True)
    selected_column = st.selectbox("Attribute: ", df.columns, index=0)
    selected_values = st.multiselect("Filter by: ", df[selected_column].unique(), placeholder="Filter by values")

    selected_range = st.date_input(
        "Select date range",
        value=[],
        min_value=default_start_date,
        max_value=default_end_date,
        help="Select a date range to filter the data",
        key=f'date_range_widget_{st.session_state.reset_counter}'
    )

    if isinstance(selected_range, tuple) and len(selected_range) == 2:
        st.session_state.date_range = selected_range

    st.button("Reset Date Range", on_click=reset_date_range)


if selected_values:
    filtered_df = df[df[selected_column].isin(selected_values)]
else:
    filtered_df = df

start_date, end_date = st.session_state.date_range
filtered_df = filtered_df[(filtered_df["Date"] >= start_date) & (filtered_df["Date"] <= end_date)]

st.header("Original Data")
st.dataframe(filtered_df, use_container_width=True)

fig = viz.create_missions_by_country_map(df)
st.plotly_chart(fig, use_container_width=True)

fig2 = viz.create_company_activity_heatmap(df)
st.plotly_chart(fig2, use_container_width=True)

fig3 = viz.create_histogram(df, 'MissionStatus')
st.plotly_chart(fig3, use_container_width=True)
