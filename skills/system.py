import os
import subprocess


def system_action(target):

    target = target.lower()


    if target in [
        "apagar",
        "apaga"
    ]:

        return (
            "ULTRON:\n"
            "Confirmación necesaria para apagar."
        )


    if target in [
        "reiniciar",
        "reinicio"
    ]:

        return (
            "ULTRON:\n"
            "Confirmación necesaria para reiniciar."
        )


    if target in [
        "terminal"
    ]:

        subprocess.Popen(
            [
                "x-terminal-emulator"
            ]
        )

        return (
            "ULTRON:\n"
            "Abriendo terminal..."
        )


    return None
