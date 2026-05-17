import numpy as np  
from scipy.ndimage import laplace
from config import D, dt

def update_cell_diffusion(bone_data, D=D, dt=dt):
    '''
    Argument: bone_data: A 4D numpy array representing the current state of the bone grid.

    Updates the cell density (n) in the bone grid based on diffusion and boundary source logic.
    The function takes the current bone data grid, applies diffusion to the cell density, and then updates the grid with the new cell density values.

    Returns: A 4D numpy array representing the updated bone grid with the new cell density values.

    '''

    n = bone_data[:, :, :, 1]
    
    # Standard diffusion calculation
    dn_dt = D * laplace(n)
    n_new = n + dn_dt * dt
    
    # --- NEW: Boundary Source Logic ---
    # Set the outer "shell" of the 50x50x50 cube as a constant source
    #n_new[0, :, :] = 1.0  # Left face
    #n_new[-1, :, :] = 1.0 # Right face
    #n_new[:, 0, :] = 1.0  # Front face
    #n_new[:, -1, :] = 1.0 # Back face
    
    bone_data[:, :, :, 1] = n_new
    return bone_data