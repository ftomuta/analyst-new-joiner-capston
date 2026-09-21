import pytest

from meridian.ticket_classifier import classify_severity, classify_category



def test_classify_severity_returns_valid_label():
    label, confidence = classify_severity("test")          
    assert label in {"low", "medium", "high"}

def test_classify_severity_returns_tuple():                
    result = classify_severity("test")
    assert isinstance(result, tuple)
    assert len(result) == 2

def test_empty_severity():
    label, confidence = classify_severity("")              
    assert label == "low"

def test_none_severity():
    label, confidence = classify_severity(None)            
    assert label == "low"

def test_repeated_severity():
    result = classify_severity("I broke my foot and died")
    result2 = classify_severity("I broke my foot and died")
    assert result == result2                               


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
    label, confidence = classify_severity(text)           
    assert label in {"low", "medium", "high"}


#--- confidence tests ---#

def test_confidence_in_range():
    label, confidence = classify_severity("Password reset isn't working")
    assert 0.0 <= confidence <= 1.0


def test_clear_ticket_high_confidence():
    label, confidence = classify_severity(
        "production database is down, 500 users affected"
    )
    assert confidence >= 0.8


def test_ambiguous_ticket_low_confidence():
    label, confidence = classify_severity("it's not working")
    assert confidence < 0.6