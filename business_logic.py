"""Lógica del negocio del monitoreo de visitantes de la Reserva Natural Bahía Coralina.

Este módulo no lee del teclado ni imprime. Cuando un dato no es válido lanza
ValueError con el mensaje exacto que la interfaz debe mostrar.
"""

import math
import random
from datetime import date, timedelta

BAJA = "baja"
MODERADA = "moderada"
ALTA = "alta"
SATURACION = "saturación"
NIVELES = (BAJA, MODERADA, ALTA, SATURACION)

# Porcentaje de la capacidad de carga desde el que empieza cada nivel (plan de manejo).
PORCENTAJE_MODERADA = 50
PORCENTAJE_ALTA = 75
PORCENTAJE_SATURACION = 90

# Requisito propio (R15): días seguidos en saturación, hasta el último registrado,
# a partir de los cuales el sector necesita un cierre temporal.
DIAS_PARA_CIERRE = 3

# Campos de cada línea de los archivos CSV.
CAMPOS_SECTOR = 5
CAMPOS_VISITANTES = 2


def convertir_entero(texto: str, mensaje: str) -> int:
    """Convierte el texto en entero o lanza ValueError con el mensaje dado."""
    try:
        return int(texto)
    except ValueError:
        raise ValueError(mensaje)


def partir_linea(linea: str) -> list[str]:
    """Parte una línea del CSV por ';' y quita los espacios de cada campo."""
    campos = []
    for campo in linea.split(";"):
        campos.append(campo.strip())
    return campos


class Sector:
    """Un sector de la reserva con su registro diario de visitantes."""

    def __init__(self, nombre: str, capacidad: int, fecha_inicio: date):
        self.nombre = nombre
        self.capacidad = capacidad
        self.fecha_inicio = fecha_inicio
        self.visitantes: list[int] = []

    # --- Registro (R2, R3) -------------------------------------------------

    def dias_registrados(self) -> int:
        return len(self.visitantes)

    def fecha_del_dia(self, posicion: int) -> date:
        """Fecha del día que ocupa esa posición en el registro (desde 0)."""
        return self.fecha_inicio + timedelta(days=posicion)

    def fecha_siguiente(self) -> date:
        # Decisión: si el registro ya llegó al 9999-12-31, la fecha más grande que maneja
        # Python, no hay día siguiente; se avisa con ValueError en vez de dejar que el
        # OverflowError cierre el programa.
        try:
            fecha = self.fecha_del_dia(self.dias_registrados())
        except OverflowError:
            raise ValueError("El registro ya llegó a la última fecha posible (9999-12-31)")
        return fecha

    def validar_visitantes(self, texto: str) -> int:
        visitantes = convertir_entero(texto, "Los visitantes deben ser un número entero")
        if visitantes < 0 or visitantes > self.capacidad:
            raise ValueError(f"Los visitantes van de 0 a {self.capacidad}")
        return visitantes

    def registrar_dia(self, visitantes: int) -> None:
        # Se pide la fecha siguiente solo para comprobar que existe (también al cargar del CSV).
        self.fecha_siguiente()
        self.visitantes.append(visitantes)

    def simular_dias(self, dias: int, minimo: int, maximo: int) -> None:
        if minimo > maximo:
            raise ValueError("El mínimo no puede ser mayor que el máximo")
        # Decisión: antes de agregar días se comprueba que exista la fecha del último día
        # simulado, para no dejar la simulación a medias si se pasa del 9999-12-31.
        try:
            self.fecha_del_dia(self.dias_registrados() + dias - 1)
        except OverflowError:
            raise ValueError("No se pueden simular tantos días: el registro pasaría del 9999-12-31")
        for _ in range(dias):
            self.registrar_dia(random.randint(minimo, maximo))

    # --- Informe (R4 a R9). Suponen al menos un día registrado. -----------

    def total_visitantes(self) -> int:
        return sum(self.visitantes)

    def promedio(self) -> float:
        return self.total_visitantes() / self.dias_registrados()

    def porcentaje_uso(self) -> float:
        return self.promedio() / self.capacidad * 100

    def desviacion_estandar(self) -> float:
        promedio = self.promedio()
        suma = 0
        for valor in self.visitantes:
            suma += (valor - promedio) ** 2
        return math.sqrt(suma / self.dias_registrados())

    def dia_mas_visitantes(self) -> date:
        # Decisión: se cambia de candidato solo con > estricto, así en un empate gana el primero.
        mejor = 0
        for i in range(1, len(self.visitantes)):
            if self.visitantes[i] > self.visitantes[mejor]:
                mejor = i
        return self.fecha_del_dia(mejor)

    def dia_menos_visitantes(self) -> date:
        mejor = 0
        for i in range(1, len(self.visitantes)):
            if self.visitantes[i] < self.visitantes[mejor]:
                mejor = i
        return self.fecha_del_dia(mejor)

    def nivel_presion(self, visitantes: int) -> str:
        # Decisión: se compara visitantes * 100 con porcentaje * capacidad, con enteros,
        # para que 540 de 600 sea exactamente el 90 % sin errores de redondeo de un float.
        ocupacion = visitantes * 100
        if ocupacion < PORCENTAJE_MODERADA * self.capacidad:
            return BAJA
        if ocupacion < PORCENTAJE_ALTA * self.capacidad:
            return MODERADA
        if ocupacion < PORCENTAJE_SATURACION * self.capacidad:
            return ALTA
        return SATURACION

    def dias_por_nivel(self) -> dict[str, int]:
        conteo = {}
        for nivel in NIVELES:
            conteo[nivel] = 0
        for valor in self.visitantes:
            conteo[self.nivel_presion(valor)] += 1
        return conteo

    def racha_saturacion(self) -> tuple[int, date | None]:
        """Duración y fecha de inicio de la racha más larga en saturación."""
        # Decisión: la mejor racha se actualiza dentro del ciclo, así también cuenta la que
        # llega hasta el último día; con > estricto, en un empate queda la que empezó primero.
        mejor_largo, mejor_inicio = 0, 0
        largo, inicio = 0, 0
        for i in range(len(self.visitantes)):
            if self.nivel_presion(self.visitantes[i]) == SATURACION:
                if largo == 0:
                    inicio = i
                largo += 1
                if largo > mejor_largo:
                    mejor_largo, mejor_inicio = largo, inicio
            else:
                largo = 0
        if mejor_largo == 0:
            return 0, None
        return mejor_largo, self.fecha_del_dia(mejor_inicio)

    # --- Requisito propio: alerta de cierre temporal (R15) ----------------

    def racha_actual_saturacion(self) -> tuple[int, date | None]:
        """Días seguidos en saturación que terminan en el último día registrado."""
        # Decisión: se recorre la lista desde el final hacia atrás y se cuenta mientras
        # el día esté en saturación. Lo que importa para cerrar es la racha de ahora,
        # no una racha que ya terminó (esa es la de R8).
        largo = 0
        posicion = len(self.visitantes) - 1
        while posicion >= 0 and self.nivel_presion(self.visitantes[posicion]) == SATURACION:
            largo += 1
            posicion -= 1
        if largo == 0:
            return 0, None
        return largo, self.fecha_del_dia(posicion + 1)

    def necesita_cierre(self) -> bool:
        largo, _ = self.racha_actual_saturacion()
        return largo >= DIAS_PARA_CIERRE

    def ultimo_dia_registrado(self) -> date:
        return self.fecha_del_dia(self.dias_registrados() - 1)

    def dias_sin_registrar(self, hoy: date) -> int:
        """Días entre el último registrado y ayer. 0 o menos: al día."""
        # Decisión: recibe hoy como parámetro para poder verificarlo con una fecha fija.
        return (hoy - self.ultimo_dia_registrado()).days - 1


class Reserva:
    """Todos los sectores de la reserva, en el orden en que se crearon."""

    def __init__(self):
        self.sectores: dict[str, Sector] = {}

    # --- Sectores (R1, R10) ------------------------------------------------

    def validar_sector(self, nombre: str, capacidad: str, anio: str, mes: str,
                       dia: str) -> tuple[str, int, date]:
        # Decisión: los datos llegan como texto y se revisan aquí, en el orden del requisito 1,
        # para que el teclado y el archivo CSV usen las mismas reglas y los mismos mensajes.
        nombre = nombre.strip()
        if nombre == "":
            raise ValueError("El nombre no puede estar vacío")
        if nombre in self.sectores:
            raise ValueError("Ya existe un sector con ese nombre")
        capacidad = convertir_entero(capacidad, "La capacidad de carga debe ser un número entero")
        if capacidad < 1:
            raise ValueError("La capacidad de carga debe ser de al menos un visitante")
        try:
            fecha = date(int(anio), int(mes), int(dia))
        except ValueError:
            raise ValueError("La fecha no es válida")
        return nombre, capacidad, fecha

    def crear_sector(self, nombre: str, capacidad: str, anio: str, mes: str,
                     dia: str) -> Sector:
        nombre, capacidad, fecha = self.validar_sector(nombre, capacidad, anio, mes, dia)
        sector = Sector(nombre, capacidad, fecha)
        self.sectores[nombre] = sector
        return sector

    def buscar_sector(self, nombre: str) -> Sector | None:
        return self.sectores.get(nombre.strip())

    def tiene_sectores(self) -> bool:
        return len(self.sectores) > 0

    # --- Simulación (R3) ---------------------------------------------------

    def validar_dias_simulados(self, texto: str) -> int:
        dias = convertir_entero(texto, "El número de días debe ser un número entero")
        if dias < 1:
            raise ValueError("Se debe simular al menos un día")
        return dias

    # --- Comparación (R11) -------------------------------------------------

    def sectores_mayor_y_menor_uso(self) -> tuple[Sector, Sector] | None:
        # Decisión: se compara sin redondear y con > y < estrictos, así en un empate
        # gana el sector que se creó o cargó primero (el diccionario conserva ese orden).
        mayor = None
        menor = None
        for sector in self.sectores.values():
            if sector.dias_registrados() == 0:
                continue
            if mayor is None or sector.porcentaje_uso() > mayor.porcentaje_uso():
                mayor = sector
            if menor is None or sector.porcentaje_uso() < menor.porcentaje_uso():
                menor = sector
        if mayor is None:
            return None
        return mayor, menor

    # --- Archivos (R12, R13) -----------------------------------------------

    def cargar_sectores(self, ruta: str) -> tuple[int, list[tuple[int, str]]]:
        """Carga sectores de un CSV. Devuelve (cargados, [(línea, causa)]).

        Si el archivo no existe, open lanza FileNotFoundError; si la ruta es una carpeta,
        IsADirectoryError o PermissionError; si no está en UTF-8, UnicodeDecodeError.
        """
        cargados = 0
        descartes = []
        # Decisión: se leen todas las líneas antes de crear el primer sector. Si el archivo
        # no está en UTF-8, el error aparece aquí y el programa queda sin cambios, en vez de
        # quedar con una parte del archivo cargada.
        with open(ruta, encoding="utf-8-sig") as archivo:
            lineas = archivo.readlines()
        for numero, linea in enumerate(lineas, start=1):
            if numero == 1 or linea.strip() == "":
                continue
            campos = partir_linea(linea)
            if len(campos) != CAMPOS_SECTOR:
                descartes.append((numero, "No tiene cinco campos"))
                continue
            try:
                self.crear_sector(campos[0], campos[1], campos[2], campos[3], campos[4])
                cargados += 1
            except ValueError as error:
                descartes.append((numero, str(error)))
        return cargados, descartes

    def cargar_visitantes(self, ruta: str) -> tuple[int, list[tuple[int, str]]]:
        """Carga días de un CSV. Devuelve (días cargados, [(línea, causa)]).

        Lanza los mismos errores de archivo que cargar_sectores.
        """
        cargados = 0
        descartes = []
        # Decisión: igual que con los sectores, se lee todo el archivo antes de registrar
        # el primer día, para que un archivo que no está en UTF-8 no deje días a medias.
        with open(ruta, encoding="utf-8-sig") as archivo:
            lineas = archivo.readlines()
        for numero, linea in enumerate(lineas, start=1):
            if numero == 1 or linea.strip() == "":
                continue
            campos = partir_linea(linea)
            if len(campos) != CAMPOS_VISITANTES:
                descartes.append((numero, "No tiene dos campos"))
                continue
            sector = self.buscar_sector(campos[0])
            if sector is None:
                descartes.append((numero, f"No hay un sector llamado {campos[0]}"))
                continue
            try:
                sector.registrar_dia(sector.validar_visitantes(campos[1]))
                cargados += 1
            except ValueError as error:
                descartes.append((numero, f"{sector.nombre}: {error}"))
        return cargados, descartes
