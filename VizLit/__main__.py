import sys
sys.path.append("..")

import os
from pathlib import Path
import utils

ROOTPATH = Path(__file__).parent.resolve()
DATAPATH = ROOTPATH.parent / "Data"

def main():
    obj = utils.ReadData(DATAPATH / "UDP_rear_left_radar_15_46_38_to_15_46_56_1759239998411.h5")
    print(obj.data["object_tracks"])

if __name__ == "__main__":
    main()