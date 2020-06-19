import requests
import json
import os
import threading
import time
import csv
import codecs
import time

def get_data_velo(type):
    #api de velo toulouse
    url='https://api.jcdecaux.com/vls/v1/stations?contract=toulouse&apiKey=716ab39c34be48fb6bd618e02d102ef18d9aec70'
    r=requests.get(url)
    content=json.loads(r.text)

    filename = str(int(time.time()))      
    if type=='csv':
        velos=[{'number':'number','contract_name':'contract_name','name':'name','address':'address',
        'lat':'lat','lng':'lng','bike_stands':'bike_stands','available_bike_stands':'available_bike_stands',
        'available_bikes':'available_bikes','status':'status','last_update':'last_update','time_get':'time_get'}]
        
        for i in range(len(content)):
            velo={}
            velo['number']=content[i]['number']
            velo['contract_name']=content[i]['contract_name']
            velo['name']=content[i]['name']
            velo['address']=content[i]['address']
            velo['lat']=content[i]['position']['lat']
            velo['lng']=content[i]['position']['lng']
            velo['bike_stands']=content[i]['bike_stands']
            velo['available_bike_stands']=content[i]['available_bike_stands']
            velo['available_bikes']=content[i]['available_bikes']
            velo['status']=content[i]['status']
            velo['last_update']=content[i]['last_update']/1000
            velo['time_get']=filename
            

            velos.append(velo)
            
        f = codecs.open('C:/Users/woshi/Desktop/API-Velo/data/'+filename+'.csv', 'w','utf_8_sig')
        writer=csv.writer(f)
        for item in velos:
            writer.writerow([item['number'], item['contract_name'],item['name'],item['address'],item['lat'],item['lng'],item['bike_stands'],item['available_bike_stands'],item['available_bikes'],item['status'],item['last_update'],
            item['time_get']])   
      
    
    elif type=='json' :
        with open('C:/Users/woshi/Desktop/API-Velo/data/'+filename+'.json','w') as file:
                data=json.dumps(content)
                file.write(data)
    
   

def fun_timer(type):
    get_data_velo(type)
    global timer
    timer = threading.Timer(5,fun_timer,args=(type,))   #Récuperer les horaires tous les 10s
    timer.start()

timer = threading.Timer(0, fun_timer,args=('csv',))  #Premier démarrage
timer.start()

time.sleep(36000)#Se termine automatiquement après une heure
timer.cancel()