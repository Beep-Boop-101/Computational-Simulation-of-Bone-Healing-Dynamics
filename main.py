import numpy as np
# Importing from your folder structure
from core.tissue_logic import run_bone_simulation_step
from core.cell_logic import update_cell_diffusion
from utils.generation import create_artificial_geometry
from utils.visualize import create_interactive_slicer
from config import applied_force, low_force, early_healing_force, mid_healing_force, late_healing_force, voxel_size, num_days, num_hours, save_interval
from utils.visualize import create_interactive_slicer

def main():
    ''' 
    Main function to run the bone healing simulation. 

    This function initializes the geometry, runs the simulation loop for the specified number of days, and captures snapshots for visualization.

    The applied force is updated over time to simulate gradual loading during healing. 

    The force starts low to represent the initial rest period after a fracture and gradually increases to simulate the patient beginning to bear weight on the healing bone.

    '''

    # --- 1. INITIALIZATION ---
    print("Initializing geometry...")
    # Create the artificial geometry with two bone segments and a fracture gap
    bone_grid = create_artificial_geometry()
    
    history = []
    days_logged = []
    
    # --- 2. SIMULATION LOOP ---
    print(f"Starting simulation for {num_hours// 24} days...")
    
    # We will simulate gradual loading during healing by increasing the applied force over time to reflect the natural process of weight-bearing and rehabilitation. 
    # The force will start low to represent the initial rest period after a fracture and will gradually increase to simulate the patient beginning to bear weight on the healing bone.
    for hour in range(num_hours):

        # 1. Calculate the current day
        day = hour / 24

        # 2. Determine the maximum applied force threshold based on the healing phase (day)
        if day < 30:
            base_force = low_force  # Initial low force to represent the rest period immediately after a fracture
        elif 30 <= day < 60:
            base_force = early_healing_force # Moderate force during the early healing phase when the patient starts to bear weight
        elif 60 <= day < 90:
            base_force = mid_healing_force # Increased force during the mid-healing phase as the patient becomes more active
        elif day >= 90:  # 90 days and beyond
            base_force = late_healing_force # Higher force during the late healing phase as the bone regains strength and the patient returns to normal activities

        # 3. Apply the daily activity pattern (Day vs. Night)

        # Checks if the current hour falls within the active daytime window (assuming 8 hours of sleep)
        if hour % 24 <= 16:
            applied_force[2] = base_force  # Full weight-bearing active force for this phase
        else:
            applied_force[2] = low_force  # Reduced force at night to simulate rest

        if hour % 24 == 0:
            print(f"Day {int(hour / 24)}: Applied Force = {applied_force[2]:g} N")

        # Step A: Biological Update (Cell Migration)
        bone_grid = update_cell_diffusion(bone_grid)
        
        # Step B: Mechanical Update (Strain -> Stimulus -> Tissue Type)
        # This function uses the PROPERTIES imported from tissue_logic
        bone_grid = run_bone_simulation_step(bone_grid, applied_force, voxel_size)
        
        # Step C: Capture snapshots for visualization
        if day % save_interval == 0 or day == num_days - 1:
            history.append(bone_grid.copy()) # Copy is vital to keep unique daily data
            days_logged.append(int(day)) # Log the day as an integer for easier visualization labels

        print(bone_grid[25, 25, 25]) # Print the properties of the central voxel for debugging


    # --- 3. VISUALIZATION ---
    print("Simulation complete. Rendering temporal progression...")
    create_interactive_slicer(history, days_logged)

if __name__ == "__main__":
    main()