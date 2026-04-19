import pyvista as pv
import os

def load_exported_mesh():
    # Ensure this path matches where you saved the file from Slicer
    mesh_path = 'data/processed/vertebrae_mesh.stl'
    
    if not os.path.exists(mesh_path):
        print(f"❌ Error: Cannot find {mesh_path}")
        return

    # Load the mesh
    mesh = pv.read(mesh_path)
    print(f"Mesh Loaded! Points: {mesh.n_points}, Cells: {mesh.n_cells}")

    # Visualize
    plotter = pv.Plotter()
    plotter.add_mesh(mesh, color="beige", smooth_shading=True)
    plotter.add_title("Bone Geometry: Segmented Thoracic Vertebrae")
    plotter.show()

if __name__ == "__main__":
    load_exported_mesh()