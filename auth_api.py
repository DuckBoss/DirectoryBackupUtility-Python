import hashlib
import os


def file_auth(file_name, buffer_size=65536):
    md5 = hashlib.md5()
    with open(file_name, 'rb') as src:
        while True:
            data_src = src.read(buffer_size)
            if not data_src:
                break
            md5.update(data_src)
    return md5.hexdigest()


def dir_auth(dir_name, buffer_size=65536):
    hash_list = []
    for root, dirs, files in os.walk(dir_name, topdown=True):
        for name in files:
            file_name = os.path.join(root, name)
            hash_list.append(file_auth(file_name, buffer_size))
    return hash_list
