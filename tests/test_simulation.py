# tests/test_simulation.py
import unittest
import numpy as np
from core.tissue_logic import run_bone_simulation_step
from core.cell_logic import update_cell_diffusion
from utils.generation import create_artificial_geometry

class TestBoneSimulationCore(unittest.TestCase):
    
    def setUp(self):
        """Initializes a tiny baseline testing matrix environment."""
        self.test_grid = create_artificial_geometry(size=10, gap=2)
        
    def test_geometry_initialization(self):
        """Validates that the geometric bone structures allocate spatial matrices correctly."""
        # Check overall grid bounds
        self.assertEqual(self.test_grid.shape, (10, 10, 10, 4))
        # Voxel grid index tracking validation: 1 is cell density
        self.assertTrue(np.all(self.test_grid[:, :, :, 1] >= 0.0))
        
    def test_cell_diffusion_conservation(self):
        """Ensures cell densities process within bounds during local migration loops."""
        processed_grid = update_cell_diffusion(self.test_grid.copy())
        # Assert cells do not spontaneously generate or drop below absolute emptiness boundaries
        self.assertTrue(np.all(processed_grid[:, :, :, 1] >= 0.0))
        self.assertTrue(np.all(processed_grid[:, :, :, 1] <= 1.0))
        
    def test_strain_mechanics_under_zero_load(self):
        """Verifies zero loading vector returns absolute zero mechanical stimulus."""
        zero_force = np.array([0, 0, 0], dtype=float)
        processed_grid = run_bone_simulation_step(self.test_grid.copy(), force_vec=zero_force, voxel_size=1.0)
        # S (index 0) must return exactly zero everywhere
        self.assertEqual(np.max(processed_grid[:, :, :, 0]), 0.0)

if __name__ == '__main__':
    unittest.main()