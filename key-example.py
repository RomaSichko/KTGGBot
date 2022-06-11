def get_app_key() -> str:
    """
    Returns Azure App password
    https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/RegisteredApps
    """
    return "1234567890abcDeFgI-#ywz"


def get_app_id() -> str:
    """
    Returns Azure App id
    https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/RegisteredApps
    """
    return "12345678-abcd-1234-abcd-1234567890ab"


def get_site_token() -> str:
    """Returns Microsoft site url"""
    return "https://login.microsoftonline.com/test-domain.onmicrosoft.com"


def get_reply_mail() -> str:
    """Returns mail"""
    return "no-reply@my.domain.com"


def get_test_bot_api() -> str:
    """
    Returns test TelegramBot API token
    https://t.me/BotFather
    """
    return "1234567890:1234567890-qwertyuio-asdfghjkl-zxcv"


def get_main_bot_api() -> str:
    """
    Returns main TelegramBot API token
    https://t.me/BotFather
    """
    return "1234567890:1234567890-qwertyuio-asdfghjkl-zxcv"


def get_base_key() -> str:
    """
    Returns HarperDB base url
    https://harperdb.io/docs/harperdb-api/
    """
    return "https://my-test-domain.harperdbcloud.com"


def get_auth_base() -> str:
    """
    Returns base auth HarperDB password
    https://harperdb.io/docs/harperdb-api/
    """
    return "Basic **********************=="
