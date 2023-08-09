from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.orm import declarative_base
from config import Config

Base = declarative_base()

class WeatherData(Base):
    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key=True)
    cities = Column(String)
    temperature = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    date = Column(DateTime)
# Leer las credenciales de conexión a la base de datos desde el archivo config.py
config = Config()

# Establecer la conexión a la base de datos PostgreSQL utilizando SQLalchemy
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)