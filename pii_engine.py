import json
import logging
from functools import lru_cache
from typing import Any

from config import (
    EMAIL_REGEX,
    MOBILE_REGEX,
    PAN_REGEX,
    AADHAR_REGEX,
    IFSC_REGEX,
    CARD_REGEX,
    UPI_REGEX,
    FIELD_MASK_RULES,
)

from strategies import (
    RegexStrategy
)

logger = logging.getLogger(__name__)

# -------------------------------------------------
# Strategy Registry
# -------------------------------------------------

PII_STRATEGY_REGISTRY = {
    "EMAIL": RegexStrategy(
        EMAIL_REGEX,
        "[REDACTED_EMAIL]",
    ),
    "MOBILE": RegexStrategy(
        MOBILE_REGEX,
        "[REDACTED_MOBILE]",
    ),
    "PAN": RegexStrategy(
        PAN_REGEX,
        "[REDACTED_PAN]",
    ),
    "IFSC": RegexStrategy(
        IFSC_REGEX,
        "[REDACTED_IFSC]",
    ),
    "CARD": RegexStrategy(
        CARD_REGEX,
        "[REDACTED_CARD]",
    ),
    "UPI": RegexStrategy(
        UPI_REGEX,
        "[REDACTED_UPI]",
    ),
    "AADHAR": RegexStrategy(
        AADHAR_REGEX,
        "[REDACTED_AADHAR]",
    ),
}


# -------------------------------------------------
# Cache
# -------------------------------------------------

@lru_cache(maxsize=10000)
def cached_mask(text: str):
    return mask_text(text)


# -------------------------------------------------
# Recursive JSON Masker
# -------------------------------------------------


def mask_sensitive_data(field_key: str, raw_value: Any):
    if raw_value is None:
        return raw_value

    if not isinstance(raw_value, str):
        return raw_value

    strategy_key = FIELD_MASK_RULES.get(field_key.lower())

    if not strategy_key:
        return raw_value

    try:
        strategy = PII_STRATEGY_REGISTRY.get(strategy_key)

        if not strategy:
            return raw_value

        return strategy.apply(raw_value)

    except Exception:
        logger.exception(
            "Masking failed for field=%s",
            field_key,
        )
        return "[REDACTION_FAILURE]"


# -------------------------------------------------
# Structured JSON Traversal
# -------------------------------------------------


def mask_json(data):
    if isinstance(data, dict):
        masked = {}

        for key, value in data.items():
            if isinstance(value, (dict, list)):
                masked[key] = mask_json(value)
            else:
                masked[key] = mask_sensitive_data(key, value)

        return masked

    if isinstance(data, list):
        return [mask_json(item) for item in data]

    return data


# -------------------------------------------------
# Unstructured Text Masking
# -------------------------------------------------


def mask_text(text: str):
    if not isinstance(text, str):
        return text

    for strategy in PII_STRATEGY_REGISTRY.values():
        text = strategy.apply(text)

    return text


# -------------------------------------------------
# Main Public Function
# -------------------------------------------------


def mask_pii(data: Any):
    try:
        if isinstance(data, dict):
            return mask_json(data)

        if isinstance(data, list):
            return mask_json(data)

        if isinstance(data, str):
            return cached_mask(data)

        return data

    except Exception:
        logger.exception("Global masking failure")
        return "[REDACTION_FAILURE]"


# -------------------------------------------------
# Pretty JSON Safe Logger
# -------------------------------------------------


def safe_json_dumps(data):
    try:
        return json.dumps(data, indent=2)
    except Exception:
        return str(data)
