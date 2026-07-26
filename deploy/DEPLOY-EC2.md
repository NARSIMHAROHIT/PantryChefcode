# Deploying PantryChef on an EC2 server with PostgreSQL

This is the full production setup: an **EC2** Ubuntu server running the app with
**gunicorn** behind **nginx**, a **PostgreSQL** database, and a **systemd timer**
that runs the expiry-alert worker daily. Follow it top to bottom.

Architecture:

```
Internet ──▶ nginx (port 80) ──▶ gunicorn (127.0.0.1:8000) ──▶ Flask app
                                                                  │
                                                            PostgreSQL (localhost:5432)
   systemd timer ──daily──▶ alerts.py ──▶ email digest (optional, via SES/SMTP)
```

> Costs money: a `t3.micro` may be free-tier eligible; otherwise it's a few dollars a
> month. Stop or terminate the instance when you're done to avoid charges.

---

## 1. Launch the EC2 instance

1. AWS Console → **EC2** → **Launch instance**.
2. Name: `pantrychef`. AMI: **Ubuntu Server 24.04 LTS**. Type: **t3.micro**.
3. **Key pair**: create one, download the `.pem` — you need it to SSH in.
4. **Network / security group** — allow inbound:
   - **SSH (22)** from *My IP*
   - **HTTP (80)** from *Anywhere (0.0.0.0/0)*
   (Add **HTTPS (443)** too if you'll set up a domain + TLS later.)
5. Launch. Note the instance's **Public IPv4 address** (call it `SERVER_IP`).

SSH in from your terminal:

```bash
chmod 400 pantrychef.pem
ssh -i pantrychef.pem ubuntu@SERVER_IP
```

## 2. Install system packages

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-venv python3-pip nginx postgresql postgresql-contrib git
```

## 3. Set up PostgreSQL

```bash
sudo -u postgres psql <<'SQL'
CREATE DATABASE pantrychef;
CREATE USER pantry WITH PASSWORD 'CHANGE_THIS_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE pantrychef TO pantry;
ALTER DATABASE pantrychef OWNER TO pantry;
SQL
```

Your database URL will be:
`postgresql://pantry:CHANGE_THIS_PASSWORD@localhost:5432/pantrychef`

## 4. Get the code onto the server

Push this project to GitHub first (see the repo's git steps), then:

```bash
cd /home/ubuntu
git clone https://github.com/<your-username>/pantrychef.git
cd pantrychef
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 5. Configure environment

```bash
cp .env.example .env
nano .env
```

Set at least:

```
SECRET_KEY=<paste a long random string>
DATABASE_URL=postgresql://pantry:CHANGE_THIS_PASSWORD@localhost:5432/pantrychef
```

Create the tables (the app does this on startup, but do it once explicitly):

```bash
python3 -c "from app import app, db; app.app_context().push(); db.create_all(); print('tables ready')"
```

## 6. Run under gunicorn as a systemd service

Copy the service file and start it:

```bash
sudo cp deploy/pantrychef.service /etc/systemd/system/pantrychef.service
sudo systemctl daemon-reload
sudo systemctl enable --now pantrychef
sudo systemctl status pantrychef        # should say "active (running)"
```

(If you edit code later: `git pull` then `sudo systemctl restart pantrychef`.)

## 7. Put nginx in front

```bash
sudo cp deploy/nginx-pantrychef.conf /etc/nginx/sites-available/pantrychef
sudo ln -s /etc/nginx/sites-available/pantrychef /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx
```

Now open **http://SERVER_IP/** in a browser — PantryChef is live. 🎉

## 8. Daily expiry alerts (optional but cool)

Install the worker service + timer so `alerts.py` runs once a day:

```bash
sudo cp deploy/pantrychef-alerts.service /etc/systemd/system/
sudo cp deploy/pantrychef-alerts.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now pantrychef-alerts.timer
systemctl list-timers | grep pantrychef      # confirm it's scheduled
```

Without SMTP configured it logs the digest (view with `journalctl -u pantrychef-alerts`).
To actually email yourself, set the `SMTP_*` and `ALERT_TO_EMAIL` values in `.env`:

- **Gmail:** `SMTP_HOST=smtp.gmail.com`, `SMTP_PORT=587`, `SMTP_USER=you@gmail.com`,
  `SMTP_PASSWORD=<an App Password>` (not your login password).
- **Amazon SES:** verify a sender identity, create SMTP credentials in the SES console,
  and use the SES SMTP endpoint for your region as `SMTP_HOST`.

## 9. (Optional) Domain + HTTPS

Point a domain's A record at `SERVER_IP`, open port 443 in the security group, then:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

---

## Everyday operations

| Task | Command |
|---|---|
| View app logs | `journalctl -u pantrychef -f` |
| Restart after code change | `git pull && sudo systemctl restart pantrychef` |
| Check alert timer | `systemctl list-timers \| grep pantrychef` |
| Back up the database | `pg_dump -U pantry pantrychef > backup.sql` |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| 502 Bad Gateway | gunicorn not running | `sudo systemctl status pantrychef`, check `journalctl -u pantrychef` |
| Can't reach site at all | Security group | Ensure HTTP(80) is open to 0.0.0.0/0 |
| DB connection refused | Wrong `DATABASE_URL` / Postgres down | `sudo systemctl status postgresql`; recheck user/password |
| Changes not showing | Service not restarted | `sudo systemctl restart pantrychef` |
