from pymongo import MongoClient

class Querys:
        def __init__(self, client):
                self.client = MongoClient(client) 
                
     
        def get_bot_data( self, bot_type, moneda):
                try:
                        db = self.client["datos_trading"]
                        collection = db["trading_data"]
                        query = collection.find(
                                { "bot_type": bot_type, "par": moneda },
                                { "_id": 0,"bet": 1, "date": 1,  },
                                sort=[("date", -1)])
                        
                        result = list(query)
                        return result  
                except Exception as e:
                        print("Error al actualizar los datos:", str(e))
        
        
        def get_lastet_bet_of_bots(self):
                bot_lista = ["MeanReversionBot", "TrendFollowingBot", "MovingAverageCrossoverBot"]
                monedas = ["BTC/USDT", "ETH/USDT", "BNB/USDT", "USDC/USDT"]
                try:
                        db = self.client['datos_trading']
                        collection = db['trading_data']

                        pipeline = [
                        {"$match": {"bot_type": {"$in": bot_lista}, "par": {"$in": monedas}}},
                        {"$sort": {"date": -1}},
                        {"$group": {
                                "_id": {"bot_type": "$bot_type", "par": "$par"},
                                "last_bet": {"$first": "$bet"}
                        }},
                        {"$project": {
                                "_id": 0,
                                "bot_type": "$_id.bot_type",
                                "par": "$_id.par",
                                "bet": "$last_bet"
                        }}
                        ]

                        results = list(collection.aggregate(pipeline))
                        lista_por_par = {}

                        for doc in results:
                                par = doc["par"]
                                bet = doc["bet"]
                                bot_type = doc["bot_type"]
                        
                                if par not in lista_por_par:
                                        lista_por_par[par] = []
                                
                                lista_por_par[par].append({"bet": bet, "bot_type": bot_type})

                        return lista_por_par
                
                except Exception as e:
                        print("Error al actualizar los datos:", str(e))


        def get_latest_data(self, bot_type, par):
                try:
                        db = self.client['datos_trading']
                        collection = db['trading_data']
                        result = collection.find(
                        { "bot_type": bot_type, "par": par },
                        { "moneda": 1, "USDT": 1 },
                        sort=[("date", -1)],
                        limit=1
                        )
                        
                        for document in result:
                                moneda = document["moneda"]
                                usdt = document["USDT"]
                                print("Moneda:", moneda)
                                print("USDT:", usdt)
                                return moneda,usdt
                except Exception as e:
                        print("Error al actualizar los datos:", str(e))
                        
       
        
        def actualizar_datos(self,elemento, valor, id_usuario, valor_numerico):
                try:   
                        db = self.client["datos_trading"]
                        collection = db["usuarios"]
                        
                        # Incrementar el valor del elemento
                        collection.update_one(
                        {"idUser": id_usuario},
                        {"$inc": {elemento: valor}}
                        )
                        
                        # Sumar el valor numérico al campo USDT
                        collection.update_one(
                        {"idUser": id_usuario},
                        {"$inc": {"USDT": valor_numerico}}
                        )
                        
                        print("Datos actualizados exitosamente.")
                except Exception as e:
                        print("Error al actualizar los datos:", str(e))
                        

        def registrarId(self,idUser):
                try:
                        db = self.client["datos_trading"]
                        collection = db["usuarios"]
                        data = {"idUser": idUser,
                                "USDT": 1000,
                                "TF-BTC":0,
                                "MR-BTC":0,
                                "MC-BTC":0,
                                "TF-ETH":0,
                                "MR-ETH":0,
                                "MC-ETH":0,
                                "TF-BNB":0,
                                "MR-BNB":0,
                                "MC-BNB":0,
                                "TF-USDC":0,
                                "MR-USDC":0,
                                "MC-USDC":0                
                                }
                        collection.insert_one(data)
                        print("ID de usuario registrado en MongoDB.")
                except Exception as e:
                        print("Error al registrar el ID de usuario en MongoDB:", str(e))


        def obtenerDatosUsuario(self,idUser):
                try:
                        db = self.client["datos_trading"]
                        collection = db["usuarios"]
                              
                        user_data = collection.find_one({"idUser": idUser})
                        if user_data:
                                del user_data["_id"]  # Eliminar el campo _id del documento
                                return user_data
                        else:
                                return None
                except Exception as e:
                        print("Error al obtener los datos del usuario en MongoDB:", str(e))


if __name__ == "__main__":
    consulta = Querys("mongodb://localhost:27017")

    results = consulta.obtenerDatosUsuario("pJcWswjRFKMuJ07yMTR7Ztof7w73")
    print(results)
    

    

