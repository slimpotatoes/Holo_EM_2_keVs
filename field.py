import numpy as np

def fields(dataem):
    constant_elec = - dataem.u_1 * dataem.u_2 / (
                2 * np.pi * dataem.e_charge * dataem.thickness * (dataem.u_2 - dataem.u_1))
    constant_magn = dataem.h_Planck / (-2 * np.pi * dataem.e_charge * dataem.thickness * (dataem.u_2 - dataem.u_1))


    dataem.potential_elec = dataem.diff_2_1_cor - dataem.diff_2_1_not_cor
    dataem.potential_magn = dataem.diff_2_1_cor - dataem.u_2 / (dataem.u_2 - dataem.u_1) * dataem.potential_elec
    # dataem.potential_magn = dataem.diff_2_1_cor - dataem.diff_2_1_not_cor
    # dataem.potential_magn = dataem.u_2 * dataem.diff_2_1_cor - dataem.u_1 * dataem.diff_2_1_not_cor

    # print('Constant electric, ', constant_elec)
    # print('Constant magnetic, ', constant_magn)
    E_cor = np.array(np.gradient(constant_elec / dataem.pixel * dataem.potential_elec))
    # B_cor = np.gradient(constant_magn / dataem.pixel * dataem.potential_magn)
    K_E = - dataem.h_Planck / dataem.u_1
    K_phi = - dataem.h_Planck / (2 * np.pi * dataem.e_charge * dataem.thickness)
    B_cor = K_E * E_cor + K_phi / dataem.pixel * np.array(np.gradient(dataem.diff_2_1_cor))
    # B_cor = np.add(np.gradient(constant_magn * dataem.u_2 / dataem.pixel * dataem.diff_2_1_cor), np.gradient(constant_magn * dataem.u_1 / dataem.pixel * dataem.diff_2_1_not_cor))


    A = np.shape(dataem.potential_elec)
    X, Y = np.meshgrid(np.arange(0, A[1]), np.arange(0, A[0]))

    dataem.field_elec = E_cor, X, Y
    dataem.field_magn = B_cor, X, Y
    print('Calculation done')