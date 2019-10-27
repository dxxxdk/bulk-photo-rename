#!/usr/bin/env python3
"""
Renames images based on EXIF metadata.
"""

import exifread
from pathlib import Path
import os

valid_extensions = [
    # JPEG
    ".jpg",
    ".jpeg",
    ".jpe",
    ".jif",
    ".jfif",
    ".jfi",
    # TIFF
    ".tiff",
    ".tif",
]
date_separator = "-"
time_separator = "-"
date_time_separator = "_"


class ExifTagNotFoundException(Exception):
    pass


def get_file_paths_recursively(file_extensions=[".*"], root_folder_path=Path(".")):
    file_paths = []
    for file_extension in file_extensions:
        file_paths.extend(root_folder_path.glob(f"**/*{file_extension}"))
    return file_paths


def get_exif_date_and_time(file_path):
    date_time_tag = "EXIF DateTimeOriginal"

    with open(file_path, "rb") as file:
        tags = exifread.process_file(file, details=False, stop_tag=date_time_tag)

        date_time = tags.get(date_time_tag, None)
        if date_time is None:
            raise ExifTagNotFoundException(f"{date_time_tag} tag not found")
        return str(date_time).split(" ")


if __name__ == "__main__":
    file_paths = get_file_paths_recursively(file_extensions=valid_extensions)
    original_to_new_paths = []

    for file_path in file_paths:
        try:
            date, time = get_exif_date_and_time(file_path)
        except ExifTagNotFoundException:
            continue

        date = date.replace(":", date_separator)
        time = time.replace(":", time_separator)

        new_file_path = file_path.with_name(
            date + date_time_separator + time + file_path.suffix
        )

        original_to_new_paths.append((file_path, new_file_path))
        print(f"{file_path} -> {new_file_path}")

    s = input("Rename all the files as seen above? [y/n] ")
    if s.lower() != "y":
        print("Operation aborted")
        exit()

    for original_to_new_path in original_to_new_paths:
        original_path, new_path = original_to_new_path
        os.rename(original_path, new_path)
