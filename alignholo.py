import numpy as np
from skimage import transform

def shift_holo(shift_gui, em_data):
    # em_data.holo_2_aligned = shift(em_data.holo_2, shift_gui)
    em_data.holo_2_aligned = np.roll(em_data.holo_2, shift_gui, axis=(0, 1))


def crop_phase(shift_gui, image_not_shifted, image_shifted):
    print('shift image horizontal ', shift_gui[1])
    print('shift gui vertical ', shift_gui[0])
    if shift_gui[0] > 0:
        if shift_gui[1] > 0:
            image_not_shifted_crop = np.array(image_not_shifted[shift_gui[0]:, shift_gui[1]:])
            image_shifted_crop = np.array(image_shifted[:-shift_gui[0], :-shift_gui[1]])
            return [image_not_shifted_crop, image_shifted_crop]
        if shift_gui[1] < 0:
            image_not_shifted_crop = np.array(image_not_shifted[shift_gui[0]:, :shift_gui[1]])
            image_shifted_crop = np.array(image_shifted[:-shift_gui[0], -shift_gui[1]:])
            return [image_not_shifted_crop, image_shifted_crop]
        if shift_gui[1] == 0:
            image_not_shifted_crop = np.array(image_not_shifted[shift_gui[0]:, :])
            image_shifted_crop = np.array(image_shifted[:-shift_gui[0], :])
            return [image_not_shifted_crop, image_shifted_crop]
    elif shift_gui[0] < 0:
        if shift_gui[1] > 0:
            image_not_shifted_crop = np.array(image_not_shifted[:shift_gui[0], shift_gui[1]:])
            image_shifted_crop = np.array(image_shifted[-shift_gui[0]:, :-shift_gui[1]])
            return [image_not_shifted_crop, image_shifted_crop]
        if shift_gui[1] < 0:
            image_not_shifted_crop = np.array(image_not_shifted[:shift_gui[0], :shift_gui[1]])
            image_shifted_crop = np.array(image_shifted[-shift_gui[0]:, -shift_gui[1]:])
            return [image_not_shifted_crop, image_shifted_crop]
        if shift_gui[1] == 0:
            image_not_shifted_crop = np.array(image_not_shifted[:shift_gui[0], :])
            image_shifted_crop = np.array(image_shifted[-shift_gui[0]:, :])
            return [image_not_shifted_crop, image_shifted_crop]
    elif shift_gui[0] == 0:
        if shift_gui[1] > 0:
            image_not_shifted_crop = np.array(image_not_shifted[:, shift_gui[1]:])
            image_shifted_crop = np.array(image_shifted[:, :-shift_gui[1]])
            return [image_not_shifted_crop, image_shifted_crop]
        if shift_gui[1] < 0:
            image_not_shifted_crop = np.array(image_not_shifted[:, :shift_gui[1]])
            image_shifted_crop = np.array(image_shifted[:, -shift_gui[1]:])
            return [image_not_shifted_crop, image_shifted_crop]
        if shift_gui[1] == 0:
            image_not_shifted_crop = np.array(image_not_shifted[:, :])
            image_shifted_crop = np.array(image_shifted[:, :])
            return [image_not_shifted_crop, image_shifted_crop]

def deform_image(scale, rotation, shear, translation, data_em):
    transformation = transform.AffineTransform(scale=scale, rotation=rotation, shear=shear, translation=translation)
    data_em.holo_2_aligned = transform.warp(data_em.holo_2 , transformation, preserve_range=1)
    print('Deformation done')