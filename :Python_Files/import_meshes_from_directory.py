import Rhino
import Rhino.Geometry as rg
import os

def import_meshes_from_directory(directory):
    """Import all meshes from 3DM files in a given directory and return them with their filenames."""
    meshes_with_filenames = []
    
    # Loop through each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".3dm"):
            file_path = os.path.join(directory, filename)
            
            # Open the 3DM file
            model = Rhino.FileIO.File3dm.Read(file_path)
            if not model:
                print("Failed to open " + file_path)
                continue
            
            # Extract meshes and store them with filenames
            for obj in model.Objects:
                geometry = obj.Geometry
                if isinstance(geometry, rg.Mesh):
                    # Append the mesh and associated filename as a tuple
                    # Note: Convert the mesh to a copy to avoid issues with disposed model
                    mesh_copy = geometry.Duplicate()  # Make a copy of the mesh
                    meshes_with_filenames.append((filename, mesh_copy))
            
            # Dispose of the model after processing
            model.Dispose()
    
    return meshes_with_filenames

# Directory containing your 3DM files
directory_path = "/Users/boenalan/Library/CloudStorage/GoogleDrive-boenalan@ethz.ch/My Drive/CEA/PhD/FoC_2024/scans_regular/02.11"

# Import all meshes and their filenames
meshes_with_filenames = import_meshes_from_directory(directory_path)

# Separate filenames and meshes for Grasshopper output, removing ".3dm" from filenames
filenames = [os.path.splitext(item[0])[0] for item in meshes_with_filenames]
meshes = [item[1] for item in meshes_with_filenames]

# Output the filenames and meshes to Grasshopper
a = filenames   # Connect this to a panel to see filenames without ".3dm"
b = meshes      # Connect this to your convex hull processing component