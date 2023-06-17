from fastapi import FastAPI
import uvicorn
import bots as b
import asyncio
import multiprocessing
import querys
import usuarios
import urllib.parse
import usuarios

app = FastAPI()
bot_manager = b.BotManager()
consultas = querys.Querys("mongodb://localhost:27017/")

@app.get("/bot_data/{bot_type}/{m1}/{m2}")
async def get_bot_data(bot_type: str, m1: str, m2: str):

    par = urllib.parse.unquote(m1) + "/" + urllib.parse.unquote(m2)
    data = consultas.get_bot_data(bot_type, par)

    return data

@app.get("/sell_buy/{idUser}/{coin_compra}/{compra}/{coin_venta}/{venta}")
async def sell_buy(idUser: str,coin_compra : str ,compra: str,coin_venta : str, venta: str):

    idUser_decode = urllib.parse.unquote(idUser) 
    compra_decode = urllib.parse.unquote(compra)
    venta_decode = urllib.parse.unquote(venta)
    coin_compra_decode = urllib.parse.unquote(coin_compra)
    coin_venta_decode = urllib.parse.unquote(coin_venta)
    compra_float = float(compra_decode)
    venta_float = float(venta_decode)
    lista = [ {"idUser": idUser_decode},{coin_compra_decode: compra_float},{coin_venta_decode: venta_float}]
    data = consultas.update_data(lista)

    return data

@app.get("/login/{email}/{password}")
async def login(email: str,password: str):
    email_decode = urllib.parse.unquote(email)
    password_decode =  urllib.parse.unquote(password)
    data = usuarios.login(email_decode,password_decode)
    print(data)
    return data


@app.get("/bot_data/")
async def get_bots_bet():
    data = consultas.get_lastet_bet_of_bots()
    return data
    
@app.get("/sing_up/{email}/{password}")
async def sing_up(email: str, password: str):
    email_decode = urllib.parse.unquote(email)
    password_decode =  urllib.parse.unquote(password)
    data = usuarios.sing_up(email_decode,password_decode)
    return data


    
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