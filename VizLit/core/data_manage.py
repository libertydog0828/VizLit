import sys
sys.path.append("..")

from utils import data_reader
from pathlib import Path

def getDataObject(path:Path):
    return data_reader.ReadData(Path)