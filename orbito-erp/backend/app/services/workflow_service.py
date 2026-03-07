import asyncio
import random
from typing import Dict, Optional
import httpx
from app.core.config import settings

RETRYABLE_STATUS_CODES = {408, 409, 425, 429, 500, 502, 503, 504}


def _is_retryable_status(status_code: int) -> bool:
    return status_code in RETRYABLE_STATUS_CODES


def _compute_delay(attempt: int) -> float:
    # Exponential backoff with jitter: base * (2^(attempt-1)) + jitter(0..base)
    exponential = settings.n8n_retry_base_delay_seconds * (2 ** (attempt - 1))
    jitter = random.uniform(0, settings.n8n_retry_base_delay_seconds)
    return exponential + jitter


async def _send_once(
    client: httpx.AsyncClient, event_type: str, payload: dict
) -> Dict[str, Optional[object]]:
    response = await client.post(
        settings.n8n_webhook_url,
        json={"event": event_type, "data": payload},
    )
    return {
        "ok": response.is_success,
        "status_code": response.status_code,
        "error": None if response.is_success else response.text[:500],
    }


async def trigger_n8n_workflow(event_type: str, payload: dict):
    if not settings.n8n_webhook_url:
        return {
            "ok": False,
            "status_code": None,
            "error": "N8N_WEBHOOK_URL is not configured",
            "attempts": 0,
        }

    max_attempts = max(1, settings.n8n_max_retries + 1)
    last_result = None

    async with httpx.AsyncClient(timeout=settings.n8n_request_timeout_seconds) as client:
        for attempt in range(1, max_attempts + 1):
            try:
                result = await _send_once(client, event_type, payload)
                result["attempts"] = attempt
                if result["ok"]:
                    return result

                last_result = result
                status_code = result.get("status_code")
                if attempt < max_attempts and status_code and _is_retryable_status(int(status_code)):
                    await asyncio.sleep(_compute_delay(attempt))
                    continue
                return result

            except (httpx.TimeoutException, httpx.ConnectError, httpx.ReadError) as exc:
                last_result = {
                    "ok": False,
                    "status_code": None,
                    "error": str(exc),
                    "attempts": attempt,
                }
                if attempt < max_attempts:
                    await asyncio.sleep(_compute_delay(attempt))
                    continue
                return last_result

            except Exception as exc:
                return {
                    "ok": False,
                    "status_code": None,
                    "error": str(exc),
                    "attempts": attempt,
                }

    return last_result or {
        "ok": False,
        "status_code": None,
        "error": "Unknown n8n trigger failure",
        "attempts": 0,
    }
