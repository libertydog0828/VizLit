import h5py
import pandas as pd
from pathlib import Path

class ReadData:
    def __init__(self, path:Path):
        self.__h5 = None
        self.__csv = None
        self.__judgeFileFormat(path)
        self.__readFile(path)


    def __judgeFileFormat(self, path:Path):
        if path.suffix == ".h5":
            self.__format = "H5"
        elif path.suffix == ".csv":
            self.__format == "CSV"
        else:
            self.__format = "INVALID"


    def __readFile(self, path:Path):
        match self.__format:
            case "H5":
                self.__readH5(path)
            case "CSV":
                self.__readCsv(path)
            case "INVALID":
                print("Not supported file.")


    def __readH5(self, path:Path):
        self.__h5 = h5py.File(path, "r")
        self.__header = list(self.__h5.keys())

        __tmp = {}
        for h in self.__header:
            if isinstance(self.h5[h], h5py.Group):
                continue
            else:
                __columns = self.__h5[h].dtype.names
                __data = self.__h5[h][:]
                __tmp[h] = pd.DataFrame(data = __data, columns = __columns)
        self.__data = __tmp
        del(__tmp)
        del(__data)


    def __readCsv(self, path:Path):
        self.__csv = pd.read_csv(path)


    @property
    def h5(self):
        return self.__h5
    
    @property
    def csv(self):
        return self.__csv
    
    @property
    def header(self):
        return self.__header
    
    @property
    def data(self):
        return self.__data