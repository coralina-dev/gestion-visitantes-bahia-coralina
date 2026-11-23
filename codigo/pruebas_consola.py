"""Casos de verificación de la entrega, comprobados ejecutando user_interface.py.

Cada caso dice qué se teclea en la consola y qué debe aparecer en pantalla.
Este script ejecuta user_interface.py con esas entradas, revisa la salida y
escribe el resultado en casos_de_verificacion.md.

Uso, desde la carpeta codigo:
    python pruebas_consola.py          ejecuta todos los casos
    python pruebas_consola.py 8.2      ejecuta solo ese caso y muestra la consola
"""

import os
import subprocess
import sys
from datetime import date, timedelta

CARPETA = os.path.dirname(os.path.abspath(__file__))
HOY = date.today()

# --- Entradas que se repiten -------------------------------------------------

# Cada opción termina con "" porque, después de atenderla, el programa espera un Enter
# ("Presione Enter para volver al menú...") antes de volver a mostrar el menú.
CARGAR = ["6", "datos/sectores.csv", "datos/visitantes.csv", ""]
CREAR_FARO = ["1", "Mirador del Faro", "80", "2026", "11", "1", ""]


def crear(nombre, capacidad, fecha=(2026, 11, 1)):
    return ["1", nombre, str(capacidad), str(fecha[0]), str(fecha[1]), str(fecha[2]), ""]


def registrar(nombre, *valores):
    entradas = []
    for valor in valores:
        entradas += ["2", nombre, str(valor), ""]
    return entradas


def informe(nombre):
    return ["4", nombre, ""]


def dias_texto(cantidad):
    return f"{cantidad} día" if cantidad == 1 else f"{cantidad} días"


def fecha_tupla(fecha):
    return (fecha.year, fecha.month, fecha.day)


# R9 depende de la fecha en que se ejecuta el programa.
ULTIMO_PLAYA = date(2026, 11, 5)
FALTAN_PLAYA = (HOY - ULTIMO_PLAYA).days - 1
if FALTAN_PLAYA <= 0:
    ESPERADO_9_1 = "El registro está al día."
else:
    ESPERADO_9_1 = (f"Faltan por registrar {dias_texto(FALTAN_PLAYA)}, del 2026-11-06 "
                    f"al {(HOY - timedelta(days=1)).isoformat()}.")
AYER = HOY - timedelta(days=1)
ANTEAYER = HOY - timedelta(days=2)

# --- Los casos -------------------------------------------------------------------
# Cada caso: id, requisito, qué prueba, entradas, textos que deben aparecer
# y, opcionalmente, textos que NO deben aparecer.

CASOS = [
    # R1. Crear un sector
    ("1.1", "R1", "Crear un sector válido; queda sin días",
     CREAR_FARO + informe("Mirador del Faro"),
     ["Se creó el sector Mirador del Faro, sin días registrados.", "El sector no tiene días registrados."], []),
    ("1.2", "R1", "Nombre vacío", ["1", "", "80", "2026", "11", "1", ""],
     ["El nombre no puede estar vacío."], ["Se creó"]),
    ("1.3", "R1", "Nombre con solo espacios", ["1", "   ", "80", "2026", "11", "1", ""],
     ["El nombre no puede estar vacío."], ["Se creó"]),
    ("1.4", "R1", "Nombre repetido; el sector original no cambia",
     CREAR_FARO + crear("Mirador del Faro", 90) + informe("Mirador del Faro"),
     ["Ya existe un sector con ese nombre.", "Capacidad de carga: 80 visitantes"], []),
    ("1.5", "R1", "Capacidad escrita en letras", ["1", "Mirador del Faro", "ochenta", "2026", "11", "1", ""],
     ["La capacidad de carga debe ser un número entero."], ["Se creó"]),
    ("1.6", "R1", "Capacidad con decimales", ["1", "Mirador del Faro", "80.5", "2026", "11", "1", ""],
     ["La capacidad de carga debe ser un número entero."], ["Se creó"]),
    ("1.7", "R1", "Capacidad 0", ["1", "Mirador del Faro", "0", "2026", "11", "1", ""],
     ["La capacidad de carga debe ser de al menos un visitante."], ["Se creó"]),
    ("1.8", "R1", "Capacidad negativa", ["1", "Mirador del Faro", "-5", "2026", "11", "1", ""],
     ["La capacidad de carga debe ser de al menos un visitante."], ["Se creó"]),
    ("1.9", "R1", "Fecha que no existe (31 de noviembre)", ["1", "Mirador del Faro", "80", "2026", "11", "31", ""],
     ["La fecha no es válida."], ["Se creó"]),
    ("1.10", "R1", "Mes escrito en letras", ["1", "Mirador del Faro", "80", "2026", "noviembre", "1", ""],
     ["La fecha no es válida."], ["Se creó"]),
    ("1.11", "R1", "29 de febrero de un año bisiesto", crear("Mirador del Faro", 80, (2028, 2, 29)),
     ["Se creó el sector Mirador del Faro"], []),
    ("1.12", "R1", "29 de febrero de un año no bisiesto", crear("Mirador del Faro", 80, (2026, 2, 29)),
     ["La fecha no es válida."], ["Se creó"]),
    ("1.13", "R1", "Dos datos malos: solo se avisa el primero", ["1", "Mirador del Faro", "0", "2026", "11", "31", ""],
     ["La capacidad de carga debe ser de al menos un visitante."], ["La fecha no es válida."]),
    ("1.14", "R1", "Capacidad mínima válida (1)", crear("Mirador del Faro", 1),
     ["Se creó el sector Mirador del Faro, sin días registrados."], []),

    # R2. Registrar los visitantes del día siguiente
    ("2.1", "R2", "Primer día de un sector nuevo", CREAR_FARO + registrar("Mirador del Faro", 52),
     ["Día por registrar: 2026-11-01", "Se registraron 52 visitantes el 2026-11-01."], []),
    ("2.2", "R2", "Visitantes en letras: vuelve a preguntar", CREAR_FARO + ["2", "Mirador del Faro", "x", "52", ""],
     ["Los visitantes deben ser un número entero.", "Se registraron 52 visitantes el 2026-11-01."], []),
    ("2.3", "R2", "Más que la capacidad: vuelve a preguntar", CREAR_FARO + ["2", "Mirador del Faro", "81", "52", ""],
     ["Los visitantes van de 0 a 80.", "Se registraron 52 visitantes"], []),
    ("2.4", "R2", "Negativo: vuelve a preguntar", CREAR_FARO + ["2", "Mirador del Faro", "-1", "52", ""],
     ["Los visitantes van de 0 a 80.", "Se registraron 52 visitantes"], []),
    ("2.5", "R2", "Límite inferior válido (0)", CREAR_FARO + registrar("Mirador del Faro", 0),
     ["Se registraron 0 visitantes el 2026-11-01."], []),
    ("2.6", "R2", "Límite superior válido (la capacidad)", CREAR_FARO + registrar("Mirador del Faro", 80),
     ["Se registraron 80 visitantes el 2026-11-01."], []),
    ("2.7", "R2", "El día siguiente cambia de año",
     crear("Cambio de Año", 100, (2026, 12, 30)) + registrar("Cambio de Año", 1, 1, 1) + ["2", "Cambio de Año", "5", ""],
     ["Día por registrar: 2027-01-02"], []),
    ("2.8", "R2", "Sector que no existe", ["2", "Isla del Pirata", ""],
     ["No hay un sector con ese nombre."], ["Día por registrar"]),
    ("2.9", "R2", "El registro ya llegó al 9999-12-31: avisa y no se cierra",
     crear("Fin", 80, (9999, 12, 31)) + registrar("Fin", 5) + ["2", "Fin", ""],
     ["El registro ya llegó a la última fecha posible (9999-12-31)."], ["Traceback"]),

    # R3. Simular días
    ("3.1", "R3", "Simular 3 días entre 40 y 80",
     CREAR_FARO + ["3", "Mirador del Faro", "3", "40", "80", ""] + informe("Mirador del Faro"),
     ["Se simularon 3 días, del 2026-11-01 al 2026-11-03.", "Días registrados: 3"], []),
    ("3.2", "R3", "Mínimo igual al máximo: resultado exacto",
     CREAR_FARO + ["3", "Mirador del Faro", "2", "50", "50", ""] + informe("Mirador del Faro"),
     ["Visitantes totales: 100", "Desviación estándar: 0.0"], []),
    ("3.3", "R3", "Días en letras: no pide el mínimo", CREAR_FARO + ["3", "Mirador del Faro", "tres", ""],
     ["El número de días debe ser un número entero."], ["Visitantes mínimos"]),
    ("3.4", "R3", "0 días: no pide el mínimo ni el máximo", CREAR_FARO + ["3", "Mirador del Faro", "0", ""],
     ["Se debe simular al menos un día."], ["Visitantes mínimos"]),
    ("3.5", "R3", "Mínimo en letras: no pide el máximo", CREAR_FARO + ["3", "Mirador del Faro", "3", "x", ""],
     ["Los visitantes deben ser un número entero."], ["Visitantes máximos"]),
    ("3.6", "R3", "Mínimo negativo: no pide el máximo", CREAR_FARO + ["3", "Mirador del Faro", "3", "-1", ""],
     ["Los visitantes van de 0 a 80."], ["Visitantes máximos"]),
    ("3.7", "R3", "Máximo mayor que la capacidad: no agrega días",
     CREAR_FARO + ["3", "Mirador del Faro", "3", "40", "81", ""] + informe("Mirador del Faro"),
     ["Los visitantes van de 0 a 80.", "El sector no tiene días registrados."], ["Se simularon"]),
    ("3.8", "R3", "Mínimo mayor que el máximo: no agrega días",
     CREAR_FARO + ["3", "Mirador del Faro", "3", "60", "40", ""] + informe("Mirador del Faro"),
     ["El mínimo no puede ser mayor que el máximo.", "El sector no tiene días registrados."], ["Se simularon"]),
    ("3.9", "R3", "La simulación continúa el registro",
     CREAR_FARO + registrar("Mirador del Faro", 10, 20) + ["3", "Mirador del Faro", "3", "0", "80", ""],
     ["Se simularon 3 días, del 2026-11-03 al 2026-11-05."], []),
    ("3.10", "R3", "Sector que no existe", ["3", "Isla del Pirata", ""],
     ["No hay un sector con ese nombre."], ["Número de días"]),

    # R4. Informe
    ("4.1", "R4", "Informe de Playa Brava cargada desde archivo", CARGAR + informe("Playa Brava"),
     ["Sector: Playa Brava", "Capacidad de carga: 600 visitantes", "Días registrados: 5",
      "Visitantes totales: 2405", "Promedio de visitantes por día: 481.0", "Porcentaje de uso: 80.17 %"], []),
    ("4.2", "R4", "Informe del Sendero de los Mangles", CARGAR + informe("Sendero de los Mangles"),
     ["Días registrados: 4", "Visitantes totales: 420", "Promedio de visitantes por día: 105.0",
      "Porcentaje de uso: 70.0 %"], []),
    ("4.3", "R4", "Un solo día: el porcentaje se muestra como 65.0",
     CREAR_FARO + registrar("Mirador del Faro", 52) + informe("Mirador del Faro"),
     ["Promedio de visitantes por día: 52.0", "Porcentaje de uso: 65.0 %"], []),
    ("4.4", "R4", "Redondeo a dos decimales", crear("Prueba", 3) + registrar("Prueba", 1, 1, 2) + informe("Prueba"),
     ["Promedio de visitantes por día: 1.33", "Porcentaje de uso: 44.44 %"], []),
    ("4.5", "R4", "Sector sin días: solo nombre, capacidad y aviso",
     crear("Cueva del Murciélago", 40) + informe("Cueva del Murciélago"),
     ["Sector: Cueva del Murciélago", "Capacidad de carga: 40 visitantes", "El sector no tiene días registrados."],
     ["Días registrados:"]),

    # R5. Desviación estándar
    ("5.1", "R5", "Playa Brava", CARGAR + informe("Playa Brava"), ["Desviación estándar: 112.53"], []),
    ("5.2", "R5", "Sendero de los Mangles", CARGAR + informe("Sendero de los Mangles"),
     ["Desviación estándar: 33.54"], []),
    ("5.3", "R5", "Un solo día", CREAR_FARO + registrar("Mirador del Faro", 52) + informe("Mirador del Faro"),
     ["Desviación estándar: 0.0"], []),
    ("5.5", "R5", "Promedio no entero", crear("Prueba", 3) + registrar("Prueba", 1, 1, 2) + informe("Prueba"),
     ["Desviación estándar: 0.47"], []),

    # R6. Día de más y de menos visitantes
    ("6.1", "R6", "Playa Brava", CARGAR + informe("Playa Brava"),
     ["Día con más visitantes: 2026-11-03", "Día con menos visitantes: 2026-11-04"], []),
    ("6.3", "R6", "Empates: gana el primero",
     crear("Empates", 600) + registrar("Empates", 300, 600, 600, 120, 120) + informe("Empates"),
     ["Día con más visitantes: 2026-11-02", "Día con menos visitantes: 2026-11-04"], []),
    ("6.4", "R6", "Un solo día", CREAR_FARO + registrar("Mirador del Faro", 52) + informe("Mirador del Faro"),
     ["Día con más visitantes: 2026-11-01", "Día con menos visitantes: 2026-11-01"], []),

    # R7. Días en cada nivel de presión
    ("7.1", "R7", "Los seis límites entre niveles (capacidad 600)",
     crear("Limites", 600) + registrar("Limites", 299, 300, 449, 450, 539, 540) + informe("Limites"),
     ["baja: 1", "moderada: 2", "alta: 2", "saturación: 1"], []),
    ("7.2", "R7", "Playa Brava: un nivel con 0 días también se muestra", CARGAR + informe("Playa Brava"),
     ["baja: 1", "moderada: 1", "alta: 0", "saturación: 3"], []),
    ("7.3", "R7", "Sendero de los Mangles", CARGAR + informe("Sendero de los Mangles"),
     ["baja: 1", "moderada: 1", "alta: 1", "saturación: 1"], []),

    # R8. Racha más larga en saturación
    ("8.1", "R8", "Playa Brava", CARGAR + informe("Playa Brava"),
     ["Racha más larga en saturación: 2 días, desde el 2026-11-02"], []),
    ("8.2", "R8", "La segunda racha es más larga",
     crear("Rachas", 600) + registrar("Rachas", 560, 570, 400, 545, 600, 590, 100) + informe("Rachas"),
     ["Racha más larga en saturación: 3 días, desde el 2026-11-04"], []),
    ("8.3", "R8", "Dos rachas empatadas: gana la primera",
     crear("Rachas", 600) + registrar("Rachas", 560, 570, 100, 545, 600) + informe("Rachas"),
     ["Racha más larga en saturación: 2 días, desde el 2026-11-01"], []),
    ("8.4", "R8", "La racha llega hasta el último día",
     crear("Rachas", 600) + registrar("Rachas", 100, 560, 570, 580) + informe("Rachas"),
     ["Racha más larga en saturación: 3 días, desde el 2026-11-02"], []),
    ("8.6", "R8", "Ningún día en saturación",
     CREAR_FARO + registrar("Mirador del Faro", 52) + informe("Mirador del Faro"),
     ["El sector no tuvo ningún día en saturación."], ["Racha más larga"]),

    # R15. Requisito propio: alerta de cierre temporal (DIAS_PARA_CIERRE = 3)
    ("15.1", "R15", "Playa Brava: termina con 1 día en saturación, no necesita cierre",
     CARGAR + informe("Playa Brava"),
     ["El sector no necesita cierre temporal (días seguidos en saturación al final del registro: 1; el cierre se recomienda desde 3)."],
     ["ALERTA"]),
    ("15.2", "R15", "Los últimos 3 días en saturación: alerta",
     crear("Cierre", 600) + registrar("Cierre", 100, 560, 570, 580) + informe("Cierre"),
     ["ALERTA: el sector necesita un cierre temporal. Lleva 3 días seguidos en saturación, desde el 2026-11-02."],
     []),
    ("15.3", "R15", "Hubo una racha de 3, pero el último día no está en saturación: sin alerta",
     crear("Cierre", 600) + registrar("Cierre", 560, 570, 580, 100) + informe("Cierre"),
     ["Racha más larga en saturación: 3 días, desde el 2026-11-01",
      "El sector no necesita cierre temporal (días seguidos en saturación al final del registro: 0;"], ["ALERTA"]),
    ("15.4", "R15", "Justo debajo del límite (2 días): sin alerta",
     crear("Cierre", 600) + registrar("Cierre", 100, 560, 570) + informe("Cierre"),
     ["El sector no necesita cierre temporal (días seguidos en saturación al final del registro: 2;"], ["ALERTA"]),
    ("15.5", "R15", "Todos los días en saturación: la racha empieza el primer día",
     crear("Cierre", 600) + registrar("Cierre", 540, 540, 540, 540, 540) + informe("Cierre"),
     ["ALERTA: el sector necesita un cierre temporal. Lleva 5 días seguidos en saturación, desde el 2026-11-01."],
     []),
    ("15.6", "R15", "Justo en el límite de saturación (90 %) cuenta",
     crear("Cierre", 80) + registrar("Cierre", 72, 72, 72) + informe("Cierre"),
     ["ALERTA: el sector necesita un cierre temporal. Lleva 3 días seguidos"], []),
    ("15.7", "R15", "Un día en presión alta corta la racha",
     crear("Cierre", 600) + registrar("Cierre", 560, 570, 539, 580, 590) + informe("Cierre"),
     ["El sector no necesita cierre temporal (días seguidos en saturación al final del registro: 2;"], ["ALERTA"]),

    # R9. Días sin registrar (depende de la fecha de hoy)
    ("9.1", "R9", "Playa Brava, con la fecha de hoy", CARGAR + informe("Playa Brava"),
     ["Último día registrado: 2026-11-05", ESPERADO_9_1], []),
    ("9.2", "R9", "Último día registrado = ayer: al día",
     crear("Hoy", 80, fecha_tupla(AYER)) + registrar("Hoy", 10) + informe("Hoy"),
     ["El registro está al día."], ["Faltan por registrar"]),
    ("9.3", "R9", "Falta exactamente un día",
     crear("Hoy", 80, fecha_tupla(ANTEAYER)) + registrar("Hoy", 10) + informe("Hoy"),
     [f"Faltan por registrar 1 día, del {AYER.isoformat()} al {AYER.isoformat()}."], []),
    ("9.4", "R9", "Último día = hoy (posible al simular): al día",
     crear("Hoy", 80, fecha_tupla(HOY)) + registrar("Hoy", 10) + informe("Hoy"),
     ["El registro está al día."], ["Faltan por registrar"]),

    # R10. Varios sectores y búsqueda por nombre
    ("10.1", "R10", "Cada sector muestra sus propios datos",
     CARGAR + informe("Playa Brava") + informe("Sendero de los Mangles"),
     ["Visitantes totales: 2405", "Visitantes totales: 420"], []),
    ("10.2", "R10", "Nombre que no existe", CARGAR + informe("Isla del Pirata"),
     ["No hay un sector con ese nombre."], []),
    ("10.3", "R10", "Distinto en mayúsculas", CARGAR + informe("playa brava"),
     ["No hay un sector con ese nombre."], ["Sector: Playa Brava"]),
    ("10.4", "R10", "Distinto en tildes", crear("Cueva del Murciélago", 40) + informe("Cueva del Murcielago"),
     ["No hay un sector con ese nombre."], []),
    ("10.5", "R10", "Espacios alrededor del nombre", CARGAR + informe("   Playa Brava   "),
     ["Sector: Playa Brava"], []),

    # R11. Porcentaje de uso más alto y más bajo
    ("11.1", "R11", "Varios sectores; uno sin días se ignora",
     CARGAR + CREAR_FARO + registrar("Mirador del Faro", 52) + crear("Cueva del Murciélago", 40) + ["5", ""],
     ["Porcentaje de uso más alto: Playa Brava, con 80.17 %",
      "Porcentaje de uso más bajo: Mirador del Faro, con 65.0 %"], []),
    ("11.2", "R11", "Sin sectores", ["5", ""], ["Ningún sector tiene días registrados."], []),
    ("11.3", "R11", "Solo sectores sin días", crear("Cueva del Murciélago", 40) + ["5", ""],
     ["Ningún sector tiene días registrados."], []),
    ("11.4", "R11", "Empate: gana el que se creó primero",
     crear("A", 100) + registrar("A", 50) + crear("B", 10) + registrar("B", 5) + ["5", ""],
     ["Porcentaje de uso más alto: A, con 50.0 %", "Porcentaje de uso más bajo: A, con 50.0 %"], []),
    ("11.6", "R11", "Se compara sin redondear (los dos se muestran 66.67)",
     crear("A", 3) + registrar("A", 2) + crear("C", 10000) + registrar("C", 6667) + ["5", ""],
     ["Porcentaje de uso más alto: C, con 66.67 %", "Porcentaje de uso más bajo: A, con 66.67 %"], []),

    # R12. Cargar sectores desde archivo
    ("12.1", "R12", "Archivo del enunciado: carga 2 y descarta 5", CARGAR,
     ["Línea 4 descartada: La capacidad de carga debe ser de al menos un visitante.",
      "Línea 5 descartada: No tiene cinco campos.",
      "Línea 6 descartada: La capacidad de carga debe ser un número entero.",
      "Línea 7 descartada: Ya existe un sector con ese nombre.",
      "Línea 8 descartada: La fecha no es válida.",
      "Se cargaron 2 sectores."], []),
    ("12.7", "R12", "El archivo de sectores no existe: no pide el de visitantes",
     ["6", "datos/no_existe.csv", ""], ["El archivo no existe."], ["Ruta del archivo de visitantes"]),
    ("12.8", "R12", "Ya hay sectores: no pide ninguna ruta", CREAR_FARO + ["6", ""],
     ["La carga solo se hace con el programa sin sectores."], ["Ruta del archivo de sectores"]),
    ("12.9", "R12", "Espacios en los campos, líneas vacías y una línea con 6 campos",
     ["6", "datos/pruebas/sectores_casos_borde.csv", "datos/pruebas/solo_encabezado_visitantes.csv", ""]
     + informe("Isla Verde"),
     ["Línea 4 descartada: No tiene cinco campos.", "Se cargaron 2 sectores.", "Sector: Isla Verde",
      "Capacidad de carga: 50 visitantes"], ["Línea 3", "Línea 5"]),
    ("12.12", "R12", "Archivo de sectores con solo el encabezado",
     ["6", "datos/pruebas/solo_encabezado_sectores.csv", "datos/pruebas/solo_encabezado_visitantes.csv", ""],
     ["Se cargaron 0 sectores.", "Se cargaron 0 días."], []),
    ("12.13", "R12", "Archivo guardado por Excel con BOM al inicio",
     ["6", "datos/pruebas/sectores_con_bom.csv", "datos/pruebas/solo_encabezado_visitantes.csv", ""]
     + informe("Playa Brava"),
     ["Se cargó 1 sector.", "Sector: Playa Brava"], ["descartada"]),
    ("12.14", "R12", "La ruta es una carpeta: avisa y no se cierra", ["6", "datos", ""],
     ["La ruta no es un archivo que se pueda leer."], ["Ruta del archivo de visitantes", "Traceback"]),
    ("12.15", "R12", "Archivo que no está en UTF-8: avisa y no se cierra",
     ["6", "datos/pruebas/sectores_ansi.csv", ""],
     ["El archivo no está guardado en UTF-8."], ["Se cargaron", "Traceback"]),

    # R13. Cargar visitantes desde archivo
    ("13.1", "R13", "Archivo del enunciado: carga 9 días y descarta 5", CARGAR,
     ["Línea 10 descartada: Sendero de los Mangles: Los visitantes van de 0 a 150.",
      "Línea 12 descartada: No hay un sector llamado Laguna Grande.",
      "Línea 13 descartada: Playa Brava: Los visitantes van de 0 a 600.",
      "Línea 14 descartada: Playa Brava: Los visitantes deben ser un número entero.",
      "Línea 15 descartada: No tiene dos campos.",
      "Se cargaron 9 días."], []),
    ("13.7", "R13", "El archivo de visitantes no existe: los sectores quedan sin días",
     ["6", "datos/sectores.csv", "datos/no_existe.csv", ""] + informe("Playa Brava"),
     ["El archivo no existe. Los sectores quedan cargados, sin días registrados.",
      "El sector no tiene días registrados."], []),
    ("13.9", "R13", "Una segunda carga no duplica los días", CARGAR + ["6", ""] + informe("Playa Brava"),
     ["La carga solo se hace con el programa sin sectores.", "Días registrados: 5"], []),

    # R14. Menú
    ("14.1", "R14", "Después de una opción pausa y vuelve a mostrar el menú", CREAR_FARO,
     ["Se creó el sector", "Presione Enter para volver al menú...", "Opción: Hasta pronto."], []),
    ("14.2", "R14", "Opción fuera de rango (8)", ["8", ""], ["La opción no es válida."], []),
    ("14.3", "R14", "Opción en letras (dos)", ["dos", ""], ["La opción no es válida."], []),
    ("14.4", "R14", "Opción 0", ["0", ""], ["La opción no es válida."], []),
    ("14.5", "R14", "Enter sin escribir nada", ["", ""], ["La opción no es válida."], []),
    ("14.6", "R14", "Salir", [], ["Hasta pronto."], []),
]


def ejecutar(entradas):
    """Ejecuta user_interface.py tecleando las entradas y luego 7 (salir), que no tiene pausa."""
    texto = "\n".join(entradas + ["7"]) + "\n"
    entorno = dict(os.environ, PYTHONIOENCODING="utf-8")
    proceso = subprocess.run([sys.executable, "user_interface.py"], input=texto, capture_output=True,
                             text=True, encoding="utf-8", cwd=CARPETA, env=entorno, timeout=20)
    return proceso.stdout + proceso.stderr


def revisar(caso):
    _, _, _, entradas, esperado, no_esperado = caso
    salida = ejecutar(entradas)
    faltan = [texto for texto in esperado if texto not in salida]
    sobran = [texto for texto in no_esperado if texto in salida]
    return faltan, sobran, salida


def mostrar_entradas(entradas):
    partes = ["(Enter)" if e == "" else f"`{e}`" for e in entradas + ["7"]]
    return " → ".join(partes)


def escribir_markdown(resultados):
    lineas = [
        "# Casos de verificación de la entrega",
        "",
        "Cada caso se comprueba ejecutando `user_interface.py` desde la carpeta `codigo`, tecleando las entradas "
        "en orden (cada flecha es un Enter). El archivo lo genera `pruebas_consola.py`, que ejecuta el programa "
        "con esas mismas entradas y revisa la salida.",
        "",
        f"**Última ejecución:** {HOY.isoformat()}. **Resultado:** "
        f"{sum(1 for r in resultados if r[1])} de {len(resultados)} casos correctos.",
        "",
        "Los casos de R9 dependen de la fecha en que se ejecuta el programa; su salida esperada se calculó con la "
        "fecha de la última ejecución.",
        "",
    ]
    requisito_actual = None
    for caso, correcto in resultados:
        numero, requisito, descripcion, entradas, esperado, no_esperado = caso
        if requisito != requisito_actual:
            requisito_actual = requisito
            lineas += [f"## {requisito}", "",
                       "| # | Qué se prueba | Qué se teclea | Qué debe aparecer | Qué no debe aparecer | ¿Pasa? |",
                       "| --- | --- | --- | --- | --- | --- |"]
        debe = "<br>".join(esperado)
        no_debe = "<br>".join(no_esperado) if no_esperado else "—"
        lineas.append(f"| {numero} | {descripcion} | {mostrar_entradas(entradas)} | {debe} | {no_debe} | "
                      f"{'✅' if correcto else '❌'} |")
        if numero == CASOS[-1][0] or requisito != CASOS[CASOS.index(caso) + 1][1]:
            lineas.append("")
    with open(os.path.join(CARPETA, "casos_de_verificacion.md"), "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(lineas))


def main():
    if len(sys.argv) > 1:
        for caso in CASOS:
            if caso[0] == sys.argv[1]:
                faltan, sobran, salida = revisar(caso)
                print(salida)
                print("Correcto" if not faltan and not sobran else f"Faltan: {faltan}\nSobran: {sobran}")
                return
        print("No hay un caso con ese número.")
        return

    resultados = []
    for caso in CASOS:
        faltan, sobran, _ = revisar(caso)
        correcto = not faltan and not sobran
        resultados.append((caso, correcto))
        if correcto:
            print(f"  ok    {caso[0]}  {caso[2]}")
        else:
            print(f"  FALLA {caso[0]}  {caso[2]}")
            for texto in faltan:
                print(f"        no apareció: {texto}")
            for texto in sobran:
                print(f"        apareció y no debía: {texto}")
    escribir_markdown(resultados)
    correctos = sum(1 for _, ok in resultados if ok)
    print(f"\n{correctos} de {len(resultados)} casos correctos. Detalle en casos_de_verificacion.md")


if __name__ == "__main__":
    main()
