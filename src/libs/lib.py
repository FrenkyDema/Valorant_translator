# -*- coding: utf-8 -*-
__author__ = "Francesco"
__version__ = "0101 2023/02/05"

import json
import logging
import os
import pathlib
import shutil
import sys

from appdirs import user_data_dir
from ..debug import debug_print
# CONSTANTS
path_separation = "\\"
file_path = 'src\\resources\\'
image_path = 'src\\resources\\icons\\'
language_path = 'src\\resources\\languages\\'

APP_NAME = "Valorant_translator"
VERSION = "v1.0.3"
CONFIG_FILE = "config.json"

# ================== Temp Files functions ==================


def resource_temp_path(relative_path: str) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    temp_path = getattr(sys, '_MEIPASS', os.path.dirname(os.getcwd()))
    debug_print("Temp - ", os.path.join(temp_path, relative_path))
    return os.path.join(temp_path, relative_path)


# ================== File functions ==================

def resource_path(relative_path: str,):
    base_path = user_data_dir(
        appname=APP_NAME, appauthor=False, version=VERSION)
    debug_print("Local - ", os.path.join(base_path, relative_path))
    return os.path.join(base_path, relative_path)


def create_app_files():
    debug_print("create app files")
    copy_dir(resource_temp_path(file_path), resource_path(
        file_path), resource_temp_path(image_path))


def copy_dir(src: str, dst: str, ignore: str = ""):
    source_path = pathlib.Path(src)
    destination_path = pathlib.Path(dst)
    destination_path.mkdir(parents=True, exist_ok=True)
    for item in os.listdir(source_path):
        s: pathlib.Path = source_path / item
        d: pathlib.Path = destination_path / item
        if s.is_dir():
            if pathlib.Path(ignore) != s:
                copy_dir(str(s), str(d), ignore)
        else:
            shutil.copy2(str(s), str(d))


# ================== JSON functions ==================


def open_json(file_name: str):
    try:
        f = open(resource_path(file_path + file_name), 'r+')
        return f
    except FileNotFoundError:
        with open(resource_path(file_path + file_name), 'w') as f:
            json.dump({}, f, indent=4)
        return open_json(file_name)
    except Exception as e:
        logging.debug(e)


def update_key_json(file_name: str, key: str, value):
    f = open_json(file_name)
    data = json.load(f)
    data[key] = value
    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()
    f.close()


def update_json(file_name: str, dix: dict):
    for key, value in dix.items():
        update_key_json(file_name, key, value)


def get_key_value_json(file_name: str, key: str):
    f = open_json(file_name)
    data = json.load(f)
    f.close()
    try:
        return data[key]
    except KeyError:
        return ""


def get_dix_json(file_name: str):
    f = open_json(file_name)
    data = json.load(f)
    f.close()
    return data


# ========= config.json =========

def default_config_values():
    debug_print("default config values")
    dix = {
        "version": VERSION,
        "repo_owner": 'FrenkyDema',
        "repo_name": APP_NAME,

        "supported_languages": {
            "Italian": "it_IT",
            "English": "en_US",
            "Japanese": "ja_JP"
        },
        "language": "it_IT",
        "valorant_directory": ""
    }

    update_json(CONFIG_FILE, dix)


# ========= image functions =========

def get_image_path(image_name: str) -> str:
    return resource_temp_path(image_path + image_name)


# ========= LANGUAGE functions =========

def get_language_path(language_filename: str = "") -> str:
    return resource_temp_path(language_path + language_filename)


boold = True
if __name__ == "__main__":
    if boold:
        debug_print("Start")

    create_app_files()

    default_config_values()

    if boold:
        debug_print("End")
