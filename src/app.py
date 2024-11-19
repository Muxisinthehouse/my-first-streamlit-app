import streamlit as st
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

mpg_df_raw = load_data(path="../data/mpg.csv")
mpg_df = deepcopy(mpg_df_raw)


# Add title and header
st.title("Introduction to Streamlit")
st.header("MPG Data Exploration")

if st.checkbox('show DF'):
    st.dataframe(data=mpg_df)


if year == "All":
    reduced_df = mpg_df
else:
    reduced_df = mpg_df[mpg_df["year"] == year]

means = reduced_df.groupby('class').mean(numeric_only=True)



m_fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(reduced_df['displ'], reduced_df['hwy'], alpha=0.7)
ax.set_title("Engine Size vs. Highway Fuel Mileage")
ax.set_xlabel('Displacement (Liters)')
ax.set_ylabel('MPG')

st.pyplot(m_fig)

