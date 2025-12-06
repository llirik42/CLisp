import shutil
from pathlib import Path


def delete_all_files_in_dir(directory_path):
    if not directory_path.exists():
        print(f"Directory {directory_path} not exists!")
        return

    for item in directory_path.iterdir():
        try:
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        except Exception as e:
            print(f"Error during deleting files: {e}")

def copy_directory_structure(source_dir, target_dir):
    source_path = Path(source_dir)
    target_path = Path(target_dir)

    target_path.mkdir(exist_ok=True)

    for dir_path in source_path.rglob("*"):
        if dir_path.is_dir():
            relative_path = dir_path.relative_to(source_path)
            new_dir = target_path / relative_path
            new_dir.mkdir(exist_ok=True)
