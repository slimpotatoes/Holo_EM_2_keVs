# GPA Module


import mask as mask
import numpy as np
from skimage.restoration import unwrap_phase
import alignholo as alignholo
# import dm3_lib


def phase(center_1, r_1, center_2, r_2, dataEM):

    # Load the elements
    ft_holo_1 = np.fft.fft2(dataEM.holo_1)
    ft_holo_2 = np.fft.fft2(dataEM.holo_2_aligned)
    ft_holo_ref = np.fft.fft2(dataEM.holo_ref)

    # Generate the mask in the image space
    m_1, g_uns_1 = mask.mask_gaussian(center_1, r_1, ft_holo_1.shape)
    m_2, g_uns_2 = mask.mask_gaussian(center_2, r_2, ft_holo_2.shape)

    # Mask and calculate the phase component
    masked_ft_holo_1 = np.multiply(m_1, np.fft.fftshift(ft_holo_1))
    masked_ft_holo_2 = np.multiply(m_2, np.fft.fftshift(ft_holo_2))
    masked_ft_holo_ref = np.multiply(m_1, np.fft.fftshift(ft_holo_ref))
    # masked_ft_holo_ref_2 =  np.multiply(m, np.fft.fftshift(ft_holo_ref_2))

    # shift and crop before unwraping
    i_fft_1 = np.fft.ifft2(np.fft.ifftshift(masked_ft_holo_1))
    i_fft_2 = np.fft.ifft2(np.fft.ifftshift(masked_ft_holo_2))
    amplitude_1_distorded = np.abs(i_fft_1)
    amplitude_2_distorded = np.abs(i_fft_2)
    phase_1_distorded = np.angle(i_fft_1)
    phase_2_distorded = np.angle(i_fft_2)

    dataEM.phase_ref = unwrap_phase(np.angle(np.fft.ifft2(np.fft.ifftshift(masked_ft_holo_ref))), seed=None)
    phase_1_distorded_unwrap = unwrap_phase(phase_1_distorded, seed=None)
    phase_2_distorded_unwrap = unwrap_phase(phase_2_distorded, seed=None)

    phase_1_unwrap = phase_1_distorded_unwrap # - dataEM.phase_ref
    phase_2_unwrap = phase_2_distorded_unwrap # - dataEM.phase_ref

    amplitude_crop = alignholo.crop_phase([0, 0], amplitude_1_distorded, amplitude_2_distorded)

    dataEM.phase_1 = np.float64(phase_1_distorded_unwrap)
    dataEM.phase_2 = np.float64(phase_2_distorded_unwrap)
    dataEM.amplitude_1 = amplitude_crop[0]
    dataEM.amplitude_2 = amplitude_crop[1]

    # dataEM.phase_ref_2 = unwrap_phase(np.angle(np.fft.ifft2(np.fft.ifftshift(masked_ft_holo_ref_2))))

    dataEM.diff_1_ref_notsmoothed = dataEM.phase_1
    dataEM.diff_2_ref_notsmoothed = dataEM.phase_2
    dataEM.diff_2_1_cor_notsmoothed = dataEM.phase_1
    dataEM.diff_2_1_not_cor_notsmoothed = dataEM.phase_2

    '''dataEM.diff_1_ref = gaussian_filter(dataEM.diff_1_ref_notsmoothed, 6)
    dataEM.diff_2_ref = gaussian_filter(dataEM.diff_2_ref_notsmoothed, 6)
    dataEM.diff_2_1_not_cor = gaussian_filter(dataEM.diff_2_1_not_cor_notsmoothed, 6)
    dataEM.diff_2_1_cor = gaussian_filter(dataEM.diff_2_1_cor_notsmoothed, 6)'''

    dataEM.diff_1_ref = dataEM.diff_1_ref_notsmoothed
    dataEM.diff_2_ref = dataEM.diff_2_ref_notsmoothed
    dataEM.diff_2_1_not_cor = dataEM.diff_2_1_not_cor_notsmoothed
    dataEM.diff_2_1_cor = dataEM.diff_2_1_cor_notsmoothed