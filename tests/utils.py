from pathlib import Path


def delete_all_files_in_dir(directory_path):
    try:
        path = Path(directory_path)

        if not path.exists():
            print(f"Directory {directory_path} not exists!")
            return

        for file_path in path.iterdir():
            if file_path.is_file():
                file_path.unlink()

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
