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
gap = 5                     # Number of voxels representing the fracture gap (total width)

# --- Normal Bone Properties ---
normal_bone_E = 20000        # MPa, Young's modulus for cortical bone
normal_bone_perm = 1e-17     # m^2, permeability for cortical
normal_cell_density = 1.0       # Fully populated with cells (0 to 1 scale)

# --- SIMULATION CONFIGURATION ---
size = 50           # Grid dimensions (50x50x50). Runtime is very dependent on this value. Adjust as needed for testing or higher resolution.
voxel_size = 1.0    # 1mm voxels
num_days = 112        # Total simulation time in days
num_hours = num_days * 24       # Simulation duration in hours
save_interval = 1  # How often to take a snapshot for the visualizer. 1 means each day.


# Applied Force: We will simulate gradual loading during healing by increasing the applied force over time to reflect the natural process of weight-bearing and rehabilitation.

applied_force = np.array([0, 0, 0], dtype=float)  # Initial force vector (Fx, Fy, Fz) in Newtons. We will update the components during the simulation to simulate loading during healing.

#___ Loading and Activity Pattern Constants ___

low_force = -0.15  # N, representing the initial rest period immediately after a fracture (e.g., during sleep or immobilization)
early_healing_force = -10  # N, representing the moderate force during the early healing phase when the patient starts to bear weight
mid_healing_force = -80  # N, representing the increased force during the mid-healing phase as the patient becomes more active
late_healing_force = -110  # N, representing the higher force during the late healing phase as the bone regains strength and the patient returns to normal activities

# ___ Movement constants ___
D = 10  # Diffusion coefficient for cell migration (arbitrary units)
dt = 1.0/24   # Time step for the simulation (1 hour in days)

# ___ Differentiation update constant ___
alpha = 0.0027  # How quickly the tissue properties update towards the target values (0 < alpha <= 1, where 1 means instant update). Prevents sudden jumps in E and permeability, creating a more gradual healing process.
                # calibrated to allow for a realistic healing timeline of around 3-4 months in the simulation, which matches clinical observations of bone healing in humans.