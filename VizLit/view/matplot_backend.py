import matplotlib.pyplot as plt
import pandas as pd
from typing import Sequence, Optional, Mapping, Any

from .base import PlotBackend

class MatplotBackend(PlotBackend):
    @classmethod
    def plotDot(cls, df:pd.DataFrame, x_col:str, y_cols:Sequence[str],*,
                size = [12, 6], alpha = 1.0,
                title = None, x_label = None, y_label = None,
                x_range = [None, None], y_range = [None, None],
                legends = None):
        legends = cls.__validateLegends(y_cols, legends)
        x_range, y_range = cls.__validateRange(df, x_col, y_cols, x_range, y_range)
        fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (size[0], size[1]))
        
        ax.grid(True)
        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_xlim(x_range[0], x_range[1])
        ax.set_ylim(y_range[0], y_range[1])
        
        for cnt,y_col in enumerate(y_cols):
            ax.plot(df[x_col], df[y_col], marker="o", linestyle = "None", alpha=alpha, label=legends[cnt])
            ax.legend()
        return fig


    @classmethod
    def plotLine(cls, df:pd.DataFrame, x_col:str, y_cols:Sequence[str],*,
                size = [12, 6], alpha = 1.0,
                title = None, x_label = None, y_label = None,
                x_range = [None, None], y_range = [None, None],
                legends = None):
        legends = cls.__validateLegends(y_cols, legends)
        x_range, y_range = cls.__validateRange(df, x_col, y_cols, x_range, y_range)
        fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (size[0], size[1]))
        
        ax.grid(True)
        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_xlim(x_range[0], x_range[1])
        ax.set_ylim(y_range[0], y_range[1])
        
        for cnt,y_col in enumerate(y_cols):
            ax.plot(df[x_col], df[y_col], linestyle = "-", alpha=alpha, label=legends[cnt])
            ax.legend()
        return fig


    @classmethod
    def plotDotLine(cls, df:pd.DataFrame, x_col:str, y_cols:Sequence[str],*,
                size = [12, 6], alpha = 1.0, style = None,
                title = None, x_label = None, y_label = None,
                x_range = [None, None], y_range = [None, None],
                legends = None):
        legends = cls.__validateLegends(y_cols, legends)
        x_range, y_range = cls.__validateRange(df, x_col, y_cols, x_range, y_range)
        fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (size[0], size[1]))
        
        ax.grid(True)
        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_xlim(x_range[0], x_range[1])
        ax.set_ylim(y_range[0], y_range[1])
        
        for cnt,y_col in enumerate(y_cols):
            ax.plot(df[x_col], df[y_col], marker = "o", linestyle = "-", alpha=alpha, label=legends[cnt])
            ax.legend()
        return fig

    @staticmethod
    def __validateLegends(y_cols, legends):
        if legends is None:
            return list(y_cols)

        if len(legends) != len(y_cols):
            raise ValueError(
                f"Length of legends ({len(legends)}) must match y_cols ({len(y_cols)})"
            )

        return legends

    @staticmethod
    def __validateRange(df, x_col, y_cols, x_range, y_range):
        if x_range[0] == None and x_range[1] == None:
            x_range[0] = df[x_col].min()
            x_range[1] = df[x_col].max()
        
        if y_range[0] == None and y_range[1] == None:
            y_range[0] = df[y_cols].min().min()
            y_range[1] = df[y_cols].max().max()

        return x_range, y_range