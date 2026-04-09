"""
JSON-схемы ответов от /chat/completions.

Определены две схемы:
- MINIMAL_RESPONSE_SCHEMA — только обязательные поля, которые гарантированно присутствуют
- FULL_RESPONSE_SCHEMA — все поля включая необязательные
"""

# Схема сообщения ответа (только обязательные поля)
RESPONSE_MESSAGE_MINIMAL_SCHEMA = {
    "type": "object",
    "properties": {
        "content": {
            "type": "string",
        },
        "role": {
            "type": "string",
            "enum": ["assistant", "function_in_progress"],
        },
    },
    "required": ["content", "role"],
    "additionalProperties": True,
}

# Схема сообщения ответа (полная)
RESPONSE_MESSAGE_FULL_SCHEMA = {
    "type": "object",
    "properties": {
        "content": {
            "type": "string",
        },
        "role": {
            "type": "string",
            "enum": ["assistant", "function_in_progress"],
        },
        "functions_state_id": {
            "type": "string",
        },
        "timestamp": {
            "type": "number",
        },
        "function_name": {
            "type": "string",
        },
    },
    "required": ["content", "role"],
    "additionalProperties": True,
}

# Схема usage (только обязательные поля)
USAGE_MINIMAL_SCHEMA = {
    "type": "object",
    "properties": {
        "prompt_tokens": {"type": "integer", "minimum": 0},
        "completion_tokens": {"type": "integer", "minimum": 0},
        "total_tokens": {"type": "integer", "minimum": 0},
    },
    "required": ["prompt_tokens", "completion_tokens", "total_tokens"],
    "additionalProperties": True,
}

# Схема usage (полная)
USAGE_FULL_SCHEMA = {
    "type": "object",
    "properties": {
        "prompt_tokens": {"type": "integer", "minimum": 0},
        "completion_tokens": {"type": "integer", "minimum": 0},
        "total_tokens": {"type": "integer", "minimum": 0},
        "precached_prompt_tokens": {"type": "integer", "minimum": 0},
    },
    "required": ["prompt_tokens", "completion_tokens", "total_tokens"],
    "additionalProperties": True,
}

# Схема одного choice (минимальная)
CHOICE_MINIMAL_SCHEMA = {
    "type": "object",
    "properties": {
        "message": RESPONSE_MESSAGE_MINIMAL_SCHEMA,
        "index": {"type": "integer", "minimum": 0},
        "finish_reason": {
            "type": "string",
            "enum": ["stop", "length", "function_call", "blacklist", "error"],
        },
    },
    "required": ["message", "index", "finish_reason"],
    "additionalProperties": True,
}

# Схема одного choice (полная)
CHOICE_FULL_SCHEMA = {
    "type": "object",
    "properties": {
        "message": RESPONSE_MESSAGE_FULL_SCHEMA,
        "index": {"type": "integer", "minimum": 0},
        "finish_reason": {
            "type": "string",
            "enum": ["stop", "length", "function_call", "blacklist", "error"],
        },
    },
    "required": ["message", "index", "finish_reason"],
    "additionalProperties": False,
}

# ========== ОСНОВНЫЕ СХЕМЫ ОТВЕТА ==========

# Минимальная схема ответа (только обязательные поля)
MINIMAL_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "choices": {
            "type": "array",
            "items": CHOICE_MINIMAL_SCHEMA,
            "minItems": 1,
        },
        "created": {
            "type": "integer",
        },
        "model": {
            "type": "string",
        },
        "object": {
            "type": "string",
            "const": "chat.completion",
        },
        "usage": USAGE_MINIMAL_SCHEMA,
    },
    "required": ["choices", "created", "model", "object", "usage"],
    "additionalProperties": True,
}

# Полная схема ответа (все поля)
FULL_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "choices": {
            "type": "array",
            "items": CHOICE_FULL_SCHEMA,
            "minItems": 1,
        },
        "created": {
            "type": "integer",
        },
        "model": {
            "type": "string",
        },
        "object": {
            "type": "string",
            "const": "chat.completion",
        },
        "usage": USAGE_FULL_SCHEMA,
    },
    "required": ["choices", "created", "model", "object", "usage"],
    "additionalProperties": False,
}

# Схема ответа об ошибке
ERROR_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "integer"},
        "message": {"type": "string"},
    },
    "required": ["message"],
    "additionalProperties": True,
}
