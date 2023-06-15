import ccxt as c
import pandas as pd
import dataFrame as d
import asyncio
from asyncio import Queue
from pymongo import MongoClient
import querys


class TrendFollowingBot:
    def __init__(self, moneda, data_queue):
        self.moneda = moneda
        self.consult = querys.Querys("mongodb://localhost:27017")
        self.btc,self.usdt = self.consult.get_latest_data("TrendFollowingBot", moneda)
        self.data_queue = data_queue

    async def run(self):
        print("ejecucion de bot TrendFollowingBot")
        while True:
            tabla = await d.Grafica(self.moneda).tabla()
            # Aplicar la estrategia de seguimiento de tendencia
            
            max_high = max(tabla['High'][(len(tabla)-1)-10:(len(tabla)-1)])
            min_low = min(tabla['Low'][(len(tabla)-1)-10:(len(tabla)-1)])
            self.current_price = tabla['Close'][len(tabla)-1]
            self.date = tabla.index[len(tabla)-1]

            if self.current_price > max_high and self.usdt > 0:
                # Realizar una compra de BTC con USDT
                self.buy_btc()

            if self.current_price < min_low and self.btc > 0:
                # Realizar una venta de BTC por USDT
                self.sell_btc()
            
            await self.calcul_bet()

            await asyncio.sleep(60)  # Esperar 60 segundos antes de la siguiente iteración

    def buy_btc(self):
        # Lógica para realizar una compra de BTC con USDT
        # Actualizar los saldos
        self.btc += (0.1*self.usdt) / self.current_price  # Comprar 0.1 BTC
        self.usdt -= 0.1 * self.usdt  # Restar el equivalente en USDT

    def sell_btc(self):
        # Lógica para realizar una venta de BTC por USDT
        # Actualizar los saldos
        self.usdt += 0.1 * self.btc * self.current_price  # Sumar el equivalente en USDT
        self.btc -= 0.1 * self.btc  # Vender 0.1 BTC
    
    async def calcul_bet(self):
        q =self.data_queue
        bet = (self.usdt + self.btc * self.current_price) / 1000
        print(f"TrendFollowingBot con {self.moneda}: {bet} Fecha: {self.date}")
        data = {
            "bot_type": "TrendFollowingBot",
            "par": self.moneda,
            "bet": bet,
            "date": self.date,
            "moneda": self.btc,
            "USDT": self.usdt
        }
        await self.data_queue.put(data)

class MeanReversionBot:
    def __init__(self, moneda, data_queue):
        self.moneda = moneda
        self.consult = querys.Querys("mongodb://localhost:27017")
        self.btc,self.usdt = self.consult.get_latest_data("MeanReversionBot", moneda)
        self.data_queue = data_queue

    async def run(self):
        print("ejecucion de bot MeanReversionBot")
        while True:
            tabla = await d.Grafica(self.moneda).tabla()
            # Calcular la media móvil de 20 periodos
            tabla['SMA_20'] = tabla['Close'].rolling(window=20).mean()

            # Aplicar la estrategia de reversión a la media
            
            self.current_price = tabla['Close'][len(tabla)-1]
            sma_20 = tabla['SMA_20'][len(tabla)-1]
            self.date = tabla.index[len(tabla)-1]

            if self.current_price < sma_20 and self.usdt > 0:
                # Realizar una compra de BTC con USDT
                self.buy_btc()

            if self.current_price > sma_20 and self.btc > 0:
                # Realizar una venta de BTC por USDT
                self.sell_btc()

            await self.calcul_bet()

            await asyncio.sleep(60)  # Esperar 60 segundos antes de la siguiente iteración

    def buy_btc(self):
        # Lógica para realizar una compra de BTC con USDT
        # Actualizar los saldos
        self.btc += (0.1*self.usdt) / self.current_price  # Comprar 0.1 BTC
        self.usdt -= 0.1 * self.usdt  # Restar el equivalente en USDT

    def sell_btc(self):
        # Lógica para realizar una venta de BTC por USDT
        # Actualizar los saldos
        self.usdt += 0.1 * self.btc * self.current_price  # Sumar el equivalente en USDT
        self.btc -= 0.1 * self.btc  # Vender 0.1 BTC

    async def calcul_bet(self):
        bet = (self.usdt + self.btc * self.current_price) / 1000
        print(f"MeanReversionBot con {self.moneda}: {bet} Fecha: {self.date}")
        data = {
            "bot_type": "MeanReversionBot",
            "par": self.moneda,
            "bet": bet,
            "date": self.date,
            "moneda": self.btc,
            "USDT": self.usdt
        }
        await self.data_queue.put(data)

class MovingAverageCrossoverBot:
    def __init__(self, moneda, data_queue):
        self.moneda = moneda
        self.consult = querys.Querys("mongodb://localhost:27017")
        self.btc,self.usdt = self.consult.get_latest_data("MovingAverageCrossoverBot", moneda)
        self.data_queue = data_queue

    async def run(self):
        print("ejecucion de bot MovingAverageCrossoverBot")
        while True:
            tabla = await d.Grafica(self.moneda).tabla()
            # Calcular las medias móviles
            tabla['SMA_50'] = tabla['Close'].rolling(window=50).mean()
            tabla['SMA_200'] = tabla['Close'].rolling(window=200).mean()
            # Aplicar la estrategia de cruce de medias móviles
            
            sma_50 = tabla['SMA_50'][len(tabla)-1]
            sma_200 = tabla['SMA_200'][len(tabla)-1]
            previous_sma_50 = tabla['SMA_50'][len(tabla)-2]
            previous_sma_200 = tabla['SMA_200'][len(tabla)-2]
            self.current_price = tabla['Close'][len(tabla)-1]
            self.date = tabla.index[len(tabla)-1]

            if previous_sma_50 < previous_sma_200 and sma_50 > sma_200 and self.usdt > 0:
                # Realizar una compra de BTC con USDT
                self.buy_btc()

            if previous_sma_50 > previous_sma_200 and sma_50 < sma_200 and self.btc > 0:
                # Realizar una venta de BTC por USDT
                self.sell_btc()

            await self.calcul_bet()

            await asyncio.sleep(60)  # Esperar 60 segundos antes de la siguiente iteración

    def buy_btc(self):
        # Lógica para realizar una compra de BTC con USDT
        # Actualizar los saldos
        self.btc += (0.1*self.usdt) / self.current_price  # Comprar 0.1 BTC
        self.usdt -= 0.1 * self.usdt  # Restar el equivalente en USDT

    def sell_btc(self):
        # Lógica para realizar una venta de BTC por USDT
        # Actualizar los saldos
        self.usdt += 0.1 * self.btc * self.current_price  # Sumar el equivalente en USDT
        self.btc -= 0.1 * self.btc  # Vender 0.1 BTC

    async def calcul_bet(self):
        bet = (self.usdt + self.btc * self.current_price) / 1000
        print(f"MovingAverageCrossoverBot con {self.moneda}: {bet} Fecha: {self.date}")

        data = {
            "bot_type": "MovingAverageCrossoverBot",
            "par": self.moneda,
            "bet": bet,
            "date": self.date,
            "moneda": self.btc,
            "USDT": self.usdt
        }
        await self.data_queue.put(data)

class BotManager:
    def __init__(self):
        self.monedas = ["BTC/USDT", "ETH/USDT", "BNB/USDT", "USDC/USDT"]
        self.bots = []
        self.data_queue = Queue()
        self.consult = querys.Querys("mongodb://localhost:27017")


    def create_bots(self):
        print("Creacion de bots")
        for par in self.monedas:
            bot1 = TrendFollowingBot(par,self.data_queue)
            bot2 = MeanReversionBot(par,self.data_queue)
            bot3 = MovingAverageCrossoverBot(par,self.data_queue)
            self.bots.extend([bot1, bot2, bot3])


    async def run_bots(self):
        bot_tasks = [bot.run() for bot in self.bots]
        await asyncio.gather( *bot_tasks)

    async def dump_data_to_mongodb(self,mongodb_uri, database_name, collection_name):
        while True:
            print("Pasando datos a la base de datos")
            client = MongoClient(mongodb_uri)
            db = client[database_name]
            collection = db[collection_name]
            data_list = []
            if not self.data_queue.empty():
                while not self.data_queue.empty():
                    data = await self.data_queue.get()
                    data_list.append(data)

                for data in data_list:
                    # Modificar los datos antes de insertarlos en MongoDB
                    collection.insert_one(data)


            await asyncio.sleep(60)
    async def main(self):
        self.create_bots()
        await asyncio.gather(self.run_bots(),self.dump_data_to_mongodb("mongodb://localhost:27017/", "datos_trading", "trading_data"))




# if __name__ == "__main__":
#     bot_manager = BotManager()
#     asyncio.run(bot_manager.main())