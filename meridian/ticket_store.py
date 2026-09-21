class TicketNotFoundError(Exception):
    pass


def save_ticket(ticket: dict) -> str:
    """Save a ticket dict and return its generated ID."""
    raise NotImplementedError


def get_ticket(ticket_id: str) -> dict:
    """Retrieve a ticket by ID. Raises TicketNotFoundError if not found."""
    raise NotImplementedError
