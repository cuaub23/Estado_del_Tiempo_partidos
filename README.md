# ⚽ Pronóstico del Tiempo para Partidos de Fútbol (SQLite + API REST)

Este proyecto automatiza la consulta del estado del tiempo para eventos deportivos. Utiliza una base de datos local para gestionar el calendario de partidos y consume la API de Open-Meteo para obtener un reporte meteorológico exacto (temperatura y humedad) a la hora del juego.

## 🛠️ Tecnologías Usadas
* **Python**: Lógica principal y consumo de red (`requests`).
* **SQLite3**: Almacenamiento y filtrado de datos mediante consultas SQL.
* **Open-Meteo API**: Servicio RESTful para pronósticos meteorológicos hiperlocales.

## 🗄️ Estructura de Datos
El proyecto utiliza una base de datos local `partidos.db`. Esta base incluye una tabla con el calendario de partidos programados para un periodo aproximado de 4 meses (a partir del 26 de septiembre de 2026).

La tabla contiene las siguientes columnas principales:
* `partido`: Equipos que se enfrentan.
* `estadio`: Sede del encuentro.
* `lat` / `log`: Coordenadas geográficas del estadio.
* `fecha_hora`: Fecha y hora exacta del evento en formato ISO.

## ⚙️ Flujo del Programa
El script principal `estado_tiempo.py` ejecuta el siguiente pipeline:
1. **Filtrado Temporal (SQL):** Se conecta a `partidos.db` y ejecuta una consulta para extraer **únicamente** los partidos que ocurrirán en los próximos 7 días a partir de la ejecución del script.
2. **Construcción de Peticiones:** Itera sobre los resultados y extrae las coordenadas (`lat`, `log`) y la `fecha_hora`.
3. **Consumo de API:** Realiza peticiones HTTP a Open-Meteo para obtener el pronóstico horario.
4. **Extracción y Reporte:** Filtra el archivo JSON de respuesta para aislar la temperatura y humedad exactas a la hora del pitazo inicial, reportándolo en consola.

> [!NOTE]
> Al usar parámetros dinámicos (la fecha de ejecución del sistema), el script funciona como una tarea automatizable (CRON job) que siempre entregará los partidos de la semana en curso.

## 🚀 Ejecución y Resultados
El script no requiere credenciales de API. Solo necesitas tener instalada la librería `requests`.

```yaml
# Ejemplo de salida en consola
Fecha: 2026-10-02
Partido: LOCAL-VISITANTE
Estadio: Azteca
Temperatura: 22.5°C
Humedad: 45%
Hora (GMT-6): 19:00
------------------------------
