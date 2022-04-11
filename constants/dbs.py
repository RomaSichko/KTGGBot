class Dbs:
    admin = "base.admins"
    system = "base.system"


class MainDbs:
    user_accounts = "base.user_accounts"
    work_accounts = "base.work_accounts"
    user_actions = "base.user_actions"


class TestDbs(MainDbs):
    user_accounts = "base.test_user_accounts"
    work_accounts = "base.test_work_accounts"
    user_actions = "base.test_user_actions"
