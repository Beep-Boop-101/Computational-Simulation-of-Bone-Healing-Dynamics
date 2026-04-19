import os

# This checks your raw data folder
path = 'data/raw'

if not os.path.exists(path):
    print(f"❌ Error: The folder '{path}' does not exist!")
else:
    # Look for files (including inside subfolders)
    all_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(('.dcm', '.png', '.jpg')):
                all_files.append(os.path.join(root, file))

    print(f"--- Data Check ---")
    print(f"Total images found: {len(all_files)}")
    
    if len(all_files) > 0:
        print(f"First file location: {all_files[0]}")
        print("✅ Success! Your data is in the right place.")
    else:
        print("❌ No images found. Make sure your PNGs or DCMs are inside 'data/raw'.")