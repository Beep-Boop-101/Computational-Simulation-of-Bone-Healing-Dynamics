import numpy as np
from scipy.ndimage import laplace

PROPERTIES = {
    'cortical_bone': {'E': 20000 , 'perm': 1e-17, 'nu': 0.3},
    'mature_bone': {'E': 6000, 'perm': 3.7e-13, 'nu': 0.3},
    'immature_bone': {'E': 1000, 'perm': 1e-13, 'nu': 0.3},
    'marrow': {'E': 2, 'perm': 1e-14,'nu': 0.17},
    'cartilage': {'E': 10, 'perm': 5e-15, 'nu': 0.17},
    'fibrous': {'E': 2, 'perm': 1e-14, 'nu': 0.17},
    'granulation': {'E': 1, 'perm': 1e-14, 'nu': 0.17}
}
# units are in MPa for Young's modulus, m^4/(Ns) for permeability, and dimensionless for Poisson's ratio

n_max = 1.0  # Max cell concentration

n_min = 0.01  # Min cell concentration
def update_material_properties(bone_grid, strain_tensors, a=0.0375):
    """
    bone_grid: [10,10,10, 3] -> Index 0: Stimulus, 1: Cell Density, 2: Young's Modulus
    strain_tensors: [10,10,10, 3, 3] -> The full 3x3 strain matrix for each voxel
    """
    # 1. Calculate Octahedral Strain and Stimulus
    # We iterate through the grid (or use vectorized linalg if performance is key)
    for i in range(10):
        for j in range(10):
            for k in range(10):
                # Get eigenvalues (Principal Strains)
                e = np.linalg.eigvalsh(strain_tensors[i,j,k])
                
                # Equation: gamma_oct = 2/3 * sqrt(sum of squared differences)
                diff_sq = (e[0]-e[1])**2 + (e[1]-e[2])**2 + (e[2]-e[0])**2
                gamma_oct = (2/3) * np.sqrt(diff_sq)
                
                # Stimulus S
                S = gamma_oct / a
                bone_grid[i,j,k, 0] = S
                
                # 2. Tissue Differentiation Decision
                # Only differentiate if cell density (n) is high enough (e.g. > 0.8)
                n = bone_grid[i,j,k, 1]
                if n > 0.8:
                    if S < 1:
                        target_E = PROPERTIES['bone']['E']
                        target_nu = PROPERTIES['bone']['nu']
                    elif 1 <= S < 3:
                        target_E = PROPERTIES['cartilage']['E']
                        target_nu = PROPERTIES['cartilage']['nu']
                    else: # S >= 3
                        target_E = PROPERTIES['fibrous']['E']
                        target_nu = PROPERTIES['fibrous']['nu']
                    
                    # 3. Rule of Mixtures (Temporal Smoothing)
                    # We blend the current E with the target E to represent maturation
                    # E_new = (1-n)*E_gran + n*E_target
                    current_E = bone_grid[i,j,k, 2]
                    alpha = 0.1 # Maturation rate constant
                    new_E = current_E + alpha * (target_E - current_E)
                    
                    bone_grid[i,j,k, 2] = new_E
                    
    return bone_grid

def calculate_shear_modulus(E, nu):
    """
    Justification: G is required for the next time step's stiffness matrix.
    G = E / (2 * (1 + nu))
    """
    return E / (2 * (1 + nu))