# DevOps Project

A complete DevOps pipeline using Python/Flask, Ansible and GitHub Actions with blue-green deployment on localhost.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Web framework | Python 3.10 + Flask |
| Testing | pytest |
| Linting | flake8 |
| Version control | Git + GitHub |
| CI pipeline | GitHub Actions |
| IaC & automation | Ansible |
| Deployment strategy | Blue-green deployment |
| Process management | systemd |
| Monitoring | Python script + cron |

---

## Project Structure
```
devops-project/
├── app/
│   ├── app.py
│   ├── static/style.css
│   └── templates/
│       ├── index.html
│       └── result.html
├── tests/
│   └── test_app.py
├── ansible/
│   ├── inventory.ini
│   ├── site.yml
│   ├── deploy.yml
│   ├── rollback.yml
│   ├── active_slot.yml
│   ├── templates/app.service.j2
│   └── roles/
│       ├── setup/tasks/main.yml
│       ├── deploy/tasks/main.yml
│       └── monitor/
│           ├── tasks/main.yml
│           └── files/health_check.py
├── .github/workflows/ci.yml
├── requirements.txt
└── .flake8
```

---

## CI/CD Workflow Diagram

<img src="images/img.png" width="600">
---


## Step 1 — Clone the repository

```bash
git clone https://github.com/gorozia0709/devops-project.git
cd devops-project
```

---

## Step 2 — Install dependencies locally

```bash
pip install -r requirements.txt
```

---

## Step 3 — Run tests

```bash
python3 -m pytest tests/ -v
```

All 4 tests should pass.

<img src="images/img_11.png" width="1200">
---

## Step 4 — Run the app locally

```bash
SLOT=blue PORT=5000 python3 app/app.py
```

Open `http://localhost:5000` in your browser.

---

## Step 5 — Provision the environment (single command)

This installs dependencies, creates directories, deploys the health check script and schedules the cron job:

```bash
ansible-playbook -i ansible/inventory.ini ansible/site.yml --ask-become-pass
```

What it does:
- Installs Python and pip via apt
- Creates `/opt/devops-app/` and `/var/log/devops-app/`
- Copies `requirements.txt` and installs Flask and pytest
- Deploys `health_check.py` to `/opt/devops-app/`
- Schedules a cron job to run the health check every 5 minutes

<img src="images/img_1.png" width="1200">
---

## Step 6 — CI Pipeline

GitHub Actions runs automatically on every push to `main` or `dev`, and on every Pull Request targeting `main`.

Pipeline steps:
1. Checkout code
2. Set up Python 3.10
3. Install dependencies from `requirements.txt`
4. Run `flake8` linter on `app/` and `tests/`
5. Run `pytest` unit tests

<img src="images/img_2.png" width="600">

---

## Step 7 — Blue-Green Deployment

```bash
ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --ask-become-pass
```

How it works:
1. Reads `active_slot.yml` to find the current active slot
2. Deploys new code to the idle slot
3. Starts the idle slot as a systemd service
4. Runs a health check against the `/health` endpoint
5. If healthy - switches active slot, stops old slot
6. If unhealthy - aborts, old slot keeps serving traffic

| Slot | Port | Badge color |
|------|------|-------------|
| blue | 5000 | Blue |
| green | 5001 | Green |

Every deployment flips between slots with zero downtime.

First deploy to green slot:

<img src="images/img_4.png" width="1200">

Go to http://localhost:5001/

<img src="images/img_3.png" width="600">

Now after some change is done and pushed to repository we get following results:

<img src="images/img_5.png" width="1200">

Go to http://localhost:5000/

<img src="images/img_6.png" width="600">

---

## Step 8 — Rollback

To instantly revert to the previous slot:

```bash
ansible-playbook -i ansible/inventory.ini ansible/rollback.yml --ask-become-pass
```

This starts the previously stopped slot, health checks it, switches traffic back and stops the broken slot.

<img src="images/img_7.png" width="1200">

Blue slot is now down when you go to http://localhost:5000/:

<img src="images/img_8.png" width="600">

Green slot is now active when you go to http://localhost:5001/:

<img src="images/img_9.png" width="600">

---

## Step 9 — Monitoring & Health Check

The health check script polls both slots and logs results. It is scheduled via cron every 5 minutes by Ansible.

Run manually:

```bash
python3 /opt/devops-app/health_check.py
```

![images/img_10.png](images/img_10.png)

View the log:

```bash
cat /var/log/devops-app/health.log
```

Example output:

![images/img_12.png](images/img_12.png)


## Branch Strategy & Merging

All development happens on `dev`. Once CI passes, changes are merged to `main` via Pull Request.

| Branch | Purpose |
|--------|---------|
| `main` | Stable, production-ready code only |
| `dev` | All active development happens here |

**To merge dev into main:**
1. Push your changes to `dev`
2. Go to GitHub → Pull Requests → New Pull Request
3. Base: `main` ← Compare: `dev`
4. Wait for CI to go green
5. Merge

<img src="images/img_13.png" width="600">


<img src="images/img_14.png" width="700">