# -*- coding: utf-8 -*-

import requests
import changePass
import key


def send_request(payload):
    url = key.get_base_key()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': key.get_auth_base()
    }

    response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8')).json()
    # .text.encode('utf8')
    return response


def add_data(telegram_id, username):
    payload = "{\n\"operation\": \"insert\",\n\"schema\": \"base\",\n\"table\": \"accounts\",\n\"records\": [\n{ " + \
              f"\n\"id\": {telegram_id},\n\"telegramID\": {telegram_id},\n\"username\": \"{username}\"" + "}\n    ]\n}"
    print(payload)

    send_request(payload)


def update_data_name(telegram_id, name):
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"UPDATE base.accounts SET name = \'{name}\' WHERE id = {telegram_id}\"\n" + "}"
    send_request(payload)


def update_data_lastname(telegram_id, lastname):
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"UPDATE base.accounts SET lastname = \'{lastname}\' WHERE id = {telegram_id}\"\n" + "}"
    send_request(payload)


def update_data_mail(telegram_id, mail):
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"UPDATE base.accounts SET email = \'{mail}\', validMail = true WHERE id = {telegram_id}\"\n" + "}"
    send_request(payload)


def update_data_teams(telegram_id, mail):
    data = changePass.get_user_data(mail)
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"UPDATE base.accounts SET teams = \'{mail}\', validTeams = true, position = \'{data[2]}\', name = \'{data[0]}\', lastname = \'{data[1]}\' WHERE id = {telegram_id}\"\n" + "}"
    send_request(payload)


def check_user_in_base(telegram_id):
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"SELECT * FROM base.accounts WHERE id = {telegram_id}\"\n" + "}"
    checker = send_request(payload)
    # print(type(checker))
    if len(checker) != 0:
        return True
    else:
        return False


def get_valid_teams(telegram_id):
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"SELECT validTeams FROM base.accounts WHERE id = {telegram_id}\"\n" + "}"
    checker = send_request(payload)

    return checker[0]['validTeams']


def get_teams(telegram_id):
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"SELECT teams FROM base.accounts WHERE id = {telegram_id}\"\n" + "}"
    checker = send_request(payload)

    return checker[0]['teams']


def get_user_data(telegram_id):
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"SELECT * FROM base.accounts WHERE id = {telegram_id}\"\n" + "}"
    checker = send_request(payload)

    userData = "Ваші дані" + '\n' + 'Електронна пошта: ' + str(checker[0]['email']) + '\n' + "Прізвище: " + str(
        checker[0]['lastname']) + '\n' + "Ім'я: " + str(checker[0]['name']) + '\n' + "MS Teams: " + str(
        checker[0]['teams']) + '\n' + "Посада: " + str(checker[0]['position'])

    return userData

# telegramID, username, name, lastname, email, teams, position, validMail = 0, validTeams = 0, status = 1
# ,\n\"name\": \"{name}\",\n\"lastname\": \"{lastname}\",\n\"email\": \"{email}\",\n\"teams\": \"{teams}\",\n        \"validMail\": {validMail},\n\"validTeams\": {validTeams}, \n\"status\": {status}, \n\"position\": \"{position}\"
