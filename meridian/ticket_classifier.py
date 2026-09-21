import re


def _compile(*phrases: str) -> re.Pattern:
    """Match any phrase as whole words, case-insensitively.

    Word boundaries avoid false hits such as "down" in "download".
    """
    return re.compile(r"\b(?:" + "|".join(phrases) + r")\b", re.IGNORECASE)


HIGH_PATTERN = _compile(
    r"down", r"outages?", r"data loss", r"lost data", r"corrupt(?:ed|ion)?",
    r"breach(?:ed|es)?", r"hacked", r"security incident", r"ransomware",
    r"fraud(?:ulent)?", r"unauthori[sz]ed", r"production", r"prod",
    r"critical", r"urgent", r"emergency", r"sev ?1", r"p1",
    r"unavailable", r"not responding", r"crash(?:es|ed|ing)?",
    r"all users", r"all customers", r"everyone", r"http 5\d\d", r"5\d\d errors?",
    r"cannot access", r"can't access", r"unable to access",
)

MEDIUM_PATTERN = _compile(
    r"cannot", r"can't", r"unable", r"won't", r"doesn't", r"does not", r"not working",
    r"errors?", r"fail(?:s|ed|ing|ure)?", r"bugs?", r"broken", r"glitch(?:es)?",
    r"slow(?:ly)?", r"timeouts?", r"timed out", r"delay(?:s|ed)?", r"stuck",
    r"freez(?:e|es|ing)", r"intermittent", r"wrong", r"incorrect", r"missing",
    r"locked out", r"blocked",
)

# Confidence scoring: heuristic values, tune here.
HIGH_BASE = 0.7  # one high signal; each extra distinct signal adds SIGNAL_STEP
HIGH_CAP = 0.95
MEDIUM_SINGLE_SIGNAL = 0.55  # one weak signal is treated as uncertain
MEDIUM_MULTI_BASE = 0.7  # two medium signals; each extra adds SIGNAL_STEP
MEDIUM_CAP = 0.9
NO_SIGNAL_CONFIDENCE = 0.5
SIGNAL_STEP = 0.1

# Order matters: the first matching category wins.
CATEGORY_PATTERNS = (
    ("billing", _compile(
        r"invoices?", r"billing", r"bill", r"charged?", r"charges", r"overcharged",
        r"refunds?", r"payments?", r"subscriptions?", r"pricing", r"price", r"fees?",
        r"receipts?", r"credit card", r"statements?",
    )),
    ("access_request", _compile(
        r"access", r"permissions?", r"passwords?", r"log ?in", r"sign ?in",
        r"reset", r"locked out", r"account locked", r"mfa", r"2fa", r"role",
        r"onboarding", r"credentials?",
    )),
    ("feature_request", _compile(
        r"features?", r"enhancements?", r"suggest(?:ion|ions)?", r"would like",
        r"would be great", r"nice to have", r"wish", r"(?:please|could you|can you) add",
        r"support for",
    )),
    ("bug", _compile(
        r"bugs?", r"errors?", r"crash(?:es|ed|ing)?", r"broken", r"fail(?:s|ed|ing|ure)?",
        r"not working", r"doesn't work", r"does not work", r"glitch(?:es)?",
        r"exceptions?", r"down",
    )),
)


def _normalize(text) -> str:
    if not isinstance(text, str) or not text.strip():
        return ""
    return text.strip()


def _distinct_matches(pattern: re.Pattern, text: str) -> int:
    """Count distinct keywords found, so repeating one word adds no evidence."""
    return len({match.lower() for match in pattern.findall(text)})


def _confidence(base: float, signals: int, step: float, cap: float) -> float:
    return round(min(cap, base + step * (signals - 1)), 2)


def classify_severity(text: str) -> tuple[str, float]:
    """
    Classify the severity of a support ticket.
    Returns: (label, confidence) where label is "low", "medium" or "high" and
    confidence is a float in [0.0, 1.0] reflecting how much keyword evidence
    supports the label. Confidence is 0.0 for empty/None input and 0.5 when
    no keywords match at all (absence of evidence is not evidence of "low").
    Raises: nothing — returns ("low", 0.0) for empty/None input
    """
    normalized = _normalize(text)
    if not normalized:
        print("Warning: empty or missing ticket text, defaulting to 'low'")
        return "low", 0.0

    high_signals = _distinct_matches(HIGH_PATTERN, normalized)
    if high_signals:
        return "high", _confidence(HIGH_BASE, high_signals, SIGNAL_STEP, HIGH_CAP)

    medium_signals = _distinct_matches(MEDIUM_PATTERN, normalized)
    if medium_signals == 1:
        return "medium", MEDIUM_SINGLE_SIGNAL
    if medium_signals > 1:
        return "medium", _confidence(
            MEDIUM_MULTI_BASE, medium_signals - 1, SIGNAL_STEP, MEDIUM_CAP
        )

    return "low", NO_SIGNAL_CONFIDENCE


def classify_category(text: str) -> str:
    """
    Classify the category of a support ticket.
    Returns: "bug", "feature_request", "billing", "access_request", or "other"
    """
    normalized = _normalize(text)
    if not normalized:
        return "other"
    for category, pattern in CATEGORY_PATTERNS:
        if pattern.search(normalized):
            return category
    return "other"
