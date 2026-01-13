import streamlit as st

def pickData():
    if st.session_state["input_data"].format == "H5":
        picked_header = st.sidebar.selectbox(
            "Click Data Header",
            st.session_state["input_data"].header
        )
        picked_data = st.session_state["input_data"].data[picked_header]

        st.session_state["x_axis_col"] = st.sidebar.selectbox(
            "Select X-Axis",
            picked_data.columns
        )

        st.session_state["y_axis_col"] = st.sidebar.multiselect(
            "Select Y-Axis (Multi Seletion is available)",
            picked_data.columns
        )

        return picked_data

    else:
        st.sidevar.warning("Sorry...Now On Development")

        return None