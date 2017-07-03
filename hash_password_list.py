# This script will create a password list of hashes of files

import hashlib
import os

hash_list = []
file_paths = []


def grab_hash(file_path):
    # To avoid loading large files to memory, each file is read in chunks (buffered) and
    # the hash is taken and updated in each loop phase for that file.

    print("Grabbing hash for " + file_path)
    buffer = 65536

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha512 = hashlib.sha512()

    with open(file_path, 'rb') as f:
        while True:
            data = f.read(buffer)
            if not data:
                break
            md5.update(data)
            sha1.update(data)
            sha512.update(data)

        hash_list.append(md5.hexdigest())
        hash_list.append(sha1.hexdigest())
        hash_list.append(sha512.hexdigest())


def save_to_txt(file_path):
    with open(file_path, 'w') as f:
        for hash_value in hash_list:
            f.write(hash_value + "\n")


def check_path(path):
    if not os.path.exists(path):
        print('Path not found: ' + path)
        return False
    else:
        print('Path exists: ' + path)
        return True


def directory_scan(path):
    print("Scanning directory...")

    for root, dirs, files in os.walk(path):
        for name in files:
            print(os.path.join(root, name))
            file_paths.append(os.path.join(root, name))


def path_collect():
    path_to_scan = input("Please enter the path that you want to scan\n")

    while check_path(path_to_scan) is False:
        path_to_scan = input("Please enter the path that you want to scan\n")

    file_path_txt_file = input("Please enter the path that you want to save the list to\n")
    file_name = input("Please enter the file name of the list\n")

    while check_path(file_path_txt_file) is False:
            file_path_txt_file = input("Please enter the path that you want to save the list to\n")

    full_path_txt_file = file_path_txt_file + "\\" + file_name + ".txt"

    return full_path_txt_file, path_to_scan


def hash_list_creation():
    path_tuple = path_collect()

    directory_scan(path_tuple[1])

    for path in file_paths:
        grab_hash(path)  # Get's the hashes of the files inside the directory entered

    save_to_txt(path_tuple[0])  # Saves hashes to a txt file TODO NEEDS TO CHECK PERMISSIONS BEFORE HASHING


hash_list_creation()
