HIGH_KEYWORDS = (
    "down", "outage", "data loss", "breach", "security", "production",
    "critical", "urgent", "cannot access", "unavailable", "crash", "500",
)
MEDIUM_KEYWORDS = (
    "cannot", "can't", "unable", "error", "fail", "slow", "broken",
    "not working", "timeout", "bug",
)

CATEGORY_KEYWORDS = (
    ("billing", ("invoice", "billing", "charge", "refund", "payment", "subscription")),
    ("access_request", ("access", "permission", "password", "log in", "login", "reset")),
    ("feature_request", ("feature", "request", "would like", "enhancement", "suggest")),
    ("bug", ("bug", "error", "crash", "broken", "fail", "not working", "down")),
)


def _normalize(text) -> str:
    if not isinstance(text, str) or not text.strip():
        return ""
    return text.strip().lower()


def classify_severity(text: str) -> str:
    """
    Classify the severity of a support ticket.
    Returns: "low", "medium", or "high"
    Raises: nothing — returns "low" for empty/None input
    """
    normalized = _normalize(text)
    if not normalized:
        print("Warning: empty or missing ticket text, defaulting to 'low'")
        return "low"
    if any(k in normalized for k in HIGH_KEYWORDS):
        return "high"
    if any(k in normalized for k in MEDIUM_KEYWORDS):
        return "medium"
    return "low"


def classify_category(text: str) -> str:
    """
    Classify the category of a support ticket.
    Returns: "bug", "feature_request", "billing", "access_request", or "other"
    """
    normalized = _normalize(text)
    if not normalized:
        return "other"
    for category, keywords in CATEGORY_KEYWORDS:
        if any(k in normalized for k in keywords):
            return category
    return "other"
