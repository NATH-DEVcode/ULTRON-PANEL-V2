from core.ui import module_banner, menu_box, clear
from core.navigation import check_navigation
import subprocess


def run_command(command):

    try:
        result = subprocess.check_output(
            command,
            shell=True,
            text=True,
            stderr=subprocess.DEVNULL
        )

        return result.strip()

    except Exception:
        return "No disponible"



def network_menu():

    while True:

        clear()

        module_banner("RED")


        menu = """
1. Ver IP
2. Ver interfaces de red
3. Escanear WiFi
4. Estado de conexión
5. Información de red

00. Inicio
0. Volver
"""


        menu_box(
            menu,
            "RED"
        )


        option = input(
            "\nSeleccione una opción: "
        )


        nav = check_navigation(option)


        if nav == "home":
            return "home"


        if nav == "back":
            return "back"



        if option == "1":

            ip = run_command(
                "hostname -I"
            )

            print(
                f"""
IP del equipo:

{ip}
"""
            )

            input("\nENTER para continuar")



        elif option == "2":

            interfaces = run_command(
                "ip link"
            )

            print(
                f"""
Interfaces de red:

{interfaces}
"""
            )

            input("\nENTER para continuar")



        elif option == "3":

            print(
                """
Escaneo WiFi

Buscando redes disponibles...
"""
            )

            wifi = run_command(
                "nmcli device wifi list"
            )

            print(wifi)

            input("\nENTER para continuar")



        elif option == "4":

            estado = run_command(
                "nmcli device status"
            )

            print(
                f"""
Estado de conexión:

{estado}
"""
            )

            input("\nENTER para continuar")



        elif option == "5":

            info = run_command(
                "nmcli general"
            )

            print(
                f"""
Información de red:

{info}
"""
            )

            input("\nENTER para continuar")



        else:

            print(
                "\nOpción no válida"
            )

            input(
                "\nENTER para continuar"
            )
