# -*- coding: utf-8 -*-

from os import truncate
import sqlite3
import requests
from codecs import encode
from json import JSONDecoder
import changePass
import key


def sendRequest(payload):
    url = key.get_base_key()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': key.get_auth_base()
    }

    response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8')).json()
# .text.encode('utf8')
    return response


def addData(telegramID, username):
    payload = "{\n\"operation\": \"insert\",\n\"schema\": \"base\",\n\"table\": \"accounts\",\n\"records\": [\n{ " + \
        f"\n\"id\": {telegramID},\n\"telegramID\": {telegramID},\n\"username\": \"{username}\"" + "}\n    ]\n}"
    print(payload)

    sendRequest(payload)


def updateDataName(telegramID, name):
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"UPDATE base.accounts SET name = \'{name}\' WHERE id = {telegramID}\"\n" + "}"
    sendRequest(payload)

def updateDataLastname(telegramID, lastname):
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"UPDATE base.accounts SET lastname = \'{lastname}\' WHERE id = {telegramID}\"\n" + "}"
    sendRequest(payload)

def updateDataMail(telegramID, mail):
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"UPDATE base.accounts SET email = \'{mail}\', validMail = true WHERE id = {telegramID}\"\n" + "}"
    sendRequest(payload)

def updateDataTeams(telegramID, mail):
    data = changePass.getUserData(mail)
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"UPDATE base.accounts SET teams = \'{mail}\', validTeams = true, position = \'{data[2]}\', name = \'{data[0]}\', lastname = \'{data[1]}\' WHERE id = {telegramID}\"\n" + "}"
    sendRequest(payload)

def checkUserInBase(telegramID):
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"SELECT * FROM base.accounts WHERE id = {telegramID}\"\n" + "}"
    checker = sendRequest(payload)
    # print(type(checker))
    if len(checker) != 0:
        return True
    else:
        return False
    

def getValidTeams(telegramID):
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"SELECT validTeams FROM base.accounts WHERE id = {telegramID}\"\n" + "}"
    checker = sendRequest(payload)
    
    return checker[0]['validTeams']

def getTeams(telegramID):
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"SELECT teams FROM base.accounts WHERE id = {telegramID}\"\n" + "}"
    checker = sendRequest(payload)
    
    return checker[0]['teams']

def getUserData(telegramID):
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"SELECT * FROM base.accounts WHERE id = {telegramID}\"\n" + "}"
    checker = sendRequest(payload)

    userData = "Ваші дані" + '\n' + 'Електронна пошта: ' + str(checker[0]['email']) + '\n' + "Прізвище: "  + str(checker[0]['lastname']) + '\n' + "Ім'я: " + str(checker[0]['name']) + '\n' + "MS Teams: " +  str(checker[0]['teams']) + '\n' + "Посада: " +  str(checker[0]['position'])

    return userData

    

# telegramID, username, name, lastname, email, teams, position, validMail = 0, validTeams = 0, status = 1
# ,\n\"name\": \"{name}\",\n\"lastname\": \"{lastname}\",\n\"email\": \"{email}\",\n\"teams\": \"{teams}\",\n        \"validMail\": {validMail},\n\"validTeams\": {validTeams}, \n\"status\": {status}, \n\"position\": \"{position}\"