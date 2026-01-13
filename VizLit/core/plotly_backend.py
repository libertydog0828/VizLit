import plotly.graph_objects as go
import pandas as pd
from typing import Sequence

class PlotlyBackend:
    @classmethod
    def genGraphObject(cls, 
                    df:pd.DataFrame, x_col:str, y_cols:Sequence[str], 
                    draw_mode:str, view_ratio:str):

        fig = go.Figure()

        for y_col in y_cols:
            fig.add_trace(
                go.Scatter(
                    x = df[x_col],
                    y = df[y_col],
                    mode = draw_mode,
                    name = y_col,
                    marker = dict(size=4),
                    line=dict(width=1)
                )
            )

        if view_ratio == "Square":
            fig.update_layout(
                width = 600,
                height = 600,
                yaxis_title = "Value",
                hovermode = "x unified",
                margin = dict(l = 40, r = 20, t = 40, b = 40),
                )
        elif view_ratio == "Rectangle":
            fig.update_layout(
                width = 800,
                height = 400,
                yaxis_title = "Value",
                hovermode = "x unified",
                margin = dict(l = 40, r = 20, t = 40, b = 40),
            )

        return fig