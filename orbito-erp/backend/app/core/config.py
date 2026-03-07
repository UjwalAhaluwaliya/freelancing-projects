import os
from dataclasses import dataclass
from typing import List
from dotenv import load_dotenv

load_dotenv()


def _get_env(name: str, default: str = "", required: bool = False) -> str:
    value = os.getenv(name, default)
    if required and not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _parse_origins(value: str) -> List[str]:
    if not value:
        return ["*"]
    return [origin.strip() for origin in value.split(",") if origin.strip()]


def _get_int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise RuntimeError(f"Environment variable {name} must be an integer") from exc


def _get_float_env(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError as exc:
        raise RuntimeError(f"Environment variable {name} must be a float") from exc


@dataclass(frozen=True)
class Settings:
    app_env: str
    supabase_url: str
    supabase_key: str
    gemini_api_key: str
    n8n_webhook_url: str
    policy_chat_webhook_url: str
    gemini_model: str
    jwt_secret_key: str
    jwt_algorithm: str
    cors_origins: List[str]
    n8n_request_timeout_seconds: float
    n8n_max_retries: int
    n8n_retry_base_delay_seconds: float
    default_employee_password: str


def _build_settings() -> Settings:
    built = Settings(
        app_env=_get_env("APP_ENV", default="development").lower(),
        supabase_url=_get_env("SUPABASE_URL", required=True),
        supabase_key=_get_env("SUPABASE_KEY", required=True),
        gemini_api_key=_get_env("GEMINI_API_KEY", required=True),
        n8n_webhook_url=_get_env("N8N_WEBHOOK_URL"),
        policy_chat_webhook_url=_get_env(
            "POLICY_CHAT_WEBHOOK_URL",
            default="http://localhost:5678/webhook-test/policy-chat",
        ),
        gemini_model=_get_env("GEMINI_MODEL", default="gemini-1.5-flash"),
        jwt_secret_key=_get_env(
            "JWT_SECRET_KEY",
            default="change-this-in-production",
        ),
        jwt_algorithm=_get_env("JWT_ALGORITHM", default="HS256"),
        cors_origins=_parse_origins(_get_env("CORS_ORIGINS", default="*")),
        n8n_request_timeout_seconds=_get_float_env("N8N_REQUEST_TIMEOUT_SECONDS", default=15.0),
        n8n_max_retries=_get_int_env("N8N_MAX_RETRIES", default=3),
        n8n_retry_base_delay_seconds=_get_float_env("N8N_RETRY_BASE_DELAY_SECONDS", default=0.5),
        default_employee_password=_get_env("DEFAULT_EMPLOYEE_PASSWORD", default="Emp@12345"),
    )

    if built.app_env == "production":
        if "*" in built.cors_origins:
            raise RuntimeError("CORS_ORIGINS cannot contain '*' in production")
        if built.jwt_secret_key == "change-this-in-production" or len(built.jwt_secret_key) < 32:
            raise RuntimeError(
                "Set a strong JWT_SECRET_KEY (min 32 chars) for production"
            )
    return built


settings = _build_settings()
