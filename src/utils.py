import pydicom
import numpy as np
import os

def load_bone_volume(directory):
    """
    Loads a folder of DICOM slices and stacks them into a 3D NumPy array.
    """
    # 1. Get all DICOM files and sort them by position so the 3D stack is in order
    files = [pydicom.dcmread(os.path.join(directory, f)) for f in os.listdir(directory) if f.endswith('.dcm')]
    files.sort(key=lambda x: float(x.ImagePositionPatient[2]))

    # 2. Extract the pixel arrays
    volume = np.stack([f.pixel_array for f in files])

    # 3. Convert to Hounsfield Units (HU)
    # HU = pixel_value * rescale_slope + rescale_intercept
    for i, f in enumerate(files):
        intercept = f.RescaleIntercept if 'RescaleIntercept' in f else -1024
        slope = f.RescaleSlope if 'RescaleSlope' in f else 1
        volume[i] = volume[i] * slope + intercept

    return volume.astype(np.int16)

def get_elastic_modulus(hu_volume):
    """
    Converts Hounsfield Units to Young's Modulus (E) in MegaPascals (MPa).
    A common empirical formula for bone: E = 0.004 * (HU + 1000)**2
    """
    # Ensure no negative values for the density calculation
    density = np.clip(hu_volume + 1000, 0, None) 
    # Placeholder empirical relation
    modulus = 0.001 * (density**1.5) 
    return modulus

if __name__ == "__main__":
    # Test path - replace with your actual folder name from the zip
    test_path = 'data/raw/B16_Subject_01' 
    if os.path.exists(test_path):
        voxels = load_bone_volume(test_path)
        print(f"Voxel Grid Shape: {voxels.shape}")
        print(f"Max HU value (Bone): {np.max(voxels)}")