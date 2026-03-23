# Computational Simulation of Bone Healing Dynamics: Integrating Mechanical Strain and Cellular Differentiation

## Project Description:

This project's purpose is to simulate in silico bone fracture healing through modeling the mechanobiological interaction between physical stress and cellular regeneration. Using a voxel-based finite element approach, the simulation will track how mesenchymal stem cells migrate to a fracture gap and differentiate into fibrous tissue, cartilage, or bone based on local mechanical strain. The primary goal is to visualize the "healing front" as it moves from the periosteum toward the center of the injury, predicting whether a specific mechanical environment will lead to successful union or a "non-union" failure.

## Numerical Methods:

- **Voxel-based Lattice**:

The physical domain of the bone is represented as a 3D NumPy ndarray, where each element stores a state vector (Density, Young’s Modulus, and Tissue Type).

- **Euler Integration**:

A first-order Forward Euler method will be used to iteratively update bone density (dp/dt) based on the "Lazy Zone" mechanostatic equations.

  
- **Finite Difference Method (FDM)**:

3D Laplacian convolution kernels will solve the Reaction-Diffusion equations for cell migration and Growth Factor (BMP-2) spread to more accurately model how cells an other materials move through bone.
  
- **Spatial Mapping**:

Spatial Mapping: Use of pydicom and PyVista to map Hounsfield Units from CT scans directly into the simulation's starting density values.


## Planned Directory Structure:

```text
.
├── data/
│   ├── raw/                # Original .dcm (DICOM) files
│   └── processed/          # .npy files (serialized NumPy arrays)
├── src/
│   ├── solver.py           # Euler integration & Diffusion logic
│   ├── physics_engine.py   # Strain/Stress calculation per voxel
│   ├── utils.py            # DICOM parsing and Voxelization functions
│   └── visualize.py        # PyVista/Matplotlib scripts for 3D plotting
├── docs/                   # Project proposal and mathematical derivations
├── results/                # Generated heatmaps and 3D growth animations
├── requirements.txt        # numpy, scipy, pydicom, pyvista, numba
└── main.py                 # Entry point for the simulation loop
```

## Resources:


- **Datasets**:

Virtual Skeleton Database (Zenodo) for baseline CT scans; TCIA for fracture-specific DICOMs.

- **Libraries**:

NumPy (Arrays), SciPy (Solvers), PyVista (3D Mesh), pydicom (Medical Data), Numba (Optimization).

## Rough Timeline:

- **Phase 1**:

Setup (March 23 – April 5): DICOM acquisition, Hounsfield-to-Density mapping, and environment setup (pydicom, PyVista).

- **Phase 2**:

Physics Implementation (April 6 – April 17): Develop the strain-calculation engine. 

- **Phase 3**:

Biological Solver (April 18 – April 30): Implement a Decision Tree for changes in bone tissue and Euler integration loops. Add Diffusion kernels for BMP-2.


- **Phase 4**:

Reach Goals & Refinement (May 1 – May 7): Integrate the Angiogenesis layer and optimize with Numba. (Ready for Peer Review on May 7).


- **Phase 5**:

Finalization (May 7 – Final Exam): Final simulation runs, data visualization, and documentation.

## Reach Goals:

- **Reach Goal 1: Angiogenesis & Vascular Coupling (VEGF)**:

I would like to implement a secondary "Vascular" layer where bone mineralization is restricted by blood vessel density. This will use a Deterministic Diffusion model for VEGF; if time permits, a Stochastic Agent-Based Model will be used to simulate realistic capillary branching.

- **Reach Goal 2: Computational Optimization**:

Utilize Numba's @njit compilation to parallelize the voxel-by-voxel calculations, allowing for higher-resolution simulations in shorter time.


### Literature:
1. **Lacroix, D., & Prendergast, P. J. (2002).** A mechano-regulation model for tissue differentiation during fracture healing: analysis of gap size and loading. *Journal of Biomechanics*, 35(9), 1163-1171.
   - *Applied to:* The voxel-based tissue phenotype decision tree.
2. **Komarova, S. V., et al. (2003).** Mathematical model predicts a critical role for osteoclast autocrine regulation in the control of bone remodeling. *Bone*, 33(2), 206-215.
   - *Applied to:* The ODE cellular dynamics of osteoblasts and osteoclasts.



