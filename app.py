import streamlit as st
from pathlib import Path
import json

from VizLit import utils

st.set_page_config(page_title = "VizLit",
                page_icon = "⭐️",
                layout = "wide",
                initial_sidebar_state = "expanded")

ROOTPATH = Path(__file__).parent.resolve()
st.session_state.input_data = None

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
                        value = "/Users/terayamatosei/Workspace/VizLit/Data")

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
        st.session_state.input_data = loadData(path)
    else:
        msg = ERRORTYPE["error_code"][key]
        st.warning(msg)

if st.session_state.input_data is not None:
    if path.suffix == ".h5":
        picked_header = st.sidebar.selectbox(
            "Select Data Header",
            st.session_state.input_data.header
        )
    picked_data = st.session_state.input_data.data[picked_header]

    x_axis_col = st.sidebar.selectbox(
        "Select choose X-Axis",
        picked_data.columns
    )
    y_axis_col = st.sidebar.multiselect(
        "Select choose Y-Axis (multi select possible)",
        picked_data.columns
    )

st.markdown(
    """<hr style="margin-top: 50px;">
    <div style = "text-align:right; color:gray; font-size:0.8em;">
    © 2025 T.Terayama
    </div>
    """,
    unsafe_allow_html = True
)

# ----------------------
# h5ファイル指定
# ----------------------
# h5_path = st.text_input(
#     "h5ファイルのパスを入力してください",
#     value="data/sample.h5"
# )

# if not Path(h5_path).exists():
#     st.warning("ファイルが存在しません")
#     st.stop()