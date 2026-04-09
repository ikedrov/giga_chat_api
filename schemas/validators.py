"""
Утилиты для валидации JSON-схем с интеграцией в Allure.
"""
import allure
import jsonschema
from jsonschema import validate, ValidationError
from utils.logger import get_logger

logger = get_logger(__name__)


@allure.step("Валидация JSON-ответа по схеме: {schema_name}")
def validate_response(response_json: dict, schema: dict, schema_name: str = "response") -> None:
    """
    Валидирует JSON-ответ по указанной JSON-схеме.

    Args:
        response_json: JSON-объект ответа API.
        schema: JSON-схема для валидации.
        schema_name: Человекочитаемое имя схемы (для отчётов).

    Raises:
        AssertionError: Если валидация провалена.
    """
    try:
        validate(instance=response_json, schema=schema)
        logger.info("Валидация по схеме '%s' пройдена успешно", schema_name)
    except ValidationError as e:
        error_msg = (
            f"Валидация по схеме '{schema_name}' провалена:\n"
            f"  Путь: {' -> '.join(str(p) for p in e.absolute_path)}\n"
            f"  Ошибка: {e.message}\n"
            f"  Значение: {e.instance}"
        )
        logger.error(error_msg)
        allure.attach(
            str(e),
            name=f"Ошибка валидации ({schema_name})",
            attachment_type=allure.attachment_type.TEXT,
        )
        raise AssertionError(error_msg) from e


@allure.step("Валидация запроса по схеме: {schema_name}")
def validate_request(request_json: dict, schema: dict, schema_name: str = "request") -> None:
    """
    Валидирует JSON-запрос по указанной JSON-схеме.

    Args:
        request_json: JSON-объект запроса.
        schema: JSON-схема для валидации.
        schema_name: Человекочитаемое имя схемы.

    Raises:
        AssertionError: Если валидация провалена.
    """
    try:
        validate(instance=request_json, schema=schema)
        logger.info("Запрос валиден по схеме '%s'", schema_name)
    except ValidationError as e:
        error_msg = (
            f"Запрос невалиден по схеме '{schema_name}':\n"
            f"  Путь: {' -> '.join(str(p) for p in e.absolute_path)}\n"
            f"  Ошибка: {e.message}"
        )
        logger.error(error_msg)
        raise AssertionError(error_msg) from e
