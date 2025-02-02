import streamlit as st
import pandas as pd
poi = pd.DataFrame({
    'lat': [37.77, 37.78, 37.79],
    'lon': [-122.41, -122.42, -122.43],
    'name': ['POI 1', 'POI 2', 'POI 3']
})

st.map(poi)