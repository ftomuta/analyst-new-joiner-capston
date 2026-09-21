# Write your tests here before implementing
from meridian.ticket_router import route_ticket


def test_route_ticket_is_callable():
    try:
        route_ticket("low", "bug")
    except NotImplementedError:
        pass  # expected until implemented
    except Exception as e:
        raise AssertionError(f"Unexpected error: {e}")


def test_high_severity_always_routes_to_tier_2():
    assert route_ticket("high", "bug") == "tier-2-escalation"


def test_high_severity_overrides_billing_rule():
    assert route_ticket("high", "billing") == "tier-2-escalation"


def test_billing_category_routes_to_billing_team():
    assert route_ticket("medium", "billing") == "billing-team"


def test_non_high_non_billing_routes_to_tier_1():
    assert route_ticket("low", "bug") == "tier-1-support"


def test_unknown_severity_routes_to_tier_1():
    assert route_ticket("critical", "bug") == "tier-1-support"


def test_unknown_category_routes_to_tier_1():
    assert route_ticket("low", "something-else") == "tier-1-support"


def test_unknown_severity_and_category_routes_to_tier_1():
    assert route_ticket("critical", "unknown") == "tier-1-support"

def test_unknown_severity_still_routes_billing_to_billing_team():
    assert route_ticket("critical", "billing") == "billing-team"


def test_low_severity_billing_routes_to_billing_team():
    assert route_ticket("low", "billing") == "billing-team"


def test_none_inputs_route_to_tier_1_without_raising():
    assert route_ticket(None, None) == "tier-1-support"
    assert route_ticket("low", None) == "tier-1-support"
    assert route_ticket(None, "bug") == "tier-1-support"


def test_severity_and_category_are_case_sensitive():
    assert route_ticket("HIGH", "bug") == "tier-1-support"
    assert route_ticket("low", "Billing") == "tier-1-support"
