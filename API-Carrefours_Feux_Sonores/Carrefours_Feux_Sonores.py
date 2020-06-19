import requests
import json
import os
import threading
import time
import csv
import codecs

def get_data_carrefour(type):
    #trouver le totalite de donnees
    url='https://data.toulouse-metropole.fr/api/records/1.0/search/?dataset=carrefours-feux-sonores&q=&rows=1'
    r=requests.get(url)
    content=json.loads(r.text)

    #trouves des donnees
    lignes=str(content['nhits'])
    dataurl='https://data.toulouse-metropole.fr/api/records/1.0/search/?dataset=carrefours-feux-sonores&q=&rows='+lignes
    re=requests.get(dataurl)
    donnees=json.loads(re.text)
    data=donnees['records']

    carrefours = [{'nom':'nom','latitue':'latitue','longitude':'longitude','type':'type','sonore':'sonore'}]
    #change des donnee dans un dictionairy non 'emboiter'
    for i in range(len(data)):
        #Créer un dictionaire vide pour stocker info utile d'une ligne
        carrefour={}
        carrefour['nom']=data[i]['fields']['nom']
        carrefour['latitue']=data[i]['fields']["geo_point_2d"][0]
        carrefour['longitude']=data[i]['fields']["geo_point_2d"][1]
        carrefour['type']=data[i]['fields']["genre"]
        carrefour['sonore']=data[i]['fields']["sonore"]
        carrefours.append(carrefour)
    
    filename = str(int(time.time()))      
    if type=='csv':
        
        f = codecs.open('C:/Users/woshi/Desktop/API-Carrefours_Feux_Sonores/data/'+filename+'.csv', 'w','utf_8_sig')
        writer=csv.writer(f)
        for item in carrefours:
            writer.writerow([item['nom'], item['latitue'],item['longitude'],item['type'],item['sonore']])   
      
    
    elif type=='json' :
        with open('C:/Users/woshi/Desktop/API-Carrefours_Feux_Sonores/data/'+filename+".json",'w') as file:
            data=json.dumps(carrefours)
            file.write(data)
    

def fun_timer(type):
    get_data_carrefour(type)
    global timer
    timer = threading.Timer(5, fun_timer,args=(type,))   #Récuperer les horaires tous les 5s
    timer.start()

timer = threading.Timer(0, fun_timer,args=('csv',))  #Premier démarrage argument signe le format de ficher: csv ou json
timer.start()

time.sleep(60)#Se termine automatiquement après une heure
timer.cancel()








