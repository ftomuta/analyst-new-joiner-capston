import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from meridian.ticket_classifier import classify_severity, classify_category
from meridian.ticket_router import route_ticket
from meridian.ticket_store import save_ticket, get_ticket


def submit(text: str) -> str:
    severity, confidence = classify_severity(text)
    category = classify_category(text)
    team = route_ticket(severity, category)
    return save_ticket(
        {
            "text": text,
            "severity": severity,
            "confidence": confidence,
            "category": category,
            "team": team,
        }
    )

PAGE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Meridian Tickets</title>
<style>
  body { font-family: system-ui, sans-serif; max-width: 640px; margin: 40px auto; padding: 0 16px; }
  textarea { width: 100%; height: 100px; padding: 8px; font: inherit; box-sizing: border-box; }
  button { margin-top: 8px; padding: 8px 16px; font: inherit; cursor: pointer; }
  .card { border: 1px solid #ccc; border-radius: 6px; padding: 12px 16px; margin-top: 16px; }
  .row { display: flex; justify-content: space-between; padding: 4px 0; }
  .high { color: #b00020; font-weight: 600; }
  .medium { color: #b26a00; font-weight: 600; }
  .low { color: #2e7d32; font-weight: 600; }
  .muted { color: #777; font-size: 0.85em; }
  .ticket-text { margin: 8px 0; padding: 8px; background: #f5f5f5; border-radius: 4px; white-space: pre-wrap; overflow-wrap: anywhere; }
</style>
</head>
<body>
<h1>Submit a ticket</h1>
<textarea id="text" placeholder="Describe the issue..."></textarea>
<button id="go">Submit</button>
<div id="out"></div>
<script>
const out = document.getElementById("out");
const btn = document.getElementById("go");
btn.onclick = async () => {
  const text = document.getElementById("text").value.trim();
  if (!text) return;
  btn.disabled = true;
  btn.textContent = "Classifying...";
  try {
    const res = await fetch("/submit", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({text}),
    });
    const t = await res.json();
    if (!res.ok) throw new Error(t.error || "Request failed");
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <div class="muted">${t.id}</div>
      <div class="ticket-text"></div>
      <div class="row"><span>Severity</span><span class="${t.severity}">${t.severity} (${(t.confidence * 100).toFixed(0)}% confident)</span></div>
      <div class="row"><span>Category</span><span>${t.category}</span></div>
      <div class="row"><span>Routed to</span><strong>${t.team}</strong></div>`;
    card.querySelector(".ticket-text").textContent = t.text;
    out.prepend(card);
  } catch (e) {
    alert(e.message);
  } finally {
    btn.disabled = false;
    btn.textContent = "Submit";
  }
};
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, content_type):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/":
            self._send(200, PAGE, "text/html; charset=utf-8")
        else:
            self._send(404, "Not found", "text/plain")

    def do_POST(self):
        if self.path != "/submit":
            self._send(404, "Not found", "text/plain")
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            text = json.loads(self.rfile.read(length))["text"]
            ticket_id = submit(text)
            ticket = {"id": ticket_id, **get_ticket(ticket_id)}
            self._send(200, json.dumps(ticket), "application/json")
        except Exception as e:
            self._send(500, json.dumps({"error": str(e)}), "application/json")


if __name__ == "__main__":
    print("Open http://localhost:8000")
    HTTPServer(("localhost", 8000), Handler).serve_forever()
