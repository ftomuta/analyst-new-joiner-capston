# Write your tests here before implementing
from scaffold.meridian.ticket_router import route_ticket
 
 
def test_route_ticket_high_severity():
    result = route_ticket("high", "billing")
    assert result == "tier-2-escalation"
 
def test_route_ticket_billing_category():
    result = route_ticket("low", "billing")
    assert result == "billing-team"
 
def test_route_ticket_default_category():
    result = route_ticket("low", "other")
    assert result == "tier-1-support"
 
def test_unknown_severity():
    result = route_ticket("medium", "access_request")
    assert result == "tier-1-support"