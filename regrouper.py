import pandas as pd
import os


def group_files():
    Folder_Path = "C:/git/trafic-toulouse/trafic-toulouse/API-TISSEO/jean/Jean_Jaurès-id=3377704015496685/"
    SaveFile_Path = 'C:/git/trafic-toulouse/trafic-toulouse/API-TISSEO/jean/Jean_Jaurès-id=3377704015496685/'  # chemin d'enregister
    SaveFile_Name = 'allData.csv'  # nom de fiche

    # change res maintenant
    os.chdir(Folder_Path)
    # concevoir tous les noms de fiches
    file_list = os.listdir()

    # premier ficher
    df = pd.read_csv(Folder_Path + file_list[0])  # utf-8 par default

    # read premier fiche
    df.to_csv(SaveFile_Path + SaveFile_Name, encoding="utf_8_sig", index=0)

    # read toutes les fiches
    for i in range(1, len(file_list)):
        df = pd.read_csv(Folder_Path + file_list[i])
        df.to_csv(SaveFile_Path + SaveFile_Name, encoding="utf_8_sig", index=0, header=0, mode='a+')



group_files()

