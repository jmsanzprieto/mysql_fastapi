# main.py
import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from app.config import DATABASE_URL

app = FastAPI()

# Crear un motor de base de datos
engine = create_engine(DATABASE_URL)

# Endpoint para verificar la conexión a la base de datos
@app.get("/health")
def check_db_connection():
    try:
        # Intentar conectar a la base de datos
        with engine.connect() as connection:
            # Si la conexión es exitosa, responder con OK
            return JSONResponse(content={"status": "OK"}, status_code=200)
    except SQLAlchemyError as e:
        # Si hay un error en la conexión, responder con KO
        return JSONResponse(content={"status": "KO", "detail": str(e)}, status_code=500)

# Endpoint para obtener los últimos registros de la tabla  y guardarlos en un archivo JSON
@app.get("/usuarios")
def get_usuarios():
    query = text("SELECT * FROM tabla ORDER BY le900Id ")
    try:
        with engine.connect() as connection:
            result = connection.execute(query)
            rows = [dict(row) for row in result.mappings()] 

            # Guardar los datos en un archivo JSON
            with open("usuarios.json", "w") as f:
                json.dump(rows, f, indent=4)

            return JSONResponse(content={"status": "OK", "data": rows}, status_code=200)
    except SQLAlchemyError as e:
        # Si hay un error en la consulta, responder con KO
        return JSONResponse(content={"status": "KO", "detail": str(e)}, status_code=500)
