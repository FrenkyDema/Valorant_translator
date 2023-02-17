from customtkinter import *

from .pages import translate_page
from ..libs import lib
# Modes: "System" (standard), "Dark", "Light"
set_appearance_mode("Dark")
# Themes: "blue" (standard), "green", "dark-blue"
set_default_color_theme("blue")


class App(CTk):
    WIDTH = 700
    HEIGHT = 400

    def __init__(self):
        super().__init__()

        self.title(lib.APP_NAME)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        # self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)
            self.createcommand('tk::mac::Quit', self.on_closing)

        # configure grid layout (1x1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_label = CTkLabel(master=self,
                                    text=lib.APP_NAME,
                                    font=("Roboto Medium", -16),
                                    )
        self.title_label.grid(row=0, column=0, pady=5, padx=10)

        self.frame = translate_page.TranslatePage(self, self)
        self.frame.grid(row=1, sticky="nswe", padx=20, pady=20)

    # def change_mode(self):
    #     if self.switch_dark_mode.get() == 1:
    #         set_appearance_mode("dark")
    #     else:
    #         set_appearance_mode("light")

    def on_closing(self):
        self.destroy()

    def start(self):
        self.mainloop()
