# -*- coding: utf-8 -*-
__author__ = "Francesco"
__version__ = "0101 2023/02/05"


import os
import glob
from typing import Optional
import subprocess
# import lib
from ..libs import lib

riot_client = "RiotClientUx.exe"


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


def translate_valorant(selected_language: str, val_packs_directory: str) -> bool:
    try:
        print(selected_language)
        current_language = search_language(val_packs_directory)
        for file in search_file_from_string(lib.get_language_path(), selected_language):

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



def process_exists(process_name: str):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    output = subprocess.check_output(call).decode(encoding='unicode_escape')
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith(process_name.lower())


boold = False
if __name__ == "__main__":
    if boold:
        print("Start")

    print(translate_valorant("it_IT", "D:\\Riot Games\\VALORANT\\live\\ShooterGame\\Content\\Paks"))

    if boold:
        print("End")
