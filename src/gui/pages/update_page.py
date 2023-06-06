import asyncio
import shutil
from tkinter import messagebox
import aiohttp
import webbrowser
from customtkinter import *
from PIL import Image, ImageSequence
import os

from ...libs import lib
from ...libs.lib import CONFIG_FILE
from ...debug import debug_print

import logging


async def update_async(latest_release):
    logger = logging.getLogger(__name__)
    logger.info("Starting async update")

    # Cerca il file exe tra gli asset della release
    exe_asset = None
    for asset in latest_release['assets']:
        if asset['name'].endswith('.exe'):
            exe_asset = asset
            break

    # Controlla se è stato trovato un file exe tra gli asset
    if exe_asset is not None:
        # Scarica il file exe
        async with aiohttp.ClientSession() as session:
            async with session.get(exe_asset['browser_download_url']) as response:
                with open(exe_asset['name'], 'wb') as f:
                    f.write(await response.read())

        # Sostituisce il file exe dell'applicazione con il nuovo file
        app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        exe_path = os.path.join(app_path, lib.APP_NAME + '.exe')
        if os.path.exists(exe_path):
            os.remove(exe_path)
        shutil.move(exe_asset['name'], exe_path)

        # Rimuovere la vecchia cartella dell' applicazione
        shutil.rmtree(os.path.dirname(os.path.dirname(lib.resource_path(""))))

        # Avvia l'applicazione aggiornata
        os.startfile(exe_path)

        # Chiude la vecchia applicazione
        os._exit(0)
    else:
        error_message = "Nessun file exe trovato nella release più recente."
        logger.error(error_message)
        messagebox.showerror("Error", error_message)


class UpdatePage(CTkFrame):
    def __init__(self, master, app, loop: asyncio.AbstractEventLoop):
        from ..main_app import App
        self.loop = loop
        self.app: App = app
        super().__init__(master)

        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.columnconfigure(0, weight=1)

        self.check_updates_button = CTkButton(
            self,
            text="Controlla aggiornamenti",
            command=self.check_for_updates_thread
        )
        self.check_updates_button.grid(row=0, column=0, padx=20, pady=10)

        self.version = CTkLabel(
            self,
            text="",
            width=150,
            height=45)
        self.version.grid(
            row=1, column=0, columnspan=2, padx=5,)

        self.loading_gif_frames: list[Image.Image] = [
            frame.copy() for frame in ImageSequence.Iterator(Image.open(lib.get_image_path('loading.gif')))
        ]

    def animate_loading_gif(self):
        self.version.configure(image=CTkImage(
            light_image=self.loading_gif_frames[self.loading_gif_index],
            size=(30, 30)
        ))
        self.loading_gif_index = (
            self.loading_gif_index + 1) % len(self.loading_gif_frames)
        self.loading_gif_animation_id = self.after(
            50, self.animate_loading_gif)

    def update_button_state(self, state):
        if state == "loading":
            self.check_updates_button.configure(
                text="Caricamento in corso...", state="disabled")
            self.loading_gif_index = 1
            self.animate_loading_gif()
        elif state == "loaded":
            self.after_cancel(self.loading_gif_animation_id)
            self.check_updates_button.configure(
                text="Controlla aggiornamenti", state="normal")
            self.version.configure(image=None)

    async def open_github(self):
        url = f'https://api.github.com/repos/{lib.get_key_value_json(CONFIG_FILE, "repo_owner")}/{lib.get_key_value_json(CONFIG_FILE, "repo_name")}/releases/latest'
        webbrowser.open_new_tab(url)

    def check_for_updates_thread(self):
        debug_print("check_for_updates_thread")
        self.loop.run_until_complete(self.check_for_updates())

    def update_app_thread(self, latest_release):
        debug_print("update_app_thread")
        self.loop.run_until_complete(update_async(latest_release))

    async def check_for_updates(self):
        current_version = lib.get_key_value_json(CONFIG_FILE, "version")

        # Disabilita il bottone di aggiornamento e mostra l'icona animata
        self.update_button_state("loading")

        debug_print("check_for_updates")

        # Recupera la versione più recente dalla repository su GitHub
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'https://api.github.com/repos/{lib.get_key_value_json(CONFIG_FILE, "repo_owner")}/{lib.get_key_value_json(CONFIG_FILE, "repo_name")}/releases/latest'
            ) as response:
                if response.status == 200:
                    latest_release = await response.json()
                    latest_version = latest_release['tag_name']
                    debug_print(latest_version)
                    if latest_version != current_version:
                        self.update_button = CTkButton(
                            self,
                            text="Aggiorna ora",
                            command=lambda: self.update_app_thread(
                                latest_release)
                        )
                        self.update_button.grid(
                            row=2, column=0, padx=20, pady=10)

                    else:
                        # Gestione dell'errore
                        messagebox.showerror(
                            "Error", "Nessun aggiornamento trovato.")
                self.update_button_state("loaded")
