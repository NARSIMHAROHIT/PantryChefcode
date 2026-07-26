"""Database models for PantryChef."""
import json
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


class UserRecipe(db.Model):
    """A recipe added by the user through the in-app form.

    Ingredients and steps are stored as JSON text so a recipe fits in one row.
    to_dict() returns the exact same shape as a built-in recipe (recipes_data.py),
    so the Cook and recipe templates render user recipes with no changes.
    """
    __tablename__ = "user_recipes"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False)  # used in the URL + image folder
    name = db.Column(db.String(160), nullable=False)
    category = db.Column(db.String(40), default="Tiffins")
    diet = db.Column(db.String(10), default="veg")
    spice = db.Column(db.String(10), default="mild")
    time = db.Column(db.String(40), default="")
    serves = db.Column(db.Integer, default=2)
    spice_tip = db.Column(db.Text, default="")
    hero = db.Column(db.String(60), default="")          # hero image filename, if uploaded
    ingredients_json = db.Column(db.Text, default="[]")
    steps_json = db.Column(db.Text, default="[]")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.slug,
            "name": self.name,
            "category": self.category,
            "diet": self.diet,
            "spice": self.spice,
            "time": self.time or "—",
            "serves": self.serves,
            "spice_tip": self.spice_tip or "Season to your taste.",
            "hero": self.hero or "hero.jpg",
            "ingredients": json.loads(self.ingredients_json or "[]"),
            "steps": json.loads(self.steps_json or "[]"),
            "user_added": True,
        }
