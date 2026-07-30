import re


MODEL_ID_PATTERN = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9._-]{2,99}$"
)


def validate_model_id(model_id: str) -> bool:
    return bool(
        MODEL_ID_PATTERN.match(model_id)
    )