# -*- coding: utf-8 -*-
__author__ = "Francesco"
__version__ = "01.01 2019\09\18"


import shutil
import os
import glob

path, tail = os.path.split(__file__)
os.chdir(path)


def search_file_from_string(directory: str, string: str):
    return glob.glob(directory + "\*" + string + ".*")


def get_language_tag(name: str, split_name: str):
    return (
        name.split(split_name)[0]
    ).strip("_")


boold = False
if __name__ == "__main__":
    if boold:
        print("Start")

    val_packs_directory = "D:\Riot Games\VALORANT\live\ShooterGame\Content\Paks"
    search_name = "Text-WindowsClient"
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
        print(language_tag)

        # todo
        # replace current correct language text file in valorant
        # with renominate selected text file

        # rename_file_audio_name = "Audio-WindowsClient"
        # for file in search_file_from_string(path, rename_file_audio_name):
        #     filename = os.path.basename(file)
        #     os.rename(
        #         file,
        #         filename.replace(
        #             get_language_tag(filename, rename_file_audio_name),
        #             language_tag
        #         )
        #     )

        # for file in search_file_from_string(path, rename_file_audio_name):
        #     cmd = 'copy "' + file + '" "' +   val_packs_directory + '\\"'
        #     print(cmd)
        #     os.system(cmd)

    except Exception as e:
        print("NO file exist\n", e)

    if boold:
        print("End")
