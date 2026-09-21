from meridian.ticket_classifier import classify_severity


def test_classify_severity_is_callable():
    try:
        classify_severity("test")
    except NotImplementedError:
        pass  # expected — scaffold not yet implemented
    except Exception as e:
        raise AssertionError(f"Unexpected error: {e}")
