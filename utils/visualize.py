import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
import numpy as np
from matplotlib.widgets import Slider, RadioButtons

def create_interactive_slicer(history, days_logged):
    curr_day_idx = 0
    curr_slice_idx = history[0].shape[0] // 2
    curr_mode = 1  # 1: Density, 2: Stiffness
    curr_axis = 2  # Default: Axial (Z)

    fig, ax = plt.subplots(figsize=(10, 8))
    plt.subplots_adjust(left=0.25, bottom=0.25)

    def get_slice_data(day_idx, s_idx, axis, mode):
        grid = history[day_idx]
        if axis == 0: return grid[s_idx, :, :, mode]   # Sagittal (X)
        if axis == 1: return grid[:, s_idx, :, mode]   # Coronal (Y)
        return grid[:, :, s_idx, mode]                 # Axial (Z)

    # Initial plot
    img = ax.imshow(get_slice_data(0, curr_slice_idx, 2, 1), cmap='viridis', vmin=0, vmax=1)
    cb = fig.colorbar(img, ax=ax)
    ax.set_title(f"Day {days_logged[0]} | Axial Slice {curr_slice_idx}")

    # --- WIDGETS ---
    ax_day = plt.axes([0.35, 0.1, 0.45, 0.03])
    s_day = Slider(ax_day, 'Day Index', 0, len(days_logged)-1, valinit=0, valfmt='%d')

    ax_slice = plt.axes([0.35, 0.05, 0.45, 0.03])
    s_slice = Slider(ax_slice, 'Voxel Slice', 0, history[0].shape[0]-1, valinit=curr_slice_idx, valfmt='%d')

    ax_data = plt.axes([0.05, 0.6, 0.15, 0.15])
    radio_data = RadioButtons(ax_data, ('Cell Density', 'Stiffness (E)'))

    ax_axis = plt.axes([0.05, 0.35, 0.15, 0.15])
    radio_axis = RadioButtons(ax_axis, ('Axial (Z)', 'Sagittal (X)', 'Coronal (Y)'))

    def update(val):
        d_idx = int(s_day.val)
        sl_idx = int(s_slice.val)
        
        # Determine Data Mode
        is_stiffness = radio_data.value_selected == 'Stiffness (E)'
        mode = 2 if is_stiffness else 1
        
        # Determine Plane
        label = radio_axis.value_selected
        axis = 2 if 'Z' in label else (0 if 'X' in label else 1)
        
        # Update Image
        img.set_data(get_slice_data(d_idx, sl_idx, axis, mode))
        
        if is_stiffness:
            img.set_cmap('jet')
            img.set_clim(1, 8000)
            cb.set_label("E (MPa)")
        else:
            img.set_cmap('viridis')
            img.set_clim(0, 1)
            cb.set_label("Cell Density (n)")

        ax.set_title(f"Day {days_logged[d_idx]} | {label} {sl_idx}")
        fig.canvas.draw_idle()

    s_day.on_changed(update)
    s_slice.on_changed(update)
    radio_data.on_clicked(update)
    radio_axis.on_clicked(update)

    plt.show()