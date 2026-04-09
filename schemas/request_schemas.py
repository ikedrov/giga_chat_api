"""
JSON-схемы запросов к /chat/completions.

Определены две схемы:
- MINIMAL_REQUEST_SCHEMA — только обязательные поля (model, messages)
- FULL_REQUEST_SCHEMA — все допустимые поля запроса
"""

# Схема отдельного сообщения (только обязательные поля)
MESSAGE_MINIMAL_SCHEMA = {
    "type": "object",
    "properties": {
        "role": {
            "type": "string",
            "enum": ["user", "system", "assistant", "function"],
        },
        "content": {
            "type": "string",
        },
    },
    "required": ["role", "content"],
    "additionalProperties": True,
}

# Схема отдельного сообщения (полная)
MESSAGE_FULL_SCHEMA = {
    "type": "object",
    "properties": {
        "role": {
            "type": "string",
            "enum": ["user", "system", "assistant", "function"],
        },
        "content": {
            "type": "string",
        },
        "functions_state_id": {
            "type": "string",
        },
        "attachments": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": ["role", "content"],
    "additionalProperties": False,
}

# Минимальная схема запроса (только обязательные поля)
MINIMAL_REQUEST_SCHEMA = {
    "type": "object",
    "properties": {
        "model": {
            "type": "string",
            "minLength": 1,
        },
        "messages": {
            "type": "array",
            "items": MESSAGE_MINIMAL_SCHEMA,
            "minItems": 1,
        },
    },
    "required": ["model", "messages"],
    "additionalProperties": True,
}

# Полная схема запроса (все допустимые поля)
FULL_REQUEST_SCHEMA = {
    "type": "object",
    "properties": {
        "model": {
            "type": "string",
            "minLength": 1,
        },
        "messages": {
            "type": "array",
            "items": MESSAGE_FULL_SCHEMA,
            "minItems": 1,
        },
        "temperature": {
            "type": "number",
            "minimum": 0,
        },
        "top_p": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
        },
        "stream": {
            "type": "boolean",
        },
        "max_tokens": {
            "type": "integer",
            "exclusiveMinimum": 0,
        },
        "repetition_penalty": {
            "type": "number",
            "minimum": 0,
        },
        "update_interval": {
            "type": "number",
            "minimum": 0,
        },
        "function_call": {
            "oneOf": [
                {"type": "string", "enum": ["none", "auto"]},
                {
                    "type": "object",
                    "properties": {"name": {"type": "string"}},
                    "required": ["name"],
                },
            ],
        },
        "functions": {
            "type": ["array", "null"],
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "parameters": {"type": "object"},
                    "few_shot_examples": {"type": "array"},
                    "return_parameters": {"type": "object"},
                },
                "required": ["name", "description", "parameters"],
            },
        },
    },
    "required": ["model", "messages"],
    "additionalProperties": False,
}
