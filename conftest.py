"""
Корневой conftest.py — фикстуры для всего проекта.
"""
import os
import json
import pytest
import allure
from dotenv import load_dotenv

from api_client.auth import get_access_token
from api_client.chat_completions import ChatCompletionsClient
from utils.logger import get_logger

logger = get_logger(__name__)

# Загружаем переменные окружения
load_dotenv()


def pytest_configure(config):
    """Выводит информацию о конфигурации в начале тестового прогона."""
    logger.info("=" * 60)
    logger.info("ЗАПУСК ТЕСТОВОГО ПРОГОНА GigaChat API")
    logger.info("=" * 60)


# ========== Фикстуры ==========

@pytest.fixture(scope="session")
def auth_config() -> dict:
    """Конфигурация авторизации из переменных окружения."""
    config = {
        "auth_url": os.getenv("GIGACHAT_AUTH_URL"),
        "auth_key": os.getenv("GIGACHAT_AUTH_KEY"),
        "scope": os.getenv("GIGACHAT_SCOPE"),
        "rquid": os.getenv("GIGACHAT_RQUID"),
        "api_url": os.getenv("GIGACHAT_API_URL"),
    }

    if not config["auth_key"]:
        pytest.skip("GIGACHAT_AUTH_KEY не задан в окружении. Пропуск тестов.")

    return config


@pytest.fixture(scope="session")
def access_token(auth_config) -> str:
    """Получает и кэширует access token на всю сессию."""
    with allure.step("Получение access token"):
        token = get_access_token(
            auth_url=auth_config["auth_url"],
            auth_key=auth_config["auth_key"],
            scope=auth_config["scope"],
            rquid=auth_config["rquid"],
        )
    return token


@pytest.fixture(scope="session")
def chat_client(auth_config, access_token) -> ChatCompletionsClient:
    """Создаёт экземпляр API-клиента для /chat/completions."""
    client = ChatCompletionsClient(
        base_url=auth_config["api_url"],
        token=access_token,
    )
    logger.info("API клиент инициализирован: %s", client.url)
    return client


# ========== Хуки Allure ==========

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Добавляет в Allure-отчёт request/response данные при падении теста."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Пытаемся достать последний ответ из фикстур теста
        if hasattr(item, "funcargs"):
            for key, value in item.funcargs.items():
                if hasattr(value, "status_code") and hasattr(value, "text"):
                    allure.attach(
                        value.text,
                        name=f"Response Body ({key})",
                        attachment_type=allure.attachment_type.JSON,
                    )
