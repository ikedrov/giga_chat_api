"""
API-клиент для эндпоинта POST /chat/completions.
"""
import requests
import urllib3
import allure
from utils.logger import get_logger

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = get_logger(__name__)


class ChatCompletionsClient:
    """Клиент для работы с /chat/completions."""

    ENDPOINT = "/chat/completions"

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.url = f"{self.base_url}{self.ENDPOINT}"

    def _headers(self, extra: dict | None = None) -> dict:
        """Формирует заголовки запроса."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        if extra:
            headers.update(extra)
        return headers

    @allure.step("Отправка POST /chat/completions")
    def send(
        self,
        payload: dict,
        headers_override: dict | None = None,
        timeout: int = 60,
    ) -> requests.Response:
        """
        Отправляет POST-запрос к /chat/completions.

        Args:
            payload: Тело запроса (JSON).
            headers_override: Дополнительные/заменяющие заголовки.
            timeout: Таймаут запроса в секундах.

        Returns:
            Объект requests.Response.
        """
        headers = self._headers(headers_override)

        logger.info("POST %s", self.url)
        logger.debug("Request payload: %s", payload)
        logger.debug("Request headers: %s", {k: v for k, v in headers.items() if k != "Authorization"})

        response = requests.post(
            self.url,
            json=payload,
            headers=headers,
            verify=False,
            timeout=timeout,
        )

        logger.info("Response status: %d", response.status_code)
        logger.debug("Response body: %s", response.text[:2000])

        return response

    @allure.step("Отправка POST /chat/completions (без авторизации)")
    def send_unauthorized(self, payload: dict, timeout: int = 60) -> requests.Response:
        """Отправляет запрос без заголовка Authorization."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        logger.info("POST %s (без авторизации)", self.url)
        return requests.post(
            self.url, json=payload, headers=headers, verify=False, timeout=timeout
        )

    @allure.step("Отправка POST /chat/completions (невалидный токен)")
    def send_invalid_token(self, payload: dict, timeout: int = 60) -> requests.Response:
        """Отправляет запрос с невалидным токеном."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer invalid_token_value_12345",
        }
        logger.info("POST %s (невалидный токен)", self.url)
        return requests.post(
            self.url, json=payload, headers=headers, verify=False, timeout=timeout
        )

    @allure.step("Отправка сырого запроса (raw body)")
    def send_raw(
        self,
        data: str,
        content_type: str = "application/json",
        timeout: int = 60,
    ) -> requests.Response:
        """Отправляет запрос с сырым телом (для невалидного JSON и т.д.)."""
        headers = {
            "Content-Type": content_type,
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        logger.info("POST %s (raw body)", self.url)
        logger.debug("Raw data: %s", data[:500])
        return requests.post(
            self.url, data=data, headers=headers, verify=False, timeout=timeout
        )
