import math

class EMdata(object):

    def __init__(self):
        self.holo_1 = None
        self.holo_2 = None
        self.holo_ref = None
        self.holo_2_aligned = None
        self.phase_1 = None
        self.amplitude_1 = None
        self.amplitude_2 = None
        self.phase_2 = None
        self.phase_ref = None
        self.diff_1_ref = None
        self.diff_2_ref = None
        self.diff_2_1_cor = None
        self.diff_2_1_not_cor = None
        self.potential_elec = None
        self.field_elec = None
        self.field_elec_not_cor = None
        self.potential_magn = None
        self.field_magn = None
        self.field_magn_not_cor = None
        self.pixel = None
        self.constant = None
        self.e_charge = 1.6 * 10 ** (-19)
        self.me_charge = 9.31 * 10 ** (-31)
        self.h_Planck = 6.62 * 10 ** (-34)
        self.u_1 = self.h_Planck * 2.3279 * 10 ** 8 # Velocity electron at 300 kev
        self.u_2 = self.h_Planck * 1.5061 * 10 ** 8 # Velocity electron at 80 kev
        self.thickness = 100 * 10 ** (-9)