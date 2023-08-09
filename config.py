class Config:
    API_TOKEN = "tu_token"
    # Configuración de la conexión a la base de datos PostgreSQL
    DB_USERNAME = "tu_usuario_de_la_bd"
    DB_PASSWORD = "tu_password"
    DB_HOST = "tu_host"
    DB_PORT = "puerto_host"
    DB_NAME = "nombre_bd"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"