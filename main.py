from src.physics_engine import calculate_strain
import numpy as np

def run_simulation():
    print("Starting Bone Healing Simulation...")
    # Create a dummy 10x10x10 bone grid
    bone_grid = np.ones((10, 10, 10))
    
    # Test the connection
    strain = calculate_strain(bone_grid)
    print("Simulation Step 1 Complete.")

if __name__ == "__main__":
    run_simulation()