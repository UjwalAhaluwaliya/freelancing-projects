"""URL safety and toxic message detection services."""

from urllib.parse import parse_qsl, unquote_plus, urlparse

# Unsafe URL/search keywords (blocked)
UNSAFE_URL_KEYWORDS = frozenset(
    {
        # generic adult markers
        "adult",
        "18+",
        "18 plus",
        "porn",
        "pornographic",
        "xxx",
        "nsfw",
        "explicit",
        "sex",
        "nude",
        "nudes",
        "nudity",
        "naked",
        "boobs",
        "breasts",
        "hentai",
        "camgirl",
        "escort",
        "hookup",
        "fetish",
        "hardcore",
        # known adult domains/terms
        "pornhub",
        "xvideos",
        "xnxx",
        "xhamster",
        "redtube",
        "brazzers",
        "onlyfans",
        # violence/self-harm markers
        "violence",
        "gore",
        "self harm",
        "suicide",
    }
)

# Toxic message keywords
TOXIC_KEYWORDS = frozenset(
    {"stupid", "idiot", "hate", "kill", "dumb", "ugly", "worthless", "loser"}
)


class SafetyService:
    """Service for URL safety and toxic message detection."""

    @staticmethod
    def check_url_unsafe(url: str) -> bool:
        """Check if URL/search query contains unsafe keywords."""
        raw = (url or "").strip().lower()
        if not raw:
            return False

        decoded = unquote_plus(raw)
        normalized = decoded.replace("%20", " ")
        compact = normalized.replace(" ", "")

        # Parse URL structure (host/path/query) even when scheme is missing.
        parse_input = raw if raw.startswith(("http://", "https://")) else f"https://{raw}"
        parsed = urlparse(parse_input)

        parts = [raw, decoded, normalized, compact, parsed.netloc.lower(), parsed.path.lower()]
        if parsed.query:
            for key, value in parse_qsl(parsed.query, keep_blank_values=True):
                parts.append(key.lower())
                parts.append(unquote_plus(value).lower())

        haystack = " ".join(p for p in parts if p)
        for keyword in UNSAFE_URL_KEYWORDS:
            if keyword in haystack:
                return True
        return False

    @staticmethod
    def detect_toxic(text: str) -> bool:
        """Detect if text contains toxic words. Returns True if toxic."""
        text_lower = text.lower()
        words = text_lower.replace(".", " ").replace(",", " ").split()
        for word in words:
            if word in TOXIC_KEYWORDS:
                return True
        return False
