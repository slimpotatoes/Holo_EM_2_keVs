import matplotlib.pyplot as plt
import matplotlib.gridspec as grid
from matplotlib.widgets import Button
from matplotlib.colors import LinearSegmentedColormap
from tkinter import filedialog
import numpy as np
import guidisplay as guidisplay
import guimask as guimask
import guirectangle as guirect
import imagedisplay


class HoloEMgui(object):

    def __init__(self, data_em):
        self.dataEM = data_em
        self.fig_flow = None
        self.event_input = None
        self.event_align = None
        self.event_ft = None
        self.event_phase = None
        self.event_refine = None
        self.event_field = None
        self.fig_align = None
        self.fig_mask_1 = None
        self.fig_mask_2 = None
        self.fig_potential = None
        self.fig_field = None
        self.circle_1 = None
        self.circle_2 = None
        self.shift = [0, 0]

    def flow(self):
        self.fig_flow = plt.figure(num='SMG Flow', figsize=(2, 5))
        self.fig_flow.canvas.mpl_connect('key_press_event', self.custom_plot)
        gs_button = grid.GridSpec(6, 1)
        self.event_input = Button(self.fig_flow.add_axes(self.fig_flow.add_subplot(gs_button[0, 0])), 'Input')
        self.event_align = Button(self.fig_flow.add_axes(self.fig_flow.add_subplot(gs_button[1, 0])), 'Align')
        self.event_ft = Button(self.fig_flow.add_axes(self.fig_flow.add_subplot(gs_button[2, 0])), 'FT')
        self.event_phase = Button(self.fig_flow.add_axes(self.fig_flow.add_subplot(gs_button[3, 0])), 'Phase')
        self.event_refine = Button(self.fig_flow.add_axes(self.fig_flow.add_subplot(gs_button[4, 0])), 'Refine')
        self.event_field = Button(self.fig_flow.add_axes(self.fig_flow.add_subplot(gs_button[5, 0])), 'Field')


    @staticmethod
    def open_files():
        file_path_holo_1 = filedialog.askopenfilename(title="Load first hologram")
        file_path_holo_2 = filedialog.askopenfilename(title="Load second hologram")
        file_path_holo_ref = filedialog.askopenfilename(title="Load reference hologram")
        #file_path_holo_ref_2 = filedialog.askopenfilename(title="Load reference hologram 2")
        return file_path_holo_1, file_path_holo_2, file_path_holo_ref

    def align_holo(self):
        self.fig_align = guidisplay.GUIDisplayOverlap(self.dataEM)
        plt.show()

    def mask_holo(self):
        self.fig_mask = plt.figure(num='Define mask')
        self.ax_fig_mask_1 = self.fig_mask.add_subplot(1, 2, 1)
        self.ax_fig_mask_2 = self.fig_mask.add_subplot(1, 2, 2)


        ft_holo_1 = self.fft_display(np.fft.fft2(self.dataEM.holo_1))
        ft_holo_2 = self.fft_display(np.fft.fft2(self.dataEM.holo_2_aligned))
        ft_holo_ref = self.fft_display(np.fft.fft2(self.dataEM.holo_ref))

        self.ax_fig_mask_1.imshow(np.log1p(ft_holo_1), cmap='gray')
        self.ax_fig_mask_2.imshow(np.log1p(ft_holo_2), cmap='gray')
        self.ax_fig_mask_1.imshow(np.log1p(ft_holo_ref), cmap='gray', alpha=0.25)

        guimaskcreate = guimask.MaskCreator(self.ax_fig_mask_1, self.dataEM.holo_1)
        guimaskcreate.make_circle('Mask 1')
        self.circle_1 = guimask.MaskEditor(self.ax_fig_mask_1.artists[0])
        self.circle_1.connect()

        guimaskcreate = guimask.MaskCreator(self.ax_fig_mask_2, self.dataEM.holo_2_aligned)
        guimaskcreate.make_circle('Mask 2', colored='b')
        self.circle_2 = guimask.MaskEditor(self.ax_fig_mask_2.artists[0])
        self.circle_2.connect()

        plt.show()

    @staticmethod
    def fft_display(fft):
        return np.fft.fftshift(np.abs(fft ** 2))

    def phase_holo(self):
        self.fig_phase = plt.figure()
        self.ax_fig_phase_1 = self.fig_phase.add_subplot(3, 2, 1)
        self.ax_fig_phase_2 = self.fig_phase.add_subplot(3, 2, 2)
        self.ax_fig_phase_diff = self.fig_phase.add_subplot(3, 2, 3)
        self.ax_fig_phase_diff_1 = self.fig_phase.add_subplot(3, 2, 4)
        self.ax_fig_ampltiude_1 = self.fig_phase.add_subplot(3, 2, 5)
        self.ax_fig_ampltiude_2 = self.fig_phase.add_subplot(3, 2, 6)
        self.ax_fig_phase_1.imshow(self.wrap(self.dataEM.diff_1_ref), cmap='gray')
        self.ax_fig_phase_2.imshow(self.wrap(self.dataEM.diff_2_ref), cmap='gray')
        self.ax_fig_phase_diff.imshow(self.dataEM.diff_2_1_cor, cmap='gray')
        self.ax_fig_phase_diff_1.imshow(self.dataEM.diff_2_1_not_cor, cmap='gray')
        self.ax_fig_ampltiude_1.imshow(self.dataEM.amplitude_1, cmap='gray')
        self.ax_fig_ampltiude_2.imshow(self.dataEM.amplitude_2, cmap='gray')

        guirectcreate = guirect.RectCreator(self.ax_fig_phase_diff, self.dataEM.diff_2_1_cor)
        guirectcreate.make_rectangle('Rect')
        self.rect = guirect.RectEditor(self.fig_phase, self.ax_fig_phase_diff, guirectcreate.rect)
        self.rect.connect()

        plt.show()

    @staticmethod
    def wrap(phase):
        return phase - np.round(phase / (2 * np.pi)) * 2 * np.pi

    def reference_extract(self, rectangle):
        x0, y0 = rectangle.get_xy()
        x1, y1 = x0 + rectangle.get_width(), y0 + rectangle.get_height()
        print(int(x0), int(y0), int(x1), int(y1))
        return int(x0), int(y0), int(x1), int(y1)

    def refine_gui(self):
        self.ax_fig_phase_diff.imshow(self.dataEM.diff_2_1_cor, cmap='gray')
        self.ax_fig_phase_diff_1.imshow(self.dataEM.diff_2_1_not_cor, cmap='gray')
        self.fig_phase.canvas.draw()

    def field_gui(self):
        self.fig_potential = plt.figure(num='Electric Potential')
        self.ax_fig_potential = self.fig_potential.add_subplot(1, 1, 1)
        image_potential = self.ax_fig_potential.imshow(self.dataEM.potential_elec, cmap='gray')
        level = np.arange(np.min(self.dataEM.potential_elec[100:-100, 100: -100]),
                          np.max(self.dataEM.potential_elec[100:-100, 100: -100]), 0.5)
        contour = self.ax_fig_potential.contour(self.dataEM.potential_elec, level, linewidths=2)
        #self.ax_fig_potential.clabel(contour, inline=1, fontsize=10, hold=False)
        self.ax_fig_potential.set_axis_off()
        cbar = plt.colorbar(image_potential)
        cbar.add_lines(contour)

        print('Electric potential mapped')

        self.fig_potential_not_cor = plt.figure(num='Magnetic Potential')
        self.ax_fig_potential_not_cor = self.fig_potential_not_cor.add_subplot(1, 1, 1)
        self.ax_fig_potential_not_cor.imshow(np.array(self.dataEM.potential_magn, dtype=float), cmap='gray')
        level_1 = np.arange(np.min(np.array(self.dataEM.potential_magn[100:-100, 100: -100], dtype=float)),
                            np.max(np.array(self.dataEM.potential_magn[100:-100, 100: -100], dtype=float)), 0.5)
        contour_1 = self.ax_fig_potential_not_cor.contour(np.array(self.dataEM.potential_magn, dtype=float), level_1)
        self.ax_fig_potential_not_cor.clabel(contour_1, inline=1, fontsize=10, hold=False)
        self.ax_fig_potential_not_cor.set_axis_off()
        print('Magnetic potential mapped')

        orient_E = np.arctan2(self.dataEM.field_elec[0][1], -self.dataEM.field_elec[0][0])

        fig_temp_E = plt.figure()
        axis_temp_E = fig_temp_E.add_subplot(1, 1, 1)
        image_temp_E = axis_temp_E.imshow(orient_E, cmap='hsv', vmin=-np.pi, vmax=np.pi, alpha=0.6)
        fig_temp_E.colorbar(image_temp_E)
        axis_temp_E.quiver(self.dataEM.field_elec[1][50:-50:30, 50:-50:30],
                           self.dataEM.field_elec[2][50:-50:30, 50:-50:30],
                           np.ma.masked_greater_equal(10 ** (-9) * self.dataEM.field_elec[0][1][50:-50:50, 50:-50:50], 0.5),
                           np.ma.masked_greater_equal(-10 ** (-9) * self.dataEM.field_elec[0][0][50:-50:50, 50:-50:50], 0.5),
                           scale=2, units='width', pivot='mid', color='k', alpha=0.7, headwidth=4, width = 0.004)
        axis_temp_E.set_axis_off()
        fig_temp_E.show()
        print('Field electric mapped')

        orient_B = np.arctan2(-self.dataEM.field_magn[0][0], -self.dataEM.field_magn[0][1])

        fig_temp_B = plt.figure()
        axis_temp_B = fig_temp_B.add_subplot(1, 1, 1)
        image_temp_B = axis_temp_B.imshow(orient_B, cmap='hsv', vmin=-np.pi, vmax=np.pi, alpha=0.6)
        fig_temp_B.colorbar(image_temp_B)
        axis_temp_B.quiver(self.dataEM.field_magn[1][50:-50:50, 50:-50:50],
                           self.dataEM.field_magn[2][50:-50:50, 50:-50:50],
                           np.ma.masked_greater_equal(-self.dataEM.field_magn[0][0][50:-50:50, 50:-50:50], 1),
                           np.ma.masked_greater_equal(-self.dataEM.field_magn[0][1][50:-50:50, 50:-50:50], 1),
                           scale=6, units='width', pivot='mid', color='k', alpha=0.7, headwidth=4, width=0.004)
        axis_temp_B.set_axis_off()
        fig_temp_B.show()
        print('Field magnetic mapped')

        fig_temp_E_magnitude = plt.figure()
        axis_temp_E_magnitude = fig_temp_E_magnitude.add_subplot(1, 1, 1)
        image_temp_E_magnitude = axis_temp_E_magnitude.imshow(10 ** (-9) *
            np.sqrt(np.square(self.dataEM.field_elec[0][0][50:-50, 50:-50])+
                    np.square(self.dataEM.field_elec[0][1][50:-50, 50:-50])), vmin=0, vmax=0.5)
        fig_temp_E_magnitude.colorbar(image_temp_E_magnitude)
        axis_temp_E_magnitude.set_axis_off()
        fig_temp_E_magnitude.show()

        fig_temp_B_magn = plt.figure()
        axis_temp_B_magn = fig_temp_B_magn.add_subplot(1, 1, 1)
        image_temp_B_magn = axis_temp_B_magn.imshow(
            np.sqrt(np.square(self.dataEM.field_magn[0][0][50:-50, 50:-50]) +
                    np.square(self.dataEM.field_magn[0][1][50:-50, 50:-50])), vmin=0, vmax=1)
        fig_temp_B_magn.colorbar(image_temp_B_magn)
        axis_temp_B_magn.set_axis_off()
        fig_temp_B_magn.show()

        plt.show()

    def custom_plot(self, event):
        if event.key == '1':
            data_to_display = self.dataEM.holo_1
            p = self.dataEM.pixel * 10 **(9)
            imagedisplay.ImageDisplay(data_to_display, cal=p)
        if event.key == '2':
            data_to_display = self.dataEM.holo_2_aligned
            p = self.dataEM.pixel * 10 **(9)
            imagedisplay.ImageDisplay(data_to_display, cal=p)
        if event.key == '3':
            data_to_display = self.dataEM.potential_elec
            p = self.dataEM.pixel * 10 **(9)
            imagedisplay.ImageDisplay(data_to_display, cal=p)
        if event.key == '4':
            data_to_display = np.sqrt(np.square(self.dataEM.field_elec[0][0]) +
                                      np.square(self.dataEM.field_elec[0][1]))
            p = self.dataEM.pixel * 10 **(9)
            imagedisplay.ImageDisplay(data_to_display, cal=p)
        if event.key == '5':
            data_to_display = self.dataEM.potential_magn
            p = self.dataEM.pixel * 10 **(9)
            imagedisplay.ImageDisplay(data_to_display, cal=p)
        if event.key == '6':
            data_to_display = np.sqrt(np.square(self.dataEM.field_magn[0][0]) +
                                      np.square(self.dataEM.field_magn[0][1]))
            p = self.dataEM.pixel * 10 **(9)
            imagedisplay.ImageDisplay(data_to_display, cal=p)