# Django on AWS Elastic Beanstalk: End-to-End Development & Deployment Plan

> **Goal**  Complete Django tutorial Parts 1–4 (the “polls” app) and deploy it to your personal AWS Elastic Beanstalk (EB) environment. Turn in ① the live EB URL and ② your public GitHub repository.

---

## 📊 Project Phases & Deliverables at a Glance

| Phase | Tag | Primary Outcome | TA-Facing Deliverables |
|-------|-----|-----------------|------------------------|
| 1 – Local Development | `phase1-complete` | Tutorial app fully working on localhost | • Source code commits<br>• Screenshot/GIF of `/polls` locally<br>• `requirements.txt` |
| 2 – Packaging & Config | `phase2-ready-for-eb` | Repo contains EB-ready config | • `.ebextensions/django.config`<br>• Updated `settings.py` (`ALLOWED_HOSTS`, `DEBUG`)<br>• Verified migrations/static files |
| 3 – EB CLI Setup | `phase3-eb-cli-configured` | Local dir bound to an EB application | • `.elasticbeanstalk/config.yml` committed<br>• README shows EB CLI version & AWS profile info |
| 4 – First Cloud Deploy | `phase4-first-deploy` | Green-health EB environment with app live | • Live URL in README<br>• Screenshot of `/polls` in the cloud<br>• Archived EB logs |
| 5 – Operational Safeguards | `phase5-safeguards` | Cost & infra protections in place | • Screenshot of default VPC (or note)<br>• Screenshot of Billing Alarm |
| 6 – Submission Package | `v1.0-submission` | Everything ready for grading | • Final README<br>• Repo URL + EB URL submitted |

---

## 🔍 Detailed Task List

### Phase 1 – Local Development
1. **Install uv (if not already installed)**  
   ```bash
   # Windows PowerShell:
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Or via pip:
   pip install uv
   ```
2. **Set up environment with uv**  
   ```bash
   uv venv
   # Activate on Windows:
   .venv\Scripts\activate
   # Activate on macOS/Linux:
   source .venv/bin/activate
   ```
3. **Install Django with uv**  
   ```bash
   uv pip install "django>=5.2,<6"
   ```
4. **Build tutorial Parts 1–4** following Django docs.
5. **Smoke-test locally**  
   `python manage.py runserver` → `http://127.0.0.1:8000/polls`  
   Take a screenshot with a sample poll.
6. **Generate requirements.txt**  
   ```bash
   uv pip freeze > requirements.txt
   ```
7. **Commit & tag:**  
   ```bash
   git add . && git commit -m "Phase 1 complete: local polls app" && git tag phase1-complete
   ```

### Phase 2 – Packaging & Configuration
1. **Static & media files**  
   In `settings.py` set `STATIC_ROOT = BASE_DIR / "staticfiles"`.
2. **Production settings**  
   ```python
   DEBUG = os.environ.get("ENV", "DEV") != "PROD"
   ALLOWED_HOSTS = [
       ".elasticbeanstalk.com", "127.0.0.1", "localhost"
   ]
   ```
3. **Create `.ebextensions/django.config`**
   ```yaml
   option_settings:
     aws:elasticbeanstalk:container:python:
       WSGIPath: mysite.wsgi:application
   container_commands:
     01_migrate:
       command: "python manage.py migrate --noinput"
     02_collectstatic:
       command: "python manage.py collectstatic --noinput"
   ```
4. **Run local migrations + collectstatic** to ensure no errors.
5. **Commit & tag** `phase2-ready-for-eb`.

### Phase 3 – EB CLI Setup
1. **Install EB CLI with uv**  
   ```bash
   uv pip install --upgrade awsebcli
   ```
   Record version: `eb --version` (paste in README).
2. `eb init -p python-3.12 polls-app`  
   • Choose AWS region  
   • Attach an SSH key (create one if prompted).
3. Verify `.elasticbeanstalk/config.yml` is tracked in Git.
4. **Commit & tag** `phase3-eb-cli-configured`.

### Phase 4 – First Cloud Deployment
1. `eb create polls-env --instance_type t3.micro` (or default).
2. Watch logs: `eb logs --stream` until **health = GREEN**.
3. Add the environment URL to README and capture a screenshot of `/polls`.
4. `eb logs > deployment_artifacts/initial_logs.txt`.
5. **Commit & tag** `phase4-first-deploy`.

### Phase 5 – Operational Safeguards
1. **Default VPC check**  
   AWS Console → VPC → if none exists click *Create default VPC* (screenshot).
2. **Billing alarm**  
   CloudWatch → Billing → Alarm at **USD 5** (screenshot).
3. (Optional) Note DB choice (SQLite vs RDS) in README.
4. **Commit & tag** `phase5-safeguards`.

### Phase 6 – Submission Package
1. Ensure public repo contains: code, configs, `deployment_artifacts/`, screenshots.
2. Finalise README sections:  
   • Overview & mapping to assignment rubric  
   • Local setup & deployment instructions  
   • Environment variable table  
   • Screenshots and links  
   • Extra-credit GitHub Actions (if added).
3. Create release tag: `git tag v1.0-submission` and push:  
   ```bash
   git push origin --tags
   ```
4. Submit GitHub URL + EB URL on Brightspace.

---

## 🛠  Optional Enhancements (Extra Credit)
* **GitHub Actions** for CI/CD (`.github/workflows/eb-deploy.yml`).
* **RDS PostgreSQL** integration via EB console.
* **S3 static/media storage** using `django-storages`.
* **Custom domain & HTTPS** via Route 53 + ACM.
* **uv lock file** for reproducible builds (`uv.lock`).

## 📝 uv-Specific Benefits
* **Faster dependency resolution** compared to pip
* **Automatic virtual environment management** 
* **Lock file support** for reproducible builds
* **Better dependency conflict resolution**
* **Cross-platform compatibility**

---

## 📂 Repository Layout After Completion
```
mysite/
├── manage.py
├── polls/
├── mysite/
│   ├── settings.py
│   └── wsgi.py
├── staticfiles/            # collected static assets
├── .ebextensions/
│   └── django.config
├── .elasticbeanstalk/
│   └── config.yml
├── deployment_artifacts/
│   └── initial_logs.txt
├── .venv/                  # uv virtual environment
├── requirements.txt        # generated by uv pip freeze
├── uv.lock                 # uv lock file (optional)
└── README.md
```

Follow the phase tags, tick off all deliverables, and you will satisfy—if not exceed—the assignment’s grading criteria.
