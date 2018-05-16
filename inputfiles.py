
import dm3_lib as dm3_lib
import matplotlib.pyplot as plt
import numpy as np


def load_files(file_path_holo_1, file_path_holo_2, file_path_holo_ref, em_data):
    data_1 = dm3_lib.DM3(file_path_holo_1)
    data_2 = dm3_lib.DM3(file_path_holo_2)
    data_ref = dm3_lib.DM3(file_path_holo_ref)
    em_data.holo_1 = data_1.imagedata
    em_data.holo_2 = data_2.imagedata
    em_data.holo_ref = data_ref.imagedata
    if data_1.pxsize[1].decode("ascii") == 'nm':
        em_data.pixel = data_1.pxsize[0] * 10 ** (-9)
    else:
        em_data.pixel = data_1.pxsize[0] * 10 ** (-9)
        print("Improper pixel unit, forced to be nm")

    # Test files

    '''em_data.holo_1 = np.loadtxt("/media/alex/Work/PhD/Research/Holography EM/Experiments/2018-04-30 - Holo Isobel T8-1/"
                                "Holo_300_Ey_100MV_Bx_1T.txt")
    em_data.holo_2 = np.loadtxt("/media/alex/Work/PhD/Research/Holography EM/Experiments/2018-04-30 - Holo Isobel T8-1/"
                                "Holo_80_Ey_100MV_Bx_1T.txt")
    em_data.holo_ref = np.loadtxt("/media/alex/Work/PhD/Research/Holography EM/"
                                "Data_Processing/Simulation/Holo_1024_reference.txt")
    em_data.pixel = 10 ** (-9)'''