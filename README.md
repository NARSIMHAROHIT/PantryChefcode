# 🥕 PantryChef

Track the food in your kitchen, get warned **before** it expires, and see what you can
cook with what you already have. A small web app that helps every household waste less
food and save money.

> A learning + portfolio project: a real web app with a database and a background worker,
> designed to be deployed on an AWS EC2 server. Great to share on GitHub and LinkedIn.

## What it does

- **Pantry dashboard** — all your food in one place, colour-coded by expiry
  (🔴 expired, 🟠 use within 3 days, 🟢 fresh).
- **Add items** — name, quantity, category, and an optional expiry date.
- **Cook page** — suggests recipes you can make right now from your ingredients, plus
  ones you're only 1–2 items away from.
- **Used / Wasted tracking** — mark what you finish; the **Stats** page shows your waste
  rate so you can watch it drop.
- **Daily alerts** — a background worker (`alerts.py`) emails you a digest of what's about
  to go bad (email optional — it prints the digest if email isn't configured).

## Tech stack

Python · Flask · SQLAlchemy · SQLite (local) / PostgreSQL (production) · gunicorn + nginx on EC2.
No external APIs — the recipe engine is self-contained, so it runs anywhere.

## Project layout

```
pantrychef/
├── app.py            # Flask app + routes
├── models.py         # database model (Item)
├── recipes.py        # recipe data + "what can I cook?" matching engine
├── alerts.py         # background worker: expiry digest (email optional)
├── templates/        # HTML pages
├── static/style.css  # styling
├── requirements.txt
├── .env.example      # copy to .env
└── deploy/
    ├── DEPLOY-EC2.md          # full step-by-step AWS EC2 + PostgreSQL guide
    ├── pantrychef.service     # systemd unit for gunicorn
    ├── nginx-pantrychef.conf  # nginx reverse proxy config
    ├── pantrychef-alerts.service + .timer  # daily alert scheduler
```

## Run it locally (2 minutes, zero AWS needed)

```bash
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                  # optional; SQLite works out of the box
python app.py
```

Open **http://localhost:5000**. Add a few items (give some a near expiry date), then
check the **Cook** and **Stats** pages. Run the alert worker any time with:

```bash
python alerts.py
```

## Deploy it on AWS EC2

Full walkthrough — launch the instance, install PostgreSQL, run under gunicorn + nginx,
and schedule the daily alert worker — is in **[deploy/DEPLOY-EC2.md](deploy/DEPLOY-EC2.md)**.

## How the recipe matcher works

Each recipe in `recipes.py` lists its ingredients. The matcher compares them against your
pantry item names (forgiving substring match, so "cherry tomatoes" matches "tomato").
A recipe with **zero** missing ingredients shows under *Ready to cook*; missing **1–2**
shows under *Almost there* with the shopping gap listed. It's simple, transparent, and
easy to extend — just add more recipes to the list.

## Ideas to extend it (your next commits)

- User accounts so multiple people have their own pantry.
- Barcode scanning to add items faster.
- Smarter recipes (quantities, dietary filters) or pull from a recipe API.
- A "shopping list" built from the *Almost there* recipes.

## Note

Single-user by default (no login) — perfect for a personal tool or a demo. Add
authentication before putting real multi-user data on the public internet.
