import streamlit as st
import pandas as pd
import plotly as plt
import numpy as np
from app import data_processing as dp


st.write("""my
         first a
         
         pp  
         Hello world""")


df = dp.load_data()
count = df['Company'].value_counts()
st.bar_chart(count)