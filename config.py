# Fracture healing simulation configuration file

import numpy as np

# --- TISSUE PROPERTIES ---
PROPERTIES = {
    'cortical_bone': {'E': 20000, 'perm': 1e-17,  'nu': 0.3},
    'mature_bone':   {'E': 6000,  'perm': 3.7e-13, 'nu': 0.3},
    'immature_bone': {'E': 1000,  'perm': 1e-13,   'nu': 0.3},
    'marrow':        {'E': 2,     'perm': 1e-14,   'nu': 0.17},
    'cartilage':     {'E': 10,    'perm': 5e-15,   'nu': 0.17},
    'fibrous':       {'E': 2,     'perm': 1e-14,   'nu': 0.17},
    'granulation':   {'E': 1,     'perm': 1e-14,   'nu': 0.17}
}

a_param = 0.0375  
n_max = 1.0     

# --- Fracture Properties ---

frac_youngs_modulus = 1.0  # MPa, for the initial granulation tissue in the fracture gap
frac__permeability = 1e-14    # m^2, for the initial granulation tissue in the fracture gap
frac_cell_density = 0.1      # Initial cell density in the fracture gap (0 to 1 scale)

# --- Normal Bone Properties ---
normal_bone_E = 20000        # MPa, Young's modulus for cortical bone
normal_bone_perm = 1e-17     # m^2, permeability for cortical
normal_cell_density = 1.0       # Fully populated with cells (0 to 1 scale)

# --- SIMULATION CONFIGURATION ---
size = 50           # Grid dimensions (50x50x50)
voxel_size = 1.0    # 1mm voxels
num_days = 150       # Simulation duration
save_interval = 20  # How often to take a snapshot for the visualizer


# Applied Force: Using 2.5 N to keep Stimulus (S) in the healing range

applied_force = np.array([0, 0, -2.5])

# ___ Movement constants ___
D = 0.45  # Diffusion coefficient for cell migration (arbitrary units)
dt = 1.0   # Time step for the simulation (1 day)
