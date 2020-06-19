import requests
import json
import os
import time


#fonction pour récupérer toutes les lignes de bus et tram
def get_data_lines():
    #Obtenir les données de ligne et Convertir le format json en string
    url='https://api.tisseo.fr/v1/lines.json?key=75149d16-8610-42e3-a29c-5b1ea8a89a13'
    r= requests.get(url)
    content=json.loads(r.text)
    lines=content['lines']['line']

    #Créer une liste vide pour stocker les lignes de bus et tram
    linesutiles = []
    #Vérifier tous les donnée
    for i in range(len(lines)):

        #les noms de la ligne spéciale
        speciale=['A','B','AERO','CIMTR','NCHR','NOCT','REL','VILLE']

        #nom court pour une ligne
        shortname=lines[i]['shortName']

        #Créer un dictionaire vide pour stocker info utile d'une ligne
        line={}

        #si la ligne est bus ou tram, ajouter info de ce ligne dans la liste
        if shortname not in speciale:
            line['shortname']=shortname
            line['id']=lines[i]['id']
            linesutiles.append(line)
    return linesutiles

#fonction pour obtenir les stations de toutes les lignes (supprimez les doublons)
def get_data_station(linesutiles):
    #Créer un liste avec les données initiales(Peut obtenir de la longueur pour la déduplication)
    allstops=[{"id":1,"name":'test',"stopareaid":1}]

    #Chercher les infos de toutes les lignes
    for i in range(len(linesutiles)):
        #Obtenir les données de station pour une ligne et Convertir le format json en string
        lineid=linesutiles[i]['id']
        url = ('https://api.tisseo.fr/v1/stop_points.json?lineId=' + lineid + '&key=75149d16-8610-42e3-a29c-5b1ea8a89a13')
        r = requests.get(url)
        content = json.loads(r.text)
        stopsforoneligne=content['physicalStops']['physicalStop']

        #Vérifier tous les stations de ce ligne
        for j in range(len(stopsforoneligne)):
            stop = {}
            stop['id']=stopsforoneligne[j]['id']
            stop ['name']=stopsforoneligne[j]['name']
            stop['stopareaid']=stopsforoneligne[j]['stopArea']['id']

            #Ajouter les infos de station, si l'ID de la station n'est plus dans la liste

            count=True
            for k in range(len(allstops)):
                if allstops[k]['id']==stop['id']:
                    count=False
                    break
            if count:
                allstops.append(stop)
    #Ecrire les infos de station dans le fichier 'allstops' en format json

    with open("C:/Users/woshi/Desktop/API-TISSEO/allstops.json", "w") as file:
        jas = json.dumps(allstops)
        file.write(jas)




get_data_station(get_data_lines())