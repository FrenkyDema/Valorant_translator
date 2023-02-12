# -*- coding: utf-8 -*-
__author__ = "Francesco"
__version__ = "01.01 2019\09\18"


import shutil
import os
import glob
from typing import Optional

path, tail = os.path.split(__file__)
os.chdir(path)

language_path = path + "\\resources\\languages\\"

def search_file_from_string(directory: str, string: str):
    return glob.glob(directory + "\*" + string + "*.*")


def get_language_tag(name: str, split_name: str):
    return (
        name.split(split_name)[0]
    ).strip("_")


def search_language(val_packs_directory: str) -> Optional[str]:
    search_name = "Audio-WindowsClient"
    try:

        language_tag = get_language_tag(
            os.path.basename(
                search_file_from_string(
                    val_packs_directory,
                    search_name
                )[0]
            ),
            search_name
        )
        return language_tag
    except Exception as e:
        print("NO file exist\n", e)
        return None


def get_renominated_text_filename(filename: str, language_tag: str) -> str:
    search_name = "Text-WindowsClient"
    return filename.replace(
        get_language_tag(filename, search_name),
        language_tag
    )


def translate_valoant(selected_language: str, val_packs_directory: str = "D:\Riot Games\VALORANT\live\ShooterGame\Content\Paks") -> bool:
    try:
        print(selected_language)
        current_language = search_language(val_packs_directory)
        for file in search_file_from_string(language_path, selected_language):

            renominated_filename = get_renominated_text_filename(
                os.path.basename(file),
                current_language
            )

            cmd = 'copy "' + file + '" "' + val_packs_directory + \
                '\\' + renominated_filename + '"'
            print(cmd)
            os.system(cmd)

        return True
    except Exception as e:
        print(e)
        return False


boold = False
if __name__ == "__main__":
    if boold:
        print("Start")

    if boold:
        print("End")
