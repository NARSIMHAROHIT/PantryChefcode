"""
Background worker: find items expiring soon and send a digest email.

Run it once (e.g. daily) from cron or a systemd timer:
    python alerts.py

Email is OPTIONAL. If SMTP_* env vars are not set, it just prints the digest to
the console — so the app is fully useful without email configured. On EC2 you can
wire this to Amazon SES or a Gmail app password (see deploy/DEPLOY-EC2.md).
"""
import os
import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv

from app import app  # reuse the Flask app + db config
from models import Item, ACTIVE

load_dotenv()

WINDOW_DAYS = int(os.getenv("ALERT_WINDOW_DAYS", 3))


def build_digest():
    """Return (subject, body) for items expired or expiring within the window."""
    with app.app_context():
        items = Item.query.filter_by(status=ACTIVE).all()
        flagged = [it for it in items
                   if it.days_to_expiry is not None and it.days_to_expiry <= WINDOW_DAYS]

    if not flagged:
        return None, None

    flagged.sort(key=lambda it: it.days_to_expiry)
    lines = ["Here's what needs attention in your pantry:\n"]
    for it in flagged:
        d = it.days_to_expiry
        when = "EXPIRED" if d < 0 else ("expires today" if d == 0 else f"expires in {d} day(s)")
        lines.append(f"  • {it.name} ({it.quantity:g} {it.unit}) — {when}")
    lines.append("\nCook the soonest ones first. Open PantryChef to see recipe ideas.")
    return f"PantryChef: {len(flagged)} item(s) to use soon", "\n".join(lines)


def send_email(subject, body):
    host = os.getenv("SMTP_HOST")
    to_addr = os.getenv("ALERT_TO_EMAIL")
    if not host or not to_addr:
        print("[alerts] SMTP not configured — printing digest instead:\n")
        print(subject)
        print(body)
        return

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = os.getenv("SMTP_FROM", os.getenv("SMTP_USER", "pantrychef@localhost"))
    msg["To"] = to_addr

    with smtplib.SMTP(host, int(os.getenv("SMTP_PORT", 587))) as server:
        server.starttls()
        if os.getenv("SMTP_USER"):
            server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD", ""))
        server.send_message(msg)
    print(f"[alerts] Sent digest to {to_addr}")


if __name__ == "__main__":
    subject, body = build_digest()
    if subject:
        send_email(subject, body)
    else:
        print("[alerts] Nothing expiring soon. No email sent.")
