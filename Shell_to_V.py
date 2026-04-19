import pyvista as pv
import os

# Define paths
input_path = 'data/processed/vertebrae_mesh.stl'
output_path = 'data/processed/vertebrae_volume.vtk'

print("--- Starting Mesh Conversion ---")

if not os.path.exists(input_path):
    print(f"❌ ERROR: Cannot find {input_path}. Check your file name!")
else:
    # 1. Load Surface
    surface = pv.read(input_path)
    # This reduces the number of points by 90% while keeping the shape
    # It makes the volume conversion much, much faster
    surface = surface.decimate(0.9) 
    print(f"Decimated mesh to {surface.n_points} points for speed.")

    print(f"Successfully loaded surface with {surface.n_points} points.")

    # 2. Convert to Volume (Delaunay 3D)
    # This fills the space between the points to create a solid
    print("Generating volume... (this may take a moment)")
    volume = surface.delaunay_3d(alpha=2.0) 

    # 3. Save the result
    volume.save(output_path)
    print(f"✅ Success! File saved to {output_path}")

    # 4. Forced Visualization
    print("Opening 3D Viewer...")
    plotter = pv.Plotter()
    plotter.add_mesh(volume, show_edges=True, color="tan", opacity=0.5)
    plotter.add_title("Volumetric Tetrahedral Mesh")
    plotter.show()