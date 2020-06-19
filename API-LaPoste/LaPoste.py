import requests
import json
import os
import threading
import time
import csv
import codecs

def get_data_LaPoste(type):
    #liste de code postal de toulouse
    listeCode=['31000','31100','31200','31300','31400','31500']
    urlNbLignes='https://datanova.laposte.fr/api/records/1.0/search/?dataset=laposte_poincont&q=&rows=1&facet=code_postal&facet=localite&facet=code_insee&facet=precision_du_geocodage&refine.code_postal='
    
    for i in listeCode:
        url=urlNbLignes+i
        r=requests.get(url)
        content=json.loads(r.text)
        #y combien de lignde pour un code postal
        lignes=str(content['nhits'])
        #toutes les donnees pour un code postal
        urlData='https://datanova.laposte.fr/api/records/1.0/search/?dataset=laposte_poincont&q=&rows='+lignes+'&facet=code_postal&facet=localite&facet=code_insee&facet=precision_du_geocodage&refine.code_postal='+i
        re=requests.get(urlData)
        contents=json.loads(re.text)
        contentData=contents['records']
        print(urlData)
        
        
        filename = str(int(time.time()))   

        if type=='csv':
            datas=[{'codePostal':'codePostal','longitude':'longitude','latitude':'latitude',
            'adress':'adress','libelle_du_site':'libelle_du_site' ,'record_timestamp':'record_timestamp'}]
            

            for j in range(len(contentData)):
                dataCsv={}
                dataCsv['codePostal']=i
                dataCsv['longitude']=contentData[j]['fields']['latlong'][1]
                dataCsv['latitude']=contentData[j]['fields']['latlong'][0]
                dataCsv['adress']=contentData[j]['fields']['adresse']
                dataCsv['libelle_du_site']=contentData[j]['fields']['libelle_du_site']
                dataCsv['record_timestamp']=contentData[j]['record_timestamp']
                datas.append(dataCsv)
            


            f = codecs.open('C:/Users/woshi/Desktop/API-LaPoste/'+i+'/'+filename+'.csv', 'w','utf_8_sig')
            writer=csv.writer(f)
            for item in datas:
                writer.writerow([item['codePostal'], item['longitude'],item['latitude'],item['adress'],
                item['libelle_du_site'],item['record_timestamp']])   

        elif type=='json' :
            with open('C:/Users/woshi/Desktop/API-LaPoste/'+i+'/'+filename+".json",'w') as file:
                data=json.dumps(contentData)
                file.write(data)

def fun_timer(type):
    get_data_LaPoste(type)
    global timer
    timer = threading.Timer(5, fun_timer,args=(type,))   #Récuperer les horaires tous les 5s
    timer.start()

timer = threading.Timer(0, fun_timer,args=('csv',))  #Premier démarrage argument signe le format de ficher: csv ou json
timer.start()

time.sleep(3600)#Se termine automatiquement après une heure
timer.cancel()
