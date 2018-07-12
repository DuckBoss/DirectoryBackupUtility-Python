import sys
import os
import auth_api
import shutil
import configparser
from time import sleep

BUFFER_SIZE = 65536

cp = configparser.ConfigParser()
cp.read('config.ini')
scan_time = float(cp['Main']['scan_time'])
src_dir = str(cp['Main']['src_dir'])
dst_dir = str(cp['Main']['dst_dir'])
blacklist_keywords = cp['Blacklist']['keywords'].replace(" ", "").split(',')
blacklist_keywords = [x.upper() for x in blacklist_keywords]
allow_remove = cp.getboolean('Options', 'allow_remove')
verbose_output = cp.getboolean('Options', 'verbose_output')

if not os.path.isdir(src_dir):
    print("ERROR: src_dir missing!")
    print("Please make sure both directories exist!")
    sys.exit(1)
if not os.path.isdir(dst_dir):
    print("ERROR: dst_dir missing!")
    print("Please make sure both directories exist!")
    sys.exit(1)


def verbose_print(text):
    if verbose_output:
        print(text)


while True:
    src_dir_hash_list = auth_api.dir_auth(src_dir, BUFFER_SIZE)
    dst_dir_hash_list = auth_api.dir_auth(dst_dir, BUFFER_SIZE)

    if src_dir_hash_list != dst_dir_hash_list:
        verbose_print("Detected change in src_dir/dst_dir... syncing!")
        for file_name in os.listdir(src_dir):
            filePathSrc = "%s/%s" % (src_dir, file_name)
            if any(x in str.upper(file_name) for x in blacklist_keywords):
                if allow_remove:
                    os.remove(filePathSrc)
                    verbose_print("--> Removed detected file: %s" % file_name)
                    continue
                verbose_print("--> Skipping detected file: %s" % file_name)
                continue
            filePathDst = "%s/%s" % (dst_dir, file_name)
            shutil.copyfile(filePathSrc, filePathDst)
        verbose_print("--> Directories synced!")
        sleep(scan_time)
        continue

    verbose_print("No changes detected...waiting %s seconds" % scan_time)
    sleep(scan_time)



