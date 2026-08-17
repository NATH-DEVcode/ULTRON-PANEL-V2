kkimport webbrowser
import subprocess
import os
import shutil

from core.app_finder import launch_app


# Alias humanos → procesos reales
PROCESS_MAP = {

    "navegador": [
        "firefox",
        "chrome",
        "chromium"
    ],

    "firefox": [
        "firefox"
    ],

    "chrome": [
        "chrome",
        "google-chrome"
    ],

    "terminal": [
        "gnome-terminal",
        "konsole",
        "xfce4-terminal",
        "x-terminal-emulator"
    ],

    "whatsapp": [
        "whatsapp"
    ],

    "editor": [
        "code",
        "gedit",
        "mousepad",
        "kate"
    ]
}



def close_program(name):

    name = name.lower()

    processes = PROCESS_MAP.get(
        name,
        [name]
    )


    closed = False


    for process in processes:

        result = subprocess.run(
            [
                "pkill",
                "-f",
                process
            ],
            capture_output=True
        )


        if result.returncode == 0:
            closed = True


    return closed




def open_folder(folder):

    folders = {

        "descargas": "~/Downloads",
        "downloads": "~/Downloads",

        "documentos": "~/Documents",
        "documentos": "~/Documents",

        "imagenes": "~/Pictures",
        "fotos": "~/Pictures",

        "musica": "~/Music",

        "escritorio": "~/Desktop"

    }


    if folder in folders:

        path = os.path.expanduser(
            folders[folder]
        )

        subprocess.Popen(
            [
                "xdg-open",
                path
            ]
        )

        return True


    return False




def execute(action):


    intent = action.get(
        "intent",
        ""
    )


    target = action.get(
        "target",
        ""
    ).lower()



    # =====================
    # ABRIR
    # =====================

    if intent == "open":


        if target in [
            "youtube",
            "yt"
        ]:

            webbrowser.open(
                "https://youtube.com"
            )

            return (
                "ULTRON:\n"
                "Abriendo YouTube..."
            )



        if target in [
            "whatsapp",
            "whatsapp web",
            "wasap",
            "whats"
        ]:

            webbrowser.open(
                "https://web.whatsapp.com"
            )

            return (
                "ULTRON:\n"
                "Abriendo WhatsApp Web..."
            )



        if target == "google":

            webbrowser.open(
                "https://google.com"
            )

            return (
                "ULTRON:\n"
                "Abriendo Google..."
            )



        if open_folder(target):

            return (
                "ULTRON:\n"
                f"Abriendo {target}..."
            )



        # Buscar aplicación instalada

        result = launch_app(
            target
        )


        if result:

            return result



        return (
            "ULTRON:\n"
            "No encontré esa aplicación."
        )



    # =====================
    # CERRAR
    # =====================

    elif intent == "close":


        if close_program(target):

            return (
                "ULTRON:\n"
                f"Cerrando {target}..."
            )


        return (
            "ULTRON:\n"
            "No encontré ese programa abierto."
        )



    # =====================
    # RESPUESTAS
    # =====================

    elif intent == "answer":

        return (
            "ULTRON:\n"
            +
            action.get(
                "content",
                ""
            )
        )



    return (
        "ULTRON:\n"
        "Necesito una habilidad nueva para eso."
    )
