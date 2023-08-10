import requests
import pandas as pd
from datetime import datetime
from config import Config
import os
from sqlalchemy import create_engine

cities =  ["London", "New York", "Cordoba", "Taipei", "Buenos Aires", "Mexico City", "Dublin", "Tbilisi", "Bogota", "Tokio"]

API_KEY = Config.API_TOKEN
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast?"
DAILY_TIME = ''

year = 0
month = 0
day = 0

def obtener_datos_climaticos_ciudades(list_of_cities):
    for j in range(1,40,8):
        d = {'ids' : [], 'cities': [], 'temperature' : [], 'humidity': [], 'wind_speed': [], 'date':[]}
        for i in list_of_cities:
            url = f"{BASE_URL}q={i}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                id = data['city']['id']
                name = data['city']['name']
                temperature = data['list'][j]['main']['temp']
                humidity = data['list'][j]['main']['humidity']
                wind_speed = data['list'][j]['wind']['speed']
                date = data['list'][j]['dt']
                date_datetime = datetime.fromtimestamp(date)
                year = date_datetime.year
                month = date_datetime.month
                day = date_datetime.day
                d["ids"].append(id)
                d["cities"].append(name)
                d["temperature"].append(temperature)
                d["humidity"].append(humidity)
                d["wind_speed"].append(wind_speed)
                d["date"].append(str(year)+"/"+str(month)+"/"+str(day))
                if(cities.index(i)==0):
                    DAILY_TIME = str(year)+str(month)+str(day)
            else:
                print(f"Error al obtener los datos de la ciudad de {name}: codigo {response.status_code}")
        df = pd.DataFrame(data=d)
        output_dir = "data_analytics/openweather"
        os.makedirs(output_dir, exist_ok=True)
        csv_file_path = os.path.join(output_dir, f"tiempodiario_{DAILY_TIME}.csv")
        df.to_csv(csv_file_path, index=False)
    return df


if __name__ == '__main__':
    obtener_datos_climaticos_ciudades(cities)

    # Leer las credenciales de conexión a la base de datos desde el archivo config.py
    config = Config()
    
    # Establecer la conexión a la base de datos PostgreSQL utilizando SQLalchemy
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)

    # Función para cargar datos de CSV a la base de datos
    def load_data_to_database(csv_path):
        df = pd.read_csv(csv_path)
        table_name = "weather_data"
        df.to_sql(table_name, engine, if_exists="append", index=True)
        print(f"Datos cargados en la tabla '{table_name}'.")

    # Ruta de los archivos CSV generados previamente
    folder_path = "data_analytics/openweather" 
    file_paths = []

    # Recorre la carpeta y obtiene la lista de rutas de archivos
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_paths.append(os.path.join(root, file))
    
    print(file_paths)

    # Cargar datos de todos los archivos CSV a la base de datos
    for csv_path in file_paths:
        load_data_to_database(csv_path)
    