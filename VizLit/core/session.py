import streamlit as st

def initSessionState():
    defaults = {
        "input_data" : None,
        "loaded" : False,
        "view" : False,
        "x_axis_col" : {},
        "y_axis_col" : {},
        "GraphObj" : None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value