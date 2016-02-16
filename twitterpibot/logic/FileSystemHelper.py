import logging
import shutil
import os
import sys

import six
import requests

try:
    # noinspection PyUnresolvedReferences,PyShadowingBuiltins
    input = raw_input
except NameError:
    pass

import pickle

logger = logging.getLogger(__name__)


def ensure_directory_exists(folder):
    if not os.path.exists(folder):
        logger.info("Creating " + folder)
        os.makedirs(folder)


def download_file(folder, url):
    logger.info("Downloading " + url)
    local_filename = folder + url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    logger.info("saved " + local_filename)
    return local_filename


def ensure_directory_exists_and_is_empty(folder):
    if os.path.exists(folder):
        logger.info("Removing " + folder)
        shutil.rmtree(folder, True)
    if not os.path.exists(folder):
        logger.info("Creating " + folder)
        os.makedirs(folder)


def remove_directory_and_contents(folder):
    if os.path.exists(folder):
        logger.info("Removing " + folder)
        shutil.rmtree(folder)


valid_extensions = {".jpg", ".jpeg", ".gif", ".png"}


def check_extension(url):
    ext = get_url_extension(url).lower()
    return ext in valid_extensions


def get_url_extension(url):
    path = six.moves.urllib.parse.urlparse(url).path
    ext = os.path.splitext(path)[1]
    return ext


def delete_files(files_list):
    if files_list:
        for file in files_list:
            if os.path.exists(file):
                logger.info("Removing " + file)
                os.remove(file)


def bytes_from_file(file_path, chunk_size):
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if chunk:
                yield chunk
            else:
                break


def get_key(key_name):
    keys_dir = "temp" + os.sep + "keys" + os.sep + str(sys.version_info[0]) + os.sep
    ensure_directory_exists(keys_dir)
    key_path = keys_dir + key_name + ".pkl"
    exists = os.path.isfile(key_path)
    if exists:
        key = pickle.load(open(key_path, "rb"))
    else:
        key = input("Enter your key for " + key_name + ": ")
        pickle.dump(key, open(key_path, "wb"))
    return key
