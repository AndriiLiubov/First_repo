import re
import sys
import scan
import shutil
import normalize
from pathlib import Path

def handle_file(path, root_folder, dist):
    target_folder = root_folder/dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize.normalize(path.name))

def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    new_name = normalize.normalize(path.name)
    new_name = re.sub(r'.zip|.gz|.tar', '', new_name)

    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass

def remove_unarchived_file(path):
    for item in path.iterdir():
        if item.is_file():
            try:
                item.unlink()
            except OSError:
                pass

def main(folder_path):
    print(folder_path)
    scan.scan(folder_path)

    for key, value in scan.registered_extensions.items():
        for file in value:
            if key == "archives":
                handle_archive(file, folder_path, "archives")
            else:
                handle_file(file, folder_path, key)

    # for file in scan.images:
    #     handle_file(file, folder_path, "images")

    # for file in scan.video:
    #     handle_file(file, folder_path, "video")

    # for file in scan.documents:
    #     handle_file(file, folder_path, "documents")

    # for file in scan.audio:
    #     handle_file(file, folder_path, "audio")

    # for file in scan.archives:
    #     handle_archive(file, folder_path, "archives")

    # for file in scan.others:
    #     handle_file(file, folder_path, "others")

    
    remove_empty_folders(folder_path)
    remove_unarchived_file(folder_path)

if __name__ == '__main__':
    path = sys.argv[1]
    print(f'Start in {path}')

    folder = Path(path)
    main(folder.resolve())


    print(f"images: {scan.images}")
    print(f"video: {scan.video}")
    print(f"documents: {scan.documents}")
    print(f"audio: {scan.audio}")
    print(f"archives: {scan.archives}")
    print(f"others: {scan.others}")
    
    print(f"All extensions: {scan.extensions}")
    print(f"Unknown extensions: {scan.unknown}")

 