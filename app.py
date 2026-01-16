import streamlit as st
from pathlib import Path
import json
import pandas as pd

from VizLit import utils
from VizLit import core
from VizLit import pages

ROOTPATH = Path(__file__).parent.resolve()

st.set_page_config(page_title = "VizLit",
                page_icon = ROOTPATH/"config"/"icon"/"icon.png",
                layout = "wide",
                initial_sidebar_state = "expanded")

# Session State Initialize
core.initSessionState()

# file reader (Cache Data)
@st.cache_resource
def loadData(path:Path):
    return utils.ReadData(path)

@st.cache_data
def loadErrors():
    path = ROOTPATH/"config"/"error.json"
    with path.open(encoding="utf-8") as f:
        return json.load(f)

ERRORTYPE = loadErrors()

st.title("Data Analyzer")

file_path = st.text_input(
    "Input File Path (.h5 or .csv)",
    value = ROOTPATH / "Data")

### データを読み込むためのbuttonウィジェット
if st.button("Read Data", help = "Read H5 or Csv File", type = "primary"):
    path = Path(file_path)
    key = "NoError"

    if not path.exists():
        key = "NotExist"
    elif path.is_dir():
        key = "IsDirectory"
    else:
        if path.suffix not in [".csv", ".h5"]:
            key = "NotSupport"

    if key == "NoError":
        msg = ERRORTYPE["error_code"][key]
        st.session_state["input_data"] = loadData(path)
        st.session_state["loaded"] = True
    else:
        msg = ERRORTYPE["error_code"][key]
        st.warning(msg)
        st.session_state["input_data"] = None
        st.session_state["loaded"] = False

mode_map = {
    "line" : "lines",
    "dot" : "markers",
    "line+dot" : "lines+markers"
}

### データ読み込み成功後 -> sidebar展開
if st.session_state["loaded"] == True:
    picked_data = pages.pickData()

    ### X-Axis, Y-Axis選択 -> button展開
    if st.session_state["x_axis_col"] and st.session_state["y_axis_col"]:
        draw_mode = st.sidebar.radio("Marker", ["line", "dot", "line+dot"])
        view_ratio = st.sidebar.radio("Ratio", ["Square", "Rectangle"])
        show_raw = st.sidebar.toggle("Picked Data", value = False)
        val_min, val_max = st.sidebar.slider(
            "View Range",
            min_value = picked_data.loc[:, st.session_state["x_axis_col"]].min(),
            max_value = picked_data.loc[:, st.session_state["x_axis_col"]].max(),
            value = (picked_data.loc[:, st.session_state["x_axis_col"]].min(), picked_data.loc[:, st.session_state["x_axis_col"]].max())
        )

        plot_data = picked_data[(picked_data[st.session_state["x_axis_col"]]>=val_min) & 
                                (picked_data[st.session_state["x_axis_col"]]<=val_max)]

        if show_raw:
            st.subheader("Extracted Data")
            st.dataframe(picked_data)
        
        backend = core.PlotlyBackend()
        fig = backend.genGraphObject(plot_data, 
                                    st.session_state["x_axis_col"], st.session_state["y_axis_col"], 
                                    mode_map[draw_mode], view_ratio)

        st.plotly_chart(fig, width='stretch')

st.markdown(
    """<hr style="margin-top: 50px;">
    <div style = "text-align:right; color:gray; font-size:0.8em;">
    © 2026 T.Terayama
    </div>
    """,
    unsafe_allow_html = True
)
