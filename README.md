# Computational Simulation of Bone Healing Dynamics: Integrating Mechanical Strain and Cellular Differentiation

## Project Description
This project simulates *in silico* bone fracture healing by modeling the mechanobiological interaction between physical stress and cellular regeneration. Using a Lattice-based Bone Map, the simulation tracks the migration of mesenchymal stem cells into a fracture gap. These cells differentiate into fibrous tissue, cartilage, or bone based on local mechanical strain profiles. 

The primary goal is to visualize the "healing front" as it moves from the intact cortical edges of the fracture toward the center of the injury, predicting whether a specific mechanical loading environment will lead to a successful union or a "non-union" clinical failure.

## Numerical Methods

- **Voxel-based Lattice**: 
  The physical domain of the bone is represented as a 3D NumPy `ndarray`, where each element stores a structural state vector: `[Stimulus (S), Cell Density (n), Young's Modulus (E), Permeability (k)]`.
  
- **Euler Integration**: 
  A first-order update method is used to iteratively evolve the Young’s Modulus ($E$) and Permeability ($k$) toward a target biological phenotype based on calculated mechanical stimulus. This creates a realistic, gradual stabilization process rather than tissue instantly appearing.
  
- **Finite Difference Method (FDM)**: 
  The rate of change of cellular concentration over time ($\partial n/\partial t$) is modeled as a 3D Laplacian of cell density, computed efficiently using `scipy.ndimage.laplace`.

---

## Directory Structure
The project is organized into a modular structure to separate simulation physics, biological logic, configuration, and utility functions:

```text
.
├── core/                        # Core simulation mechanics
│   ├── __init__.py              # Declares directory as a Python package
│   ├── cell_logic.py            # Cell diffusion and migration (Laplace operator)
│   └── tissue_logic.py          # Mechano-regulation and differentiation decision trees
├── data/                        # Medical image & data storage
│   ├── processed/               # Cleaned or final simulation outputs (e.g., STL/VTK)
│   └── raw/                     # Initial conditions or external clinical scan profiles
├── results/                     # Directory for saved plots and visualization snapshots
├── tests/                       # Automated validation protocols
│   ├── __init__.py              # Declares directory as a Python package
│   └── test_simulation.py       # Unit tests verifying structural math and matrices
├── utils/                       # Secondary helper scripts
│   ├── __init__.py              # Declares directory as a Python package
│   ├── generation.py            # Generates artificial, cubic cortical bone geometries
│   └── visualize.py             # Matplotlib GUI logic for interactive 4D timeline slicing
├── config.py                    # Central configuration (properties, forces, time steps)
├── LICENSE                      # Project open-source distribution terms (BSD License)
├── main.py                      # Main simulation loop entry point
├── README.md                    # System documentation and project overview
└── requirements.txt             # Mandatory environment external dependencies
```

## Core Program Modules

core/cell_logic.py: Handles cell diffusion throughout the fracture gap using finite difference methods.

core/tissue_logic.py: Computes octahedral shear strains from applied loads to update localized Young's Moduli of the bone voxels.

utils/generation.py: Initializes the starting geometric domain consisting of two rigid bone blocks separated by a granulation tissue fracture gap. Good for easy testing. 

## Further Structural Building & Imaging Data

If a user wishes to store the structural state at any given step, snapshots can be logged inside the results/ folder. Additionally, the data/raw/ and data/processed/ folders can accept scanned geometries (such as segmentations from human CT scans). For complex geometries, 3D Slicer can be utilized to generate compatible mesh formats which will require conversion of pixel density into Young's modulus.

## System Performance Note

The simulation updates 4-dimensional attributes over a 50×50×50 matrix space as standard. Because it recalculates finite-difference physics explicitly for every simulated hour over multiple months, the loop is computationally intensive. Expect high CPU and memory utilization on personal laptops during long execution timelines.


## Resources:

- **Libraries**:

NumPy (Arrays), SciPy (Solvers), Matplot lib (Graphing)

If trying to use external geometries, like from a CT, 3D Slicer is used to generate the mesh and can be saved in processed data.

## Usage guide

To execute the core simulation loop and open the dynamic, interactive slicer GUI dashboard:
run in terminal "python main.py"

All major numerical parameters are bound globally to config.py to prevent local hardcoding. You can modify things like the diffusion coefficient D, the material convergence factor alpha, or the day night loading parameters by altering their values inside config.py.

Caution: The mechanobiological decision trees are highly sensitive to variations in constants like D, alpha, and the applied force. They have been calibrated to model general bone healing over 3-4 months.

Install all external package dependencies using the central requirements file:
run in terminal "pip install -r requirements.txt"

## Expected Output

```text
Initializing geometry...
Starting simulation for 112 days...
Day 0: Applied Force = -0.15 N
Day 1: Applied Force = -0.15 N
...
Day 30: Applied Force = -10 N
...
Day 60: Applied Force = -80 N
...
Simulation complete. Rendering temporal progression...
```
Upon completion, a 2-panel GUI will render showing interactive slice cross-sections coupled with a real-time biomechanical timeline graph tracing the core of the fracture gap.

## Verification & Unit Testing

To run the automated validation tests checking that geometry initialization, zero-loading configurations, and cell boundary parameters remain correct:
run in terminal "python -m unittest discover tests"

 **Expected Output**

```text
...
----------------------------------------------------------------------
Ran 3 tests in 0.002s

OK
```

## Report Location

This project is part of the final assignment for the Numerical Methods course I am taking at Adelphi University. For my Professor when they read this, the final report can be found in "Numerical Methods (Project Report).ipynb" file.

### Literature:
1. **Lacroix, D., & Prendergast, P. J. (2002).** A mechano-regulation model for tissue differentiation during fracture healing: analysis of gap size and loading. *Journal of Biomechanics*, 35(9), 1163-1171.
   - *Applied to:* The voxel-based tissue phenotype decision tree.
2. **Komarova, S. V., et al. (2003).** Mathematical model predicts a critical role for osteoclast autocrine regulation in the control of bone remodeling. *Bone*, 33(2), 206-215.
   - *Applied to:* The ODE cellular dynamics of osteoblasts and osteoclasts.
3. **R. HUISKES*, W. D., & Prendergast, P. J. (1997).** A biomechanical regulatory model for periprosthetic fibrous-tissue differentiation. *Journal of Material Science*, 8, 785–788.
