import argparse
import shutil
from pathlib import Path

count_files = 0
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Recursively copies files from source directory to destination directory, "
                    "sorting by subdirectories based on extension."
    )
    p.add_argument("src", type=Path, help="path to source directory")
    p.add_argument("dest", nargs="?", default=Path("dist"), type=Path, help="path to destination directory (default: ./dist)")
    return p.parse_args()

def copy_file(file_path: Path, dest_root: Path) -> None:
    """
    Copy a file to the destination directory, creating subdirectories as needed.
    If file already exists, add suffix (_1, _2, ...) to avoid overwriting.
    """
    ext = "".join(file_path.suffixes).lstrip(".").lower() or "_noext"
    result_path = dest_root / ext
    try:
        result_path.mkdir(parents=True, exist_ok=True)
        # path for the copied file
        target_path = result_path / file_path.name
        # Check if the file exists, and if so, add a suffix
        if target_path.exists():
            stem, suffix = file_path.stem, file_path.suffix
            counter = 1
            while target_path.exists():
                new_name = f"{stem}_{counter}{suffix}"
                target_path = result_path / new_name
                counter += 1
        shutil.copy2(file_path, target_path)
        global count_files
        count_files += 1
    except PermissionError as e:
        print(f"Not enough permissions to copy {file_path}: {e}")
    except FileNotFoundError as e:
        print(f"File disappeared during copying {file_path}: {e}")
    except OSError as e:
        print(f"Error copying {file_path}: {e}")
    except Exception as e:
        print(f"Unexpected error copying {file_path}: {e}")
        print("Skipping file.")

def read_and_copy(src: Path, dest: Path) -> None:
    """
    Recursively reads src and copies files to dest, sorting by extension.
        args:
            src (Path): The source directory to read files from.
            dest (Path): The root destination directory to copy files to.
    """
    try:
        for item in src.iterdir():
            try:
                # Skip symlinks
                if item.is_symlink():
                    print(f"Skipping symlink: {item}")
                    continue
                # Skip the destination folder itself if it's inside the source
                if item.is_dir():
                    if item.is_relative_to(dest):
                        print(f"Skipping destination directory during traversal: {item}")
                        continue
                    read_and_copy(item, dest)
                elif item.is_file():
                    copy_file(item, dest)
                else:
                    print(f"Skipping non-file and non-directory: {item}")
            except PermissionError as e:
                print(f"Not enough permissions to access {item}: {e}")
                continue
            except OSError as e:
                print(f"Error accessing {item}: {e}")
                continue
            except Exception as e:
                print(f"Unexpected error accessing {item}: {e}")
                continue
    except PermissionError as e:
        print(f"Not enough permissions to read directory {src}: {e}")
    except Exception as e:
        print(f"Error reading directory {src}: {e}")

def main() -> int:
    args = parse_args()

    # get absolute paths
    src = args.src.resolve()
    dest = args.dest.resolve()

    if src == dest:
        print("Source and destination directories must be different.")
        return 1

    # check if source directory exists
    if not src.exists() or not src.is_dir():
        print(f"Source directory does not exist or is not a directory: {src}")
        return 1

    if dest.is_file():
        print(f"Destination is a file: {dest}")
        return 1

    # Create destination directory if it doesn't exist
    try:
        dest.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Failed to create destination directory {dest}: {e}")
        return 1

    print(f"Started copying from {src} to {dest}")
    read_and_copy(src, dest)
    print(f"Total files copied: {count_files}")
    print("Done.")
    return 0

if __name__ == "__main__":
    main()