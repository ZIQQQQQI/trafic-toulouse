import pandas as pd
import os


def group_files():
    Folder_Path = "C:/Users/woshi/Desktop/API-TISSEO/jean/Jean_Jaurès-id=3377704015496685/"
    SaveFile_Path = 'C:/Users/woshi/Desktop/API-TISSEO/jean/Jean_Jaurès-id=3377704015496685/'  # 拼接后要保存的文件路径
    SaveFile_Name = 'all.csv'  # 合并后要保存的文件名

    # 修改当前工作目录
    os.chdir(Folder_Path)
    # 将该文件夹下的所有文件名存入一个列表
    file_list = os.listdir()

    # 读取第一个CSV文件并包含表头
    df = pd.read_csv(Folder_Path + file_list[0])  # 编码默认UTF-8，若乱码自行更改

    # 将读取的第一个CSV文件写入合并后的文件保存
    df.to_csv(SaveFile_Path + SaveFile_Name, encoding="utf_8_sig", index=0)

    # 循环遍历列表中各个CSV文件名，并追加到合并后的文件
    for i in range(1, len(file_list)):
        df = pd.read_csv(Folder_Path + file_list[i])
        df.to_csv(SaveFile_Path + SaveFile_Name, encoding="utf_8_sig", index=0, header=0, mode='a+')



group_files()

