import numpy as np
from config import PROPERTIES, size, frac_cell_density, normal_cell_density


def create_artificial_geometry(size=size):
    """
    Creates a 50x50x50 cube with two bone segments and a 5-voxel fracture gap.
    """
    # Initialize grid: 0:S, 1:n, 2:E, 3:k
    grid = np.zeros((size, size, size, 4))
    
    # Fill the entire grid with 'marrow' or 'granulation' initially
    grid[:, :, :, 2] = PROPERTIES['granulation']['E']   # E = 1 MPa (Granulation)
    grid[:, :, :, 3] = PROPERTIES['granulation']['perm'] # Permeability (Granulation)
    grid[:, :, :, 1] =  frac_cell_density  # Initial cell density
    
    # Define two solid bone blocks (the 'Cortical' segments)
    center = size // 2
    radius = size // 4
    gap_middle = size // 2
    gap_half_width = 2 # Total gap of 5 voxels
    
    for z in range(size):
        # Skip the gap area to leave it as granulation tissue
        if gap_middle - gap_half_width <= z <= gap_middle + gap_half_width:
            continue # This creates the 5-voxel gap in the middle
        for x in range(size):
            for y in range(size):
                grid[x, y, z, 2] = PROPERTIES['cortical_bone']['E']   # Cortical Bone E
                grid[x, y, z, 3] = PROPERTIES['cortical_bone']['perm']  # Cortical Bone Perm
                grid[x, y, z, 1] =  normal_cell_density   # Fully populated with cells
                    
    return grid