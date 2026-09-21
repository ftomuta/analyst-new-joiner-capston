# Write your tests here before implementing
import pytest
 
from meridian.ticket_store import save_ticket, get_ticket, TicketNotFoundError
 
 
#  1: save_ticket returns a generated ID
def test_save_ticket_returns_an_id():
    ticket_id = save_ticket({"title": "Cannot log in", "severity": "medium"})
    assert isinstance(ticket_id, str)
 
 
#  2: get_ticket returns the same dict that was saved
def test_get_ticket_returns_saved_dict():
    ticket = {"title": "Cannot log in", "severity": "medium"}
    ticket_id = save_ticket(ticket)
    assert get_ticket(ticket_id) == ticket
 
 
# 3: unknown ID raises TicketNotFoundError
def test_get_ticket_not_found():
    with pytest.raises(TicketNotFoundError):
        get_ticket("non_existent_ticket")
 
 
# 4: two saves get different IDs
def test_two_tickets_get_different_ids():
    first_id = save_ticket({"title": "Cannot log in"})
    second_id = save_ticket({"title": "Cannot log in"})
    assert first_id != second_id
 