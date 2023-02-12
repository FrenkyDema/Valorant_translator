from genericpath import isdir
import tkinter
from customtkinter import *
import lib
import Valorant

CONFIG_FILE = "config.json"


def get_languages_dict() -> dict[str: str]:
    return lib.get_key_value_json(
        CONFIG_FILE, "supported_languages")


def get_selected_language_tag() -> str:
    return lib.get_key_value_json(
        CONFIG_FILE, "language")


def get_selected_language() -> str:

    languages = get_languages_dict()
    return list(languages.keys())[
        list(languages.values()).index(get_selected_language_tag())
    ]


def option_languages() -> list[str]:

    options = list(get_languages_dict().keys())
    options.remove(get_selected_language())

    return options


def optionmenu_callback(choice):

    language_tag: dict[str: str] = lib.get_key_value_json(
        CONFIG_FILE, "supported_languages")

    lib.update_key_json(
        CONFIG_FILE, "language",
        language_tag.get(choice)
    )

    print("Selected language:", choice)
    combobox.configure(values=option_languages())
    combobox.grid(padx=20, pady=10)


def button_event():
    print(Valorant.translate_valoant(get_selected_language_tag()))


boold = True
if __name__ == "__main__":
    if boold:
        print("Start")
    
    if not isdir(lib.resource_path("")):
        print("not exist")
        lib.create_app_files()

    lib.default_config_values()
    
    set_appearance_mode("dark")
    set_default_color_theme("blue")

    app = CTk()
    app.geometry("400x240")

    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure((0, 1), weight=1)

    combobox = CTkOptionMenu(
        master=app,
        values=option_languages(),
        command=optionmenu_callback
    )
    combobox.grid(padx=20, pady=10, row=0, column=0)
    combobox.set(get_selected_language())

    button = CTkButton(
        master=app, text="Translate", command=button_event)
    button.grid(padx=20, pady=10, row=1, column=0)

    app.mainloop()

    if boold:
        print("End")