import os
import subprocess


FOLDERS = {

    "descargas": "~/Downloads",
    "downloads": "~/Downloads",

    "documentos": "~/Documents",

    "imagenes": "~/Pictures",
    "fotos": "~/Pictures",

    "musica": "~/Music",

    "escritorio": "~/Desktop",

    "inicio": "~"

}



def open_folder(name):

    name = name.lower()

    if name in FOLDERS:

        path = os.path.expanduser(
            FOLDERS[name]
        )

        subprocess.Popen(
            [
                "xdg-open",
                path
            ]
        )

        return (
            "ULTRON:\n"
            f"Abriendo {name}..."
        )


    return None
