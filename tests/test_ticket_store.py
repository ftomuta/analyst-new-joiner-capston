# Write your tests here before implementing
import pytest

from meridian.ticket_store import (
    save_ticket,
    get_ticket,
    TicketNotFoundError,
)


def test_save_ticket_returns_string_id():
    ticket = {"title": "Login issue", "severity": "low"}

    ticket_id = save_ticket(ticket)

    assert isinstance(ticket_id, str)
    assert ticket_id != ""


def test_saved_ticket_can_be_retrieved():
    ticket = {
        "title": "Database unavailable",
        "severity": "high",
    }

    ticket_id = save_ticket(ticket)

    assert get_ticket(ticket_id) == ticket


def test_retrieving_unknown_ticket_raises_error():
    with pytest.raises(TicketNotFoundError):
        get_ticket("does-not-exist")


def test_saving_two_tickets_generates_different_ids():
    ticket_1 = {"title": "Issue 1"}
    ticket_2 = {"title": "Issue 2"}

    id_1 = save_ticket(ticket_1)
    id_2 = save_ticket(ticket_2)

    assert id_1 != id_2


def test_multiple_saved_tickets_can_be_retrieved_independently():
    ticket_1 = {
        "title": "Password reset",
        "severity": "low",
    }

    ticket_2 = {
        "title": "Production outage",
        "severity": "high",
    }

    id_1 = save_ticket(ticket_1)
    id_2 = save_ticket(ticket_2)

    assert get_ticket(id_1) == ticket_1
    assert get_ticket(id_2) == ticket_2