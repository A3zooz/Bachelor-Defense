import pandas as pd
import numpy as np
import json

def Create_input():
    df_excel = pd.read_csv('loldata.csv')
    print(len(df_excel))
    External = []
    Supervisor = []
    ID = []
    Room = []

    for i in range(len(df_excel)-1):
        External.append(df_excel["External Reviewer"][i])
    for i in range(len(df_excel)-1):
        Supervisor.append(df_excel["Supervisor"][i])
    for i in range(len(df_excel)-1):
        ID.append(df_excel["Student ID"][i])
    for i in range(len(df_excel)-1):
        Room.append(df_excel["Defense Location"][i])
        
    Room2=list(set(Room))
    External2=list(set(External))
    Supervisor2=list(set(Supervisor))

    dictionary = {
        "Rooms": Room2,
        "Defense": [],
        "External constraints":[],
        "Supervisor constraints":[]
    }
    dic2 ={}
    for i in range(len(External)):
        dic ={
            "Examiner":External[i],
            "Supervisor":Supervisor[i],
            "Student": ID[i]
        }
        dictionary["Defense"].append(dic)
        
    for i in range(len(External2)):
        test = {}
        test[External2[i]]=[0]*180
        # dic2.setdefault(External2[i], [])
        dictionary["External constraints"].append(test)
    for i in range(len(Supervisor2)):
        test = {}
        test[Supervisor2[i]]=[0]*180
        # dic2.setdefault(External2[i], [])
        dictionary["Supervisor constraints"].append(test)

    # Serializing json
    json_object = json.dumps(dictionary, indent=4)

    # Writing to sample.json
    with open("InputData.json", "w") as outfile:
        outfile.write(json_object)
    return "InputData.json"