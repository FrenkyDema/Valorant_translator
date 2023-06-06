import asyncio
import logging
from customtkinter import *


from PIL import Image
from PIL.ImageTk import PhotoImage
from .pages import translate_page
from .pages import update_page
from ..libs import lib
from . import main_app_enum
# Modes: "System" (standard), "Dark", "Light"
set_appearance_mode("Dark")
# Themes: "blue" (standard), "green", "dark-blue"
set_default_color_theme("blue")


class App(CTk):
    WIDTH = 700
    HEIGHT = 400

    def __init__(self):
        super().__init__()

        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

        self.title(lib.APP_NAME)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        # self.minsize(App.WIDTH, App.HEIGHT)

        self.setup_close_handler()

        # configure grid layout (3x1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_rowconfigure(2, weight=15)

        self.title_label = CTkLabel(
            master=self,
            text=lib.APP_NAME,
            font=("Roboto Medium", -16),
        )
        self.title_label.grid(
            row=0, rowspan=2, column=0, pady=5, padx=10, sticky=""
        )

        self.settings_button = CTkButton(
            master=self,
            text="",
            height=35,
            width=35,
            image=CTkImage(
                light_image=Image.open(
                    lib.get_image_path("settings_icon.png")
                ),
                dark_image=Image.open(
                    lib.get_image_path("settings_icon.png")
                ),
                size=(30, 30)
            ),
            # <- custom tuple-color
            fg_color=(
                "gray65", "gray25"),
            command=lambda: self.chose_frame(
                page_type=main_app_enum.MainAppEnum.SETTINGS)
        )
        self.settings_button.grid(
            row=1, column=0, sticky="e", padx=10, pady=5)

        self.main_frame = translate_page.TranslatePage(self, self)
        self.main_frame.grid(row=2, column=0, sticky="nswe", padx=20, pady=20)

    def change_main_frame(self, frame: CTkFrame):
        self.clear_frame()

        self.main_frame = frame

        self.main_frame.grid(row=2, column=0, sticky="nswe", padx=20, pady=20)

    def change_settigs_button(self, isSettings: bool):
        if isSettings:
            self.settings_button.configure(image=CTkImage(
                light_image=Image.open(
                    lib.get_image_path("back_icon.png")
                ),
                dark_image=Image.open(
                    lib.get_image_path("back_icon.png")
                ),
                size=(30, 30)
            ),
                command=lambda: self.chose_frame(
                page_type=main_app_enum.MainAppEnum.TRANSLATE))
        else:
            self.settings_button.configure(
                image=CTkImage(
                    light_image=Image.open(
                        lib.get_image_path("settings_icon.png")
                    ),
                    dark_image=Image.open(
                        lib.get_image_path("settings_icon.png")
                    ),
                    size=(30, 30)
                ),
                command=lambda: self.chose_frame(
                    page_type=main_app_enum.MainAppEnum.SETTINGS)
            )
        self.settings_button.grid(
            row=1, column=0, sticky="e", padx=10, pady=5)

    def chose_frame(self, page_type):
        match page_type:
            case main_app_enum.MainAppEnum.TRANSLATE:
                self.change_main_frame(
                    translate_page.TranslatePage(self, self))
                self.change_settigs_button(False)

            case main_app_enum.MainAppEnum.SETTINGS:
                self.change_main_frame(
                    update_page.UpdatePage(self, self, self.loop))
                self.change_settigs_button(True)

            case _:
                pass

    def handle_close(self) -> None:
        if self.loop.is_running():
            try:
                future = asyncio.ensure_future(self.do_close())
                self.loop.run_until_complete(future)
            except RuntimeError:
                logging.exception(
                    "Error occurred while trying to close the application")
        else:
            self.destroy()

    def setup_close_handler(self) -> None:
        self.protocol("WM_DELETE_WINDOW", self.handle_close)
        if sys.platform == "darwin":
            self.bind("<Command-q>", self.handle_close)
            self.bind("<Command-w>", self.handle_close)
            self.createcommand("tk::mac::Quit", self.handle_close)

    def clear_frame(self):
        self.main_frame.destroy()

    async def do_close(self) -> None:
        self.loop.stop()
        self.destroy()

    def start(self):
        self.mainloop()
