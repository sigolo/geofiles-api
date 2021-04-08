from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import os

def make_zip(tree_path, zip_path, mode='w', skip_empty_dir=False):
    with ZipFile(zip_path, mode=mode, compression=ZIP_DEFLATED) as zf:
        length = len(tree_path)
        for root, dirs, files in os.walk(tree_path):
            # path without "parent"
            folder = root[length:]
            for file in files:
                zf.write(os.path.join(root, file), os.path.join(folder, file))
    return zip_path