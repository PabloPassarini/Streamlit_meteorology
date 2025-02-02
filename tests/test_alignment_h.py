import streamlit as st
key = 1
value = 19
col3, col4, col5, col6 = st.columns([2, 2, 1, 1]) # Note the change  in spec
with col3:  
    st.markdown(f"**{key}**:")  
with col4:  
    st.markdown(f"{value}")  
with col5:  
    thumbs_down_key = f"thumbs_down_{key}" 
    thumbs_down_button = st.button("👎", thumbs_down_key)  
with col6:
    thumbs_up_key = f"thumbs_up_{key}"  
    thumbs_up_button = st.button("👍", thumbs_up_key)