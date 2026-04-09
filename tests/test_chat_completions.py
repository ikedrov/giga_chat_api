"""
Автотесты для POST /chat/completions GigaChat API.

Классы:
    TestPositiveChatCompletions — позитивные тесты + валидация схемы ответа
    TestNegativeChatCompletions — негативные тесты (невалидные данные, авторизация)
"""
import json
import pytest
import allure

from schemas.response_schemas import MINIMAL_RESPONSE_SCHEMA, USAGE_MINIMAL_SCHEMA
from schemas.request_schemas import MINIMAL_REQUEST_SCHEMA
from schemas.validators import validate_response, validate_request
from test_data.params import (
    # позитивные
    POSITIVE_MINIMAL_PAYLOADS,
    POSITIVE_OPTIONAL_PAYLOADS,
    POSITIVE_DIALOG_PAYLOADS,
    TEMPERATURE_VALUES,
    MAX_TOKENS_VALUES,
    TOP_P_VALUES,
    # негативные
    NEGATIVE_MISSING_FIELDS,
    NEGATIVE_INVALID_TYPES,
    NEGATIVE_INVALID_VALUES,
    NEGATIVE_INVALID_JSON,
)
from utils.logger import get_logger

logger = get_logger(__name__)


# =============================================================================
#                         ПОЗИТИВНЫЕ ТЕСТЫ
# =============================================================================


@allure.epic("GigaChat API")
@allure.feature("POST /chat/completions")
@allure.story("Позитивные тесты")
@pytest.mark.positive
class TestPositiveChatCompletions:
    """Позитивные тесты и валидация схемы ответа."""

    # ---------- Минимальные запросы ----------

    @allure.title("Минимальный запрос: {test_case[id]}")
    @pytest.mark.smoke
    @pytest.mark.schema
    @pytest.mark.parametrize(
        "test_case",
        POSITIVE_MINIMAL_PAYLOADS,
        ids=[tc["id"] for tc in POSITIVE_MINIMAL_PAYLOADS],
    )
    def test_minimal_request(self, chat_client, test_case):
        """Запрос с минимальным набором полей возвращает 200 и валидную схему."""
        payload = test_case["payload"]

        allure.dynamic.description(test_case["description"])
        allure.attach(
            json.dumps(payload, ensure_ascii=False, indent=2),
            name="Request Payload",
            attachment_type=allure.attachment_type.JSON,
        )

        validate_request(payload, MINIMAL_REQUEST_SCHEMA, "minimal_request")

        response = chat_client.send(payload)

        allure.attach(
            json.dumps(response.json(), ensure_ascii=False, indent=2),
            name="Response Body",
            attachment_type=allure.attachment_type.JSON,
        )

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}: {response.text}"
        )

        body = response.json()
        validate_response(body, MINIMAL_RESPONSE_SCHEMA, "minimal_response")

        assert body["choices"][0]["message"]["content"], "Ответ модели пуст"
        assert body["choices"][0]["message"]["role"] == "assistant"
        assert body["object"] == "chat.completion"

    @allure.title("Опциональные параметры: {test_case[id]}")
    @pytest.mark.schema
    @pytest.mark.parametrize(
        "test_case",
        POSITIVE_OPTIONAL_PAYLOADS,
        ids=[tc["id"] for tc in POSITIVE_OPTIONAL_PAYLOADS],
    )
    def test_optional_params(self, chat_client, test_case):
        """Запросы с опциональными параметрами возвращают 200."""
        payload = test_case["payload"]

        allure.dynamic.description(test_case["description"])
        allure.attach(
            json.dumps(payload, ensure_ascii=False, indent=2),
            name="Request Payload",
            attachment_type=allure.attachment_type.JSON,
        )

        response = chat_client.send(payload)

        allure.attach(
            json.dumps(response.json(), ensure_ascii=False, indent=2),
            name="Response Body",
            attachment_type=allure.attachment_type.JSON,
        )

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}: {response.text}"
        )

        body = response.json()
        validate_response(body, MINIMAL_RESPONSE_SCHEMA, "minimal_response")
        assert body["choices"][0]["message"]["content"], "Ответ модели пуст"
        assert body["choices"][0]["finish_reason"] in ("stop", "length")

    # ---------- Диалоговая история ----------

    @allure.title("Диалоговая история: {test_case[id]}")
    @pytest.mark.parametrize(
        "test_case",
        POSITIVE_DIALOG_PAYLOADS,
        ids=[tc["id"] for tc in POSITIVE_DIALOG_PAYLOADS],
    )
    def test_dialog_history(self, chat_client, test_case):
        """Модель учитывает историю диалога."""
        payload = test_case["payload"]

        allure.dynamic.description(test_case["description"])
        allure.attach(
            json.dumps(payload, ensure_ascii=False, indent=2),
            name="Request Payload",
            attachment_type=allure.attachment_type.JSON,
        )

        response = chat_client.send(payload)

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}: {response.text}"
        )

        body = response.json()
        validate_response(body, MINIMAL_RESPONSE_SCHEMA, "minimal_response")

        content = body["choices"][0]["message"]["content"]
        assert content, "Ответ модели пуст"
        logger.info("Ответ модели на диалог: %s", content[:200])

    # ---------- Параметризация по temperature ----------

    @allure.title("Параметр temperature={temperature}")
    @pytest.mark.parametrize("temperature", TEMPERATURE_VALUES)
    def test_temperature_values(self, chat_client, temperature):
        """Различные значения temperature принимаются API."""
        payload = {
            "model": "GigaChat",
            "messages": [{"role": "user", "content": "Привет"}],
            "temperature": temperature,
        }

        allure.dynamic.description(f"Запрос с temperature={temperature}")
        response = chat_client.send(payload)

        assert response.status_code == 200, (
            f"temperature={temperature}: ожидался 200, получен {response.status_code}"
        )
        validate_response(response.json(), MINIMAL_RESPONSE_SCHEMA, "minimal_response")

    # ---------- Параметризация по max_tokens ----------

    @allure.title("Параметр max_tokens={max_tokens}")
    @pytest.mark.parametrize("max_tokens", MAX_TOKENS_VALUES)
    def test_max_tokens_values(self, chat_client, max_tokens):
        """Различные значения max_tokens принимаются API."""
        payload = {
            "model": "GigaChat",
            "messages": [{"role": "user", "content": "Расскажи о Python"}],
            "max_tokens": max_tokens,
        }

        allure.dynamic.description(f"Запрос с max_tokens={max_tokens}")
        response = chat_client.send(payload)

        assert response.status_code == 200, (
            f"max_tokens={max_tokens}: ожидался 200, получен {response.status_code}"
        )

        body = response.json()
        validate_response(body, MINIMAL_RESPONSE_SCHEMA, "minimal_response")
        assert body["choices"][0]["finish_reason"] in ("stop", "length")

    # ---------- Параметризация по top_p ----------

    @allure.title("Параметр top_p={top_p}")
    @pytest.mark.parametrize("top_p", TOP_P_VALUES)
    def test_top_p_values(self, chat_client, top_p):
        """Различные значения top_p принимаются API."""
        payload = {
            "model": "GigaChat",
            "messages": [{"role": "user", "content": "Привет"}],
            "top_p": top_p,
        }

        allure.dynamic.description(f"Запрос с top_p={top_p}")
        response = chat_client.send(payload)

        assert response.status_code == 200, (
            f"top_p={top_p}: ожидался 200, получен {response.status_code}"
        )
        validate_response(response.json(), MINIMAL_RESPONSE_SCHEMA, "minimal_response")

    # ---------- Валидация usage ----------

    @allure.title("Проверка объекта usage в ответе")
    @pytest.mark.schema
    def test_usage_fields(self, chat_client):
        """Объект usage содержит корректные данные о токенах."""
        payload = {
            "model": "GigaChat",
            "messages": [{"role": "user", "content": "Скажи одно слово"}],
            "max_tokens": 10,
        }

        response = chat_client.send(payload)
        assert response.status_code == 200

        usage = response.json()["usage"]
        validate_response(usage, USAGE_MINIMAL_SCHEMA, "usage_minimal")

        assert usage["prompt_tokens"] > 0, "prompt_tokens должен быть > 0"
        assert usage["completion_tokens"] > 0, "completion_tokens должен быть > 0"
        assert usage["total_tokens"] > 0, "total_tokens должен быть > 0"

        logger.info(
            "Usage: prompt=%d, completion=%d, total=%d",
            usage["prompt_tokens"],
            usage["completion_tokens"],
            usage["total_tokens"],
        )

    # ---------- Валидация полей верхнего уровня ----------

    @allure.title("Все обязательные поля верхнего уровня присутствуют и типы корректны")
    @pytest.mark.schema
    def test_top_level_required_fields(self, chat_client):
        """Обязательные поля ответа присутствуют с правильными типами."""
        payload = {
            "model": "GigaChat",
            "messages": [{"role": "user", "content": "Скажи одно слово."}],
            "max_tokens": 20,
        }

        response = chat_client.send(payload)
        assert response.status_code == 200

        body = response.json()

        allure.attach(
            json.dumps(body, ensure_ascii=False, indent=2),
            name="Response Body",
            attachment_type=allure.attachment_type.JSON,
        )

        # Наличие полей
        for field in ("choices", "created", "model", "object", "usage"):
            assert field in body, f"Обязательное поле '{field}' отсутствует"

        # Типы
        assert isinstance(body["choices"], list), "choices должен быть list"
        assert isinstance(body["created"], int), "created должен быть int"
        assert isinstance(body["model"], str), "model должен быть str"
        assert isinstance(body["object"], str), "object должен быть str"
        assert isinstance(body["usage"], dict), "usage должен быть dict"

        # Значения
        assert body["object"] == "chat.completion"
        assert "GigaChat" in body["model"]
        assert 1577836800 < body["created"] < 1893456000, "created вне разумного диапазона"

    # ---------- finish_reason ----------

    @allure.title("finish_reason имеет допустимое значение")
    @pytest.mark.schema
    def test_finish_reason_values(self, chat_client):
        """finish_reason входит в допустимый набор значений."""
        payload = {
            "model": "GigaChat",
            "messages": [{"role": "user", "content": "Привет"}],
        }

        response = chat_client.send(payload)
        assert response.status_code == 200

        valid_reasons = {"stop", "length", "function_call", "blacklist", "error"}
        for choice in response.json()["choices"]:
            assert choice["finish_reason"] in valid_reasons, (
                f"finish_reason='{choice['finish_reason']}' недопустим"
            )

    # ---------- choices[0].index ----------

    @allure.title("choices[0].index == 0")
    def test_choices_index(self, chat_client):
        """Индекс первого choice равен 0."""
        payload = {
            "model": "GigaChat",
            "messages": [{"role": "user", "content": "Привет"}],
        }

        response = chat_client.send(payload)
        assert response.status_code == 200
        assert response.json()["choices"][0]["index"] == 0

    # ---------- model в ответе ----------

    @allure.title("Поле model в ответе содержит имя запрошенной модели")
    def test_response_model_field(self, chat_client):
        """Поле model в ответе содержит название запрошенной модели."""
        payload = {
            "model": "GigaChat",
            "messages": [{"role": "user", "content": "Привет"}],
        }

        response = chat_client.send(payload)
        assert response.status_code == 200
        assert "GigaChat" in response.json()["model"]

    # ---------- Согласованность токенов ----------

    @allure.title("Счётчики токенов логически согласованы")
    @pytest.mark.schema
    def test_usage_tokens_consistency(self, chat_client):
        """prompt_tokens и completion_tokens неотрицательны, total_tokens > 0."""
        payload = {
            "model": "GigaChat",
            "messages": [{"role": "user", "content": "Привет"}],
            "max_tokens": 20,
        }

        response = chat_client.send(payload)
        assert response.status_code == 200

        usage = response.json()["usage"]
        assert usage["prompt_tokens"] >= 0
        assert usage["completion_tokens"] >= 0
        assert usage["total_tokens"] > 0


# =============================================================================
#                         НЕГАТИВНЫЕ ТЕСТЫ
# =============================================================================


@allure.epic("GigaChat API")
@allure.feature("POST /chat/completions")
@allure.story("Негативные тесты")
@pytest.mark.negative
class TestNegativeChatCompletions:
    """Негативные тесты: невалидные данные, отсутствие полей, авторизация."""

    # ---------- Отсутствие обязательных полей ----------

    @allure.title("Отсутствие поля: {test_case[id]}")
    @pytest.mark.parametrize(
        "test_case",
        NEGATIVE_MISSING_FIELDS,
        ids=[tc["id"] for tc in NEGATIVE_MISSING_FIELDS],
    )
    def test_missing_required_fields(self, chat_client, test_case):
        """API возвращает 4xx при отсутствии обязательных полей."""
        payload = test_case["payload"]

        allure.dynamic.description(test_case["description"])

        if known_issue := test_case.get("known_issue"):
            allure.dynamic.issue(known_issue)
            pytest.xfail(known_issue)

        allure.attach(
            json.dumps(payload, ensure_ascii=False, indent=2),
            name="Request Payload",
            attachment_type=allure.attachment_type.JSON,
        )

        response = chat_client.send(payload)

        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.TEXT)

        logger.info("[%s] Статус: %d (ожидался 4xx)", test_case["id"], response.status_code)

        assert 400 <= response.status_code < 500, (
            f"Ожидался 4xx, получен {response.status_code}: {response.text}"
        )

    # ---------- Невалидные типы ----------

    @allure.title("Невалидный тип: {test_case[id]}")
    @pytest.mark.parametrize(
        "test_case",
        NEGATIVE_INVALID_TYPES,
        ids=[tc["id"] for tc in NEGATIVE_INVALID_TYPES],
    )
    def test_invalid_field_types(self, chat_client, test_case):
        """API возвращает 4xx при невалидных типах полей."""
        payload = test_case["payload"]

        allure.dynamic.description(test_case["description"])
        allure.attach(
            json.dumps(payload, ensure_ascii=False, indent=2),
            name="Request Payload",
            attachment_type=allure.attachment_type.JSON,
        )

        response = chat_client.send(payload)

        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.TEXT)

        logger.info("[%s] Статус: %d (ожидался 4xx)", test_case["id"], response.status_code)

        assert 400 <= response.status_code < 500, (
            f"Ожидался 4xx, получен {response.status_code}: {response.text}"
        )

    # ---------- Невалидные значения ----------

    @allure.title("Невалидное значение: {test_case[id]}")
    @pytest.mark.parametrize(
        "test_case",
        NEGATIVE_INVALID_VALUES,
        ids=[tc["id"] for tc in NEGATIVE_INVALID_VALUES],
    )
    def test_invalid_field_values(self, chat_client, test_case):
        """API возвращает 4xx при невалидных значениях полей."""
        payload = test_case["payload"]
        expected_status = test_case["expected_status"]

        allure.dynamic.description(test_case["description"])
        allure.attach(
            json.dumps(payload, ensure_ascii=False, indent=2),
            name="Request Payload",
            attachment_type=allure.attachment_type.JSON,
        )

        response = chat_client.send(payload)

        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.TEXT)

        logger.info("[%s] Статус: %d (ожидался %d)", test_case["id"], response.status_code, expected_status)

        if expected_status == 404:
            assert response.status_code in (404, 400, 422), (
                f"Ожидался 404/400/422, получен {response.status_code}"
            )
        else:
            assert 400 <= response.status_code < 500, (
                f"Ожидался 4xx, получен {response.status_code}: {response.text}"
            )

    # ---------- Невалидный JSON ----------

    @allure.title("Невалидный JSON: {test_case[id]}")
    @pytest.mark.parametrize(
        "test_case",
        NEGATIVE_INVALID_JSON,
        ids=[tc["id"] for tc in NEGATIVE_INVALID_JSON],
    )
    def test_invalid_json_body(self, chat_client, test_case):
        """API возвращает 400 при невалидном JSON в теле."""
        raw_data = test_case["raw_data"]

        allure.dynamic.description(test_case["description"])
        allure.attach(raw_data, name="Raw Request Body", attachment_type=allure.attachment_type.TEXT)

        response = chat_client.send_raw(raw_data)

        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.TEXT)

        logger.info("[%s] Статус: %d", test_case["id"], response.status_code)

        assert 400 <= response.status_code < 500, (
            f"Ожидался 4xx, получен {response.status_code}: {response.text}"
        )

    # ---------- Без авторизации ----------

    @allure.title("Запрос без заголовка Authorization")
    def test_no_authorization_header(self, chat_client):
        """API возвращает 401 без заголовка Authorization."""
        payload = {
            "model": "GigaChat",
            "messages": [{"role": "user", "content": "Привет"}],
        }

        response = chat_client.send_unauthorized(payload)

        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.TEXT)

        assert response.status_code == 401, (
            f"Ожидался 401, получен {response.status_code}: {response.text}"
        )

    # ---------- Невалидный токен ----------

    @allure.title("Запрос с невалидным токеном")
    def test_invalid_token(self, chat_client):
        """API возвращает 401/403 при невалидном токене."""
        payload = {
            "model": "GigaChat",
            "messages": [{"role": "user", "content": "Привет"}],
        }

        response = chat_client.send_invalid_token(payload)

        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.TEXT)

        assert response.status_code in (401, 403), (
            f"Ожидался 401/403, получен {response.status_code}: {response.text}"
        )

    # ---------- Пустое тело ----------

    @allure.title("Запрос без тела (пустая строка)")
    def test_empty_request_body(self, chat_client):
        """API возвращает 4xx при пустом теле запроса."""
        response = chat_client.send_raw("")

        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.TEXT)

        assert 400 <= response.status_code < 500, (
            f"Ожидался 4xx, получен {response.status_code}: {response.text}"
        )

    # ---------- Неверный Content-Type ----------

    @allure.title("Запрос с Content-Type: text/plain")
    def test_wrong_content_type(self, chat_client):
        """Запрос с неправильным Content-Type не вызывает 5xx."""
        payload = json.dumps({
            "model": "GigaChat",
            "messages": [{"role": "user", "content": "Привет"}],
        })

        response = chat_client.send_raw(payload, content_type="text/plain")

        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.TEXT)

        assert response.status_code < 500, (
            f"Получена серверная ошибка {response.status_code}: {response.text}"
        )
