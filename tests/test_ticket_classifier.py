from meridian.ticket_classifier import classify_category, classify_severity

VALID_CATEGORIES = {"bug", "feature_request", "billing", "access_request", "other"}


def test_classify_severity_is_callable():
    try:
        classify_severity("test")
    except NotImplementedError:
        pass  # scaffold not implemented yet
    except Exception as e:
        raise AssertionError(f"Unexpected error: {e}")


def test_returns_valid_label():
    result = classify_severity("Customer cannot log in")

    assert result in {"low", "medium", "high"}


def test_empty_string_returns_low():
    assert classify_severity("") == "low"


def test_none_returns_low():
    assert classify_severity(None) == "low"


def test_is_deterministic():
    text = "Production database is down and customers cannot access the platform"

    first = classify_severity(text)
    second = classify_severity(text)

    assert first == second


def test_returns_string():
    result = classify_severity("Unable to reset password")

    assert isinstance(result, str)

def test_category_returns_valid_label():
    result = classify_category("Customer cannot log in")

    assert result in VALID_CATEGORIES


def test_category_empty_string_returns_other():
    assert classify_category("") == "other"


def test_category_none_returns_other():
    assert classify_category(None) == "other"


def test_category_is_deterministic():
    text = "I was charged twice on my last invoice"

    assert classify_category(text) == classify_category(text)


def test_category_billing():
    assert classify_category("I was charged twice on my last invoice") == "billing"


def test_category_access_request():
    assert classify_category("Please reset my password") == "access_request"


def test_category_feature_request():
    assert classify_category("We would like a dark mode feature") == "feature_request"


def test_category_unrecognised_text_returns_other():
    assert classify_category("Hello there") == "other"


import pytest


@pytest.mark.parametrize(
    "text",
    [
        "Production database is down, 500 users affected",
        "Complete outage of the payments platform",
        "We suspect a security breach on the admin portal",
        "Customer data loss after last night's migration",
        "The app crashes on startup for everyone",
        "URGENT: service unavailable",
        "Getting HTTP 500 errors on every request",
        "Possible fraudulent transactions on customer accounts",
    ],
)
def test_severity_high_examples(text):
    assert classify_severity(text) == "high"


@pytest.mark.parametrize(
    "text",
    [
        "Unable to reset password",
        "Page is loading slowly",
        "Export fails with an error message",
        "Report shows the wrong totals",
        "Dashboard is not working for me",
        "I keep getting timed out when saving",
        "Feature is broken on mobile",
        "I am locked out of my account",
    ],
)
def test_severity_medium_examples(text):
    assert classify_severity(text) == "medium"


@pytest.mark.parametrize(
    "text",
    [
        "How do I change my display name?",
        "I would like to download my statement",
        "Thanks for the quick help yesterday",
        "Payment of $1500 was received",
    ],
)
def test_severity_low_examples_avoid_substring_false_positives(text):
    assert classify_severity(text) == "low"


def test_severity_is_case_insensitive():
    assert classify_severity("PRODUCTION IS DOWN") == "high"


@pytest.mark.parametrize(
    "text,expected",
    [
        ("Refund my subscription please", "billing"),
        ("Wrong amount on my receipt", "billing"),
        ("My credit card was overcharged", "billing"),
        ("I need permission to view the reports folder", "access_request"),
        ("Please grant me access to the finance dashboard", "access_request"),
        ("I am locked out and need a password reset", "access_request"),
        ("MFA code is not arriving, cannot sign in", "access_request"),
        ("It would be great to have an export to CSV", "feature_request"),
        ("Could you add a dark mode?", "feature_request"),
        ("Suggestion: support bulk uploads", "feature_request"),
        ("The app crashes when I open settings", "bug"),
        ("Search returns an error", "bug"),
        ("Save button does not work", "bug"),
        ("Just saying hello", "other"),
    ],
)
def test_category_examples(text, expected):
    assert classify_category(text) == expected


def test_category_avoids_substring_false_positives():
    assert classify_category("The discharge summary is ready") == "other"
