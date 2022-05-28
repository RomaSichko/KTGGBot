class Dbs:
    admin = "base.admins"
    system = "base.system"
    confirm_codes = "base.confirm_codes"
    messages = "base.messages"


class MainDbs:
    user_accounts = "base.user_accounts"
    work_accounts = "base.work_accounts"
    user_actions = "base.user_actions"


class TestDbs(MainDbs):
    user_accounts = "base.test_user_accounts"
    work_accounts = "base.test_work_accounts"
    user_actions = "base.test_user_actions"


class JsonConstants:
    student_name = "Здобувач"
    document_type = "Тип ДПО"
    document_series = "Серія документа"
    document_number = "Номер документа"
    student_ticket = "Студентський (учнівський) квиток"


class DocumentType:
    id_card = "Паспорт громадянина України з безконтактним електронним носієм"
    birth_sertificate = "Свідоцтво про народження"
    passport = "Паспорт громадянина України"
