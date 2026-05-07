import numpy as np
# Importing from your folder structure
from core.tissue_logic import run_bone_simulation_step
from core.cell_logic import update_cell_diffusion
from utils.generation import create_artificial_geometry
from utils.visualize import plot_healing_over_time
from config import PROPERTIES, applied_force, voxel_size, num_days, save_interval

def main():
    # --- 2. INITIALIZATION ---
    print("Initializing geometry...")
    # Create the two bone cylinders with the 5-voxel fracture gap
    bone_grid = create_artificial_geometry()
    
    history = []
    days_logged = []
    
    # --- 3. SIMULATION LOOP ---
    print(f"Starting simulation for {num_days} days...")
    
    for day in range(num_days):
        # Step A: Biological Update (Cell Migration)
        bone_grid = update_cell_diffusion(bone_grid)
        
        # Step B: Mechanical Update (Strain -> Stimulus -> Tissue Type)
        # This function uses the PROPERTIES imported from tissue_logic
        bone_grid = run_bone_simulation_step(bone_grid, applied_force, voxel_size)
        
        # Monitor progress in the terminal
        if day % 1 == 0:
            max_s = np.max(bone_grid[:, :, 25, 0])
            max_e = np.max(bone_grid[:, :, 25, 2])
            print(f"Day {day:02d} | Max S: {max_s:.4f} | Max E: {max_e:.2f}")
        if day %9 ==0:
            print(bone_grid[:, 25, :, 1])
        # Step C: Capture snapshots for visualization
        if day % save_interval == 0 or day == num_days - 1:
            history.append(bone_grid.copy()) # Copy is vital to keep unique daily data
            days_logged.append(day)

    # --- 4. VISUALIZATION ---
    print("Simulation complete. Rendering temporal progression...")
    # We choose Slice Z=25 because it sits in the middle of the fracture gap
    # defined in your generation.py (gap is around size // 2).
    plot_healing_over_time(history, days_logged, slice_idx=25)

if __name__ == "__main__":
    main()