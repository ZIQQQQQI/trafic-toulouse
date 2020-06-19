import requests
import json
import os
import threading
import time
import csv
import codecs

def get_data_schedule(type):
    #lire des infos de tous les station et Convertir le format json en string
    with open("C:/Users/woshi/Desktop/API-TISSEO/allstops.json",encoding='utf-8') as filestops:#changer en votre propre chemin
        allstops=json.load(filestops)

        #Obtenir les horaires pour chaque station
        for i in range (1,3):#j'essaie seulement 2 ligne,pour recuperer tous les infos, il faut changer en 'range(lens(allstops))'
            stopname=allstops[i]['name']
            stopid=allstops[i]['id']

            #Obtenir les horaires de station
            url = ('https://api.tisseo.fr/v1/stops_schedules.json?stopPointId='+stopid+'&key=75149d16-8610-42e3-a29c-5b1ea8a89a13')
            r = requests.get(url)
            content = json.loads(r.text)
            infoforonestop=content['departures']['departure']

            #Ecrire les info dans un fichier    ex:donnees/Arènes-id=3377699722770341
            pathclasseur="C:/Users/woshi/Desktop/API-TISSEO/data/"+stopname+"-id="+stopid #changer en votre propre chemin
            classeur=os.path.exists(pathclasseur)
            if not classeur:
                os.makedirs(pathclasseur)

            
               
           
               
    
            filename = str(int(time.time()))    

            if type=='csv':
                #change en format csv
                #table head
                datas=[{'stopId':'stopId','dateTime':'dateTime','desCityName':'desCityName',
                'desStopAreaId':'desStopAreaId','desStopName':'desStopName','lineColor':'lineColor',
                'lineName':'lineName','network':'stopAreaName','shortName':'shortName','realTime':'realTime'}]
                
                #donnees d'une ligne
                for i in range(len(infoforonestop)):
                    data={}
                    data['stopId']=stopid
                    data['dateTime']=str(infoforonestop[i]['dateTime'])
                    data['desCityName']=infoforonestop[i]['destination'][0]['cityName']
                    data['desStopAreaId']=infoforonestop[i]['destination'][0]['id']
                    data['desStopName']=infoforonestop[i]['destination'][0]['name']
                    data['lineColor']=infoforonestop[i]['line']['color']
                    data['lineName']=infoforonestop[i]['line']['name']
                    data['network']=infoforonestop[i]['line']['network']
                    data['shortName']=infoforonestop[i]['line']['shortName']
                    data['realTime']=infoforonestop[i]['realTime']
                    
                    datas.append(data)
                f = codecs.open( pathclasseur+'/'+filename+'.csv', 'w','utf_8_sig')
                writer=csv.writer(f)
                
                for item in datas:
                   
                    writer.writerow([item['stopId'], item['dateTime'],item['desCityName'],item['desStopAreaId'],
                    item['desStopName'], item['lineColor'],item['lineName'],item['network'],
                    item['shortName'], item['realTime']])  
                
                    
                    
                    
                
            
            elif type=='json' :
                with open(pathclasseur+'/'+filename+'.json','w') as file:
                    data=json.dumps(infoforonestop)
                    file.write(data)
                    

#Obtenir automatiquement des données à intervalles réguliers
def fun_timer(type):
    get_data_schedule(type)
    global timer
    timer = threading.Timer(5, fun_timer,args=(type,))   #Récuperer les horaires tous les 10 mins
    timer.start()

timer = threading.Timer(5, fun_timer,args=('csv',))  #Premier démarrage
timer.start()

time.sleep(60)#Se termine automatiquement après une heure
timer.cancel()



