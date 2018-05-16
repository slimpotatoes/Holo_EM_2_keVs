import gui as gui
import data as data
import inputfiles as inputfiles
import phase as phase
import refine as refine
import field as field
import alignholo as alignholo
import matplotlib.pyplot as plt


def main():

    def input_files(event):
        if not event.inaxes == emgui.event_input.ax:
            raise Exception('Improper input axis')
        file_path_holo_1, file_path_holo_2, file_path_holo_ref = emgui.open_files()
        inputfiles.load_files(file_path_holo_1, file_path_holo_2, file_path_holo_ref, emdata)
        print('Files Loaded')

    def align_holograms(event):
        if not event.inaxes == emgui.event_align.ax:
            raise Exception('Improper axis')
        emgui.align_holo()

    def ft(event):
        if not event.inaxes == emgui.event_ft.ax:
            raise Exception('Improper axis')
        alignholo.deform_image(emgui.fig_align.scale, emgui.fig_align.rotation,
                               emgui.fig_align.shear, emgui.fig_align.translation, emdata)
        emgui.mask_holo()

    def phase_calc(event):
        if not event.inaxes == emgui.event_phase.ax:
            raise Exception('Improper axis')
        print(emgui.circle_1.artist.radius)
        print(emgui.circle_1.artist.center)
        phase.phase(emgui.circle_1.artist.center, emgui.circle_1.artist.radius,
                    emgui.circle_2.artist.center, emgui.circle_2.artist.radius, emdata)
        emgui.phase_holo()

    def refine_calc(event):
        if not event.inaxes == emgui.event_refine.ax:
            raise Exception('Improper axis')
        u = emgui.reference_extract(emgui.rect.rectangle)
        refine.update_ref(u, emdata)
        emgui.refine_gui()

    def field_calc(event):
        if not event.inaxes == emgui.event_field.ax:
            raise Exception('Improper axis')
        field.fields(emdata)
        emgui.field_gui()

    emdata = data.EMdata()
    emgui = gui.HoloEMgui(emdata)

    emgui.flow()

    emgui.event_input.on_clicked(input_files)
    emgui.event_align.on_clicked(align_holograms)
    emgui.event_ft.on_clicked(ft)
    emgui.event_phase.on_clicked(phase_calc)
    emgui.event_refine.on_clicked(refine_calc)
    emgui.event_field.on_clicked(field_calc)

    plt.show()


if __name__ == "__main__":
    main()
