import copy
import uuid

_tickets: dict[str, dict] = {}


class TicketNotFoundError(Exception):
    pass


def save_ticket(ticket: dict) -> str:
    """Save a ticket dict and return its generated ID."""
    ticket_id = str(uuid.uuid4())
    _tickets[ticket_id] = copy.deepcopy(ticket)
    return ticket_id


def get_ticket(ticket_id: str) -> dict:
    """Retrieve a ticket by ID. Raises TicketNotFoundError if not found."""
    try:
        return copy.deepcopy(_tickets[ticket_id])
    except (KeyError, TypeError):
        raise TicketNotFoundError(ticket_id) from None
