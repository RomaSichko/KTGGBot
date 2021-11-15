import requests
import json
import telebot
import random, string
import logging
import msal
import pandas
import img
import codecs

# Functions
def authenticate():
    authority = "https://login.microsoftonline.com/kdktgg.onmicrosoft.com"
    appID = ""
    appSecret = ""
    scope = ["https://graph.microsoft.com/.default"]

    app = msal.ConfidentialClientApplication(
        appID, authority=authority, client_credential = appSecret)

    result = None
    result = app.acquire_token_silent(["https://graph.microsoft.com/.default"], account=None)

    if not result:
        logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

    return result['access_token']


def resetPass(img_name):
    # generate password

    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
    password = []
    password.append(random.choice(upper))
    for i in range(2):
        password.append(random.choice(lower))
    for i in range(5):
        password.append(random.choice(digits))
    strpass = ''.join(password)


    # graph
    headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + authenticate(),
          }

    body = {
                "passwordProfile": {
                  "forceChangePasswordNextSignIn": True,
                  "password": strpass
                }
            }


    # get user id

    result = requests.get(f'https://graph.microsoft.com/beta/users/', headers = headers).json()

    user_name = img.get_username(img_name)
    if user_name == 'error':
        print("error")
        return False, ""
    
    user_id = ""
    while "@odata.nextLink" in result:
        i = 0

        while len(result["value"]) != i:
            if user_name == result["value"][i]["displayName"]:
                user_id = result["value"][i]["userPrincipalName"]
            i += 1        

        result = requests.get(result["@odata.nextLink"], headers = headers).json()

    print(user_id)

    # change pass

    response = requests.patch(f'https://graph.microsoft.com/beta/users/{user_id}',headers = headers, data=json.dumps(body))

    # result

    if str(response.status_code)[0] == '2':
        print(f'Success! {response.status_code}')
        print(strpass)
        return True, strpass, user_id
    else:
        print(response.status_code)
        print(response.json())
        return False, ""


# reset command
def resetPass_bot(uid = None, uname = None, ulastname = None):
    # generate password

    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
    password = []
    password.append(random.choice(upper))
    for i in range(2):
        password.append(random.choice(lower))
    for i in range(5):
        password.append(random.choice(digits))
    strpass = ''.join(password)


    # graph
    headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + authenticate(),
          }

    body = {
                "passwordProfile": {
                  "forceChangePasswordNextSignIn": True,
                  "password": strpass
                }
            }

    result = requests.get(f'https://graph.microsoft.com/beta/users/', headers = headers).json()

    if uid == '0':
        user_id = ""
        user_name = uname + " " + ulastname
        while "@odata.nextLink" in result:
            i = 0

            while len(result["value"]) != i:
                if user_name == result["value"][i]["displayName"]:
                    user_id = result["value"][i]["userPrincipalName"]
                i += 1        

            result = requests.get(result["@odata.nextLink"], headers = headers).json()

    else:
        user_id = uid


    response = requests.patch(f'https://graph.microsoft.com/beta/users/{user_id}',headers = headers, data=json.dumps(body))

    # result

    if str(response.status_code)[0] == '2':
        print(f'Success! {response.status_code}')
        print(strpass)
        return True, strpass, user_id
    else:
        print(response.status_code)
        print(response.json())
        return False, "", ""
    

# reset command
def resetPass_idcard(ulastname = None, uname = None, uthirdname = None, uidcard = None):
    # generate password

    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
    password = []
    password.append(random.choice(upper))
    for i in range(2):
        password.append(random.choice(lower))
    for i in range(5):
        password.append(random.choice(digits))
    strpass = ''.join(password)


    # graph
    headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + authenticate(),
          }

    body = {
                "passwordProfile": {
                  "forceChangePasswordNextSignIn": True,
                  "password": strpass
                }
            }

    uallname = ulastname + " " + uname + " " + uthirdname
    print(uallname)

    result = requests.get(f'https://graph.microsoft.com/beta/users/', headers = headers).json()

    text_json = json.load(codecs.open("students.json", 'r', 'utf-8-sig'))

    user_name = ""

    for i in text_json:
        name = i["Здобувач"]
        
        if name == uallname:
            if i["Тип ДПО"] == "Паспорт громадянина України з безконтактним електронним носієм":
                ucard = i["Номер документа"][-4:]
                
                if uidcard == ucard:
                    user_name = uname + " " + ulastname 

    if user_name != "":
        user_id = ""
        while "@odata.nextLink" in result:
            i = 0
            while len(result["value"]) != i:
                if user_name == result["value"][i]["displayName"]:
                    user_id = result["value"][i]["userPrincipalName"]
                i += 1        

            result = requests.get(result["@odata.nextLink"], headers = headers).json()



        response = requests.patch(f'https://graph.microsoft.com/beta/users/{user_id}',headers = headers, data=json.dumps(body))

        # result

        if str(response.status_code)[0] == '2':
            print(f'Success! {response.status_code}')
            print(strpass)
            return True, strpass, user_id
        else:
            print(response.status_code)
            print(response.json())
            return False, "", ""
    else:
        return False, "Вибачте, ваші дані в базі не знайдено, перевірте правильність введення даних та відправте ще раз", ""