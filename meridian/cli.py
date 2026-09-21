import cmd

from meridian.ticket_classifier import classify_category, classify_severity
from meridian.ticket_router import route_ticket
from meridian.ticket_store import TicketNotFoundError, get_ticket, save_ticket


class MeridianShell(cmd.Cmd):
    intro = "Meridian ticket triage. Type 'help' for commands, 'quit' to exit."
    prompt = "meridian> "

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ticket_ids: list[str] = []

    def do_create(self, arg):
        """create <ticket text> - classify, route and store a new ticket."""
        text = arg.strip()
        if not text:
            self.stdout.write("Usage: create <ticket text>\n")
            return
        severity = classify_severity(text)
        category = classify_category(text)
        team = route_ticket(severity, category)
        ticket_id = save_ticket(
            {"text": text, "severity": severity, "category": category, "team": team}
        )
        self.ticket_ids.append(ticket_id)
        self.stdout.write(
            f"Created ticket {ticket_id}\n"
            f"  severity: {severity}\n  category: {category}\n  team: {team}\n"
        )

    def do_get(self, arg):
        """get <ticket id> - show a stored ticket."""
        ticket_id = arg.strip()
        try:
            ticket = get_ticket(ticket_id)
        except TicketNotFoundError:
            self.stdout.write(f"Ticket not found: {ticket_id}\n")
            return
        for key, value in ticket.items():
            self.stdout.write(f"  {key}: {value}\n")

    def do_list(self, arg):
        """list - show tickets created in this session."""
        if not self.ticket_ids:
            self.stdout.write("No tickets created yet.\n")
            return
        for ticket_id in self.ticket_ids:
            t = get_ticket(ticket_id)
            self.stdout.write(
                f"{ticket_id}  [{t['severity']}] {t['team']}  {t['text']}\n"
            )

    def do_quit(self, arg):
        """quit - exit the shell."""
        return True

    do_exit = do_quit
    do_EOF = do_quit

    def emptyline(self):
        pass


if __name__ == "__main__":
    MeridianShell().cmdloop()
