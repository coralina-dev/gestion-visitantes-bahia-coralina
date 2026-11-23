"""Interfaz de consola del monitoreo de visitantes de la Reserva Natural Bahía Coralina.

Aquí solo se lee del teclado, se llama a business_logic y se muestran los
resultados. Los mensajes de error vienen de los ValueError de business_logic.
"""

from datetime import date, timedelta

from business_logic import DIAS_PARA_CIERRE, NIVELES, Reserva, Sector


def dias_texto(cantidad: int) -> str:
    return f"{cantidad} día" if cantidad == 1 else f"{cantidad} días"


def pedir_sector(reserva: Reserva) -> Sector | None:
    """Lee un nombre y devuelve su sector, o avisa y devuelve None (R10)."""
    nombre = input("Nombre del sector: ")
    sector = reserva.buscar_sector(nombre)
    if sector is None:
        print("No hay un sector con ese nombre.")
    return sector


# --- Opción 1 (R1) -------------------------------------------------------

def crear_sector(reserva: Reserva) -> None:
    nombre = input("Nombre del sector: ")
    capacidad = input("Capacidad de carga: ")
    anio = input("Año de inicio: ")
    mes = input("Mes de inicio: ")
    dia = input("Día de inicio: ")
    try:
        sector = reserva.crear_sector(nombre, capacidad, anio, mes, dia)
    except ValueError as error:
        print(f"{error}.")
        return
    print(f"Se creó el sector {sector.nombre}, sin días registrados.")


# --- Opción 2 (R2) -------------------------------------------------------

def registrar_dia(reserva: Reserva) -> None:
    sector = pedir_sector(reserva)
    if sector is None:
        return
    try:
        fecha = sector.fecha_siguiente().isoformat()
    except ValueError as error:
        print(f"{error}.")
        return
    print(f"Día por registrar: {fecha}")
    while True:
        try:
            visitantes = sector.validar_visitantes(input(f"Visitantes del {fecha}: "))
            break
        except ValueError as error:
            print(f"{error}.")
    sector.registrar_dia(visitantes)
    print(f"Se registraron {visitantes} visitantes el {fecha}.")


# --- Opción 3 (R3) -------------------------------------------------------

def simular_dias(reserva: Reserva) -> None:
    sector = pedir_sector(reserva)
    if sector is None:
        return
    try:
        dias = reserva.validar_dias_simulados(input("Número de días a simular: "))
        minimo = sector.validar_visitantes(input("Visitantes mínimos: "))
        maximo = sector.validar_visitantes(input("Visitantes máximos: "))
        primera = sector.fecha_siguiente()
        sector.simular_dias(dias, minimo, maximo)
    except ValueError as error:
        print(f"{error}.")
        return
    ultima = sector.ultimo_dia_registrado()
    print(f"Se simularon {dias_texto(dias)}, del {primera.isoformat()} al {ultima.isoformat()}.")


# --- Opción 4 (R4 a R9 y R15) --------------------------------------------

def mostrar_informe(reserva: Reserva) -> None:
    sector = pedir_sector(reserva)
    if sector is None:
        return
    print()
    print(f"Sector: {sector.nombre}")
    print(f"Capacidad de carga: {sector.capacidad} visitantes")
    if sector.dias_registrados() == 0:
        print("El sector no tiene días registrados.")
        return

    # R4 y R5
    print(f"Días registrados: {sector.dias_registrados()}")
    print(f"Visitantes totales: {sector.total_visitantes()}")
    print(f"Promedio de visitantes por día: {round(sector.promedio(), 2)}")
    print(f"Porcentaje de uso: {round(sector.porcentaje_uso(), 2)} %")
    print(f"Desviación estándar: {round(sector.desviacion_estandar(), 2)}")

    # R6
    print(f"Día con más visitantes: {sector.dia_mas_visitantes().isoformat()}")
    print(f"Día con menos visitantes: {sector.dia_menos_visitantes().isoformat()}")

    # R7
    print("Días en cada nivel de presión:")
    conteo = sector.dias_por_nivel()
    for nivel in NIVELES:
        print(f"  {nivel}: {conteo[nivel]}")

    # R8
    largo, inicio = sector.racha_saturacion()
    if largo == 0:
        print("El sector no tuvo ningún día en saturación.")
    else:
        print(f"Racha más larga en saturación: {dias_texto(largo)}, desde el {inicio.isoformat()}")

    # R15 (requisito propio): alerta de cierre temporal
    actual, desde_cuando = sector.racha_actual_saturacion()
    if sector.necesita_cierre():
        print(f"ALERTA: el sector necesita un cierre temporal. Lleva {dias_texto(actual)} seguidos "
              f"en saturación, desde el {desde_cuando.isoformat()}.")
    else:
        print(f"El sector no necesita cierre temporal (días seguidos en saturación al final del registro: "
              f"{actual}; el cierre se recomienda desde {DIAS_PARA_CIERRE}).")

    # R9
    ultimo = sector.ultimo_dia_registrado()
    print(f"Último día registrado: {ultimo.isoformat()}")
    faltan = sector.dias_sin_registrar(date.today())
    if faltan <= 0:
        print("El registro está al día.")
    else:
        desde = ultimo + timedelta(days=1)
        hasta = ultimo + timedelta(days=faltan)
        print(f"Faltan por registrar {dias_texto(faltan)}, del {desde.isoformat()} al {hasta.isoformat()}.")


# --- Opción 5 (R11) ------------------------------------------------------

def mostrar_mayor_y_menor_uso(reserva: Reserva) -> None:
    resultado = reserva.sectores_mayor_y_menor_uso()
    if resultado is None:
        print("Ningún sector tiene días registrados.")
        return
    mayor, menor = resultado
    print(f"Porcentaje de uso más alto: {mayor.nombre}, con {round(mayor.porcentaje_uso(), 2)} %")
    print(f"Porcentaje de uso más bajo: {menor.nombre}, con {round(menor.porcentaje_uso(), 2)} %")


# --- Opción 6 (R12 y R13) ------------------------------------------------

def mostrar_descartes(descartes: list[tuple[int, str]]) -> None:
    for numero, causa in descartes:
        print(f"Línea {numero} descartada: {causa}.")


def cargar_archivos(reserva: Reserva) -> None:
    if reserva.tiene_sectores():
        print("La carga solo se hace con el programa sin sectores.")
        return
    # Decisión: se separan tres causas para que el aviso diga qué pasó: la ruta no existe,
    # la ruta es una carpeta (en Windows llega como PermissionError) o el archivo no está
    # en UTF-8. En los tres casos el programa avisa y sigue, en vez de cerrarse.
    try:
        cargados, descartes = reserva.cargar_sectores(input("Ruta del archivo de sectores: "))
    except FileNotFoundError:
        print("El archivo no existe.")
        return
    except (IsADirectoryError, PermissionError):
        print("La ruta no es un archivo que se pueda leer.")
        return
    except UnicodeDecodeError:
        print("El archivo no está guardado en UTF-8.")
        return
    mostrar_descartes(descartes)
    print(f"Se cargó 1 sector." if cargados == 1 else f"Se cargaron {cargados} sectores.")

    try:
        cargados, descartes = reserva.cargar_visitantes(input("Ruta del archivo de visitantes: "))
    except FileNotFoundError:
        print("El archivo no existe. Los sectores quedan cargados, sin días registrados.")
        return
    except (IsADirectoryError, PermissionError):
        print("La ruta no es un archivo que se pueda leer. Los sectores quedan cargados, sin días registrados.")
        return
    except UnicodeDecodeError:
        print("El archivo no está guardado en UTF-8. Los sectores quedan cargados, sin días registrados.")
        return
    mostrar_descartes(descartes)
    print(f"Se cargaron {dias_texto(cargados)}.")


# --- Menú (R14) ----------------------------------------------------------

def menu() -> None:
    reserva = Reserva()
    while True:
        print()
        print("=== Reserva Natural Bahía Coralina ===")
        print("1. Crear un sector")
        print("2. Registrar los visitantes del día siguiente")
        print("3. Simular días")
        print("4. Ver el informe de un sector")
        print("5. Ver el sector con el porcentaje de uso más alto y el más bajo")
        print("6. Cargar los sectores y los visitantes desde archivos")
        print("7. Salir")
        opcion = input("Opción: ").strip()
        if opcion == "1":
            crear_sector(reserva)
        elif opcion == "2":
            registrar_dia(reserva)
        elif opcion == "3":
            simular_dias(reserva)
        elif opcion == "4":
            mostrar_informe(reserva)
        elif opcion == "5":
            mostrar_mayor_y_menor_uso(reserva)
        elif opcion == "6":
            cargar_archivos(reserva)
        elif opcion == "7":
            print("Hasta pronto.")
            break
        else:
            print("La opción no es válida.")
        # Decisión: se pausa antes de volver a mostrar el menú para que la persona alcance
        # a leer el resultado o el mensaje de error; sigue cuando presiona Enter.
        input("\nPresione Enter para volver al menú...")


if __name__ == "__main__":
    menu()
