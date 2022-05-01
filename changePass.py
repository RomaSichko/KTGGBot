import re
import sys
from typing import Union, List, Tuple, Optional

import requests
import json
import random
import string
import logging
import msal
import codecs
import cv2
from pyzbar.pyzbar import decode
import key
from KTGGBot.constants.dbs import JsonConstants, DocumentType


def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
    logger.addHandler(handler)
    return logger


def valid_mail(email: str):
    """Validate email address"""
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, email)


def barcode_reader(image: str) -> Union[int, None]:
    """Read barcode from image"""
    img = cv2.imread(image)
    try:
        detected_barcodes = decode(img)
    except TypeError:
        return

    if not detected_barcodes:
        return
    else:
        for barcode in detected_barcodes:
            if barcode.data != "":
                return int(barcode.data)
            return


def generate_password():
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
    password = [*[random.choice(upper) for _ in range(random.randint(1, 4))],
                *[random.choice(lower) for _ in range(random.randint(4, 8))],
                *[random.choice(digits) for _ in range(random.randint(4, 8))]]

    return ''.join(password)


def get_username_by_student_ticket(img_name: str) -> Union[str, bool]:
    """Return username from EDBO"""
    student_base = json.load(codecs.open("students.json", 'r', 'utf-8-sig'))

    user_name = ""
    try:
        check_barcode = str(barcode_reader(img_name))
    except ValueError:
        return False

    for student in student_base:
        if student[JsonConstants.student_ticket] == "KB " + check_barcode:
            name = student[JsonConstants.student_name].split()
            user_name = f"{name[1]} {name[0]}"

    if user_name:
        return user_name
    return False


def get_username_by_passport(user_name: str,
                             user_lastname: str,
                             user_thirdname: str,
                             user_card: str) -> Union[str, bool]:
    user_all_name = f"{user_lastname} {user_name} {user_thirdname}".lower()

    text_json = json.load(codecs.open("students.json", 'r', 'utf-8-sig'))
    user_name = ""

    for i in text_json:
        name = i[JsonConstants.student_name].lower()
        name = name.replace('`', '\'')

        if name == user_all_name:
            if i[JsonConstants.document_type] == DocumentType.id_card:
                user_card_doc = i[JsonConstants.document_number][-4:]

                if user_card_doc == user_card:
                    user_name = f"{user_name} {user_lastname}"

    return user_name


class MicrosoftTeamsFunctions:
    logger = get_logger()

    @property
    def authenticate(self) -> str:
        """Authenticate to graph"""
        authority = key.get_site_token()
        app_id = key.get_app_id()
        app_secret = key.get_app_key()

        app = msal.ConfidentialClientApplication(
            client_id=app_id, authority=authority, client_credential=app_secret)

        result = app.acquire_token_silent(
            ["https://graph.microsoft.com/.default"], account=None)

        if not result:
            result = app.acquire_token_for_client(
                scopes=["https://graph.microsoft.com/.default"])

        return result['access_token']

    @property
    def headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.authenticate,
        }

    def reset_password(self, user_id: str) -> Union[Tuple[bool, str, str], bool]:
        password = generate_password()
        body = {
            "passwordProfile": {
                "forceChangePasswordNextSignIn": True,
                "password": password
            }
        }

        response = requests.patch(
            f'https://graph.microsoft.com/beta/users/{user_id}', headers=self.headers,
            data=json.dumps(body))

        if response.status_code // 100 == 2:
            self.logger.info(msg=f"Password changed for {user_id}")
            return True, password, user_id

        self.logger.error(msg=f"{response.status_code}: Password not changed for {user_id}")
        return False

    def get_user_id_by_name(self, name: str) -> str:
        result = requests.get(
            'https://graph.microsoft.com/beta/users/', headers=self.headers).json()
        user_id = ""
        while "@odata.nextLink" in result:
            i = 0

            while len(result["value"]) != i:
                if name == result["value"][i]["displayName"]:
                    user_id = result["value"][i]["userPrincipalName"]
                i += 1

            result = requests.get(
                result["@odata.nextLink"], headers=self.headers).json()
        return user_id

    def get_username_by_student_ticket(self, img_name: str) -> Optional[str]:
        user_name = get_username_by_student_ticket(img_name)
        if not user_name:
            return

        return self.get_user_id_by_name(user_name)

    def reset_password_by_student_ticket(self, img_name: str) -> Union[Tuple[bool, str, str], bool]:
        user_id = self.get_username_by_student_ticket(img_name=img_name)
        return self.reset_password(user_id=user_id)

    def reset_password_by_user_name(self, user_name: str,
                                    user_lastname: str) -> Union[Tuple[bool, str, str], bool]:
        user_id = self.get_user_id_by_name(name=f"{user_name} {user_lastname}")
        return self.reset_password(user_id=user_id)

    def reset_password_by_passport(self,
                                   user_name: str,
                                   user_lastname: str,
                                   user_thirdname: str,
                                   user_card: str) -> Union[Tuple[bool, str, str], bool]:
        if get_username_by_passport(user_name=user_name,
                                    user_lastname=user_lastname,
                                    user_thirdname=user_thirdname,
                                    user_card=user_card):
            user_id = self.get_user_id_by_name(name=f"{user_name} {user_lastname}")
            return self.reset_password(user_id=user_id)
        return False

    def detete_user(self, name, lastname):
        # graph
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.authenticate,
        }

        result = requests.get(
            f'https://graph.microsoft.com/beta/users/', headers=headers).json()

        user_name = name + ' ' + lastname

        user_id = ''

        while "@odata.nextLink" in result:
            i = 0
            while len(result["value"]) != i:
                if user_name == result["value"][i]["displayName"]:
                    user_id = result["value"][i]["userPrincipalName"]
                i += 1

            result = requests.get(
                result["@odata.nextLink"], headers=headers).json()

        response = requests.delete(
            f'https://graph.microsoft.com/beta/users/{user_id}', headers=self.headers)

        if str(response.status_code)[0] == '2':
            print(f'Success! {response.status_code}')
            return True, user_id, user_name
        else:
            print(response.status_code)
            print(response.json())
            return False, "", ""

    def mail_send(self, to_user_email, code):
        user_id = key.get_reply_mail()
        endpoint = f'https://graph.microsoft.com/v1.0/users/{user_id}/sendMail'

        email_msg = {
            'Message':
                {'Subject': "Verify code KTGG Bot",
                 'Body':
                     {
                         'ContentType': 'Text',
                         'Content': f"Ваш код підтвердження: {code}. Нікому не розголошуйте його, якщо Ви не реєструєте акаунт в боті ігноруйте це повідомлення"},
                 'ToRecipients': [{'EmailAddress': {'Address': to_user_email}}]
                 },
            'SaveToSentItems': 'true'}
        r = requests.post(endpoint,
                          headers={'Authorization': 'Bearer ' + self.authenticate}, json=email_msg)
        if r.ok:
            print('Sent email successfully')
        else:
            print(r.json())

    def valid_teams(self, user_mail):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.authenticate,
        }

        result = requests.get(
            f'https://graph.microsoft.com/v1.0/users/{user_mail}', headers=headers).json()

        if 'error' in result:
            return False
        else:
            return True

    def get_user_data(self, user_mail):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.authenticate,
        }

        result = requests.get(
            f'https://graph.microsoft.com/v1.0/users/{user_mail}', headers=headers).json()

        user_data = [result['givenName'], result['surname']]

        if result['jobTitle'] != 'Викладач':
            user_data.append('Студент')
        else:
            user_data.append('Викладач')

        return user_data
