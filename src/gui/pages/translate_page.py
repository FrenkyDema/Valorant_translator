from genericpath import isdir
from tkinter import messagebox

from PIL import Image
from customtkinter import *

from ...debug import debug_print
from ...libs import Valorant, lib
from ...libs.lib import CONFIG_FILE


class TranslatePage(CTkFrame):
    def __init__(self, master, app):
        self.app = app
        super().__init__(master)

        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.columnconfigure(0, weight=1)

        self.directory_frame = CTkFrame(master=self)
        self.directory_frame.grid(
            row=0, column=0, pady=10, padx=15)

        self.directory_frame.columnconfigure((0, 1, 2), weight=1)

        self.root_display = CTkLabel(
            self.directory_frame,
            width=400,
            height=45)
        self.root_display.grid(
            row=0, column=0, columnspan=2, padx=5, sticky="e")

        self.chose_directory_button = CTkButton(
            self.directory_frame,
            height=45,
            width=45,
            image=CTkImage(
                light_image=Image.open(lib.get_image_path(
                    "add-folder_ico.png"
                )),
                dark_image=Image.open(lib.get_image_path(
                    "add-folder_ico.png"
                )),
                size=(30, 30)
            ),
            text="",
            fg_color=("gray65", "gray25"),  # <- custom tuple-color
            command=self.chose_directory
        )
        self.chose_directory_button.grid(row=0, column=2, sticky="w")

        self.voice_language_frame = CTkFrame(master=self)
        self.voice_language_frame.grid(
            row=1, column=0, pady=10, padx=15)

        self.voice_language_frame.columnconfigure((0, 1, 2), weight=1)

        self.label_voice_language = CTkLabel(
            self.voice_language_frame,
            text="Client avviato:",
            width=150,
            height=45)
        self.label_voice_language.grid(
            row=0, column=0, columnspan=2, padx=5, sticky="e")

        self.client_check = CTkLabel(
            self.voice_language_frame,
            height=45,
            width=45,
            text="",
        )
        self.client_check.bind(sequence='<Button-1>',
                               command=self.update_client_check)

        self.client_check.grid(row=0, column=2, padx=5, sticky="w")

        self.text_language_frame = CTkFrame(master=self)
        self.text_language_frame.grid(
            row=2, column=0, pady=10, padx=15)

        self.text_language_frame.columnconfigure((0, 1, 2), weight=1)
        self.text_language_frame.rowconfigure((0, 1), weight=1)

        self.label_voice_language = CTkLabel(
            self.text_language_frame,
            text="Voice language:",
            width=150,
            height=45)
        self.label_voice_language.grid(
            row=0, column=0, columnspan=2, padx=5, sticky="e")

        self.label_voice_language_value = CTkLabel(
            self.text_language_frame,
            width=150,
            height=45)
        self.label_voice_language_value.grid(
            row=0, column=2, padx=5, sticky="w")

        self.label_text_language = CTkLabel(
            self.text_language_frame,
            text="Text language:",
            width=150,
            height=45)
        self.label_text_language.grid(
            row=1, column=0, columnspan=2, padx=5, sticky="e")

        self.combobox = CTkOptionMenu(
            self.text_language_frame,
            values=option_languages(),
            command=self.optionmenu_callback
        )
        self.combobox.grid(row=1, column=2, pady=7, padx=7, sticky="w")
        self.combobox.set(get_language_from_tag(get_selected_language_tag()))

        self.submit_button = CTkButton(
            self,
            height=40,
            text="Translate",
            compound="right",
            image=CTkImage(
                dark_image=Image.open(lib.get_image_path(
                    "translate_text_icon.png")),
                light_image=Image.open(lib.get_image_path(
                    "translate_text_icon.png")),
                size=(30, 30)
            ),
            fg_color=("gray65", "gray25"),  # <- custom tuple-color
            command=submit_all)
        self.submit_button.grid(
            row=3, column=0, padx=10, pady=10, sticky="se")

        self.set_default_values()

    def set_default_values(self):
        self.update_voice_language()
        self.update_root_display()
        self.update_client_check()

    def optionmenu_callback(self, choice):
        language_tag: dict[str: str] = lib.get_key_value_json(
            CONFIG_FILE, "supported_languages")

        lib.update_key_json(
            CONFIG_FILE, "language",
            language_tag.get(choice)
        )

        debug_print("Selected language:", choice)
        self.combobox.configure(values=option_languages())
        self.combobox.grid(padx=20, pady=10)

    def chose_directory(self):
        directory = filedialog.askdirectory()
        lib.update_key_json(
            CONFIG_FILE, "valorant_directory", directory.replace("\\", "/"))
        self.update_root_display()
        self.update_voice_language()
        self.update_client_check()

    def update_client_check(self, event=None):

        icon_path = "true_icon.png" if Valorant.process_exists(
            Valorant.riot_client) else "false_icon.png"
        img = Image.open(lib.get_image_path(icon_path))
        photo = CTkImage(dark_image=img, light_image=img, size=(30, 30))
        self.client_check.configure(image=photo)

    def update_root_display(self):
        self.root_display.configure(text=get_valorant_directory())

    def update_voice_language(self):
        self.label_voice_language_value.configure(text=get_language_from_tag(
            Valorant.search_language(get_valorant_directory())))
        self.label_voice_language_value.grid(
            row=0, column=2, padx=5, sticky="w")


def get_languages_dict() -> dict[str: str]:
    return lib.get_key_value_json(
        CONFIG_FILE, "supported_languages")


def get_selected_language_tag() -> str:
    return lib.get_key_value_json(
        CONFIG_FILE, "language")


def get_language_from_tag(language_tag: str = None) -> str:
    languages = get_languages_dict()
    if not language_tag:
        return "English"
    return list(languages.keys())[
        list(languages.values()).index(language_tag)
    ]


def get_valorant_directory() -> str:
    # "D:\Riot Games\VALORANT\live\ShooterGame\Content\Paks"

    return lib.get_key_value_json(
        CONFIG_FILE, "valorant_directory")


def project_directory_check() -> bool:
    if not isdir(lib.get_key_value_json(CONFIG_FILE, "valorant_directory")):
        messagebox.showerror(
            "Error", "Selezionare un percorso valido")
        return False
    return True


def option_languages() -> list[str]:
    options = list(get_languages_dict().keys())
    options.remove(get_language_from_tag(get_selected_language_tag()))

    return options


def submit_all():

    if project_directory_check():
        translate = Valorant.translate_valorant(
            get_selected_language_tag(),
            get_valorant_directory()
        )
        debug_print(translate)
        if translate:
            messagebox.showinfo("Confirm", "Traduzione avvenuta con successo")
