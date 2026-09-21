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
