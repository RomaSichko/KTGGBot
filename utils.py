import codecs
import json
import logging
import random
import re
import string
import sys
from typing import List, Optional, Tuple, Union

import cv2
import msal
import requests
from pyzbar.pyzbar import decode

import key
from constants.dbs import DocumentType, JsonConstants


def get_logger() -> logging.Logger:
    """Returns logger"""
    logger = logging.getLogger(__name__)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setFormatter(logging.Formatter(fmt="[%(asctime)s: %(levelname)s] %(message)s"))
        logger.addHandler(handler)
    return logger


def get_random_sticker_set() -> str:
    """Returns random sticker set"""
    set_names = [
        "travelbook_ukraine", "WorryGreenFrog", "comics_memes", "Meow_by_mysticise", "codebark",
        "TroyBeaver", "TheCurl", "LolAnimals2", "kocheng", "MrLittlePrince", "Sonic",
        "KermitTheDog", "MrSeal", "BlueBird", "SnappyCrab", "MrSeagull", "CloudiaSheep", "Snail",
        "KangarooFighter", "CyberGirl", "Tapir", "Minions", "Eggdog"]

    return random.choice(set_names)


def valid_mail(email: str):
    """Validate email address"""
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
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


def generate_password() -> str:
    """Returns random password"""
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
    password = [*[random.choice(upper) for _ in range(random.randint(1, 3))],
                *[random.choice(lower) for _ in range(random.randint(4, 5))],
                *[random.choice(digits) for _ in range(random.randint(4, 5))]]

    return "".join(password)


def get_username_by_student_ticket(img_name: str) -> Union[str, bool]:
    """Return username from EDBO"""
    student_base = json.load(codecs.open("students.json", "r", "utf-8-sig"))

    user_name = ""
    try:
        check_barcode = str(barcode_reader(img_name))
    except ValueError:
        return False

    for student in student_base:
        if "KB " + check_barcode in student[JsonConstants.student_ticket]:
            name = student[JsonConstants.student_name].split()
            user_name = f"{name[1]} {name[0]}"

    if user_name:
        return user_name
    return False


def get_username_by_passport(user_name: str,
                             user_lastname: str,
                             user_thirdname: str,
                             user_card: str) -> str:
    """Returns user data by id-card"""
    user_all_name = f"{user_lastname} {user_name} {user_thirdname}".lower()

    text_json = json.load(codecs.open("students.json", "r", "utf-8-sig"))
    user_name = ""

    for i in text_json:
        name = i[JsonConstants.student_name].lower()
        name = name.replace("`", "\'")

        if name == user_all_name:
            if i[JsonConstants.document_type] == DocumentType.id_card:
                user_card_doc = str(i[JsonConstants.document_number])

                if user_card_doc.endswith(user_card):
                    user_name = f"{user_name} {user_lastname}"

    return user_name


def get_work_account_by_codes(code: str,
                              user_name: str,
                              user_lastname: str,
                              user_thirdname: str) -> bool:
    """Returns worker in db"""
    work_base = json.load(codecs.open("teacher.json", "r", "utf-8-sig"))
    template = {"ID працівника": code, "ПІБ": f"{user_lastname} {user_name} {user_thirdname}"}

    return template in work_base


class MicrosoftTeamsFunctions:
    """
    Class to work with Graph API
    https://developer.microsoft.com/en-us/graph/graph-explorer
    """

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

        return result["access_token"]

    @property
    def headers(self) -> dict:
        """Return authentication header"""
        return {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.authenticate,
        }

    def reset_password(self, user_id: str) -> Union[Tuple[bool, str, str], bool]:
        """Change password for user"""
        password = generate_password()
        body = {
            "passwordProfile": {
                "forceChangePasswordNextSignIn": True,
                "password": password,
            },
        }

        self.logger.info(f"Send request https://graph.microsoft.com/beta/users/{user_id}"
                         f"\nData: {body}")

        response = requests.patch(
            f"https://graph.microsoft.com/beta/users/{user_id}", headers=self.headers,
            data=json.dumps(body))

        if response.status_code // 100 == 2:
            self.logger.info(msg=f"Password changed for {user_id}")
            return True, password, user_id

        self.logger.error(msg=f"{response.status_code}: Password not changed for {user_id}")
        return False

    def get_user_id_by_name(self, name: str) -> str:
        """Returns user email by username"""
        result = requests.get(
            "https://graph.microsoft.com/beta/users/", headers=self.headers).json()
        user_id = ""
        while True:
            for current in result["value"]:
                if name == current["displayName"]:
                    user_id = current["userPrincipalName"]
            if "@odata.nextLink" not in result:
                break

            result = requests.get(
                result["@odata.nextLink"], headers=self.headers).json()
        return user_id

    def get_username_by_student_ticket(self, img_name: str) -> Optional[str]:
        """Returns username by student ticket"""
        user_name = get_username_by_student_ticket(img_name)
        if not user_name:
            return

        return self.get_user_id_by_name(user_name)

    def reset_password_by_student_ticket(self, img_name: str) -> Union[Tuple[bool, str, str], bool]:
        """Reset user password by student ticket"""
        user_id = self.get_username_by_student_ticket(img_name=img_name)
        if not user_id:
            return False, "", ""
        return self.reset_password(user_id=user_id)

    def reset_password_by_user_name(self, user_name: str,
                                    user_lastname: str) -> Union[Tuple[bool, str, str], bool]:
        """Reset user password by username and lastname"""
        user_id = self.get_user_id_by_name(name=f"{user_name} {user_lastname}")
        return self.reset_password(user_id=user_id)

    def reset_password_by_passport(self,
                                   user_name: str,
                                   user_lastname: str,
                                   user_thirdname: str,
                                   user_card: str) -> Union[Tuple[bool, str, str], bool]:
        """Reset user password by id-card"""
        if get_username_by_passport(user_name=user_name,
                                    user_lastname=user_lastname,
                                    user_thirdname=user_thirdname,
                                    user_card=user_card):
            user_id = self.get_user_id_by_name(name=f"{user_name} {user_lastname}")
            return self.reset_password(user_id=user_id)
        return False

    def mail_send(self, to_user_email: str, code: int) -> None:
        """Sends email to user email with confirm code"""
        user_id = key.get_reply_mail()
        endpoint = f"https://graph.microsoft.com/v1.0/users/{user_id}/sendMail"
        self.logger.info(f"Send request {endpoint}")

        email_msg = {
            "Message":
                {"Subject": "Verify code KTGG Bot",
                 "Body":
                     {
                         "ContentType": "Text",
                         "Content": (
                             f"Твій код підтвердження: {code}. Нікому не розголошуйте його, "
                             f"якщо ти не реєструєш акаунт в боті ігноруй це повідомлення")},
                 "ToRecipients": [{"EmailAddress": {"Address": to_user_email}}],
                 },
            "SaveToSentItems": "true"}
        r = requests.post(endpoint,
                          headers=self.headers, json=email_msg)
        if r.ok:
            self.logger.info(f"Sent message to {to_user_email}")
        else:
            self.logger.info(f"Fail to send message{r.json()}")

    def delete_user(self,
                    user_id: str = None,
                    user_name: str = None) -> bool:
        """Delete user from MS Teams platform by id or email"""
        if not user_id:
            self.logger.info("Send request https://graph.microsoft.com/beta/users/")
            result = requests.get(
                f"https://graph.microsoft.com/beta/users/", headers=self.headers).json()

            while True:
                for current in result["value"]:
                    if user_name == current["displayName"]:
                        user_id = current["userPrincipalName"]
                if "@odata.nextLink" not in result:
                    break

                result = requests.get(
                    result["@odata.nextLink"], headers=self.headers).json()

        response = requests.delete(
            f"https://graph.microsoft.com/beta/users/{user_id}", headers=self.headers)
        if response.status_code // 100 == 2:
            self.logger.info(msg=f"Deleted user {user_id}")
            return True
        self.logger.info(msg=f"User {user_id} not found")
        return False

    def get_user_data(self, user_mail) -> str:
        """Returns username and lastname by user email"""
        self.logger.info(f"Send request https://graph.microsoft.com/v1.0/users/{user_mail}")
        result = requests.get(
            f"https://graph.microsoft.com/v1.0/users/{user_mail}", headers=self.headers).json()

        return f"{result['givenName']} {result['surname']}"

    def delete_all_groups(self, ignored_groups: List[str] = None) -> Union[List, None]:
        """Delete all groups from MS Teams which not in ignored_groups"""
        result = requests.get(
            f"https://graph.microsoft.com/v1.0/groups", headers=self.headers).json()
        list_of_exception = []
        while True:
            for current in result["value"]:
                if current["displayName"] not in ignored_groups:
                    self.logger.info(
                        f"Send request https://graph.microsoft.com/v1.0/groups/{current['id']}")
                    delete_group = requests.delete(
                        url=f"https://graph.microsoft.com/v1.0/groups/{current['id']}",
                        headers=self.headers,
                    )

                    if delete_group.status_code // 100 == 2:
                        self.logger.info(msg=f"Deleted group {current['displayName']}")
                    else:
                        list_of_exception.append(current["displayName"])
                        self.logger.info(msg=f"Group deleting failed {current['displayName']} ")

            if "@odata.nextLink" not in result:
                break
            result = requests.get(
                result["@odata.nextLink"], headers=self.headers).json()
        if list_of_exception:
            return list_of_exception
        return None
