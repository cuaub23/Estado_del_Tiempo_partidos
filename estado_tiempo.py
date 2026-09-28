import requests
import json
import sqlite3
from datetime import date, timedelta


def obtener_partidos_proxima_semana(db_path="partidos.db"):
    """
    Se conecta a la base de datos y recupera los partidos programados 
    para los próximos 7 días a partir de la fecha actual.
    
    Salida: Lista de registros (tipo sqlite3.Row) con los datos de cada partido.
    """
    hoy = date.today()
    semana_despues = hoy + timedelta(days=7)
    
    with sqlite3.connect(db_path) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        
        sql_query = f""" 
            SELECT partido, estadio, lat, log, fecha_hora
            FROM partidos
            WHERE fecha_hora > ? AND fecha_hora < ?
            ORDER BY fecha_hora ASC;
        """
        
        cur.execute(sql_query, (hoy.isoformat(), semana_despues.isoformat()))
        return cur.fetchall()


def obtener_clima_partido(lat, lon, hora_partido):
    """
    Consulta la API de Open-Meteo para obtener la temperatura y humedad 
    exacta pronosticada a la hora del evento.
    
    Entrada: latitud, longitud (float/str) y la hora del partido (str formato ISO).
    Salida: Tupla con (temperatura, humedad) o (None, None) en caso de error.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,precipitation,relative_humidity_2m",
        "timezone": "America/Mexico_City"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status() 
        
        data = response.json()
        
        indice = data["hourly"]["time"].index(hora_partido)
        temp = data["hourly"]["temperature_2m"][indice]
        humedad = data["hourly"]["relative_humidity_2m"][indice]
        
        return temp, humedad
        
    except requests.exceptions.RequestException as e:
        print(f"Error de red al consultar el clima: {e}")
    except ValueError:
        print(f"Error: La hora '{hora_partido}' no se encontró en el pronóstico de la API.")
        
    return None, None


# =============================================================================
# BLOQUE DE EJECUCIÓN PRINCIPAL
# =============================================================================
if __name__ == "__main__":
    # 1. Extraemos los partidos de la base de datos
    partidos = obtener_partidos_proxima_semana("partidos.db")

    # 2. Iteramos para obtener los datos con el clima
    for partido in partidos:
        hora_partido = partido["fecha_hora"]
        part = partido["partido"]
        estadio = partido["estadio"]
        
        temp, humedad = obtener_clima_partido(
            lat=partido["lat"], 
            lon=partido["log"], 
            hora_partido=hora_partido
        )
        
        # Solo imprimimos si la API nos devolvió datos válidos
        if temp is not None and humedad is not None:
            # Dividimos la fecha y la hora basándonos en el formato ISO (YYYY-MM-DDTHH:MM)
            fecha = hora_partido[:10]
            hora = hora_partido[11:]
            
            print(f"Fecha: {fecha}")
            print(f"Partido: {part}")
            print(f"Estadio: {estadio}")
            print(f"Temperatura: {temp}°C")
            print(f"Humedad: {humedad}%")
            print(f"Hora (GMT-6): {hora}\n")
            print("-" * 30)
