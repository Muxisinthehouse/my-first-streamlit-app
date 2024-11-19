import streamlit as st
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy
import random





@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

mpg_df_raw = load_data(path="./data/mpg.csv")
mpg_df = deepcopy(mpg_df_raw)


# Add title and header
st.title("Wo chöi mer mit em Hund umeluege?  ")
st.header("Where to walk the dog? \n Find your dog-peers in Zürich")

hunde = pd.read_csv("./data/20200306_hundehalter.csv")# skiprows=2)
hunde['halter_alter'] = hunde['ALTER'].str[:2].astype(int)+random.randint(0,9)
hunde['hunde_alter'] = 2024-hunde['GEBURTSJAHR_HUND'].astype(int)
hunde['anschaffungsalter']=hunde.halter_alter-hunde.hunde_alter
hunde.head(5)
hunde = hunde[hunde['hunde_alter'] <= 20]

stadtkreise = json.load(open("./data/stzh.adm_stadtkreise_a.json"))


left_column,right_column = st.columns(2)
status_list = ['All'] +  list(hunde.RASSE1.unique())
status1 = left_column.selectbox('What kind of dog do you have?',status_list)

if status1!='All':
    df_temp=hunde[hunde.RASSE1==status1].groupby('STADTKREIS').count().reset_index()
else:
    df_temp=hunde.groupby('STADTKREIS').count().reset_index()


status_list = ['All'] +  list(hunde[hunde.RASSE1==status1].GESCHLECHT_HUND.unique())
status2 = left_column.selectbox('What is the gender of your dog?',status_list)

if status2!='All':
    df_temp=hunde[(hunde['GESCHLECHT_HUND'] == status2 ) & (hunde['RASSE1'] == status1)].groupby('STADTKREIS').count().reset_index()

status_list = ['All'] +  list(hunde[(hunde['GESCHLECHT_HUND'] == status2 ) & (hunde['RASSE1'] == status1)].HUNDEFARBE.unique())
status3 = left_column.selectbox('What color does your dog have?',status_list)

if status3!='All':
    df_temp=hunde[(hunde['GESCHLECHT_HUND'] == status2 ) & (hunde['RASSE1'] == status1)& (hunde['HUNDEFARBE'] == status3)].groupby('STADTKREIS').count().reset_index()


df_temp.rename(columns={'RASSE1':'Dogs'},inplace=True)


fig = px.choropleth_mapbox(
                data_frame=df_temp,
                geojson = stadtkreise,
                locations='STADTKREIS', 
                featureidkey = 'properties.name', 
                color = 'Dogs',
                color_continuous_scale="Viridis",
                mapbox_style="carto-positron",
                zoom=10, 
                center = {"lat": 47.3769, "lon": 8.5417},
                opacity=0.5,
    #            hover_data = {'ISO': False, status: True},
    #            hover_name = 'Country'
    )

fig.update_layout(title="Dog-Peers")
                
        
st.plotly_chart(fig)

