import uuid

#in-memory ticket storage, ticket_id -> ticket dict
_tickets = {}


class TicketNotFoundError(Exception):
    pass


def save_ticket(ticket: dict) -> str:
    """Save a ticket dict and return its generated ID."""
    ticket_id = str(uuid.uuid4())
    _tickets[ticket_id] = ticket
    return ticket_id


def get_ticket(ticket_id: str) -> dict:
    """Retrieve a ticket by ID. Raises TicketNotFoundError if not found."""
    if ticket_id not in _tickets:
        raise TicketNotFoundError(ticket_id)
    return _tickets[ticket_id]