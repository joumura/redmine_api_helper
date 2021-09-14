#
#   Redmine API Helper?
#
#   requires: pip install pysimplegui requests
#
# @auther kaz@jomura.net
# @version 2021.09.14

import os
import datetime
import pickle
import requests
import webbrowser
import PySimpleGUI as sg

sg.theme('DarkBlue11')
apiRefUrl = 'https://www.redmine.org/projects/redmine/wiki/Rest_api'
#font = ('Any', 10, 'underline')

# restore configs
oVals = {}
if os.path.isfile('settings.pkl'):
    with open('settings.pkl', 'rb') as f:
        oVals = pickle.load(f)
    print("old getUrl:" + str(oVals))

layout = [
    [sg.MenuBar([['ファイル',['値を保存して終了']],['ヘルプ',['Redmine API']]], key='myMenu')],
    [sg.Text('API Key:'), sg.InputText(oVals.get('apiKey', '{your_api_key}'),
        size=(40, 1), key='apiKey')],
    [sg.TabGroup ([[sg.Tab('GET', [
        [sg.Text(' Redmine APIの接続先URLを指定してください')],
        [sg.InputText(oVals.get('getUrl', 'http://localhost:81/redmine/issues.json'),
            size=(60, 1), key='getUrl')],
        [sg.Button('GET', key='get')],
        [sg.Multiline('', size=(80,20), key='getData')]
    ]) , sg.Tab('POST', [
        [sg.Text(' Redmine APIの接続先URLを指定してください')],
        [sg.InputText(oVals.get('postUrl', 'http://localhost:81/redmine/issues.json'),
            size=(60, 1), key='postUrl')],
        [sg.Text(' 送信データを入力してください')],
        [sg.Multiline(oVals.get('postData', '{\n  "issue": {\n    "project_id": 1,\n    "tracker_id" : 5,\n    "subject": "{題名}",\n    "description": "{説明}"\n }\n}\n'), size=(80,20), key='postData')],
        [sg.Button('POST', key='post')]
    ]), sg.Tab('PUT', [
        [sg.Text(' Redmine APIの接続先URLを指定してください')],
        [sg.InputText(oVals.get('putUrl', 'http://localhost:81/redmine/issues.json'),
            size=(60, 1), key='putUrl')],
        [sg.Multiline(oVals.get('putData', '{\n  "issue": {\n    "project_id": 1,\n    "tracker_id" : 5,\n    "subject": "{題名}",\n    "description": "{説明}"\n }\n}\n'), size=(80,20), key='putData')],
        [sg.Button('PUT', key='put')]
    ]), sg.Tab('DELETE', [
        [sg.Text(' Redmine APIの接続先URLを指定してください')],
        [sg.InputText(oVals.get('deleteUrl', 'http://localhost:81/redmine/issues.json'),
            size=(60, 1), key='deleteUrl')],
        [sg.Button('DELETE', key='delete')]
    ])]])],
    [sg.Output(size=(80,10))]
]

window = sg.Window('Redmine API Helper?', layout)

# event loop
while True:
    try:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            # valuesに値が入ってないため、保存できない。
            break

        elif values['myMenu'] == '値を保存して終了':
            with open('settings.pkl', 'wb') as f:
               pickle.dump(values, f)
            break

        elif values['myMenu'] == 'Redmine API':
            webbrowser.open(apiRefUrl)
            continue

        elif event == 'get':
            headers = {'Content-Type': 'application/json', 'X-Redmine-API-Key': values['apiKey']}
            response = requests.get(values['getUrl'], headers=headers)
            print('---' + datetime.datetime.now().strftime('%H:%M:%S')
                + ' GET HTTP ' + str(response.status_code))
            window['getData'].Update(response.text)

        elif event == 'post':
            headers = {'Content-Type': 'application/json', 'X-Redmine-API-Key': values['apiKey']}
            payload = values['postData'].encode("utf-8")
            response = requests.post(values['postUrl'], headers=headers, data=payload)
            print('---' + datetime.datetime.now().strftime('%H:%M:%S')
                + ' POST HTTP ' + str(response.status_code))
            print(response.text)

        elif event == 'put':
            headers = {'Content-Type': 'application/json', 'X-Redmine-API-Key': values['apiKey']}
            payload = values['putData'].encode("utf-8")
            response = requests.put(values['putUrl'], headers=headers, data=payload)
            print('---' + datetime.datetime.now().strftime('%H:%M:%S')
                + ' PUT HTTP ' + str(response.status_code))
            print(response.text)

        elif event == 'delete':
            headers = {'Content-Type': 'application/json', 'X-Redmine-API-Key': values['apiKey']}
            response = requests.delete(values['deleteUrl'], headers=headers)
            print('---' + datetime.datetime.now().strftime('%H:%M:%S')
                + ' DELETE HTTP ' + str(response.status_code))
            print(response.text)

    except Exception as e:
        print('---' + datetime.datetime.now().strftime('%H:%M:%S') + ' ERROR ' + event)
        print(e)
        continue

window.close()
