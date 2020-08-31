import requests
import json
import pprint
import csv

#Abro el csv
key_open_weather = 'dbab0df10e6e13cff5c0becfbfae9139'
key_open_geo  = '931f2abe294f4d9ea74afa0cf790df99'

#Si tuviera un archivo con 500 ciudades es dificil darse cuenta rapida donde esta el error
#Por eso se crea un archivo con los logs de errores 
with open('sucursales_sol_360.csv') as csv_hoteles, open('sucursales_con_clima.csv','w') as csv_hoteles_clima, open('log_errores.txt','w') as errores:
    hoteles=csv.reader(csv_hoteles, delimiter=';')
    for ciudad in hoteles:
        nombre_ciudad = ciudad[0]+ ', ' +ciudad[1] + ', Argentina' #CLAVE PONER ARGENTINA SINO TE PUEDE TOMAR DE OTRO PAIS
        #print(nombre_ciudad) Merlo, San Luis  Ushuaia, Tierra del fuego  etc
        ciudad_cod=requests.utils.quote(nombre_ciudad)
        #Primero tengo que darle de comer a la primera API 
        url_geo='https://api.opencagedata.com/geocode/v1/json?q=' + ciudad_cod +'&key=' + key_open_geo
        objeto_geo=json.loads(requests.get(url_geo).text)
        #pprint.pprint(objeto_geo)
        lat = objeto_geo['results'][0]['geometry']['lat']
        lon = objeto_geo['results'][0]['geometry']['lng']
        #print(nombre_ciudad,lat,lon)
        
        
#%%        
        
        #api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={your api key}
        #No necesito mas el nombre de la ciudad_cod ahora pongo directamente las coordenadas
        url = "https://api.openweathermap.org/data/2.5/weather?lat=" + str(lat) + "&lon=" + str(lon) + "&units=metric&lang=es&appid=" + key_open_weather
        objeto=json.loads(requests.get(url).text)
        #if 'main' in objeto.keys(): #Poprque sino da Keyerror main entonces veo si lo agarra
        if objeto.get('main'):
            print("El clima en", nombre_ciudad)
            print("La temperatura es de ",objeto['main']['temp'],'C')
            print("La humedad es de ", objeto['main']['humidity'],'%')
            print("El clima: ", objeto['weather'][0]['description'] + '\n')
        else: 
            print("No existe la ciudad: ", nombre_ciudad, '\n')
            errores.write("No existe lal ciudad " + nombre_ciudad + '\n')
            #Escribo en un txt las ciudades que dieron error o que no existen
#Ahora hay que solucionar esos errores de CABA e IBERA parece que no estan en la base de datos de open weather
#Necesito encontrar una API que le pase la ciudad y me devuelva las coordenadas
            