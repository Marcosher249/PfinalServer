from fastapi import FastAPI
import uvicorn
import bots as b
import asyncio
import multiprocessing
import querys
import usuarios
import urllib.parse

app = FastAPI()
bot_manager = b.BotManager()
consultas = querys.Querys("mongodb://localhost:27017/")

@app.get("/bot_data/{bot_type}/{m1}/{m2}")
def get_bot_data(bot_type: str, m1: str, m2: str):

    par = urllib.parse.unquote(m1) + "/" + urllib.parse.unquote(m2)
    data = consultas.get_bot_data(bot_type, par)
    return data

@app.get("/bot_data/")
def get_bots_bet():
    data = consultas.get_lastet_bet_of_bots( pa)
    return data

@app.get("/login/{correo}/{contraseña}")
def login(correo: str, contraseña: str):
    correo_des = urllib.parse.unquote(correo)
    contraseña_des = urllib.parse.unquote(contraseña)
    data = usuarios.login(correo_des,contraseña_des)
    return data

@app.get("/singUp/{correo}/{contraseña}")
def login(correo: str, contraseña: str):
    usuarios.login(correo,contraseña)


    
def run_bot_manager():
    asyncio.run(bot_manager.main())

if __name__ == "__main__":
    # Crear un proceso para ejecutar el BotManager
    bot_manager_process = multiprocessing.Process(target=run_bot_manager)
    bot_manager_process.start()

    # Ejecutar la API FastAPI en el proceso principal
    uvicorn.run(app, host="0.0.0.0", port=8000)

    # Esperar a que el proceso del BotManager termine
    bot_manager_process.join()