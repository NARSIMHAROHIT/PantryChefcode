"""Database models for PantryChef."""
from datetime import datetime, date

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Item lifecycle status
ACTIVE = "active"   # still in the pantry
USED = "used"       # cooked/eaten (a win)
WASTED = "wasted"   # thrown away (what we want to reduce)

CATEGORIES = [
    "Produce", "Dairy", "Meat & Fish", "Grains & Pasta",
    "Canned & Jars", "Spices", "Frozen", "Snacks", "Drinks", "Other",
]


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Float, default=1)
    unit = db.Column(db.String(30), default="pcs")
    category = db.Column(db.String(40), default="Other")

    expiry_date = db.Column(db.Date)  # optional
    added_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    status = db.Column(db.String(10), default=ACTIVE, nullable=False)
    resolved_at = db.Column(db.DateTime)  # when it was used/wasted

    # ---- convenience properties used by the templates ----
    @property
    def days_to_expiry(self):
        if not self.expiry_date:
            return None
        return (self.expiry_date - date.today()).days

    @property
    def expiry_state(self):
        """One of: none, expired, soon, ok — drives the colour coding."""
        d = self.days_to_expiry
        if d is None:
            return "none"
        if d < 0:
            return "expired"
        if d <= 3:
            return "soon"
        return "ok"

    def normalized_name(self):
        return self.name.strip().lower()
