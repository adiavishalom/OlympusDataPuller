import os
import pandas as pd
import PySimpleGUI as sg


def readCSV(path):
    try:
        df = pd.read_csv(path + '/list.csv')
    except:
        df = pd.DataFrame({'Host Name': [], 'IMEI': [], 'Processor board ID': [], 'MAC': [],})
        df.to_csv(path + '/list.csv', index = False)

    return df



def openFile(path, filename):
    with open(path + '/' + filename) as file:
        content = file.readlines()

    content = [x.strip('\n') for x in content]

    return content    


def extractInfo(content):
    contentDict = {}
    macCounter = 0
    for lines in content:
        if lines[:8]=='hostname':
            contentDict['Host Name'] = lines[9:]
        elif lines[:13]=='International':
            contentDict['IMEI'] = lines[-15:]
        elif lines[:18]=='Processor board ID':
            contentDict['Processor board ID'] = lines[19:]
        elif lines[-5:]=='Vlan1':
            contentDict['MAC'] = lines[:14]

    return contentDict
        


def ConsolidateConfig(path):
    all_files = os.listdir(path)
    txt_files = []
    for filename in all_files:
        if filename[-21:]== (path[-10:] + '-output.txt'):
            txt_files.extend([filename])
    
    df = readCSV(path)
    
    for filename in txt_files:
        filecontent = openFile(path, filename)
        infoDict = extractInfo(filecontent)
        if infoDict['Processor board ID'] in df['Processor board ID'].values:
            for key in df.keys():
                df.loc[df['Processor board ID']==infoDict['Processor board ID'], [key]] = infoDict[key]
        else:
            df = df.append(infoDict, ignore_index=True)
    print(df)    
    df.to_csv(path + '/list.csv', index = False)
        



# All the stuff inside your window.
layout = [ [sg.Text("Choose a directory:\t"), sg.Input(key="-DIR-" ,change_submits=True), sg.FolderBrowse(key="-DIR2-")],
            [sg.Button('Combine Data'), sg.Exit()]
]

# Create the Window
window = sg.Window('Config Consolidate', layout).Finalize()

while True:             # Event Loop
    event, values = window.Read()
    if event in (None, 'Exit'):
        break
    elif event == 'Combine Data':
        ConsolidateConfig(values['-DIR-'])
        
        

window.Close()
