# Casos de verificación de la entrega

Cada caso se comprueba ejecutando `user_interface.py` desde la carpeta `codigo`, tecleando las entradas en orden (cada flecha es un Enter). El archivo lo genera `pruebas_consola.py`, que ejecuta el programa con esas mismas entradas y revisa la salida.

**Última ejecución:** 2026-11-21. **Resultado:** 91 de 91 casos correctos.

Los casos de R9 dependen de la fecha en que se ejecuta el programa; su salida esperada se calculó con la fecha de la última ejecución.

## R1

| # | Qué se prueba | Qué se teclea | Qué debe aparecer | Qué no debe aparecer | ¿Pasa? |
| --- | --- | --- | --- | --- | --- |
| 1.1 | Crear un sector válido; queda sin días | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `4` → `Mirador del Faro` → (Enter) → `7` | Se creó el sector Mirador del Faro, sin días registrados.<br>El sector no tiene días registrados. | — | ✅ |
| 1.2 | Nombre vacío | `1` → (Enter) → `80` → `2026` → `11` → `1` → (Enter) → `7` | El nombre no puede estar vacío. | Se creó | ✅ |
| 1.3 | Nombre con solo espacios | `1` → `   ` → `80` → `2026` → `11` → `1` → (Enter) → `7` | El nombre no puede estar vacío. | Se creó | ✅ |
| 1.4 | Nombre repetido; el sector original no cambia | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `1` → `Mirador del Faro` → `90` → `2026` → `11` → `1` → (Enter) → `4` → `Mirador del Faro` → (Enter) → `7` | Ya existe un sector con ese nombre.<br>Capacidad de carga: 80 visitantes | — | ✅ |
| 1.5 | Capacidad escrita en letras | `1` → `Mirador del Faro` → `ochenta` → `2026` → `11` → `1` → (Enter) → `7` | La capacidad de carga debe ser un número entero. | Se creó | ✅ |
| 1.6 | Capacidad con decimales | `1` → `Mirador del Faro` → `80.5` → `2026` → `11` → `1` → (Enter) → `7` | La capacidad de carga debe ser un número entero. | Se creó | ✅ |
| 1.7 | Capacidad 0 | `1` → `Mirador del Faro` → `0` → `2026` → `11` → `1` → (Enter) → `7` | La capacidad de carga debe ser de al menos un visitante. | Se creó | ✅ |
| 1.8 | Capacidad negativa | `1` → `Mirador del Faro` → `-5` → `2026` → `11` → `1` → (Enter) → `7` | La capacidad de carga debe ser de al menos un visitante. | Se creó | ✅ |
| 1.9 | Fecha que no existe (31 de noviembre) | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `31` → (Enter) → `7` | La fecha no es válida. | Se creó | ✅ |
| 1.10 | Mes escrito en letras | `1` → `Mirador del Faro` → `80` → `2026` → `noviembre` → `1` → (Enter) → `7` | La fecha no es válida. | Se creó | ✅ |
| 1.11 | 29 de febrero de un año bisiesto | `1` → `Mirador del Faro` → `80` → `2028` → `2` → `29` → (Enter) → `7` | Se creó el sector Mirador del Faro | — | ✅ |
| 1.12 | 29 de febrero de un año no bisiesto | `1` → `Mirador del Faro` → `80` → `2026` → `2` → `29` → (Enter) → `7` | La fecha no es válida. | Se creó | ✅ |
| 1.13 | Dos datos malos: solo se avisa el primero | `1` → `Mirador del Faro` → `0` → `2026` → `11` → `31` → (Enter) → `7` | La capacidad de carga debe ser de al menos un visitante. | La fecha no es válida. | ✅ |
| 1.14 | Capacidad mínima válida (1) | `1` → `Mirador del Faro` → `1` → `2026` → `11` → `1` → (Enter) → `7` | Se creó el sector Mirador del Faro, sin días registrados. | — | ✅ |

## R2

| # | Qué se prueba | Qué se teclea | Qué debe aparecer | Qué no debe aparecer | ¿Pasa? |
| --- | --- | --- | --- | --- | --- |
| 2.1 | Primer día de un sector nuevo | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `2` → `Mirador del Faro` → `52` → (Enter) → `7` | Día por registrar: 2026-11-01<br>Se registraron 52 visitantes el 2026-11-01. | — | ✅ |
| 2.2 | Visitantes en letras: vuelve a preguntar | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `2` → `Mirador del Faro` → `x` → `52` → (Enter) → `7` | Los visitantes deben ser un número entero.<br>Se registraron 52 visitantes el 2026-11-01. | — | ✅ |
| 2.3 | Más que la capacidad: vuelve a preguntar | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `2` → `Mirador del Faro` → `81` → `52` → (Enter) → `7` | Los visitantes van de 0 a 80.<br>Se registraron 52 visitantes | — | ✅ |
| 2.4 | Negativo: vuelve a preguntar | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `2` → `Mirador del Faro` → `-1` → `52` → (Enter) → `7` | Los visitantes van de 0 a 80.<br>Se registraron 52 visitantes | — | ✅ |
| 2.5 | Límite inferior válido (0) | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `2` → `Mirador del Faro` → `0` → (Enter) → `7` | Se registraron 0 visitantes el 2026-11-01. | — | ✅ |
| 2.6 | Límite superior válido (la capacidad) | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `2` → `Mirador del Faro` → `80` → (Enter) → `7` | Se registraron 80 visitantes el 2026-11-01. | — | ✅ |
| 2.7 | El día siguiente cambia de año | `1` → `Cambio de Año` → `100` → `2026` → `12` → `30` → (Enter) → `2` → `Cambio de Año` → `1` → (Enter) → `2` → `Cambio de Año` → `1` → (Enter) → `2` → `Cambio de Año` → `1` → (Enter) → `2` → `Cambio de Año` → `5` → (Enter) → `7` | Día por registrar: 2027-01-02 | — | ✅ |
| 2.8 | Sector que no existe | `2` → `Isla del Pirata` → (Enter) → `7` | No hay un sector con ese nombre. | Día por registrar | ✅ |
| 2.9 | El registro ya llegó al 9999-12-31: avisa y no se cierra | `1` → `Fin` → `80` → `9999` → `12` → `31` → (Enter) → `2` → `Fin` → `5` → (Enter) → `2` → `Fin` → (Enter) → `7` | El registro ya llegó a la última fecha posible (9999-12-31). | Traceback | ✅ |

## R3

| # | Qué se prueba | Qué se teclea | Qué debe aparecer | Qué no debe aparecer | ¿Pasa? |
| --- | --- | --- | --- | --- | --- |
| 3.1 | Simular 3 días entre 40 y 80 | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `3` → `Mirador del Faro` → `3` → `40` → `80` → (Enter) → `4` → `Mirador del Faro` → (Enter) → `7` | Se simularon 3 días, del 2026-11-01 al 2026-11-03.<br>Días registrados: 3 | — | ✅ |
| 3.2 | Mínimo igual al máximo: resultado exacto | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `3` → `Mirador del Faro` → `2` → `50` → `50` → (Enter) → `4` → `Mirador del Faro` → (Enter) → `7` | Visitantes totales: 100<br>Desviación estándar: 0.0 | — | ✅ |
| 3.3 | Días en letras: no pide el mínimo | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `3` → `Mirador del Faro` → `tres` → (Enter) → `7` | El número de días debe ser un número entero. | Visitantes mínimos | ✅ |
| 3.4 | 0 días: no pide el mínimo ni el máximo | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `3` → `Mirador del Faro` → `0` → (Enter) → `7` | Se debe simular al menos un día. | Visitantes mínimos | ✅ |
| 3.5 | Mínimo en letras: no pide el máximo | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `3` → `Mirador del Faro` → `3` → `x` → (Enter) → `7` | Los visitantes deben ser un número entero. | Visitantes máximos | ✅ |
| 3.6 | Mínimo negativo: no pide el máximo | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `3` → `Mirador del Faro` → `3` → `-1` → (Enter) → `7` | Los visitantes van de 0 a 80. | Visitantes máximos | ✅ |
| 3.7 | Máximo mayor que la capacidad: no agrega días | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `3` → `Mirador del Faro` → `3` → `40` → `81` → (Enter) → `4` → `Mirador del Faro` → (Enter) → `7` | Los visitantes van de 0 a 80.<br>El sector no tiene días registrados. | Se simularon | ✅ |
| 3.8 | Mínimo mayor que el máximo: no agrega días | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `3` → `Mirador del Faro` → `3` → `60` → `40` → (Enter) → `4` → `Mirador del Faro` → (Enter) → `7` | El mínimo no puede ser mayor que el máximo.<br>El sector no tiene días registrados. | Se simularon | ✅ |
| 3.9 | La simulación continúa el registro | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `2` → `Mirador del Faro` → `10` → (Enter) → `2` → `Mirador del Faro` → `20` → (Enter) → `3` → `Mirador del Faro` → `3` → `0` → `80` → (Enter) → `7` | Se simularon 3 días, del 2026-11-03 al 2026-11-05. | — | ✅ |
| 3.10 | Sector que no existe | `3` → `Isla del Pirata` → (Enter) → `7` | No hay un sector con ese nombre. | Número de días | ✅ |

## R4

| # | Qué se prueba | Qué se teclea | Qué debe aparecer | Qué no debe aparecer | ¿Pasa? |
| --- | --- | --- | --- | --- | --- |
| 4.1 | Informe de Playa Brava cargada desde archivo | `6` → `datos/sectores.csv` → `datos/visitantes.csv` → (Enter) → `4` → `Playa Brava` → (Enter) → `7` | Sector: Playa Brava<br>Capacidad de carga: 600 visitantes<br>Días registrados: 5<br>Visitantes totales: 2405<br>Promedio de visitantes por día: 481.0<br>Porcentaje de uso: 80.17 % | — | ✅ |
| 4.2 | Informe del Sendero de los Mangles | `6` → `datos/sectores.csv` → `datos/visitantes.csv` → (Enter) → `4` → `Sendero de los Mangles` → (Enter) → `7` | Días registrados: 4<br>Visitantes totales: 420<br>Promedio de visitantes por día: 105.0<br>Porcentaje de uso: 70.0 % | — | ✅ |
| 4.3 | Un solo día: el porcentaje se muestra como 65.0 | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `2` → `Mirador del Faro` → `52` → (Enter) → `4` → `Mirador del Faro` → (Enter) → `7` | Promedio de visitantes por día: 52.0<br>Porcentaje de uso: 65.0 % | — | ✅ |
| 4.4 | Redondeo a dos decimales | `1` → `Prueba` → `3` → `2026` → `11` → `1` → (Enter) → `2` → `Prueba` → `1` → (Enter) → `2` → `Prueba` → `1` → (Enter) → `2` → `Prueba` → `2` → (Enter) → `4` → `Prueba` → (Enter) → `7` | Promedio de visitantes por día: 1.33<br>Porcentaje de uso: 44.44 % | — | ✅ |
| 4.5 | Sector sin días: solo nombre, capacidad y aviso | `1` → `Cueva del Murciélago` → `40` → `2026` → `11` → `1` → (Enter) → `4` → `Cueva del Murciélago` → (Enter) → `7` | Sector: Cueva del Murciélago<br>Capacidad de carga: 40 visitantes<br>El sector no tiene días registrados. | Días registrados: | ✅ |

## R5

| # | Qué se prueba | Qué se teclea | Qué debe aparecer | Qué no debe aparecer | ¿Pasa? |
| --- | --- | --- | --- | --- | --- |
| 5.1 | Playa Brava | `6` → `datos/sectores.csv` → `datos/visitantes.csv` → (Enter) → `4` → `Playa Brava` → (Enter) → `7` | Desviación estándar: 112.53 | — | ✅ |
| 5.2 | Sendero de los Mangles | `6` → `datos/sectores.csv` → `datos/visitantes.csv` → (Enter) → `4` → `Sendero de los Mangles` → (Enter) → `7` | Desviación estándar: 33.54 | — | ✅ |
| 5.3 | Un solo día | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `2` → `Mirador del Faro` → `52` → (Enter) → `4` → `Mirador del Faro` → (Enter) → `7` | Desviación estándar: 0.0 | — | ✅ |
| 5.5 | Promedio no entero | `1` → `Prueba` → `3` → `2026` → `11` → `1` → (Enter) → `2` → `Prueba` → `1` → (Enter) → `2` → `Prueba` → `1` → (Enter) → `2` → `Prueba` → `2` → (Enter) → `4` → `Prueba` → (Enter) → `7` | Desviación estándar: 0.47 | — | ✅ |

## R6

| # | Qué se prueba | Qué se teclea | Qué debe aparecer | Qué no debe aparecer | ¿Pasa? |
| --- | --- | --- | --- | --- | --- |
| 6.1 | Playa Brava | `6` → `datos/sectores.csv` → `datos/visitantes.csv` → (Enter) → `4` → `Playa Brava` → (Enter) → `7` | Día con más visitantes: 2026-11-03<br>Día con menos visitantes: 2026-11-04 | — | ✅ |
| 6.3 | Empates: gana el primero | `1` → `Empates` → `600` → `2026` → `11` → `1` → (Enter) → `2` → `Empates` → `300` → (Enter) → `2` → `Empates` → `600` → (Enter) → `2` → `Empates` → `600` → (Enter) → `2` → `Empates` → `120` → (Enter) → `2` → `Empates` → `120` → (Enter) → `4` → `Empates` → (Enter) → `7` | Día con más visitantes: 2026-11-02<br>Día con menos visitantes: 2026-11-04 | — | ✅ |
| 6.4 | Un solo día | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `2` → `Mirador del Faro` → `52` → (Enter) → `4` → `Mirador del Faro` → (Enter) → `7` | Día con más visitantes: 2026-11-01<br>Día con menos visitantes: 2026-11-01 | — | ✅ |

## R7

| # | Qué se prueba | Qué se teclea | Qué debe aparecer | Qué no debe aparecer | ¿Pasa? |
| --- | --- | --- | --- | --- | --- |
| 7.1 | Los seis límites entre niveles (capacidad 600) | `1` → `Limites` → `600` → `2026` → `11` → `1` → (Enter) → `2` → `Limites` → `299` → (Enter) → `2` → `Limites` → `300` → (Enter) → `2` → `Limites` → `449` → (Enter) → `2` → `Limites` → `450` → (Enter) → `2` → `Limites` → `539` → (Enter) → `2` → `Limites` → `540` → (Enter) → `4` → `Limites` → (Enter) → `7` | baja: 1<br>moderada: 2<br>alta: 2<br>saturación: 1 | — | ✅ |
| 7.2 | Playa Brava: un nivel con 0 días también se muestra | `6` → `datos/sectores.csv` → `datos/visitantes.csv` → (Enter) → `4` → `Playa Brava` → (Enter) → `7` | baja: 1<br>moderada: 1<br>alta: 0<br>saturación: 3 | — | ✅ |
| 7.3 | Sendero de los Mangles | `6` → `datos/sectores.csv` → `datos/visitantes.csv` → (Enter) → `4` → `Sendero de los Mangles` → (Enter) → `7` | baja: 1<br>moderada: 1<br>alta: 1<br>saturación: 1 | — | ✅ |

## R8

| # | Qué se prueba | Qué se teclea | Qué debe aparecer | Qué no debe aparecer | ¿Pasa? |
| --- | --- | --- | --- | --- | --- |
| 8.1 | Playa Brava | `6` → `datos/sectores.csv` → `datos/visitantes.csv` → (Enter) → `4` → `Playa Brava` → (Enter) → `7` | Racha más larga en saturación: 2 días, desde el 2026-11-02 | — | ✅ |
| 8.2 | La segunda racha es más larga | `1` → `Rachas` → `600` → `2026` → `11` → `1` → (Enter) → `2` → `Rachas` → `560` → (Enter) → `2` → `Rachas` → `570` → (Enter) → `2` → `Rachas` → `400` → (Enter) → `2` → `Rachas` → `545` → (Enter) → `2` → `Rachas` → `600` → (Enter) → `2` → `Rachas` → `590` → (Enter) → `2` → `Rachas` → `100` → (Enter) → `4` → `Rachas` → (Enter) → `7` | Racha más larga en saturación: 3 días, desde el 2026-11-04 | — | ✅ |
| 8.3 | Dos rachas empatadas: gana la primera | `1` → `Rachas` → `600` → `2026` → `11` → `1` → (Enter) → `2` → `Rachas` → `560` → (Enter) → `2` → `Rachas` → `570` → (Enter) → `2` → `Rachas` → `100` → (Enter) → `2` → `Rachas` → `545` → (Enter) → `2` → `Rachas` → `600` → (Enter) → `4` → `Rachas` → (Enter) → `7` | Racha más larga en saturación: 2 días, desde el 2026-11-01 | — | ✅ |
| 8.4 | La racha llega hasta el último día | `1` → `Rachas` → `600` → `2026` → `11` → `1` → (Enter) → `2` → `Rachas` → `100` → (Enter) → `2` → `Rachas` → `560` → (Enter) → `2` → `Rachas` → `570` → (Enter) → `2` → `Rachas` → `580` → (Enter) → `4` → `Rachas` → (Enter) → `7` | Racha más larga en saturación: 3 días, desde el 2026-11-02 | — | ✅ |
| 8.6 | Ningún día en saturación | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `2` → `Mirador del Faro` → `52` → (Enter) → `4` → `Mirador del Faro` → (Enter) → `7` | El sector no tuvo ningún día en saturación. | Racha más larga | ✅ |

## R15

| # | Qué se prueba | Qué se teclea | Qué debe aparecer | Qué no debe aparecer | ¿Pasa? |
| --- | --- | --- | --- | --- | --- |
| 15.1 | Playa Brava: termina con 1 día en saturación, no necesita cierre | `6` → `datos/sectores.csv` → `datos/visitantes.csv` → (Enter) → `4` → `Playa Brava` → (Enter) → `7` | El sector no necesita cierre temporal (días seguidos en saturación al final del registro: 1; el cierre se recomienda desde 3). | ALERTA | ✅ |
| 15.2 | Los últimos 3 días en saturación: alerta | `1` → `Cierre` → `600` → `2026` → `11` → `1` → (Enter) → `2` → `Cierre` → `100` → (Enter) → `2` → `Cierre` → `560` → (Enter) → `2` → `Cierre` → `570` → (Enter) → `2` → `Cierre` → `580` → (Enter) → `4` → `Cierre` → (Enter) → `7` | ALERTA: el sector necesita un cierre temporal. Lleva 3 días seguidos en saturación, desde el 2026-11-02. | — | ✅ |
| 15.3 | Hubo una racha de 3, pero el último día no está en saturación: sin alerta | `1` → `Cierre` → `600` → `2026` → `11` → `1` → (Enter) → `2` → `Cierre` → `560` → (Enter) → `2` → `Cierre` → `570` → (Enter) → `2` → `Cierre` → `580` → (Enter) → `2` → `Cierre` → `100` → (Enter) → `4` → `Cierre` → (Enter) → `7` | Racha más larga en saturación: 3 días, desde el 2026-11-01<br>El sector no necesita cierre temporal (días seguidos en saturación al final del registro: 0; | ALERTA | ✅ |
| 15.4 | Justo debajo del límite (2 días): sin alerta | `1` → `Cierre` → `600` → `2026` → `11` → `1` → (Enter) → `2` → `Cierre` → `100` → (Enter) → `2` → `Cierre` → `560` → (Enter) → `2` → `Cierre` → `570` → (Enter) → `4` → `Cierre` → (Enter) → `7` | El sector no necesita cierre temporal (días seguidos en saturación al final del registro: 2; | ALERTA | ✅ |
| 15.5 | Todos los días en saturación: la racha empieza el primer día | `1` → `Cierre` → `600` → `2026` → `11` → `1` → (Enter) → `2` → `Cierre` → `540` → (Enter) → `2` → `Cierre` → `540` → (Enter) → `2` → `Cierre` → `540` → (Enter) → `2` → `Cierre` → `540` → (Enter) → `2` → `Cierre` → `540` → (Enter) → `4` → `Cierre` → (Enter) → `7` | ALERTA: el sector necesita un cierre temporal. Lleva 5 días seguidos en saturación, desde el 2026-11-01. | — | ✅ |
| 15.6 | Justo en el límite de saturación (90 %) cuenta | `1` → `Cierre` → `80` → `2026` → `11` → `1` → (Enter) → `2` → `Cierre` → `72` → (Enter) → `2` → `Cierre` → `72` → (Enter) → `2` → `Cierre` → `72` → (Enter) → `4` → `Cierre` → (Enter) → `7` | ALERTA: el sector necesita un cierre temporal. Lleva 3 días seguidos | — | ✅ |
| 15.7 | Un día en presión alta corta la racha | `1` → `Cierre` → `600` → `2026` → `11` → `1` → (Enter) → `2` → `Cierre` → `560` → (Enter) → `2` → `Cierre` → `570` → (Enter) → `2` → `Cierre` → `539` → (Enter) → `2` → `Cierre` → `580` → (Enter) → `2` → `Cierre` → `590` → (Enter) → `4` → `Cierre` → (Enter) → `7` | El sector no necesita cierre temporal (días seguidos en saturación al final del registro: 2; | ALERTA | ✅ |

## R9

| # | Qué se prueba | Qué se teclea | Qué debe aparecer | Qué no debe aparecer | ¿Pasa? |
| --- | --- | --- | --- | --- | --- |
| 9.1 | Playa Brava, con la fecha de hoy | `6` → `datos/sectores.csv` → `datos/visitantes.csv` → (Enter) → `4` → `Playa Brava` → (Enter) → `7` | Último día registrado: 2026-11-05<br>Faltan por registrar 15 días, del 2026-11-06 al 2026-11-20. | — | ✅ |
| 9.2 | Último día registrado = ayer: al día | `1` → `Hoy` → `80` → `2026` → `11` → `20` → (Enter) → `2` → `Hoy` → `10` → (Enter) → `4` → `Hoy` → (Enter) → `7` | El registro está al día. | Faltan por registrar | ✅ |
| 9.3 | Falta exactamente un día | `1` → `Hoy` → `80` → `2026` → `11` → `19` → (Enter) → `2` → `Hoy` → `10` → (Enter) → `4` → `Hoy` → (Enter) → `7` | Faltan por registrar 1 día, del 2026-11-20 al 2026-11-20. | — | ✅ |
| 9.4 | Último día = hoy (posible al simular): al día | `1` → `Hoy` → `80` → `2026` → `11` → `21` → (Enter) → `2` → `Hoy` → `10` → (Enter) → `4` → `Hoy` → (Enter) → `7` | El registro está al día. | Faltan por registrar | ✅ |

## R10

| # | Qué se prueba | Qué se teclea | Qué debe aparecer | Qué no debe aparecer | ¿Pasa? |
| --- | --- | --- | --- | --- | --- |
| 10.1 | Cada sector muestra sus propios datos | `6` → `datos/sectores.csv` → `datos/visitantes.csv` → (Enter) → `4` → `Playa Brava` → (Enter) → `4` → `Sendero de los Mangles` → (Enter) → `7` | Visitantes totales: 2405<br>Visitantes totales: 420 | — | ✅ |
| 10.2 | Nombre que no existe | `6` → `datos/sectores.csv` → `datos/visitantes.csv` → (Enter) → `4` → `Isla del Pirata` → (Enter) → `7` | No hay un sector con ese nombre. | — | ✅ |
| 10.3 | Distinto en mayúsculas | `6` → `datos/sectores.csv` → `datos/visitantes.csv` → (Enter) → `4` → `playa brava` → (Enter) → `7` | No hay un sector con ese nombre. | Sector: Playa Brava | ✅ |
| 10.4 | Distinto en tildes | `1` → `Cueva del Murciélago` → `40` → `2026` → `11` → `1` → (Enter) → `4` → `Cueva del Murcielago` → (Enter) → `7` | No hay un sector con ese nombre. | — | ✅ |
| 10.5 | Espacios alrededor del nombre | `6` → `datos/sectores.csv` → `datos/visitantes.csv` → (Enter) → `4` → `   Playa Brava   ` → (Enter) → `7` | Sector: Playa Brava | — | ✅ |

## R11

| # | Qué se prueba | Qué se teclea | Qué debe aparecer | Qué no debe aparecer | ¿Pasa? |
| --- | --- | --- | --- | --- | --- |
| 11.1 | Varios sectores; uno sin días se ignora | `6` → `datos/sectores.csv` → `datos/visitantes.csv` → (Enter) → `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `2` → `Mirador del Faro` → `52` → (Enter) → `1` → `Cueva del Murciélago` → `40` → `2026` → `11` → `1` → (Enter) → `5` → (Enter) → `7` | Porcentaje de uso más alto: Playa Brava, con 80.17 %<br>Porcentaje de uso más bajo: Mirador del Faro, con 65.0 % | — | ✅ |
| 11.2 | Sin sectores | `5` → (Enter) → `7` | Ningún sector tiene días registrados. | — | ✅ |
| 11.3 | Solo sectores sin días | `1` → `Cueva del Murciélago` → `40` → `2026` → `11` → `1` → (Enter) → `5` → (Enter) → `7` | Ningún sector tiene días registrados. | — | ✅ |
| 11.4 | Empate: gana el que se creó primero | `1` → `A` → `100` → `2026` → `11` → `1` → (Enter) → `2` → `A` → `50` → (Enter) → `1` → `B` → `10` → `2026` → `11` → `1` → (Enter) → `2` → `B` → `5` → (Enter) → `5` → (Enter) → `7` | Porcentaje de uso más alto: A, con 50.0 %<br>Porcentaje de uso más bajo: A, con 50.0 % | — | ✅ |
| 11.6 | Se compara sin redondear (los dos se muestran 66.67) | `1` → `A` → `3` → `2026` → `11` → `1` → (Enter) → `2` → `A` → `2` → (Enter) → `1` → `C` → `10000` → `2026` → `11` → `1` → (Enter) → `2` → `C` → `6667` → (Enter) → `5` → (Enter) → `7` | Porcentaje de uso más alto: C, con 66.67 %<br>Porcentaje de uso más bajo: A, con 66.67 % | — | ✅ |

## R12

| # | Qué se prueba | Qué se teclea | Qué debe aparecer | Qué no debe aparecer | ¿Pasa? |
| --- | --- | --- | --- | --- | --- |
| 12.1 | Archivo del enunciado: carga 2 y descarta 5 | `6` → `datos/sectores.csv` → `datos/visitantes.csv` → (Enter) → `7` | Línea 4 descartada: La capacidad de carga debe ser de al menos un visitante.<br>Línea 5 descartada: No tiene cinco campos.<br>Línea 6 descartada: La capacidad de carga debe ser un número entero.<br>Línea 7 descartada: Ya existe un sector con ese nombre.<br>Línea 8 descartada: La fecha no es válida.<br>Se cargaron 2 sectores. | — | ✅ |
| 12.7 | El archivo de sectores no existe: no pide el de visitantes | `6` → `datos/no_existe.csv` → (Enter) → `7` | El archivo no existe. | Ruta del archivo de visitantes | ✅ |
| 12.8 | Ya hay sectores: no pide ninguna ruta | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `6` → (Enter) → `7` | La carga solo se hace con el programa sin sectores. | Ruta del archivo de sectores | ✅ |
| 12.9 | Espacios en los campos, líneas vacías y una línea con 6 campos | `6` → `datos/pruebas/sectores_casos_borde.csv` → `datos/pruebas/solo_encabezado_visitantes.csv` → (Enter) → `4` → `Isla Verde` → (Enter) → `7` | Línea 4 descartada: No tiene cinco campos.<br>Se cargaron 2 sectores.<br>Sector: Isla Verde<br>Capacidad de carga: 50 visitantes | Línea 3<br>Línea 5 | ✅ |
| 12.12 | Archivo de sectores con solo el encabezado | `6` → `datos/pruebas/solo_encabezado_sectores.csv` → `datos/pruebas/solo_encabezado_visitantes.csv` → (Enter) → `7` | Se cargaron 0 sectores.<br>Se cargaron 0 días. | — | ✅ |
| 12.13 | Archivo guardado por Excel con BOM al inicio | `6` → `datos/pruebas/sectores_con_bom.csv` → `datos/pruebas/solo_encabezado_visitantes.csv` → (Enter) → `4` → `Playa Brava` → (Enter) → `7` | Se cargó 1 sector.<br>Sector: Playa Brava | descartada | ✅ |
| 12.14 | La ruta es una carpeta: avisa y no se cierra | `6` → `datos` → (Enter) → `7` | La ruta no es un archivo que se pueda leer. | Ruta del archivo de visitantes<br>Traceback | ✅ |
| 12.15 | Archivo que no está en UTF-8: avisa y no se cierra | `6` → `datos/pruebas/sectores_ansi.csv` → (Enter) → `7` | El archivo no está guardado en UTF-8. | Se cargaron<br>Traceback | ✅ |

## R13

| # | Qué se prueba | Qué se teclea | Qué debe aparecer | Qué no debe aparecer | ¿Pasa? |
| --- | --- | --- | --- | --- | --- |
| 13.1 | Archivo del enunciado: carga 9 días y descarta 5 | `6` → `datos/sectores.csv` → `datos/visitantes.csv` → (Enter) → `7` | Línea 10 descartada: Sendero de los Mangles: Los visitantes van de 0 a 150.<br>Línea 12 descartada: No hay un sector llamado Laguna Grande.<br>Línea 13 descartada: Playa Brava: Los visitantes van de 0 a 600.<br>Línea 14 descartada: Playa Brava: Los visitantes deben ser un número entero.<br>Línea 15 descartada: No tiene dos campos.<br>Se cargaron 9 días. | — | ✅ |
| 13.7 | El archivo de visitantes no existe: los sectores quedan sin días | `6` → `datos/sectores.csv` → `datos/no_existe.csv` → (Enter) → `4` → `Playa Brava` → (Enter) → `7` | El archivo no existe. Los sectores quedan cargados, sin días registrados.<br>El sector no tiene días registrados. | — | ✅ |
| 13.9 | Una segunda carga no duplica los días | `6` → `datos/sectores.csv` → `datos/visitantes.csv` → (Enter) → `6` → (Enter) → `4` → `Playa Brava` → (Enter) → `7` | La carga solo se hace con el programa sin sectores.<br>Días registrados: 5 | — | ✅ |

## R14

| # | Qué se prueba | Qué se teclea | Qué debe aparecer | Qué no debe aparecer | ¿Pasa? |
| --- | --- | --- | --- | --- | --- |
| 14.1 | Después de una opción pausa y vuelve a mostrar el menú | `1` → `Mirador del Faro` → `80` → `2026` → `11` → `1` → (Enter) → `7` | Se creó el sector<br>Presione Enter para volver al menú...<br>Opción: Hasta pronto. | — | ✅ |
| 14.2 | Opción fuera de rango (8) | `8` → (Enter) → `7` | La opción no es válida. | — | ✅ |
| 14.3 | Opción en letras (dos) | `dos` → (Enter) → `7` | La opción no es válida. | — | ✅ |
| 14.4 | Opción 0 | `0` → (Enter) → `7` | La opción no es válida. | — | ✅ |
| 14.5 | Enter sin escribir nada | (Enter) → (Enter) → `7` | La opción no es válida. | — | ✅ |
| 14.6 | Salir | `7` | Hasta pronto. | — | ✅ |
