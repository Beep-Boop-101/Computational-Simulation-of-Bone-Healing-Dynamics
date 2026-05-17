import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
import numpy as np

def create_interactive_slicer(history, days_logged):
    # Enable a clean, modern aesthetic base
    plt.style.use('dark_background')
    
    # Track states
    curr_slice_idx = history[0].shape[0] // 2
    
    # 1. Calculate History-over-Time for a point right in the middle of the fracture gap
    # Assuming center voxel coordinates [mid_x, mid_y, mid_z]
    mid_x = history[0].shape[0] // 2
    mid_y = history[0].shape[1] // 2
    mid_z = history[0].shape[2] // 2
    
    # Extract structural progression over time at that explicit point
    density_over_time = [grid[mid_x, mid_y, mid_z, 1] for grid in history]
    stiffness_over_time = [grid[mid_x, mid_y, mid_z, 2] for grid in history]
    
    # --- UI & CANVAS CREATION ---
    fig, (ax_img, ax_graph) = plt.subplots(1, 2, figsize=(14, 8), gridspec_kw={'width_ratios': [1.2, 1]})
    plt.subplots_adjust(left=0.22, bottom=0.25, wspace=0.3)
    
    # Stylize the Main Figure Window background color
    fig.patch.set_facecolor('#121212')
    for ax in [ax_img, ax_graph]:
        ax.set_facecolor('#1e1e1e')

    def get_slice_data(day_idx, s_idx, axis, mode):
        grid = history[day_idx]
        if axis == 0: return grid[s_idx, :, :, mode]   # Sagittal (X)
        if axis == 1: return grid[:, s_idx, :, mode]   # Coronal (Y)
        return grid[:, :, s_idx, mode]                 # Axial (Z)

    # --- INITIAL RENDER ---
    # Left Side: Slicer Image
    img = ax_img.imshow(get_slice_data(0, curr_slice_idx, 2, 1), cmap='viridis', vmin=0, vmax=1)
    cb = fig.colorbar(img, ax=ax_img, shrink=0.7)
    cb.set_label("Cell Density (n)", color='#ffffff', fontsize=10)
    ax_img.set_title(f"Day {days_logged[0]} | Axial Slice {curr_slice_idx}", color='#00ffcc', fontsize=12, pad=12)
    ax_img.axis('off') # Hides unnecessary structural image borders

    # Right Side: Mechanical Over-Time Graph
    ax_graph.set_title("Biomechanical Healing Progress\n(Fracture Gap Center Over Time)", color='#00ffcc', fontsize=12, pad=12)
    ax_graph.set_xlabel("Simulation Days", color='#888888')
    ax_graph.set_ylabel("Cell Density", color='#ffffff')
    ax_graph.grid(True, linestyle='--', alpha=0.15)
    
    # Plot initial point tracker marker & time series line
    line_plot, = ax_graph.plot(days_logged, density_over_time, color='#00ffcc', linewidth=2, label='Density Tracker')
    time_marker, = ax_graph.plot([days_logged[0]], [density_over_time[0]], color='#ff3366', marker='o', markersize=8)

    # --- WIDGETS DESIGN & PLACEMENT ---
    # Slider Styles
    slider_bg = '#2a2a2a'
    slider_fill = '#00ffcc'

    ax_day = plt.axes([0.30, 0.12, 0.45, 0.025], facecolor=slider_bg)
    s_day = Slider(ax_day, 'Day Index', 0, len(days_logged)-1, valinit=0, valfmt='%d', color=slider_fill)
    s_day.label.set_color('#ffffff')

    ax_slice = plt.axes([0.30, 0.06, 0.45, 0.025], facecolor=slider_bg)
    s_slice = Slider(ax_slice, 'Voxel Slice', 0, history[0].shape[0]-1, valinit=curr_slice_idx, valfmt='%d', color=slider_fill)
    s_slice.label.set_color('#ffffff')

    # Radio Button Styles
    radio_bg = '#1e1e1e'
    ax_data = plt.axes([0.03, 0.6, 0.14, 0.15], facecolor=radio_bg)
    radio_data = RadioButtons(ax_data, ('Cell Density', 'Stiffness (E)'), activecolor=slider_fill)
    for label in radio_data.labels: label.set_color('#ffffff')

    ax_axis = plt.axes([0.03, 0.35, 0.14, 0.15], facecolor=radio_bg)
    radio_axis = RadioButtons(ax_axis, ('Axial (Z)', 'Sagittal (X)', 'Coronal (Y)'), activecolor=slider_fill)
    for label in radio_axis.labels: label.set_color('#ffffff')

    # --- UPDATE INTERACTION LOGIC ---
    def update(val):
        d_idx = int(s_day.val)
        sl_idx = int(s_slice.val)
        
        is_stiffness = radio_data.value_selected == 'Stiffness (E)'
        mode = 2 if is_stiffness else 1
        
        label = radio_axis.value_selected
        axis = 2 if 'Z' in label else (0 if 'X' in label else 1)
        
        # A. Update Slicer Plane View 
        img.set_data(get_slice_data(d_idx, sl_idx, axis, mode))
        
        # B. Dynamically Scale Colors and Graph context based on Active Feature Mode
        if is_stiffness:
            img.set_cmap('magma') # More subtle/polished than raw 'jet'
            img.set_clim(1, 6000)
            cb.set_label("Stiffness E (MPa)", color='#ffffff')
            
            # Switch live graph content to stiffness data tracking
            line_plot.set_ydata(stiffness_over_time)
            line_plot.set_color('#ffaa00')
            time_marker.set_data([days_logged[d_idx]], [stiffness_over_time[d_idx]])
            
            ax_graph.set_ylabel("Stiffness E (MPa)", color='#ffffff')
            ax_graph.set_ylim(-100, 6500)
        else:
            img.set_cmap('viridis')
            img.set_clim(0, 1)
            cb.set_label("Cell Density (n)", color='#ffffff')
            
            # Switch live graph content back to density data tracking
            line_plot.set_ydata(density_over_time)
            line_plot.set_color('#00ffcc')
            time_marker.set_data([days_logged[d_idx]], [density_over_time[d_idx]])
            
            ax_graph.set_ylabel("Cell Density", color='#ffffff')
            ax_graph.set_ylim(-0.05, 1.05)

        ax_img.set_title(f"Day {days_logged[d_idx]} | {label} {sl_idx}", color='#00ffcc', fontsize=12)
        fig.canvas.draw_idle()

    s_day.on_changed(update)
    s_slice.on_changed(update)
    radio_data.on_clicked(update)
    radio_axis.on_clicked(update)

    plt.show()