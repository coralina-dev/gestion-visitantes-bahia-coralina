# Reserva Natural Bahía Coralina: monitoreo de visitantes

Trabajo de fin de curso de **Fundamentos de Programación**, Universidad del Magdalena, Facultad de Ingeniería.  
**Alternativa B.**

Programa de consola en Python que lleva el registro diario de visitantes de cada sector de la reserva y calcula los indicadores con que la oficina de monitoreo vigila la presión de los turistas: visitantes totales, promedio, porcentaje de uso de la capacidad de carga, desviación estándar, niveles de presión, la racha más larga en saturación y los días que faltan por registrar.

Además de los 14 requisitos del enunciado, el equipo agregó el **requisito 15: alerta de cierre temporal**. El informe avisa cuando los últimos días registrados de un sector forman una racha de 3 o más días en saturación.

## Equipo

| Integrante | Usuario de GitHub |
| --- | --- |
| Isabella Gutiérrez Pérez | `@bellaguut` |
| Carlos Beltrán Carvallo | `@cabeto-sys` |
| Hugo Suárez Oñate | `@hasuarezum` |

## Video explicativo

* **Enlace público al video (10 a 15 minutos, sin requerir inicio de sesión):** [Ver video explicativo](PEGAR_AQUI_EL_ENLACE_PUBLICO_DEL_VIDEO)

## Cómo ejecutar

Se necesita Python 3.10 o más reciente. Desde la carpeta `codigo`:

```bash
python user_interface.py
```

Para cargar los datos de ejemplo, elija la opción `6` y escriba las rutas `datos/sectores.csv` y `datos/visitantes.csv`.

Para comprobar los 91 casos de verificación ejecutando el programa:

```bash
python pruebas_consola.py
```

## Estructura

```text
├── README.md                    portada e índice del proyecto
├── docs/                        análisis, diseño e informes
│   ├── Documento de analisis.pdf
│   ├── Diseno de clases.pdf
│   ├── informe_integral.md
│   └── informe_uso_ia.md
├── evidencias_ia/               respaldo de conversaciones con la IA
└── codigo/
    ├── business_logic.py        clases Sector y Reserva (cálculos y validaciones)
    ├── user_interface.py        menú de consola
    ├── pruebas_consola.py       ejecuta los 91 casos de verificación en la consola
    ├── casos_de_verificacion.md los casos, con sus datos y su salida esperada
    ├── verificar_logica.py      prueba rápida de la lógica
    └── datos/                   archivos CSV de ejemplo y de prueba
        ├── sectores.csv
        ├── visitantes.csv
        └── pruebas/
```

## Productos de la entrega

| Producto | Dónde |
| --- | --- |
| Documento de análisis | `docs/Documento de analisis.pdf` |
| Informe integral | `docs/informe_integral.md` |
| Código fuente | `codigo/` |
| Casos de verificación | `codigo/casos_de_verificacion.md` |
| Video | Enlace arriba |
| Informe del uso de la IA | `docs/informe_uso_ia.md` y evidencias en `evidencias_ia/` |
| Prueba de trabajo en equipo | Hitos, issues y el tablero del proyecto en este repositorio |