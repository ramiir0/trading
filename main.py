
"""mi key de APIKEY https://www.alphavantage.co/support/#api-key

LRKO3AKQFVFVULAK.

mi key de newsapi   https://newsapi.org/
ac87867e6155429dad8ab909b00ccfc2
"""
import requests
import os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

MY_STOCK_KEY_API = "LRKO3AKQFVFVULAK"
NEWS_KEY_API = "ac87867e6155429dad8ab909b00ccfc2"

SID_TWILIO = "AC9755cfa4a9472a38695c8a4676acd379"
TOKEN_TWILIO = "adffd131de2d2dfe7ffb4b619fb75aaf"

#client = Client(account_sid, auth_token)
cliente = Client(SID_TWILIO, TOKEN_TWILIO)

stock_parametros= {
    "function": "TIME_SERIES_DAILY", 
    "symbol": STOCK_NAME,
    "apikey": MY_STOCK_KEY_API,
}
conexion = requests.get(url=STOCK_ENDPOINT, params=stock_parametros)
conexion.raise_for_status()
datos = conexion.json()["Time Series (Daily)"]
# print(datos)

lista_datos = [valor for (llave, valor) in datos.items()]
# print(lista_datos)
precio_ayer = lista_datos[0]
# print(precio_ayer)
cierre_ayer = precio_ayer["4. close"]
# print(cierre_ayer)
datos_antier = lista_datos[1]
cierre_antier = datos_antier["4. close"]
# print(cierre_antier)
diferencia_precio = abs(float(cierre_ayer) - float(cierre_antier))
# print(diferencia_precio)
dif_porcentaje = (diferencia_precio / float(cierre_ayer)) * 100
print(dif_porcentaje)

parametros_noticia = {
    "apiKey": NEWS_KEY_API,
    "qInTitle": COMPANY_NAME,
}
if dif_porcentaje > 0.1:
    conexion_noticias = requests.get(NEWS_ENDPOINT, params= parametros_noticia)
    conexion_noticias.raise_for_status()
    datos_noticia = conexion_noticias.json()["articles"]
    # print(datos_noticia)
    tres_articulos = datos_noticia[:3]  #es un cortador y solo nos mostrara el numero de datos que queremos de una lista
    # print(tres_articulos)
    formato_msj = [f"Titulo:{article['title']}. \nDescrip:{article['description']}" for article in tres_articulos]
    # print(formato_msj)
    for article in formato_msj:
        mensaje = cliente.messages.create(
            body=article,
            from_= +13852339889,
            to= +523310815627
        )