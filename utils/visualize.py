import numpy as np
import matplotlib.pyplot as plt

def plot_healing_over_time(history, days_logged, slice_idx=None):
    """
    Plots a 2-row grid: 
    Top Row: Cell Density (n)
    Bottom Row: Young's Modulus (E)
    """
    num_snaps = len(history)
    # Create 2 rows (one for n, one for E)
    fig, axes = plt.subplots(2, num_snaps, figsize=(num_snaps * 3, 7))
    
    if slice_idx is None:
        slice_idx = history[0].shape[2] // 2

    for i, grid in enumerate(history):
        # --- ROW 1: CELL DENSITY (Index 1) ---
        n_data = grid[:, slice_idx, :, 1] 
        im_n = axes[0, i].imshow(n_data, cmap='viridis', vmin=0, vmax=1.0)
        axes[0, i].set_title(f"Day {days_logged[i]}\nCell Density", fontsize=10)
        axes[0, i].axis('off')
        
        # --- ROW 2: YOUNG'S MODULUS (Index 2) ---
        e_data = grid[:, slice_idx, :, 2]
        # Use vmin/vmax to see the healing gap clearly against the 20,000MPa bone
        im_e = axes[1, i].imshow(e_data, cmap='jet', vmin=1)
        axes[1, i].set_title(f"Young's Modulus", fontsize=10)
        axes[1, i].axis('off')
        
    # Add colorbars for each row
    fig.subplots_adjust(right=0.9)
    cbar_ax_n = fig.add_axes([0.92, 0.55, 0.015, 0.35])
    fig.colorbar(im_n, cax=cbar_ax_n, label="Cell Density (n)")
    
    cbar_ax_e = fig.add_axes([0.92, 0.1, 0.015, 0.35])
    fig.colorbar(im_e, cax=cbar_ax_e, label="E (MPa)")

    plt.suptitle(f"Healing Progression at Z-Slice {slice_idx} (Top: n, Bottom: E)", fontsize=14)
    plt.show()