import os
import subprocess


APP_PATHS = [

    "/usr/share/applications",
    os.path.expanduser(
        "~/.local/share/applications"
    )

]


ALIASES = {

    "editor de dibujos": [
        "pinta",
        "krita",
        "gimp",
        "kolourpaint",
        "inkscape"
    ],

    "navegador web": [
        "firefox",
        "chrome",
        "chromium"
    ],

    "editor de texto": [
        "gedit",
        "mousepad",
        "kate",
        "code"
    ],

    "calculadora": [
        "calculator",
        "calc",
        "galculator"
    ]

}



def get_apps():

    apps = {}


    for path in APP_PATHS:

        if not os.path.exists(path):
            continue


        for file in os.listdir(path):

            if file.endswith(".desktop"):

                name = file.replace(
                    ".desktop",
                    ""
                ).lower()

                apps[name] = file


    return apps



def search_app(target):

    apps = get_apps()


    # Buscar alias

    if target in ALIASES:

        for program in ALIASES[target]:

            for app in apps:

                if program in app:

                    return apps[app]


    # Buscar coincidencia normal

    for app in apps:

        if target in app:

            return apps[app]


    return None



def launch_app(target):

    app = search_app(target)


    if not app:
        return None


    name = app.replace(
        ".desktop",
        ""
    )


    try:

        subprocess.Popen(
            [
                "gtk-launch",
                name
            ]
        )

        return (
            "ULTRON:\n"
            f"Abriendo {target}..."
        )


    except:

        return None
