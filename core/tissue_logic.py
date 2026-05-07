# new version
import numpy as np
from config import PROPERTIES, a_param, n_max, applied_force, voxel_size

def run_bone_simulation_step(bone_grid, force_vec=applied_force, voxel_size=voxel_size):
    """
    bone_grid index map:
    0: Stimulus (S)
    1: Cell Density (n)
    2: Young's Modulus (E)
    3: Permeability (k)
    """
    E_current = bone_grid[:, :, :, 2]
    n = bone_grid[:, :, :, 1]
    
    # --- PART 1: PHYSICS (Force to Strain) ---
    area = voxel_size**2
    sigma = force_vec / area
    nu = 0.3 
    
    eps_x = (1/E_current) * (sigma[0] - nu*(sigma[1] + sigma[2]))
    eps_y = (1/E_current) * (sigma[1] - nu*(sigma[0] + sigma[2]))
    eps_z = (1/E_current) * (sigma[2] - nu*(sigma[1] + sigma[0]))
    
    # --- PART 2: STIMULUS ---
    diff_sq = (eps_x - eps_y)**2 + (eps_y - eps_z)**2 + (eps_z - eps_x)**2
    gamma_oct = (2/3) * np.sqrt(diff_sq)
    S = gamma_oct / a_param # shortened form
    bone_grid[:, :, :, 0] = S

    # --- PART 3: DIFFERENTIATION (Using np.select) ---
    # Define the masks for each tissue type
    conds = [
        (S >= 3.0),                               # Fibrous
        (S >= 1.0) & (S < 3.0),                   # Cartilage
        (S >= 0.01) & (S < 1.0) & (n > 0.8),      # Mature Bone
        (S >= 0.01) & (S < 1.0) & (n <= 0.8),     # Immature Bone
        (S < 0.01)                                # Marrow
    ]
    
    # Define the target values for E and Permeability
    targets_E = [
        PROPERTIES['fibrous']['E'],
        PROPERTIES['cartilage']['E'],
        PROPERTIES['mature_bone']['E'],
        PROPERTIES['immature_bone']['E'],
        PROPERTIES['marrow']['E']
    ]
    
    targets_K = [
        PROPERTIES['fibrous']['perm'],
        PROPERTIES['cartilage']['perm'],
        PROPERTIES['mature_bone']['perm'],
        PROPERTIES['immature_bone']['perm'],
        PROPERTIES['marrow']['perm']
    ]
    
    # np.select matches the condition to the target value across the whole grid
    target_E_grid = np.select(conds, targets_E, default=PROPERTIES['granulation']['E'])
    target_K_grid = np.select(conds, targets_K, default=PROPERTIES['granulation']['perm'])
    
    # --- NEW: PART 3.5: THE PROTECTIVE MASK ---
    # Identify voxels that are already Cortical Bone (E = 20000)
    # We use a threshold of 19000 to be safe
    #is_cortical = bone_grid[:, :, :, 2] >= 19000

    # --- PART 4: RULE OF MIXTURES (With Mask) ---
    # --- PART 4: RULE OF MIXTURES (With Mask) ---
    E_gran = PROPERTIES['granulation']['E']
    K_gran = PROPERTIES['granulation']['perm']
    
    # Calculate the "Target" values the biology is aiming for
    target_new_E = (n / n_max) * target_E_grid + (1 - n/n_max) * E_gran
    target_new_K = (n / n_max) * target_K_grid + (1 - n/n_max) * K_gran
    
    bone_grid[:, :, :, 2] = target_new_E
    bone_grid[:, :, :, 3] = target_new_K
        
    return bone_grid








    ## --- PART 4: RULE OF MIXTURES (Temporal Update) ---
    #E_gran = PROPERTIES['granulation']['E']
    #K_gran = PROPERTIES['granulation']['perm']
    
    # Update E and Permeability based on cell density maturation
    #bone_grid[:, :, :, 2] = (n / n_max) * target_E_grid + (1 - n/n_max) * E_gran
    #bone_grid[:, :, :, 3] = (n / n_max) * target_K_grid + (1 - n/n_max) * K_gran
    
    #return bone_grid)