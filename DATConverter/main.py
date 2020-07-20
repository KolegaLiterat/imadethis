import os
import subprocess
from progress.bar import IncrementalBar
from typing import List

def list_dat_files(path) -> List[str]:
    return os.listdir(path)

def remove_non_dat_files(listed_dat_files: List[str]):
    for filename in listed_dat_files:
        if filename.endswith(".DAT") != True:
            listed_dat_files.remove(filename)

def export_dat_to_jpg(dat_files: List[str], dat_folder_path: str, jpg_folder_path):
    
    try:
        if is_dat_folder_empty(dat_files) == False:
            bar = IncrementalBar("Exporting", max=len(dat_files))

            for file in dat_files:
                dat: str = create_dat_path(file, dat_folder_path)
                jpg: str = create_jpg_path(file, jpg_folder_path)

                subprocess.call(["magick", dat, jpg])

                bar.next()

            bar.finish()
    except Exception as export_error_info:
        print(f'EXCEPTION: {export_error_info}')

def create_dat_path(file: str, files_path: str) -> str:
    path_to_dat_file: str = files_path + file

    return path_to_dat_file

def create_jpg_path(file: str, files_path: str) -> str:
    path_to_jpg_file = files_path + file[:-3] + "jpg"

    return path_to_jpg_file

def is_jpg_folder_empty(jpg_folder: str) -> bool:
    is_empty: bool = False
    files_count: int = len(os.listdir(jpg_folder))

    if files_count == 0:
        is_empty = True
    else:
        raise Exception("JPGfiles is not empty! You need to remove files from this folder to start export!")
        exit()

    return is_empty

def is_dat_folder_empty(dat_files: List[str]) -> bool:
    is_empty: bool = True

    files_count: int = len(dat_files)

    if files_count > 0:
        is_empty = False
    else:
        raise Exception("DATFiles is empty! There's nothing to export")
    
    return is_empty

def main():
    dat_files_path: str = "./DATfiles/"
    jpg_files_path: str = "./JPGfiles/"

    try:
        if is_jpg_folder_empty(jpg_files_path):
            dat_files: List[str] = list_dat_files(dat_files_path)
            remove_non_dat_files(dat_files)
            export_dat_to_jpg(dat_files, dat_files_path, jpg_files_path)
    except Exception as exception_info:
        print(f'EXECPTION: {exception_info}')


if __name__ == "__main__":
    main()
