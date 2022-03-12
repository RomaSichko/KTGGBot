# -*- coding: utf-8 -*-
from typing import Any

import requests

import changePass
import key


def send_request(payload) -> Any:
    """Send POST request with custom payload"""
    url = key.get_base_key()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': key.get_auth_base()
    }

    response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8')).json()

    return response


def add_data(telegram_id: int, username: str) -> None:
    """Add user telegram_id and username to db"""
    payload = "{\n\"operation\": \"insert\",\n\"schema\": \"base\",\n\"table\": \"accounts\",\n\"records\": [\n{ " + \
              f"\n\"id\": {telegram_id},\n\"telegramID\": {telegram_id},\n\"username\": \"{username}\"" + "}\n    ]\n}"

    send_request(payload)


def update_data_name(telegram_id: int, name: str) -> None:
    """Update user name in db"""
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"UPDATE base.accounts SET name = \'{name}\' WHERE id = {telegram_id}\"\n" + "}"
    send_request(payload)


def update_data_lastname(telegram_id: int, lastname: str) -> None:
    """Update user lastname in db"""
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"UPDATE base.accounts SET lastname = \'{lastname}\' WHERE id = {telegram_id}\"\n" + "}"
    send_request(payload)


def update_data_mail(telegram_id: int, mail: str) -> None:
    """Update user email in db"""
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"UPDATE base.accounts SET email = \'{mail}\', validMail = true WHERE id = {telegram_id}\"\n" + "}"
    send_request(payload)


def update_data_teams(telegram_id: int, mail: str) -> None:
    """Update user teams login in db"""
    data = changePass.get_user_data(mail)
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"UPDATE base.accounts SET teams = \'{mail}\', validTeams = true, position = \'{data[2]}\', name = \'{data[0]}\', lastname = \'{data[1]}\' WHERE id = {telegram_id}\"\n" + "}"
    send_request(payload)


def check_user_in_base(telegram_id: int) -> bool:
    """Check is user in db"""
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"SELECT * FROM base.accounts WHERE id = {telegram_id}\"\n" + "}"
    checker = send_request(payload)

    if len(checker) != 0:
        return True

    return False


def get_valid_teams(telegram_id: int) -> bool:
    """Get user valid_teams status from db"""
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"SELECT validTeams FROM base.accounts WHERE id = {telegram_id}\"\n" + "}"
    checker = send_request(payload)

    return checker[0]['validTeams']


def get_teams(telegram_id: int) -> str:
    """Get user teams login from db"""
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"SELECT teams FROM base.accounts WHERE id = {telegram_id}\"\n" + "}"
    checker = send_request(payload)

    return checker[0]['teams']


def get_user_data(telegram_id: int) -> str:
    """Get all user data from db"""
    payload = "{" + f"\n    \"operation\": \"sql\",\n    \"sql\": \"SELECT * FROM base.accounts WHERE id = {telegram_id}\"\n" + "}"
    checker = send_request(payload)

    user_data = (f"Ваші дані \n Електронна пошта: {str(checker[0]['email'])} Прізвище: "
                 f"{str(checker[0]['lastname'])} \nІм\'я: {str(checker[0]['name'])} MS Teams: "
                 f"{str(checker[0]['teams'])} \nПосада: {str(checker[0]['position'])}")

    return user_data
