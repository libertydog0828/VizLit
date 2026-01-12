from abc import ABC, abstractmethod
from typing import Sequence, Optional, Any
import pandas as pd

class PlotBackend(ABC):
    @abstractmethod
    def plotDot(self,
                df:pd.DataFrame,
                x_col: str,
                y_cols: Sequence[str],
                *,
                size: Optional[tuple[int, int]],
                alpha: float = 1.0,
                title: Optional[str] = None,
                x_label: Optional[str] = None,
                y_label: Optional[str] = None,
                x_range: Optional[tuple[float, float]],
                y_range: Optional[tuple[float, float]],
                legends: Optional[Sequence[str]]
                ):
        pass

    @abstractmethod
    def plotLine(self,
                df:pd.DataFrame,
                x_col: str,
                y_cols: Sequence[str],
                *,
                size: Optional[tuple[int, int]],
                alpha: float = 1.0,
                title: Optional[str] = None,
                x_label: Optional[str] = None,
                y_label: Optional[str] = None,
                x_range: Optional[tuple[float, float]],
                y_range: Optional[tuple[float, float]],
                legends: Optional[Sequence[str]]):
        pass

    @abstractmethod
    def plotDotLine(self,
                df:pd.DataFrame,
                x_col: str,
                y_cols: Sequence[str],
                *,
                size: Optional[tuple[int, int]],
                alpha: float = 1.0,
                title: Optional[str] = None,
                x_label: Optional[str] = None,
                y_label: Optional[str] = None,
                x_range: Optional[tuple[float, float]],
                y_range: Optional[tuple[float, float]],
                legends: Optional[Sequence[str]]):
        pass