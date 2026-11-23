"""Comprobación automática de business_logic.py con los casos del documento de análisis.

No reemplaza los casos de verificación de la entrega, que se comprueban
ejecutando user_interface.py. Sirve para detectar rápido si un cambio en la
lógica rompe un resultado esperado.

Uso: python verificar_logica.py
"""

import os
from datetime import date

from business_logic import Reserva, Sector

CARPETA = os.path.dirname(os.path.abspath(__file__))
fallos = 0


def caso(numero, obtenido, esperado):
    global fallos
    if obtenido == esperado:
        print(f"  ok   {numero}")
    else:
        fallos += 1
        print(f"  FALLA {numero}: se esperaba {esperado!r} y se obtuvo {obtenido!r}")


def error_de(funcion, *argumentos):
    """Devuelve el mensaje del ValueError que lanza la función, o None."""
    try:
        funcion(*argumentos)
    except ValueError as error:
        return str(error)
    return None


def sector_con(capacidad, visitantes, inicio=date(2026, 11, 1)):
    sector = Sector("Prueba", capacidad, inicio)
    for valor in visitantes:
        sector.registrar_dia(valor)
    return sector


print("R1. Crear un sector")
reserva = Reserva()
reserva.crear_sector("Mirador del Faro", "80", "2026", "11", "1")
caso("1.1", reserva.buscar_sector("Mirador del Faro").dias_registrados(), 0)
caso("1.2", error_de(reserva.crear_sector, "", "80", "2026", "11", "1"), "El nombre no puede estar vacío")
caso("1.3", error_de(reserva.crear_sector, "   ", "80", "2026", "11", "1"), "El nombre no puede estar vacío")
caso("1.4", error_de(reserva.crear_sector, "Mirador del Faro", "90", "2026", "11", "1"), "Ya existe un sector con ese nombre")
caso("1.4b", reserva.buscar_sector("Mirador del Faro").capacidad, 80)
caso("1.5", error_de(reserva.crear_sector, "A", "ochenta", "2026", "11", "1"), "La capacidad de carga debe ser un número entero")
caso("1.6", error_de(reserva.crear_sector, "A", "80.5", "2026", "11", "1"), "La capacidad de carga debe ser un número entero")
caso("1.7", error_de(reserva.crear_sector, "A", "0", "2026", "11", "1"), "La capacidad de carga debe ser de al menos un visitante")
caso("1.8", error_de(reserva.crear_sector, "A", "-5", "2026", "11", "1"), "La capacidad de carga debe ser de al menos un visitante")
caso("1.9", error_de(reserva.crear_sector, "A", "80", "2026", "11", "31"), "La fecha no es válida")
caso("1.10", error_de(reserva.crear_sector, "A", "80", "2026", "noviembre", "1"), "La fecha no es válida")
caso("1.11", error_de(reserva.crear_sector, "Bisiesto", "80", "2028", "2", "29"), None)
caso("1.12", error_de(reserva.crear_sector, "B", "80", "2026", "2", "29"), "La fecha no es válida")
caso("1.13", error_de(reserva.crear_sector, "A", "0", "2026", "11", "31"), "La capacidad de carga debe ser de al menos un visitante")

print("R2. Registrar el día siguiente")
faro = Sector("Mirador del Faro", 80, date(2026, 11, 1))
caso("2.1", faro.fecha_siguiente().isoformat(), "2026-11-01")
caso("2.2", error_de(faro.validar_visitantes, "x"), "Los visitantes deben ser un número entero")
caso("2.3", error_de(faro.validar_visitantes, "81"), "Los visitantes van de 0 a 80")
caso("2.4", error_de(faro.validar_visitantes, "-1"), "Los visitantes van de 0 a 80")
caso("2.5", faro.validar_visitantes("0"), 0)
caso("2.6", faro.validar_visitantes("80"), 80)
caso("2.7", sector_con(80, [1, 2, 3], date(2026, 12, 30)).fecha_siguiente().isoformat(), "2027-01-02")
caso("2.9", error_de(sector_con(80, [5], date(9999, 12, 31)).fecha_siguiente),
     "El registro ya llegó a la última fecha posible (9999-12-31)")

print("R3. Simular días")
simulado = Sector("Mirador del Faro", 80, date(2026, 11, 1))
simulado.simular_dias(3, 40, 80)
caso("3.1", simulado.dias_registrados() == 3 and all(40 <= v <= 80 for v in simulado.visitantes), True)
exacto = Sector("Exacto", 80, date(2026, 11, 1))
exacto.simular_dias(2, 50, 50)
caso("3.2", exacto.visitantes, [50, 50])
caso("3.3", error_de(reserva.validar_dias_simulados, "tres"), "El número de días debe ser un número entero")
caso("3.4", error_de(reserva.validar_dias_simulados, "0"), "Se debe simular al menos un día")
vacio = Sector("Vacío", 80, date(2026, 11, 1))
caso("3.8", error_de(vacio.simular_dias, 3, 60, 40), "El mínimo no puede ser mayor que el máximo")
caso("3.8b", vacio.dias_registrados(), 0)
continua = sector_con(80, [10, 20])
continua.simular_dias(3, 0, 80)
caso("3.9", continua.ultimo_dia_registrado().isoformat(), "2026-11-05")

playa = sector_con(600, [420, 555, 600, 290, 540])
sendero = sector_con(150, [90, 120, 150, 60])
uno = sector_con(80, [52])

print("R4. Informe")
caso("4.1", (playa.dias_registrados(), playa.total_visitantes(), round(playa.promedio(), 2), round(playa.porcentaje_uso(), 2)), (5, 2405, 481.0, 80.17))
caso("4.2", (sendero.dias_registrados(), sendero.total_visitantes(), round(sendero.promedio(), 2), round(sendero.porcentaje_uso(), 2)), (4, 420, 105.0, 70.0))
caso("4.3", (round(uno.promedio(), 2), round(uno.porcentaje_uso(), 2)), (52.0, 65.0))
caso("4.4", (round(sector_con(3, [1, 1, 2]).promedio(), 2), round(sector_con(3, [1, 1, 2]).porcentaje_uso(), 2)), (1.33, 44.44))

print("R5. Desviación estándar")
caso("5.1", round(playa.desviacion_estandar(), 2), 112.53)
caso("5.2", round(sendero.desviacion_estandar(), 2), 33.54)
caso("5.3", round(uno.desviacion_estandar(), 2), 0.0)
caso("5.4", round(sector_con(200, [100, 100, 100]).desviacion_estandar(), 2), 0.0)
caso("5.5", round(sector_con(3, [1, 1, 2]).desviacion_estandar(), 2), 0.47)

print("R6. Día de más y de menos visitantes")
caso("6.1", (playa.dia_mas_visitantes().isoformat(), playa.dia_menos_visitantes().isoformat()), ("2026-11-03", "2026-11-04"))
caso("6.2", (sendero.dia_mas_visitantes().isoformat(), sendero.dia_menos_visitantes().isoformat()), ("2026-11-03", "2026-11-04"))
empates = sector_con(600, [300, 600, 600, 120, 120])
caso("6.3", (empates.dia_mas_visitantes().isoformat(), empates.dia_menos_visitantes().isoformat()), ("2026-11-02", "2026-11-04"))
caso("6.4", (uno.dia_mas_visitantes().isoformat(), uno.dia_menos_visitantes().isoformat()), ("2026-11-01", "2026-11-01"))

print("R7. Días en cada nivel de presión")
caso("7.1", list(sector_con(600, [299, 300, 449, 450, 539, 540]).dias_por_nivel().values()), [1, 2, 2, 1])
caso("7.2", list(playa.dias_por_nivel().values()), [1, 1, 0, 3])
caso("7.3", list(sendero.dias_por_nivel().values()), [1, 1, 1, 1])
caso("7.4", list(sector_con(80, [0, 80]).dias_por_nivel().values()), [1, 0, 0, 1])
caso("7.5", list(sector_con(1, [0, 1]).dias_por_nivel().values()), [1, 0, 0, 1])

print("R8. Racha más larga en saturación")
caso("8.1", playa.racha_saturacion(), (2, date(2026, 11, 2)))
caso("8.2", sector_con(600, [560, 570, 400, 545, 600, 590, 100]).racha_saturacion(), (3, date(2026, 11, 4)))
caso("8.3", sector_con(600, [560, 570, 100, 545, 600]).racha_saturacion(), (2, date(2026, 11, 1)))
caso("8.4", sector_con(600, [100, 560, 570, 580]).racha_saturacion(), (3, date(2026, 11, 2)))
caso("8.5", sector_con(600, [540, 540, 540]).racha_saturacion(), (3, date(2026, 11, 1)))
caso("8.6", uno.racha_saturacion(), (0, None))

print("R15. Alerta de cierre temporal (requisito propio)")
caso("15.1", (playa.racha_actual_saturacion()[0], playa.necesita_cierre()), (1, False))
caso("15.2", (sector_con(600, [100, 560, 570, 580]).racha_actual_saturacion(), sector_con(600, [100, 560, 570, 580]).necesita_cierre()),
     ((3, date(2026, 11, 2)), True))
caso("15.3", sector_con(600, [560, 570, 580, 100]).racha_actual_saturacion(), (0, None))
caso("15.4", sector_con(600, [100, 560, 570]).necesita_cierre(), False)
caso("15.5", sector_con(600, [540] * 5).racha_actual_saturacion(), (5, date(2026, 11, 1)))
caso("15.6", sector_con(80, [72, 72, 72]).necesita_cierre(), True)
caso("15.7", sector_con(600, [560, 570, 539, 580, 590]).racha_actual_saturacion()[0], 2)

print("R9. Días sin registrar")
caso("9.1", playa.dias_sin_registrar(date(2026, 11, 20)), 14)
caso("9.2", uno.dias_sin_registrar(date(2026, 11, 2)) <= 0, True)
caso("9.3", uno.dias_sin_registrar(date(2026, 11, 3)), 1)
caso("9.4", playa.dias_sin_registrar(date(2026, 11, 4)) <= 0, True)
caso("9.5", sector_con(80, [1, 2, 3], date(2026, 12, 30)).dias_sin_registrar(date(2027, 1, 5)), 3)

print("R10. Búsqueda por nombre")
varios = Reserva()
varios.crear_sector("Playa Brava", "600", "2026", "11", "1")
varios.crear_sector("Cueva del Murciélago", "40", "2026", "11", "1")
caso("10.2", varios.buscar_sector("Isla del Pirata"), None)
caso("10.3", varios.buscar_sector("playa brava"), None)
caso("10.4", varios.buscar_sector("Cueva del Murcielago"), None)
caso("10.5", varios.buscar_sector("  Playa Brava  ").nombre, "Playa Brava")

print("R11. Porcentaje de uso más alto y más bajo")
comparar = Reserva()
caso("11.2", comparar.sectores_mayor_y_menor_uso(), None)
for nombre, capacidad, valores in [("Playa Brava", "600", [420, 555, 600, 290, 540]),
                                   ("Sendero de los Mangles", "150", [90, 120, 150, 60]),
                                   ("Mirador del Faro", "80", [52]),
                                   ("Cueva del Murciélago", "40", [])]:
    sector = comparar.crear_sector(nombre, capacidad, "2026", "11", "1")
    for valor in valores:
        sector.registrar_dia(valor)
mayor, menor = comparar.sectores_mayor_y_menor_uso()
caso("11.1", (mayor.nombre, menor.nombre), ("Playa Brava", "Mirador del Faro"))
solo_cueva = Reserva()
solo_cueva.crear_sector("Cueva del Murciélago", "40", "2026", "11", "1")
caso("11.3", solo_cueva.sectores_mayor_y_menor_uso(), None)
empate = Reserva()
empate.crear_sector("A", "100", "2026", "11", "1").registrar_dia(50)
empate.crear_sector("B", "10", "2026", "11", "1").registrar_dia(5)
mayor, menor = empate.sectores_mayor_y_menor_uso()
caso("11.4", (mayor.nombre, menor.nombre), ("A", "A"))
redondeo = Reserva()
redondeo.crear_sector("A", "3", "2026", "11", "1").registrar_dia(2)
redondeo.crear_sector("C", "10000", "2026", "11", "1").registrar_dia(6667)
mayor, menor = redondeo.sectores_mayor_y_menor_uso()
caso("11.6", (mayor.nombre, menor.nombre), ("C", "A"))

print("R12 y R13. Carga desde archivos")
archivos = Reserva()
cargados, descartes = archivos.cargar_sectores(os.path.join(CARPETA, "datos", "sectores.csv"))
caso("12.1", (cargados, list(archivos.sectores)), (2, ["Playa Brava", "Sendero de los Mangles"]))
caso("12.2-12.6", descartes, [
    (4, "La capacidad de carga debe ser de al menos un visitante"),
    (5, "No tiene cinco campos"),
    (6, "La capacidad de carga debe ser un número entero"),
    (7, "Ya existe un sector con ese nombre"),
    (8, "La fecha no es válida"),
])
cargados, descartes = archivos.cargar_visitantes(os.path.join(CARPETA, "datos", "visitantes.csv"))
caso("13.1", (cargados, archivos.buscar_sector("Playa Brava").visitantes, archivos.buscar_sector("Sendero de los Mangles").visitantes),
     (9, [420, 555, 600, 290, 540], [90, 120, 150, 60]))
caso("13.2-13.6", [numero for numero, _ in descartes], [10, 12, 13, 14, 15])
try:
    Reserva().cargar_sectores(os.path.join(CARPETA, "datos", "no_existe.csv"))
    caso("12.7", "no lanzó error", "FileNotFoundError")
except FileNotFoundError:
    caso("12.7", "FileNotFoundError", "FileNotFoundError")
try:
    Reserva().cargar_sectores(os.path.join(CARPETA, "datos"))
    caso("12.14", "no lanzó error", "IsADirectoryError o PermissionError")
except (IsADirectoryError, PermissionError):
    caso("12.14", "IsADirectoryError o PermissionError", "IsADirectoryError o PermissionError")
try:
    Reserva().cargar_sectores(os.path.join(CARPETA, "datos", "pruebas", "sectores_ansi.csv"))
    caso("12.15", "no lanzó error", "UnicodeDecodeError")
except UnicodeDecodeError:
    caso("12.15", "UnicodeDecodeError", "UnicodeDecodeError")

print()
print("Todos los casos pasaron." if fallos == 0 else f"{fallos} caso(s) fallaron.")
