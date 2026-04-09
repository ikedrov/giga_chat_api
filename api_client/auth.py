"""
Модуль авторизации: получение токена GigaChat API.
"""
import requests
import urllib3
from utils.logger import get_logger

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = get_logger(__name__)


def get_access_token(auth_url: str, auth_key: str, scope: str, rquid: str) -> str:
    """
    Получает access token для GigaChat API.

    Args:
        auth_url: URL эндпоинта авторизации.
        auth_key: Ключ авторизации (Basic ...).
        scope: Скоуп доступа (GIGACHAT_API_PERS / GIGACHAT_API_CORP).
        rquid: Уникальный идентификатор запроса.

    Returns:
        Access token в виде строки.

    Raises:
        requests.HTTPError: Если сервер вернул ошибку.
    """
    logger.info("Запрос access token по адресу: %s", auth_url)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": rquid,
        "Authorization": f"Basic {auth_key}",
    }
    payload = f"scope={scope}"

    response = requests.post(auth_url, headers=headers, data=payload, verify=False, timeout=30)

    logger.debug("Auth response status: %d", response.status_code)
    response.raise_for_status()

    token = response.json().get("access_token")
    if not token:
        raise ValueError("access_token отсутствует в ответе авторизации")

    logger.info("Access token получен успешно")
    return token
