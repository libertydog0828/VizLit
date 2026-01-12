import streamlit as st
from pathlib import Path
import json
import pandas as pd

from VizLit import utils
from VizLit import view

ROOTPATH = Path(__file__).parent.resolve()

st.set_page_config(page_title = "VizLit",
                page_icon = ROOTPATH/"config"/"icon"/"icon.png",
                layout = "wide",
                initial_sidebar_state = "expanded")

# Definition Check
if not "input_data" in st.session_state:
    st.session_state["input_data"] = None

if not "loaded" in st.session_state:
    st.session_state["loaded"] = False

if not "view" in st.session_state:
    st.session_state["view"] = False

if not "x_axis_col" in st.session_state:
    st.session_state["x_axis_col"] = {}

if not "y_axis_col" in st.session_state:
    st.session_state["y_axis_col"] = {}

if not "graph_obj" in st.session_state:
    st.session_state["GraphObj"] = None

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

file_path = st.text_input("Input File Path (.h5 or .csv)",
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
        st.text(msg)
        st.session_state["input_data"] = loadData(path)
        st.session_state["loaded"] = True
    else:
        msg = ERRORTYPE["error_code"][key]
        st.warning(msg)
        st.session_state["input_data"] = None
        st.session_state["loaded"] = False

viewer_mode = st.sidebar.radio("Viewer Mode", ["Matplotlib", "Plotly", "Seaborn"])

### データ読み込み成功後 -> sidebar展開
if st.session_state["loaded"] == True:
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
            "Select Y-Axis (Multi Selection is available)",
            picked_data.columns
        )
    else:
        st.sidebar.warning("Sorry...Now On Developping")

    ### X-Axis, Y-Axis選択 -> button展開
    if st.session_state["x_axis_col"] and st.session_state["y_axis_col"]:
        __x_axis_col = st.session_state["x_axis_col"]
        __y_axis_col = st.session_state["y_axis_col"]
        marker = st.sidebar.radio("Marker", 
                                ["line", "dot", "line + dot"],
                                horizontal = True)
        
        x_min, x_max = st.sidebar.slider("X Range",
                                min_value = picked_data[__x_axis_col].min(),
                                max_value = picked_data[__x_axis_col].max(),
                                value = (picked_data[__x_axis_col].min(), picked_data[__x_axis_col].max()))
        # y_min, y_max = st.sidebar.slider("Y Range",
        #                         min_value = picked_data[__y_axis_col].min().min(),
        #                         max_value = picked_data[__y_axis_col].max().max(),
        #                         value = (picked_data[__y_axis_col].min().min(), picked_data[__y_axis_col].max().max()))

        if st.sidebar.button("Plot", type = "primary"):
            if viewer_mode == "Matplotlib":
                tmp_df = picked_data[(picked_data[__x_axis_col] >= x_min) & (picked_data[__x_axis_col] <= x_max)]
                # for col in __y_axis_col:
                #     tmp_df = tmp_df[(tmp_df[col] >= y_min) & (tmp_df[col] <= y_max)]
                backend = view.MatplotBackend
                
                if marker == "dot":
                    st.session_state["GraphObj"] = backend.plotDot(
                        tmp_df, __x_axis_col, __y_axis_col, size = [12, 6],
                        alpha = 1.0, title = f"{__x_axis_col} vs {__y_axis_col}",
                        x_label = __x_axis_col, y_label = __y_axis_col,
                        x_range = [])
                    st.session_state["view"] = True
                
                elif marker == "line":
                    st.session_state["GraphObj"] = backend.plotLine(
                        tmp_df, __x_axis_col, __y_axis_col, size = [12, 6],
                        alpha = 1.0, title = f"{__x_axis_col} vs {__y_axis_col}",
                        x_label = __x_axis_col, y_label = __y_axis_col)
                    st.session_state["view"] = True
                
                elif marker == "line + dot":
                    st.session_state["GraphObj"] = backend.plotDotLine(
                        tmp_df, __x_axis_col, __y_axis_col, size = [12, 6],
                        alpha = 1.0, title = f"{__x_axis_col} vs {__y_axis_col}",
                        x_label = __x_axis_col, y_label = __y_axis_col)
                    st.session_state["view"] = True
                
                else:
                    st.warning("Invalid Input!!!!")
                    st.session_state["view"] = False
                
            else:
                st.text("Sorry...Now ondevlopment.")

if st.session_state["view"] == True:
    if viewer_mode == "Matplotlib":
        st.pyplot(st.session_state["GraphObj"], clear_figure = True)
    else:
        st.text("Sorry...Now ondevlopment.")

st.markdown(
    """<hr style="margin-top: 50px;">
    <div style = "text-align:right; color:gray; font-size:0.8em;">
    © 2026 T.Terayama
    </div>
    """,
    unsafe_allow_html = True
)
