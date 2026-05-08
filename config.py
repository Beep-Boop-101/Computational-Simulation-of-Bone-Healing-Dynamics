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
size = 50           # Grid dimensions (50x50x50). Runtime is very dependent on this value. Adjust as needed for testing or higher resolution.
voxel_size = 1.0    # 1mm voxels
num_hours = 112 * 24       # Simulation duration in hours (112 days)
save_interval = 24  # How often to take a snapshot for the visualizer. 1 means every hour, 24 means every day, etc.


# Applied Force: We will simulate gradual loading during healing by increasing the applied force over time to reflect the natural process of weight-bearing and rehabilitation. The force will start low to represent the initial rest period after a fracture and will gradually increase to simulate the patient beginning to bear weight on the healing bone.

applied_force = np.array([0, 0, -0.15])  # Initial force vector (Fx, Fy, Fz) in Newtons. We will update the components during the simulation to simulate loading during healing.

# ___ Movement constants ___
D = 10  # Diffusion coefficient for cell migration (arbitrary units)
dt = 1.0/24   # Time step for the simulation (1 hour in days)

# ___ Differentiation update constant ___
alpha = 0.005  # How quickly the tissue properties update towards the target values (0 < alpha <= 1, where 1 means instant update). Prevents sudden jumps in E and permeability, creating a more gradual healing process.

# Body weight and force growth rate for simulating gradual loading during healing. Not used in the current implementation but can potentially be used to more accurately calculate the rate of increase in applied force over time to simulate rehabilitation and weight-bearing during the healing process.
body_weight = 0.05  # Newtons Approximate weight of the limb being simulated on the bone segment. Adjust as needed for different scenarios (e.g., upper limb vs lower limb).

rate_force_growth = body_weight / (num_hours / 24) # How much the applied force increases each day to simulate gradual loading during healing. Adjust as needed for different healing scenarios.