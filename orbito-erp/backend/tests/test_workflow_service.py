import asyncio
from types import SimpleNamespace
from app.services import workflow_service


def test_trigger_n8n_workflow_retries_on_retryable_status(monkeypatch):
    calls = {"count": 0}

    async def fake_send_once(client, event_type, payload):
        calls["count"] += 1
        if calls["count"] < 3:
            return {"ok": False, "status_code": 503, "error": "service unavailable"}
        return {"ok": True, "status_code": 200, "error": None}

    async def fake_sleep(_delay):
        return None

    monkeypatch.setattr(workflow_service, "_send_once", fake_send_once)
    monkeypatch.setattr(workflow_service.asyncio, "sleep", fake_sleep)
    monkeypatch.setattr(workflow_service, "_compute_delay", lambda attempt: 0.0)
    monkeypatch.setattr(
        workflow_service,
        "settings",
        SimpleNamespace(
            n8n_webhook_url="http://fake-n8n.local",
            n8n_request_timeout_seconds=1.0,
            n8n_max_retries=3,
            n8n_retry_base_delay_seconds=0.0,
        ),
    )

    result = asyncio.run(workflow_service.trigger_n8n_workflow("resume_shortlisted", {"x": 1}))
    assert result["ok"] is True
    assert result["status_code"] == 200
    assert result["attempts"] == 3
    assert calls["count"] == 3


def test_trigger_n8n_workflow_does_not_retry_on_non_retryable_status(monkeypatch):
    calls = {"count": 0}

    async def fake_send_once(client, event_type, payload):
        calls["count"] += 1
        return {"ok": False, "status_code": 400, "error": "bad request"}

    async def fake_sleep(_delay):
        return None

    monkeypatch.setattr(workflow_service, "_send_once", fake_send_once)
    monkeypatch.setattr(workflow_service.asyncio, "sleep", fake_sleep)
    monkeypatch.setattr(
        workflow_service,
        "settings",
        SimpleNamespace(
            n8n_webhook_url="http://fake-n8n.local",
            n8n_request_timeout_seconds=1.0,
            n8n_max_retries=3,
            n8n_retry_base_delay_seconds=0.0,
        ),
    )

    result = asyncio.run(workflow_service.trigger_n8n_workflow("resume_shortlisted", {"x": 1}))
    assert result["ok"] is False
    assert result["status_code"] == 400
    assert result["attempts"] == 1
    assert calls["count"] == 1
