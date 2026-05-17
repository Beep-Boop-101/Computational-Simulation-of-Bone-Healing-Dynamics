import numpy as np
from config import PROPERTIES, size, gap, frac_cell_density, normal_cell_density


def create_artificial_geometry(size=size, gap=5, frac_cell_density=frac_cell_density, normal_cell_density=normal_cell_density):
    """
    Argument: size: The dimensions of the cubic grid (size x size x size). Default is 50, which creates a 50x50x50 grid. Adjust as needed for testing or higher resolution.

    Creates a cube with two bone segments and a fracture gap.

    The grid is initialized with the following index mapping:
    0: Stimulus (S)
    1: Cell Density (n)
    2: Young's Modulus (E)
    3: Permeability (k)

    The two bone segments are represented as 'cortical bone' with high stiffness and low permeability, while the fracture gap is initialized as 'granulation tissue' with low stiffness and higher permeability.
    The cell density is set to a low value in the fracture gap and a high value in the bone segments to reflect the biological conditions immediately after a fracture.

    Returns:
    A 4D numpy array representing the bone grid with the initialized geometry and properties.

    """
    # Initialize grid: 0:S, 1:n, 2:E, 3:k
    grid = np.zeros((size, size, size, 4))
    
    # Fill the entire grid with 'marrow' or 'granulation' initially
    grid[:, :, :, 2] = PROPERTIES['granulation']['E']   # E = 1 MPa (Granulation)
    grid[:, :, :, 3] = PROPERTIES['granulation']['perm'] # Permeability (Granulation)
    grid[:, :, :, 1] =  frac_cell_density  # Initial cell density
    
    # Define two solid bone blocks (the 'Cortical' segments)
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