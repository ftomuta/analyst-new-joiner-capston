import io

from meridian.cli import MeridianShell


def run(*commands):
    out = io.StringIO()
    shell = MeridianShell(stdout=out)
    for command in commands:
        shell.onecmd(command)
    return out.getvalue()


def test_create_classifies_routes_and_stores_ticket():
    output = run("create Production database is down")

    assert "severity: high" in output
    assert "category: bug" in output
    assert "team: tier-2-escalation" in output


def test_create_then_get_returns_the_ticket():
    out = io.StringIO()
    shell = MeridianShell(stdout=out)
    shell.onecmd("create Payment failed with an error on my invoice")
    ticket_id = shell.ticket_ids[0]

    shell.onecmd(f"get {ticket_id}")

    assert "billing-team" in out.getvalue()


def test_create_without_text_reports_usage_and_stores_nothing():
    out = io.StringIO()
    shell = MeridianShell(stdout=out)

    shell.onecmd("create")

    assert "Usage" in out.getvalue()
    assert shell.ticket_ids == []


def test_get_unknown_id_reports_not_found_without_raising():
    assert "not found" in run("get nope").lower()


def test_list_shows_tickets_created_this_session():
    output = run("create Please reset my password", "create Production is down", "list")

    assert "Please reset my password" in output
    assert "Production is down" in output


def test_list_with_no_tickets():
    assert "No tickets" in run("list")


def test_quit_ends_the_session():
    shell = MeridianShell(stdout=io.StringIO())

    assert shell.onecmd("quit") is True


def test_create_shows_confidence():
    assert "confidence: 0.80" in run("create Production database is down")


def test_low_confidence_ticket_is_flagged_and_not_routed():
    out = io.StringIO()
    shell = MeridianShell(stdout=out)

    shell.onecmd("create The report looks a bit off")

    output = out.getvalue()
    assert "needs human review" in output.lower()
    assert "team: unassigned" in output
    assert "tier-1-support" not in output


def test_low_confidence_ticket_is_still_stored_with_review_flag():
    out = io.StringIO()
    shell = MeridianShell(stdout=out)
    shell.onecmd("create The report looks a bit off")

    ticket_id = shell.ticket_ids[0]
    shell.onecmd(f"get {ticket_id}")

    assert "needs_review: True" in out.getvalue()
    assert "team: None" in out.getvalue()


def test_confident_ticket_is_not_flagged():
    output = run("create Production database is down")

    assert "needs human review" not in output.lower()


def test_list_marks_tickets_needing_review():
    out = io.StringIO()
    shell = MeridianShell(stdout=out)
    shell.onecmd("create The report looks a bit off")
    out.truncate(0)
    out.seek(0)

    shell.onecmd("list")

    assert "unassigned" in out.getvalue()
    assert "None" not in out.getvalue()
