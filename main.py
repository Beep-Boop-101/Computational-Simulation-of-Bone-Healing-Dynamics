import numpy as np
# Importing from your folder structure
from core.tissue_logic import run_bone_simulation_step
from core.cell_logic import update_cell_diffusion
from utils.generation import create_artificial_geometry
from utils.visualize import create_interactive_slicer
from config import PROPERTIES, applied_force, body_weight, rate_force_growth, voxel_size, num_hours, save_interval
from utils.visualize import create_interactive_slicer

def main():
    # --- 1. INITIALIZATION ---
    print("Initializing geometry...")
    # Create the artificial geometry with two bone segments and a fracture gap
    bone_grid = create_artificial_geometry()
    
    history = []
    days_logged = []
    
    # --- 2. SIMULATION LOOP ---
    print(f"Starting simulation for {num_hours// 24} days...")
    
    # We will simulate gradual loading during healing by increasing the applied force over time to reflect the natural process of weight-bearing and rehabilitation. The force will start low to represent the initial rest period after a fracture and will gradually increase to simulate the patient beginning to bear weight on the healing bone.
    for hour in range(num_hours):
        if 50> hour / 24 > 20:  # After 20 days, we can simulate gradual loading during healing
            applied_force[2] = -1 
        elif 50 <= hour / 24 < 80:  # After 50 days, we can simulate gradual loading during healing
            applied_force[2] = -70  
        elif 80 <= hour / 24:  # After 80 days, we can simulate gradual loading during healing
            applied_force[2] = -150  

        # Simulate a daily activity pattern: more force during the day, less at night. Still being worked on.
        #______
        #if hour % 24 <= 12:  # Simulate a daily activity pattern: more force during the day, less at night
            #applied_force[2] = -0.01 - rate_force_growth * (hour/ 24)  # Gradually increase the applied force during the day to simulate loading during healing
        #else: 
            #applied_force[2] = -0.01  # Reduced force at night to simulate rest
        #______

        if hour % 24 == 0:
            print(f"Day {hour // 24}: Applied Force = {applied_force[2]:g} N")

        # Step A: Biological Update (Cell Migration)
        bone_grid = update_cell_diffusion(bone_grid)
        
        # Step B: Mechanical Update (Strain -> Stimulus -> Tissue Type)
        # This function uses the PROPERTIES imported from tissue_logic
        bone_grid = run_bone_simulation_step(bone_grid, applied_force, voxel_size)
        
        # Step C: Capture snapshots for visualization
        if hour % save_interval == 0 or hour == num_hours - 1:
            history.append(bone_grid.copy()) # Copy is vital to keep unique daily data
            days_logged.append(hour // 24)

    # --- 3. VISUALIZATION ---
    print("Simulation complete. Rendering temporal progression...")
    create_interactive_slicer(history, days_logged)

if __name__ == "__main__":
    main()