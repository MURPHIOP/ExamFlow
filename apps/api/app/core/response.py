from typing import Any


def api_response(*, success: bool, message: str, data: Any | None = None, meta: Any | None = None):
    payload: dict[str, Any] = {"success": success, "message": message}
    if data is not None:
        payload["data"] = data
    if meta is not None:
        payload["meta"] = meta
    return payload
