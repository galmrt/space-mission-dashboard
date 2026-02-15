import streamlit as st
import pandas as pd
from src import data_processing as dp
from src import visualizations as viz

st.set_page_config(
    page_title="Space Mission Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Space Mission Dataset Dashboard")
st.write("""
This dashboard provides an overview of space missions from 1957 to 2023. The data is sourced from a public dataset and includes information about the company, mission status, and launch date. The dashboard provides various visualizations to help you understand the data.
""")

df = dp.load_data()

#-----------------------------
# Data filtering
#-----------------------------
default_start_date = df["Date"].min()
default_end_date = df["Date"].max()


def reset_date_range():
    st.session_state.date_range = (default_start_date, default_end_date)
    st.session_state.reset_counter += 1


if 'date_range' not in st.session_state:
    st.session_state.date_range = (default_start_date, default_end_date)
if 'reset_counter' not in st.session_state:
    st.session_state.reset_counter = 0

data_col1, data_col2 = st.columns([1, 8])
with data_col1:
    st.markdown("#### Filters")
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

    st.button("Reset dates", on_click=reset_date_range)

if selected_values:
    filtered_df = df[df[selected_column].isin(selected_values)]
else:
    filtered_df = df
start_date, end_date = st.session_state.date_range
filtered_df = filtered_df[(filtered_df["Date"] >= start_date) & (filtered_df["Date"] <= end_date)]

with data_col2:
    st.dataframe(filtered_df, use_container_width=True)
st.divider()

#-----------------------------
# Summary statistics
#-----------------------------
cols = st.columns([1, 1, 1.4, 0.8, 0.8])
with cols[0]:
    st.metric("Total Missions", len(df))
with cols[1]:
    st.metric("First Mission", df["Date"].min().strftime("%d %B %Y"))
with cols[2]:
    st.metric("Most used Rocket", dp.getMostUsedRocket())
with cols[3]:
    st.metric("Company with most missions", dp.getTopCompaniesByMissionCount(1)[0][0])
with cols[4]:
    firstYear = df["Date"].apply(lambda x: x.year).min()
    lastYear = df["Date"].apply(lambda x: x.year).max()
    st.metric("Average missions per year", dp.getAverageMissionsPerYear(firstYear, lastYear))

cols = st.columns([1, 1, 3])
with cols[0]:
    st.metric("Number of Companies", len(df["Company"].unique()))
with cols[1]:
    st.metric("Last Mission", df["Date"].max().strftime("%d %B %Y"))
with cols[2]:
    most_used_location = df["Location"].value_counts().index[0]
    st.metric("Most used Launchpad", most_used_location)
st.divider()

#-----------------------------
# Map with missions by country
#-----------------------------
st.header("🌍 Global Launch Activity")
st.write("This map shows the distribution of space missions across different countries. Darker colors indicate more launches.")
fig = viz.create_missions_by_country_map(df)
st.plotly_chart(fig, use_container_width=True)
st.caption("**Key Insight:** Russia (USSR), USA, and Kazakhstan dominate global launch activity, reflecting the Cold War space race legacy and continued investment in space programs.")

st.divider()

#-----------------------------
# Company activity heatmap
#-----------------------------
st.header("📅 Company Activity Over Time")
st.write("This heatmap displays when each company was most active in launching missions. Each row represents a company, and the color intensity shows the number of launches per year.")
fig2 = viz.create_company_activity_heatmap(df)
st.plotly_chart(fig2, use_container_width=True)
st.caption("**Key Insight:** RVSN USSR was highly active during the 1970s-80s. SpaceX shows rapid growth from 2015 onwards, reflecting the rise of commercial spaceflight.")

st.divider()

#-----------------------------
# Histograms
#-----------------------------
st.header("📊 Data Exploration")
st.write("Create custom histograms to explore the distribution of different attributes in the dataset. Click 'Add histogram' to get started.")
st.caption("**Tip:** Try the 'Time' histogram to see that most launches occur during daytime hours (06:00-18:00 UTC).")

allowed_columns_hist = ["Company", "Date", "Time", "RocketStatus", "MissionStatus", 'Rocket']

if 'histograms' not in st.session_state:
    st.session_state.histograms = []
if 'hist_counter' not in st.session_state:
    st.session_state.hist_counter = 0

def add_histogram():
    st.session_state.hist_counter += 1
    st.session_state.histograms.append({"id": st.session_state.hist_counter})

def remove_histogram(hist_id):
    st.session_state.histograms = [h for h in st.session_state.histograms if h["id"] != hist_id]

for i, hist in enumerate(st.session_state.histograms):
    hist_id = hist["id"]
    already_selected = [
        st.session_state.get(f'hist_select_{h["id"]}')
        for h in st.session_state.histograms
        if h["id"] != hist_id and st.session_state.get(f'hist_select_{h["id"]}')
    ]
    available_columns = [col for col in allowed_columns_hist if col not in already_selected]

    col1, col2 = st.columns([2, 9])
    with col1:
        selected = st.selectbox(
            f"Select attribute for histogram {i+1}:",
            available_columns,
            index=0,
            key=f'hist_select_{hist_id}',
            width = 300
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Remove histogram", key=f'remove_hist_{hist_id}', on_click=remove_histogram, args=(hist_id,), type="tertiary")

    fig = viz.create_histogram(df, selected)
    st.plotly_chart(fig, use_container_width=True, key=f'hist_chart_{hist_id}')

if len(st.session_state.histograms) == len(allowed_columns_hist):
    st.warning("No more columns available for histograms")
else:
    st.button("Add histogram", on_click=add_histogram)