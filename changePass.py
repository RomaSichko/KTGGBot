from urllib.parse import urldefrag
import requests
import json
import random, string
import logging
import msal
import codecs
import cv2
from pyzbar.pyzbar import decode

def BarcodeReader(image):
      
    # read the image in numpy array using cv2
    img = cv2.imread(image)
       
    # Decode the barcode image
    try:
        detectedBarcodes = decode(img)
    except TypeError:
        return 0
       
    # If not detected then print the message
    if not detectedBarcodes:
        return 0
    else:
        
          # Traveres through all the detected barcodes in image
        for barcode in detectedBarcodes:  
            
            # Locate the barcode position in image
            (x, y, w, h) = barcode.rect
              
            # Put the rectangle in image using 
            # cv2 to heighlight the barcode
            cv2.rectangle(img, (x-10, y-10),
                          (x + w+10, y + h+10), 
                          (255, 0, 0), 2)
              
            if barcode.data!="":

                return barcode.data
            else:
                return barcode.data


def get_username(img_name):

    text_json = json.load(codecs.open("students.json", 'r', 'utf-8-sig'))

    list_items = []

    user_name = ""
    try:
        check_barcode = int(BarcodeReader(img_name))
    except ValueError:
        check_barcode = 0
    # check_barcode = int(shtrih_kod.BarcodeReader(img_name))

    # check json
    if check_barcode:
        for i in text_json:
            name = i["Здобувач"].split()
            
            name[0], name[1] = name[1], name[0]
            stud_ticket = i["Студентський (учнівський) квиток"].split()[1]
            # print(name, stud_ticket)
            if stud_ticket == str(check_barcode):
                user_name = " ".join(name[:2])

    if user_name == "":
        return "error"
    else:
        return user_name


# Functions
def authenticate():
    authority = "https://login.microsoftonline.com/kdktgg.onmicrosoft.com"
    appID = "7c882179-7805-49ef-8e69-a98fe56d33d3"
    appSecret = "pobMCR1174{*#^higsDJZK1"
    scope = ["https://graph.microsoft.com/.default"]

    app = msal.ConfidentialClientApplication(
        appID, authority=authority, client_credential = appSecret)

    result = None
    result = app.acquire_token_silent(["https://graph.microsoft.com/.default"], account=None)

    if not result:
        logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

    return result['access_token']

# bot = telebot.TeleBot('1305496539:AAHKPM4qB9ONh6xwHoMzJCPiSxlynnPsp8Y')

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

    user_name = get_username(img_name)
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



def resetPass_teacher(ulastname = None, uname = None, uthirdname = None, uid = None):
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

    text_json = json.load(codecs.open("teacher.json", 'r', 'utf-8-sig'))

    user_name = ""

    for i in text_json:
        name = i["ПІБ"].lower()
        
        if name == uallname.lower():
            if uid == i["ID працівника"]:
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


def detete_user(name, lastname):
    # graph
    headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + authenticate(),
          }

    result = requests.get(f'https://graph.microsoft.com/beta/users/', headers = headers).json()

    user_name = name + ' ' + lastname

    user_id = ''

    while "@odata.nextLink" in result:
            i = 0
            while len(result["value"]) != i:
                if user_name == result["value"][i]["displayName"]:
                    user_id = result["value"][i]["userPrincipalName"]
                i += 1        

            result = requests.get(result["@odata.nextLink"], headers = headers).json()



    response = requests.delete(f'https://graph.microsoft.com/beta/users/{user_id}',headers = headers)

    # print(response)

    if str(response.status_code)[0] == '2':
        print(f'Success! {response.status_code}')
        return True, user_id, user_name
    else:
        print(response.status_code)
        print(response.json())
        return False, "", ""



def nextcourse():
    headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + authenticate(),
          }


    

    result = requests.get(f'https://graph.microsoft.com/beta/users/', headers = headers).json()


    user_id = ''
    user_group = ''
    

    while "@odata.nextLink" in result:
        i = 0

        while len(result["value"]) != i:
            user_id = result["value"][i]["userPrincipalName"]
            user_group = result["value"][i]["jobTitle"]
            print(user_group)

            if user_group != None and '-' in user_group:
                group_id = user_group.split("-")[1]

                if user_group.split("-")[0].isdigit():

                    group_number = int(user_group.split("-")[0])
                    if group_id == "ПТБД" or  group_id == "ОО" or  group_id == "ФБС" or  "РО" in group_id:
                        if group_number > 30:
                            user_group = group_id
                        else:
                            group_number += 10
                            user_group = str(group_number) + '-' + group_id

                    elif group_number > 40:
                        user_group = group_id

                    else:
                        group_number += 10
                        user_group = str(group_number) + '-' + group_id
            
            else:
                print("Error")
                # continue

            print(user_group)

            body = {
                    "jobTitle": user_group
                }

            response = requests.patch(f'https://graph.microsoft.com/beta/users/{user_id}',headers = headers, data=json.dumps(body))

            if str(response.status_code)[0] == '2':
                print(f'Success! {response.status_code}')
                print(user_id)
                # return True
            else:
                print(user_id)
                print(response.status_code)
                print(response.json())
                # return False
            i += 1
            print("=======")

        result = requests.get(result["@odata.nextLink"], headers = headers).json()

    
# nextcourse()