import pytest

from meridian.ticket_classifier import classify_severity, classify_category



def test_classify_severity_returns_valid_label():
    assert classify_severity("test") in {"low", "medium", "high"}
 
def test_classify_severity_returns_string():
    result = classify_severity("test")
    assert isinstance(result, str)
 
def test_empty_severity():
    result = classify_severity("")
    assert result=="low"
 
def test_none_severity():
    result = classify_severity(None)
    assert result=="low"
 
def test_repeated_severity():
    result = classify_severity("I broke my foot and died")
    result2 = classify_severity("I broke my foot and died")
    assert result==result2
 
 
#classify the type of the ticket
def test_classify_category():
    result = classify_category("My feature isn't working")
    assert result in {"bug", "feature_request", "billing", "access_request", "other"}
 
 
 
#--- LLM behavior tests ---#
 
@pytest.mark.parametrize(
    "text",
    [
        "I have a question about my bill",
        "I need help with my account",
        "My feature isn't working",
        "Password reset isn't working",
    ],
)
def test_llm_gives_valid_label(text):
    result = classify_severity(text)
    assert result in {"low", "medium", "high"}
 