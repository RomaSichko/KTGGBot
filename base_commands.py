# -*- coding: utf-8 -*-
from typing import Any, Type, List, Union

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

    logger = changePass.get_logger()

    def send_request(self, payload: str) -> Any:
        """Send POST request with custom payload"""
        url = key.get_base_key()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': key.get_auth_base()
        }

        payload = "{" + payload + "}"

        response = requests.request("POST", url, headers=headers,
                                    data=payload.encode('utf-8')).json()

        self.logger.info(msg=f"db work, payload \n{payload} \nresponse: {response}")
        return response

    def current_db(self):
        # TODO: change db
        payload = self.sql_template.format(
            # sql_request=f"SELECT * FROM {Dbs.system} WHERE parameter = \'db\'",
            sql_request=f"SELECT * FROM base.test_system WHERE parameter = \'db\'",
        )
        response = self.send_request(payload)

        return response[0]["value"]

    def switch_db(self, new_db):
        payload = self.sql_template.format(
            sql_request=f"UPDATE {Dbs.system} SET `value` = \'{new_db}\' WHERE parameter = \'db\'"
        )

        self.send_request(payload)

    def get_user_action(self, telegram_id: int):
        payload = self.sql_template.format(
            sql_request=f"SELECT action FROM {self.db_type.user_actions} WHERE telegramID = {telegram_id}",
        )
        response = self.send_request(payload)
        if response:
            return response[0]["action"]
        return False

    def update_user_action(self, telegram_id: int, action: str):
        response = self.get_user_action(telegram_id=telegram_id)

        if not response:
            payload = self.sql_template.format(
                sql_request=f"INSERT INTO {self.db_type.user_actions} (telegramID, action) VALUE ({telegram_id}, \'{action}\')",
            )
        else:
            payload = self.sql_template.format(
                sql_request=f"UPDATE {self.db_type.user_actions} SET action = \'{action}\' WHERE telegramID = {telegram_id}",
            )

        return self.send_request(payload)

    def add_data(self, telegram_id: int, username: str, base: MainDbs) -> None:
        """Add user telegram_id and username to db"""
        payload = self.sql_template.format(
            sql_request=f"INSERT INTO {base} (telegramID, telegramNickname) VALUE ({telegram_id}, \'{username}\')",
        )

        return self.send_request(payload)

    def add_data_main_account(self, telegram_id: int, username: str):
        self.add_data(telegram_id=telegram_id, username=username, base=self.db_type.user_accounts)

    def add_data_work_account(self, telegram_id: int, username: str):
        self.add_data(telegram_id=telegram_id, username=username, base=self.db_type.work_accounts)

    def update_user_email(self,
                          telegram_id: int,
                          mail: str,
                          base: MainDbs,
                          email_status: bool = True, **kwargs) -> None:
        """Update user email in db"""
        payload = self.sql_template.format(
            sql_request=f"UPDATE {base} SET email = \'{mail}\', validMail = {email_status} WHERE telegramID = {telegram_id}",
        )

        return self.send_request(payload)

    def update_user_email_main_account(self, telegram_id: int, mail: str) -> None:
        self.update_user_email(telegram_id=telegram_id,
                               base=self.db_type.user_accounts,
                               mail=mail)

    def update_user_email_work_account(self, telegram_id: int, mail: str) -> None:
        self.update_user_email(telegram_id=telegram_id,
                               base=self.db_type.work_accounts,
                               mail=mail)

    def update_user_teams(self,
                          telegram_id: int,
                          mail: str,
                          base: MainDbs,
                          user_name: str,
                          teams_status: bool = True) -> None:
        """Update user email in db"""
        payload = self.sql_template.format(
            sql_request=f"UPDATE {base} SET teamsEmail = \'{mail}\', validTeams = {teams_status}, userName = \'{user_name}\' WHERE telegramID = {telegram_id}",
        )

        self.send_request(payload)

    def update_user_teams_main_account(self, telegram_id: int, user_name: str, mail: str) -> None:
        self.update_user_teams(telegram_id=telegram_id,
                               user_name=user_name,
                               base=self.db_type.user_accounts,
                               mail=mail)

    def update_user_teams_work_account(self, telegram_id: int, user_name: str, mail: str) -> None:
        self.update_user_teams(telegram_id=telegram_id,
                               user_name=user_name,
                               base=self.db_type.work_accounts,
                               mail=mail)

    def check_user_in_base(self, telegram_id: int, base: MainDbs) -> bool:
        """Check is user in db"""
        payload = self.sql_template.format(
            sql_request=f"SELECT * FROM {base} WHERE telegramID = {telegram_id}",
        )
        result = self.send_request(payload)

        return bool(result)

    def check_user_in_work_base(self, telegram_id: int) -> bool:
        return self.check_user_in_base(telegram_id=telegram_id, base=self.db_type.work_accounts)

    def check_user_in_main_base(self, telegram_id: int) -> bool:
        return self.check_user_in_base(telegram_id=telegram_id, base=self.db_type.user_accounts)

    def get_valid_teams(self, telegram_id: int, base: MainDbs) -> bool:
        """Get user valid_teams status from db"""
        # self.db_type.user_accounts
        payload = self.sql_template.format(
            sql_request=f"SELECT validTeams FROM {base} WHERE telegramID = {telegram_id}",
        )
        result = self.send_request(payload)

        return bool(result[0]['validTeams'])

    def get_valid_teams_main_account(self, telegram_id: int) -> bool:
        return self.get_valid_teams(telegram_id=telegram_id, base=self.db_type.user_accounts)

    def get_valid_teams_work_account(self, telegram_id: int) -> bool:
        return self.get_valid_teams(telegram_id=telegram_id, base=self.db_type.work_accounts)

    def get_teams(self, telegram_id: int, base: MainDbs) -> str:
        """Get user teams email status from db"""
        payload = self.sql_template.format(
            sql_request=f"SELECT teamsEmail FROM {base} WHERE telegramID = {telegram_id}",
        )
        result = self.send_request(payload)

        return result[0]['teamsEmail']

    def get_teams_main_account(self, telegram_id: int) -> str:
        return self.get_teams(telegram_id=telegram_id, base=self.db_type.user_accounts)

    def get_teams_work_account(self, telegram_id: int) -> str:
        return self.get_teams(telegram_id=telegram_id, base=self.db_type.work_accounts)

    def get_valid_mail(self, telegram_id: int, base: MainDbs) -> bool:
        """Get user valid_teams status from db"""
        payload = self.sql_template.format(
            sql_request=f"SELECT validMail FROM {base} WHERE telegramID = {telegram_id}",
        )
        result = self.send_request(payload)

        return bool(result[0]['validMail'])

    def get_valid_mail_main_account(self, telegram_id: int) -> bool:
        return self.get_valid_mail(telegram_id=telegram_id, base=self.db_type.user_accounts)

    def get_valid_mail_work_account(self, telegram_id: int) -> bool:
        return self.get_valid_mail(telegram_id=telegram_id, base=self.db_type.work_accounts)

    # def get_teams(self, telegram_id: int, base: MainDbs) -> str:
    #     """Get user teams login from db"""
    #     payload = self.sql_template.format(
    #         sql_request=f"SELECT teamsMail FROM {base} WHERE telegramID = {telegram_id}",
    #     )
    #     result = self.send_request(payload)
    #
    #     return result[0]['teamsMail']
    #
    # def get_teams_main_account(self, telegram_id: int) -> str:
    #     return self.get_teams(telegram_id=telegram_id, base=self.db_type.user_accounts)
    #
    # def get_teams_work_account(self, telegram_id: int) -> str:
    #     return self.get_teams(telegram_id=telegram_id, base=self.db_type.work_accounts)

    def get_user_data(self, telegram_id: int, base: MainDbs) -> dict:
        """Get all user data from db"""
        payload = self.sql_template.format(
            sql_request=f"SELECT * FROM {base} WHERE telegramID = {telegram_id}",
        )
        result = self.send_request(payload)[0]
        return result

    def get_user_data_main_account(self, telegram_id: int) -> dict:
        return self.get_user_data(telegram_id=telegram_id, base=self.db_type.user_accounts)

    def get_user_data_work_account(self, telegram_id: int) -> dict:
        return self.get_user_data(telegram_id=telegram_id, base=self.db_type.work_accounts)

    def get_admin(self, telegram_id: int) -> List:
        payload = self.sql_template.format(
            sql_request=f"SELECT * FROM {Dbs.admin} WHERE telegramId = {telegram_id}",
        )
        result = self.send_request(payload)
        return result

    def add_user_email_code(self,
                            telegram_id: int,
                            confirm_code: int,
                            email: str,
                            code_type: str) -> List[dict]:
        """Insert user email confirm code in db"""
        if self.get_user_email_confirm_codes(telegram_id=telegram_id, code_type=code_type):
            payload = self.sql_template.format(
                sql_request=f"UPDATE {Dbs.confirm_codes} SET code = {confirm_code}, mail = \'{email}\' WHERE telegramId = {telegram_id}",
            )
        else:
            payload = self.sql_template.format(
                sql_request=f"INSERT INTO {Dbs.confirm_codes} (telegramId, codeType, code, mail) VALUE ({telegram_id}, \'{code_type}\', {confirm_code}, \'{email}\')",
            )

        return self.send_request(payload)

    def get_user_confirm_codes(self,
                               telegram_id: int,
                               code_type: str) -> List[dict]:
        """Get data from base.confirm_codes"""
        payload = self.sql_template.format(
            sql_request=f"SELECT * FROM {Dbs.confirm_codes} WHERE telegramId = {telegram_id} AND codeType = \'{code_type}\'",
        )

        return self.send_request(payload)

    def get_user_confirm_code(self,
                              telegram_id: int,
                              code_type: str) -> Union[int, bool]:
        """Get email confirm_code from base.confirm_codes"""
        response = self.get_user_confirm_codes(telegram_id=telegram_id, code_type=code_type)
        if response:
            return response[0]["code"]
        return False

    def get_user_email_confirm_codes(self,
                                     telegram_id: int,
                                     code_type: str) -> Union[str, bool]:
        """Get email confirm_code from base.confirm_codes"""
        response = self.get_user_confirm_codes(telegram_id=telegram_id, code_type=code_type)
        if response:
            return response[0]["mail"]
        return False

    def delete_user_confirm_code(self,
                                 telegram_id: int,
                                 code_type: str) -> None:
        payload = self.sql_template.format(
            sql_request=f"DELETE FROM {Dbs.confirm_codes} WHERE telegramId = {telegram_id} AND codeType = \'{code_type}\'",
        )

        self.send_request(payload)
