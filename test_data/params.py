"""
Все параметры тестов для /chat/completions — позитивные и негативные.
"""

# =============================================================================
#                         ПОЗИТИВНЫЕ ТЕСТЫ
# =============================================================================

# ---------- Минимальные запросы ----------

MINIMAL_REQUEST_USER_ONLY = {
    "id": "minimal_user_only",
    "description": "Минимальный запрос: только model и одно user-сообщение",
    "payload": {
        "model": "GigaChat",
        "messages": [
            {"role": "user", "content": "Привет"}
        ],
    },
}

MINIMAL_REQUEST_WITH_SYSTEM = {
    "id": "minimal_with_system",
    "description": "Запрос с system + user сообщениями",
    "payload": {
        "model": "GigaChat",
        "messages": [
            {"role": "system", "content": "Ты — полезный ассистент."},
            {"role": "user", "content": "Что такое Python?"},
        ],
    },
}

# ---------- Запросы с опциональными параметрами ----------

REQUEST_WITH_TEMPERATURE = {
    "id": "with_temperature",
    "description": "Запрос с параметром temperature=0.1 (низкая случайность)",
    "payload": {
        "model": "GigaChat",
        "messages": [
            {"role": "user", "content": "Столица России?"}
        ],
        "temperature": 0.1,
    },
}

REQUEST_WITH_MAX_TOKENS = {
    "id": "with_max_tokens",
    "description": "Запрос с ограничением max_tokens=50",
    "payload": {
        "model": "GigaChat",
        "messages": [
            {"role": "user", "content": "Расскажи о космосе кратко"}
        ],
        "max_tokens": 50,
    },
}

REQUEST_WITH_TOP_P = {
    "id": "with_top_p",
    "description": "Запрос с параметром top_p=0.5",
    "payload": {
        "model": "GigaChat",
        "messages": [
            {"role": "user", "content": "Что такое машинное обучение?"}
        ],
        "top_p": 0.5,
    },
}

REQUEST_WITH_REPETITION_PENALTY = {
    "id": "with_repetition_penalty",
    "description": "Запрос с параметром repetition_penalty=1.2",
    "payload": {
        "model": "GigaChat",
        "messages": [
            {"role": "user", "content": "Перечисли 5 планет Солнечной системы"}
        ],
        "repetition_penalty": 1.2,
    },
}

REQUEST_ALL_OPTIONAL_PARAMS = {
    "id": "all_optional_params",
    "description": "Запрос со всеми опциональными параметрами",
    "payload": {
        "model": "GigaChat",
        "messages": [
            {"role": "system", "content": "Отвечай кратко."},
            {"role": "user", "content": "Сколько будет 2+2?"},
        ],
        "temperature": 0.5,
        "top_p": 0.8,
        "max_tokens": 100,
        "repetition_penalty": 1.0,
        "stream": False,
        "update_interval": 0,
    },
}

REQUEST_STREAM_FALSE = {
    "id": "stream_false",
    "description": "Запрос с явным stream=false",
    "payload": {
        "model": "GigaChat",
        "messages": [
            {"role": "user", "content": "Расскажи анекдот"}
        ],
        "stream": False,
    },
}

# ---------- Диалоговая история ----------

REQUEST_WITH_DIALOG_HISTORY = {
    "id": "dialog_history",
    "description": "Запрос с историей диалога (system + user + assistant + user)",
    "payload": {
        "model": "GigaChat",
        "messages": [
            {"role": "system", "content": "Ты — ассистент по математике."},
            {"role": "user", "content": "Сколько будет 2+2?"},
            {"role": "assistant", "content": "2+2 = 4"},
            {"role": "user", "content": "А 3+3?"},
        ],
    },
}

# ---------- Списки для параметризации (позитивные) ----------

POSITIVE_MINIMAL_PAYLOADS = [
    MINIMAL_REQUEST_USER_ONLY,
    MINIMAL_REQUEST_WITH_SYSTEM,
]

POSITIVE_OPTIONAL_PAYLOADS = [
    REQUEST_WITH_TEMPERATURE,
    REQUEST_WITH_MAX_TOKENS,
    REQUEST_WITH_TOP_P,
    REQUEST_WITH_REPETITION_PENALTY,
    REQUEST_ALL_OPTIONAL_PARAMS,
    REQUEST_STREAM_FALSE,
]

POSITIVE_DIALOG_PAYLOADS = [
    REQUEST_WITH_DIALOG_HISTORY,
]

TEMPERATURE_VALUES = [0, 0.1, 0.5, 1.0, 1.5, 2.0]
MAX_TOKENS_VALUES = [1, 10, 50, 100, 512, 1024]
TOP_P_VALUES = [0.0, 0.1, 0.5, 0.9, 1.0]


# =============================================================================
#                         НЕГАТИВНЫЕ ТЕСТЫ
# =============================================================================

# ---------- Пустое / отсутствующее тело запроса ----------

EMPTY_BODY = {
    "id": "empty_body",
    "description": "Пустое тело запроса",
    "payload": {},
    "expected_status": 404,
}

# ---------- Отсутствие обязательных полей ----------

MISSING_MODEL = {
    "id": "missing_model",
    "description": "Отсутствует обязательное поле model",
    "payload": {
        "messages": [
            {"role": "user", "content": "Привет"}
        ],
    },
    "expected_status": 422,
}

MISSING_MESSAGES = {
    "id": "missing_messages",
    "description": "Отсутствует обязательное поле messages",
    "payload": {
        "model": "GigaChat",
    },
    "expected_status": 422,
}

MISSING_ROLE_IN_MESSAGE = {
    "id": "missing_role",
    "description": "Отсутствует role в сообщении",
    "payload": {
        "model": "GigaChat",
        "messages": [
            {"content": "Привет"}
        ],
    },
    "expected_status": 422,
}

MISSING_CONTENT_IN_MESSAGE = {
    "id": "missing_content",
    "description": "Отсутствует content в сообщении",
    "payload": {
        "model": "GigaChat",
        "messages": [
            {"role": "user"}
        ],
    },
    "expected_status": 422,
    "known_issue": (
        "API не валидирует отсутствие поля content и возвращает 200 вместо 422. "
        "Расхождение с документацией: content — обязательное поле сообщения."
    ),
}

# ---------- Невалидные типы полей ----------

INVALID_MODEL_TYPE = {
    "id": "invalid_model_type",
    "description": "model имеет невалидный тип (число вместо строки)",
    "payload": {
        "model": 12345,
        "messages": [
            {"role": "user", "content": "Привет"}
        ],
    },
    "expected_status": 422,
}

INVALID_MESSAGES_TYPE = {
    "id": "invalid_messages_type",
    "description": "messages — строка вместо массива",
    "payload": {
        "model": "GigaChat",
        "messages": "Привет",
    },
    "expected_status": 422,
}

INVALID_TEMPERATURE_TYPE = {
    "id": "invalid_temperature_type",
    "description": "temperature — строка вместо числа",
    "payload": {
        "model": "GigaChat",
        "messages": [
            {"role": "user", "content": "Привет"}
        ],
        "temperature": "hot",
    },
    "expected_status": 422,
}

INVALID_MAX_TOKENS_TYPE = {
    "id": "invalid_max_tokens_type",
    "description": "max_tokens — строка вместо числа",
    "payload": {
        "model": "GigaChat",
        "messages": [
            {"role": "user", "content": "Привет"}
        ],
        "max_tokens": "много",
    },
    "expected_status": 422,
}

INVALID_STREAM_TYPE = {
    "id": "invalid_stream_type",
    "description": "stream — строка вместо boolean",
    "payload": {
        "model": "GigaChat",
        "messages": [
            {"role": "user", "content": "Привет"}
        ],
        "stream": "yes",
    },
    "expected_status": 422,
}

INVALID_TOP_P_TYPE = {
    "id": "invalid_top_p_type",
    "description": "top_p — строка вместо числа",
    "payload": {
        "model": "GigaChat",
        "messages": [
            {"role": "user", "content": "Привет"}
        ],
        "top_p": "half",
    },
    "expected_status": 422,
}

# ---------- Невалидные значения полей ----------

INVALID_MODEL_NAME = {
    "id": "invalid_model_name",
    "description": "Несуществующая модель",
    "payload": {
        "model": "NonExistentModel-999",
        "messages": [
            {"role": "user", "content": "Привет"}
        ],
    },
    "expected_status": 404,
}

INVALID_ROLE = {
    "id": "invalid_role",
    "description": "Невалидная роль сообщения",
    "payload": {
        "model": "GigaChat",
        "messages": [
            {"role": "admin", "content": "Привет"}
        ],
    },
    "expected_status": 422,
}

EMPTY_MESSAGES_ARRAY = {
    "id": "empty_messages_array",
    "description": "Пустой массив messages",
    "payload": {
        "model": "GigaChat",
        "messages": [],
    },
    "expected_status": 422,
}

NEGATIVE_MAX_TOKENS = {
    "id": "negative_max_tokens",
    "description": "Отрицательное значение max_tokens",
    "payload": {
        "model": "GigaChat",
        "messages": [
            {"role": "user", "content": "Привет"}
        ],
        "max_tokens": -10,
    },
    "expected_status": 422,
}

ZERO_MAX_TOKENS = {
    "id": "zero_max_tokens",
    "description": "max_tokens = 0",
    "payload": {
        "model": "GigaChat",
        "messages": [
            {"role": "user", "content": "Привет"}
        ],
        "max_tokens": 0,
    },
    "expected_status": 422,
}

NEGATIVE_TEMPERATURE = {
    "id": "negative_temperature",
    "description": "Отрицательная temperature",
    "payload": {
        "model": "GigaChat",
        "messages": [
            {"role": "user", "content": "Привет"}
        ],
        "temperature": -1.0,
    },
    "expected_status": 422,
}

TOP_P_OUT_OF_RANGE = {
    "id": "top_p_out_of_range",
    "description": "top_p > 1 (за пределами допустимого диапазона)",
    "payload": {
        "model": "GigaChat",
        "messages": [
            {"role": "user", "content": "Привет"}
        ],
        "top_p": 1.5,
    },
    "expected_status": 422,
}

EMPTY_MODEL_STRING = {
    "id": "empty_model_string",
    "description": "Пустая строка в поле model",
    "payload": {
        "model": "",
        "messages": [
            {"role": "user", "content": "Привет"}
        ],
    },
    "expected_status": 422,
}

# ---------- Невалидный JSON ----------

INVALID_JSON_STRING = {
    "id": "invalid_json",
    "description": "Невалидный JSON (битая строка)",
    "raw_data": '{"model": "GigaChat", "messages": [{"role": "user", "content": "test"}',
    "expected_status": 400,
}

PLAIN_TEXT_BODY = {
    "id": "plain_text_body",
    "description": "Текст вместо JSON",
    "raw_data": "просто текст без JSON",
    "expected_status": 400,
}

# ---------- Списки для параметризации (негативные) ----------

NEGATIVE_MISSING_FIELDS = [
    EMPTY_BODY,
    MISSING_MODEL,
    MISSING_MESSAGES,
    MISSING_ROLE_IN_MESSAGE,
    MISSING_CONTENT_IN_MESSAGE,
]

NEGATIVE_INVALID_TYPES = [
    INVALID_MODEL_TYPE,
    INVALID_MESSAGES_TYPE,
    INVALID_TEMPERATURE_TYPE,
    INVALID_MAX_TOKENS_TYPE,
    INVALID_STREAM_TYPE,
    INVALID_TOP_P_TYPE,
]

NEGATIVE_INVALID_VALUES = [
    INVALID_MODEL_NAME,
    INVALID_ROLE,
    EMPTY_MESSAGES_ARRAY,
    NEGATIVE_MAX_TOKENS,
    ZERO_MAX_TOKENS,
    NEGATIVE_TEMPERATURE,
    TOP_P_OUT_OF_RANGE,
    EMPTY_MODEL_STRING,
]

NEGATIVE_INVALID_JSON = [
    INVALID_JSON_STRING,
    PLAIN_TEXT_BODY,
]
