import requests
import streamlit as st


def remove_streamlit_elements():
    hide_default_format = """
    <style>
    #MainMenu {visibility: hidden; }
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
    """
    st.markdown(hide_default_format, unsafe_allow_html=True)
