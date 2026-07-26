"""
PantryChef — track your food, avoid waste, cook from what you have.

Run locally:
    pip install -r requirements.txt
    python app.py
    open http://localhost:5000
"""
import os
import re
import json
from datetime import datetime, date

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from models import db, Item, UserRecipe, CATEGORIES, ACTIVE, USED, WASTED
from recipes import suggest
import recipes_data as rd

load_dotenv()

RESERVED_SLUGS = {"new"}


def slugify(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")
    return s or "recipe"


def all_recipes():
    """Built-in recipes + user-added recipes, as a single uniform list of dicts."""
    extra = [u.to_dict() for u in
             UserRecipe.query.order_by(UserRecipe.created_at.desc()).all()]
    return list(rd.RECIPES) + extra


def filter_recipes(recipes, category, diet, spice):
    out = recipes
    if category:
        out = [r for r in out if r["category"] == category]
    if diet:
        out = [r for r in out if r["diet"] == diet]
    if spice:
        out = [r for r in out if r["spice"] == spice]
    return out


def find_recipe(rid):
    r = rd.by_id(rid)
    if r:
        return r
    u = UserRecipe.query.filter_by(slug=rid).first()
    return u.to_dict() if u else None


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

    # Lets templates show a real photo if the file exists, else a placeholder.
    def has_image(rel_path):
        return os.path.isfile(os.path.join(app.static_folder, "images", rel_path))

    @app.context_processor
    def inject_helpers():
        return {"has_image": has_image, "DIET_LABELS": rd.DIET_LABELS,
                "SPICE_LABELS": rd.SPICE_LABELS}

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

    @app.route("/cook")
    def cook():
        # Filters from the query string (all optional)
        category = request.args.get("category") or None
        diet = request.args.get("diet") or None
        spice = request.args.get("spice") or None
        if category not in rd.CATEGORY_ORDER:
            category = None

        recipes = filter_recipes(all_recipes(), category, diet, spice)
        groups = rd.grouped_by_category(recipes)

        # "Cook from your pantry" section
        names = [it.normalized_name() for it in Item.query.filter_by(status=ACTIVE)]
        can_make, almost = suggest(names)

        return render_template(
            "cook.html", groups=groups, categories=rd.CATEGORY_ORDER,
            active={"category": category, "diet": diet, "spice": spice},
            total=len(recipes), can_make=can_make, almost=almost,
            have_items=bool(names))

    @app.route("/recipe/new", methods=["GET", "POST"])
    def new_recipe():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            if not name:
                flash("Please give your recipe a name.", "error")
                return redirect(url_for("new_recipe"))

            # Build a unique slug (used in the URL + image folder name)
            base = slugify(name)
            reserved = RESERVED_SLUGS | {r["id"] for r in rd.RECIPES}
            slug, n = base, 2
            while slug in reserved or UserRecipe.query.filter_by(slug=slug).first():
                slug, n = f"{base}-{n}", n + 1

            img_dir = os.path.join(app.static_folder, "images", slug)
            os.makedirs(img_dir, exist_ok=True)

            def save_upload(fs, target_name):
                """Save an uploaded image, return the stored filename (or '')."""
                if not fs or not fs.filename:
                    return ""
                ext = os.path.splitext(secure_filename(fs.filename))[1].lower() or ".jpg"
                fname = f"{target_name}{ext}"
                fs.save(os.path.join(img_dir, fname))
                return fname

            hero_name = save_upload(request.files.get("hero"), "hero")

            texts = request.form.getlist("step_text")
            minutes = request.form.getlist("step_minutes")
            files = request.files.getlist("step_image")
            steps = []
            for i, t in enumerate(texts):
                t = t.strip()
                if not t:
                    continue
                try:
                    mins = float(minutes[i]) if i < len(minutes) and minutes[i] else 0
                except ValueError:
                    mins = 0
                n_step = len(steps) + 1
                fs = files[i] if i < len(files) else None
                img_name = save_upload(fs, f"step{n_step}") or f"step{n_step}.jpg"
                steps.append({"text": t, "wait_sec": int(mins * 60), "image": img_name})

            ingredients = [x.strip() for x in
                           re.split(r"[,\n]", request.form.get("ingredients", "")) if x.strip()]
            try:
                serves = int(request.form.get("serves") or 2)
            except ValueError:
                serves = 2

            db.session.add(UserRecipe(
                slug=slug, name=name,
                category=request.form.get("category") or "Tiffins",
                diet=request.form.get("diet") or "veg",
                spice=request.form.get("spice") or "mild",
                time=request.form.get("time") or "",
                serves=serves,
                spice_tip=request.form.get("spice_tip") or "",
                hero=hero_name,
                ingredients_json=json.dumps(ingredients),
                steps_json=json.dumps(steps),
            ))
            db.session.commit()
            flash(f"Added your recipe “{name}”! 🎉", "ok")
            return redirect(url_for("recipe", recipe_id=slug))

        return render_template("add_recipe.html", categories=rd.CATEGORY_ORDER)

    @app.route("/recipe/<recipe_id>")
    def recipe(recipe_id):
        r = find_recipe(recipe_id)
        if not r:
            flash("Recipe not found.", "error")
            return redirect(url_for("cook"))
        # Which of this recipe's ingredients you already have
        have = {it.normalized_name() for it in Item.query.filter_by(status=ACTIVE)}

        def owned(ing):
            i = ing.lower()
            return any(i in h or h in i for h in have)

        return render_template("recipe.html", r=r, owned=owned)

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
