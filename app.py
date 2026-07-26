"""
PantryChef — track your food, avoid waste, cook from what you have.

Run locally:
    pip install -r requirements.txt
    python app.py
    open http://localhost:5000
"""
import os
from datetime import datetime, date

from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

from models import db, Item, CATEGORIES, ACTIVE, USED, WASTED
from recipes import suggest

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")

    # SQLite by default so it runs with zero setup; Postgres in production via env.
    db_url = os.getenv("DATABASE_URL", "sqlite:///pantrychef.db")
    # SQLAlchemy wants "postgresql://", some providers give "postgres://"
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    # ---------------- routes ----------------

    @app.route("/")
    def dashboard():
        items = (Item.query.filter_by(status=ACTIVE)
                 .order_by(Item.expiry_date.is_(None), Item.expiry_date).all())
        buckets = {"expired": [], "soon": [], "ok": [], "none": []}
        for it in items:
            buckets[it.expiry_state].append(it)
        return render_template("dashboard.html", buckets=buckets,
                               total=len(items), today=date.today())

    @app.route("/add", methods=["GET", "POST"])
    def add_item():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            if not name:
                flash("Please give the item a name.", "error")
                return redirect(url_for("add_item"))

            expiry = request.form.get("expiry_date") or None
            expiry_date = (datetime.strptime(expiry, "%Y-%m-%d").date()
                           if expiry else None)
            try:
                qty = float(request.form.get("quantity") or 1)
            except ValueError:
                qty = 1

            db.session.add(Item(
                name=name,
                quantity=qty,
                unit=request.form.get("unit") or "pcs",
                category=request.form.get("category") or "Other",
                expiry_date=expiry_date,
            ))
            db.session.commit()
            flash(f"Added “{name}” to your pantry.", "ok")
            return redirect(url_for("dashboard"))

        return render_template("add_item.html", categories=CATEGORIES, today=date.today())

    @app.route("/item/<int:item_id>/<action>", methods=["POST"])
    def resolve_item(item_id, action):
        it = Item.query.get_or_404(item_id)
        if action == "used":
            it.status, it.resolved_at = USED, datetime.utcnow()
            flash(f"Nice — marked “{it.name}” as used. \U0001f389", "ok")
        elif action == "wasted":
            it.status, it.resolved_at = WASTED, datetime.utcnow()
            flash(f"Logged “{it.name}” as wasted. We'll help you catch it sooner next time.", "ok")
        elif action == "delete":
            db.session.delete(it)
            flash("Item removed.", "ok")
        else:
            flash("Unknown action.", "error")
            return redirect(url_for("dashboard"))
        db.session.commit()
        return redirect(request.referrer or url_for("dashboard"))

    @app.route("/recipes")
    def recipes_page():
        names = [it.normalized_name() for it in Item.query.filter_by(status=ACTIVE)]
        can_make, almost = suggest(names)
        return render_template("recipes.html", can_make=can_make,
                               almost=almost, have_items=bool(names))

    @app.route("/stats")
    def stats():
        active = Item.query.filter_by(status=ACTIVE).count()
        used = Item.query.filter_by(status=USED).count()
        wasted = Item.query.filter_by(status=WASTED).count()
        resolved = used + wasted
        waste_rate = round(100 * wasted / resolved) if resolved else 0
        expiring = Item.query.filter_by(status=ACTIVE).all()
        soon = sum(1 for it in expiring if it.expiry_state in ("soon", "expired"))
        return render_template("stats.html", active=active, used=used,
                               wasted=wasted, waste_rate=waste_rate, soon=soon)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
