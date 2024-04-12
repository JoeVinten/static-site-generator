import os
import shutil


def copy_static(dir_from, dir_to):
    if not os.path.exists(dir_from):
        raise ValueError(f"Directory from path {dir_from} does not exit")
    if os.path.exists(dir_to):
        print(f"Removing old {dir_to}")
        shutil.rmtree(dir_to)
    print(f"Creating directory: {dir_to}")
    os.mkdir(dir_to)

    files_to_copy = os.listdir(dir_from)

    for file in files_to_copy:
        old_path = os.path.join(dir_from, file)
        new_path = os.path.join(dir_to, file)
        if os.path.isfile(old_path):
            print(f"Copying {old_path} into {new_path}")
            shutil.copy(old_path, new_path)
        if os.path.isdir(old_path):
            copy_static(old_path, new_path)
