# -*- coding: utf-8 -*-
import datetime
from typing import Any, Type

import requests

import changePass
import key
from KTGGBot.constants.dbs import MainDbs, Dbs

db_schema = {
    "id": "auto",
    "email": str,
    "teamsMail": str,
    "telegramID": int,
    "telegramNickname": str,
    "userName": str,
    "userRole": str,
    "validMail": bool,
    "validTeams": bool,
    "memeees": bool,
}


class DbExecutor:
    sql_template = "\n    \"operation\": \"sql\",\n    \"sql\": \"{sql_request}\"\n"
    db_type: MainDbs = None

    def send_request(self, payload: str) -> Any:
        """Send POST request with custom payload"""
        url = key.get_base_key()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': key.get_auth_base()
        }

        payload = "{" + payload + "}"

        response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8')).json()

        print(f"{datetime.datetime.now()}: db work, payload \n{payload} \nresponse: {response}")
        return response

    def current_db(self):
        payload = self.sql_template.format(
            sql_request=f"SELECT * FROM {Dbs.system} WHERE parameter = \'db\'",
        )
        response = self.send_request(payload)

        return response[0]["value"]

    def switch_db(self, new_db):
        payload = self.sql_template.format(
            sql_request=f"UPDATE {Dbs.system} SET `value` = \'{new_db}\' WHERE parameter = \'db\'"
        )

        self.send_request(payload)

    def update_user_action(self, telegram_id: int, action: str):
        payload = self.sql_template.format(
            sql_request=f"SELECT * FROM {self.db_type.user_actions} WHERE telegramID = {telegram_id}",
        )
        response = self.send_request(payload)

        if not response:
            payload = self.sql_template.format(
                sql_request=f"INSERT INTO {self.db_type.user_actions} (telegramID, action) VALUE ({telegram_id}, \'{action}\')",
            )
        else:
            payload = self.sql_template.format(
                sql_request=f"UPDATE {self.db_type.user_actions} SET action = \'{action}\' WHERE telegramID = {telegram_id}",
            )

        return self.send_request(payload)

    def add_data(self, telegram_id: int, username: str) -> None:
        """Add user telegram_id and username to db"""
        payload = self.sql_template.format(
            sql_request=f"INSERT INTO {self.db_type.user_accounts} (telegramID, telegramNickname) VALUE ({telegram_id}, \'{username}\')",
        )

        return self.send_request(payload)

    def update_data_name(self, telegram_id: int, name: str) -> None:
        """Update user name in db"""
        payload = self.sql_template.format(
            sql_request=f"UPDATE {self.db_type.user_accounts} SET userName = \'{name}\' WHERE telegramID = {telegram_id}",
        )

        return self.send_request(payload)

    def update_data_mail(self, telegram_id: int, mail: str) -> None:
        """Update user email in db"""
        payload = self.sql_template.format(
            sql_request=f"UPDATE {self.db_type.user_accounts} SET email = \'{mail}\', validMail = true WHERE telegramID = {telegram_id}",
        )

        return self.send_request(payload)

    def update_data_teams(self, telegram_id: int, mail: str) -> None:
        """Update user teams login in db"""
        data = changePass.get_user_data(mail)
        user_name = f"{data[0]} {data[1]}"
        payload = self.sql_template.format(
            sql_request=f"UPDATE {self.db_type.user_accounts} SET teamsMail = \'{mail}\', validTeams = true, userRole = \'{data[2]}\', userName = \'{user_name}\' WHERE telegramID = {telegram_id}",
        )

        return self.send_request(payload)

    def check_user_in_base(self, telegram_id: int) -> bool:
        """Check is user in db"""
        payload = self.sql_template.format(
            sql_request=f"SELECT * FROM {self.db_type.user_accounts} WHERE telegramID = {telegram_id}",
        )
        result = self.send_request(payload)

        return bool(result)

    def get_valid_teams(self, telegram_id: int) -> bool:
        """Get user valid_teams status from db"""
        payload = self.sql_template.format(
            sql_request=f"SELECT validTeams FROM {self.db_type.user_accounts} WHERE telegramID = {telegram_id}",
        )
        result = self.send_request(payload)

        return bool(result[0]['validTeams'])

    def get_valid_mail(self, telegram_id: int) -> bool:
        """Get user valid_teams status from db"""
        payload = self.sql_template.format(
            sql_request=f"SELECT validMail FROM {self.db_type.user_accounts} WHERE telegramID = {telegram_id}",
        )
        result = self.send_request(payload)

        return bool(result[0]['validMail'])

    def get_teams(self, telegram_id: int) -> str:
        """Get user teams login from db"""
        payload = self.sql_template.format(
            sql_request=f"SELECT teamsMail FROM {self.db_type.user_accounts} WHERE telegramID = {telegram_id}",
        )
        result = self.send_request(payload)

        return result[0]['teamsMail']

    def get_user_data(self, telegram_id: int) -> str:
        """Get all user data from db"""
        payload = self.sql_template.format(
            sql_request=f"SELECT * FROM {self.db_type.user_accounts} WHERE telegramID = {telegram_id}",
        )
        result = self.send_request(payload)[0]
        user_data = "Ваші дані \nEmail: {email} \nІм\'я та прізвище: {name} \nTeams email: {teams} \nПосада: {status}"
        user_data = user_data.format(
            email=result["email"],
            name=result["userName"],
            teams=result["teamsMail"],
            status=result["userRole"],
        )

        return user_data
