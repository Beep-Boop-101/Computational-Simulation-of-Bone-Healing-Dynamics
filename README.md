# Computational Simulation of Bone Healing Dynamics: Integrating Mechanical Strain and Cellular Differentiation

## Project Description:

This project's purpose is to simulate in silico bone fracture healing through modeling the mechanobiological interaction between physical stress and cellular regeneration. Using a Lattice-based Bone Map, the simulation tracks mesenchymal stem cells migrate to a fracture gap. These cells can then differentiate into fibrous tissue, cartilage, or bone based on local mechanical strain. The primary goal is to visualize the "healing front" as it moves from the edges of the fracture toward the center of the injury, predicting whether a specific mechanical environment will lead to successful union or a "non-union" failure.

## Numerical Methods:

- **Voxel-based Lattice**:

The physical domain of the bone is represented as a 3D NumPy ndarray, where each element stores a state vector (stimulus, cell density, young's modulus, and permitivity).

- **Euler Integration**:

A first-order update method is used to iteratively evolve the Young’s Modulus toward a target phenotype based on the calculated stimulus. Avoids bone suddenly "appearing" out of nowhere.
  
- **Finite Difference Method (FDM)**:

dn/dt is calculated as the 3D Laplacian of the cell density which will be calculated using scipy.ndimage.laplace which solves for the laplacian of cell density.

## Directory Structure:

The project is organized into a modular structure to separate simulation logic, configuration, and utility functions:

```text
.
├── core/                        # Core simulation logic
│   ├── __init__.py              # Makes the directory a Python package
│   ├── cell_logic.py            # Cell diffusion and migration (laplace operator)
│   └── tissue_logic.py          # Mechano-regulation and differentiation logic
├── data/                        # Data storage
│   ├── processed/               # Cleaned or final simulation outputs
│   └── raw/                     # Initial conditions or external data
├── results/                     # Directory for saved plots and snapshots
├── utils/                       # Helper functions
│   ├── __init__.py              # Makes the directory a Python package
│   ├── generation.py            # Functions to create artificial bone geometry
│   └── visualize.py             # Matplotlib logic for temporal healing plots
├── config.py                    # Central configuration (properties, forces, constants)
├── main.py                      # Main entry point; runs the simulation loop
├── README.md                    # Project documentation and overview
├── requirements.txt             # List of required Python libraries
└── .gitignore                   # Files and folders for Git to ignore (e.g., __pycache__)
```
## important modules

*cell_logic.py*

Handles cell diffusion throughout fracture. Is where laplacian is calculated

*tissue_logic.py*

Handles calculation of stimulation due to applied force and subsequent change in Young's modulus of bone in fracture.

*generation.py*

Handles generation of artificial bone geometery.


## Further building

If the user wants to store the bone grid at any given time step, there is a results section which these can be saved to. additionally, there is a raw and processed data section for the storage of scan data if one wants to try using this code on a more complicated geometry like a CT scan. An example scan would be included, but it is too much data to upload.


## Resources:

- **Libraries**:

NumPy (Arrays), SciPy (Solvers), Matplot lib (Graphing)

If trying to use external geometries, like from a CT, 3D Slicer is used to generate the mesh and is saved.

## Usage guide

To run the simulation, you just need to run the main.py module.

If you want to modify anything about the simulation, you only need to look in the config and the main files. All the modulus are built around config so that they do not define any constants locally. If you change anything about the structure of the package, make sure the imports from config are still intact so that there are no missing values (I would recommend just keeping my structure).

Make sure to have numpy, matplotlib, and scipy pip installed before running. you could run this to do that 
"pip install numpy matplotlib scipy".

Be carful about modifying constants like D, alpha, and the applied force. The simulation is very sensitive to these constants. The force is an especially sensitive constant.

Be careful about running this simulations on a personal laptop, unless you enjoy the sound of your cooling fans trying to achieve lift-off. The simulation is very memory intensive and it could be very demanding depending on your device.

You may see some sections of the code that are commented out. Most of these are pieces of code I am hoping I will be able to implement later, if possible.

At the moment, I am using a "brick" of artificially generated bone for tests of the simulation. If you want to make any changes in this regard, that would be in the utils.generation module.

### Literature:
1. **Lacroix, D., & Prendergast, P. J. (2002).** A mechano-regulation model for tissue differentiation during fracture healing: analysis of gap size and loading. *Journal of Biomechanics*, 35(9), 1163-1171.
   - *Applied to:* The voxel-based tissue phenotype decision tree.
2. **Komarova, S. V., et al. (2003).** Mathematical model predicts a critical role for osteoclast autocrine regulation in the control of bone remodeling. *Bone*, 33(2), 206-215.
   - *Applied to:* The ODE cellular dynamics of osteoblasts and osteoclasts.
3. **R. HUISKES*, W. D., & Prendergast, P. J. (1997).** A biomechanical regulatory model for periprosthetic fibrous-tissue differentiation. *Journal of Material Science*, 8, 785–788.
