def route_ticket(severity: str, category: str) -> str:
    """
    Route a ticket to the appropriate support team.
    Returns: team name string
    Routing rules:
      - severity "high": always "tier-2-escalation"
      - category "billing": "billing-team"
      - all others: "tier-1-support"
    """
    if severity == "high":
        return "tier-2-escalation"
    if category == "billing":
        return "billing-team"
    return "tier-1-support"
