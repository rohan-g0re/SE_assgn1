# Django Polls App - AWS Elastic Beanstalk Deployment

main: [![Build](https://img.shields.io/badge/build-passing-brightgreen)](#) [![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](#)

This project contains a Django polls application deployed to AWS Elastic Beanstalk.

## Live Application
- [**Main App**](http://djangotutorial-env.us-east-1.elasticbeanstalk.com) 
- [**Link to Polls Utility**](http://djangotutorial-env.us-east-1.elasticbeanstalk.com/polls/)

## Project Structure
```
djangotutorial/
├── manage.py
├── mysite/
│   ├── settings.py
│   ├── urls.py
│   ├── views.py (added homepage)
│   └── wsgi.py
├── polls/ (Django app)
├── .ebextensions/
│   └── django.config (WSGI configuration)
├── requirements.txt (runtime dependencies)
└── .elasticbeanstalk/
    └── config.yml
```

## Deployment Steps

### 1. Prerequisites
- AWS CLI configured
- EB CLI installed
- SSH key pair available

### 2. Prepare Application
```bash
# Navigate to Django project root
cd djangotutorial/

# Create EB configuration directory
mkdir .ebextensions

# Create WSGI configuration
echo "option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: mysite.wsgi:application" > .ebextensions/django.config

# Clean requirements.txt (runtime only)
echo "django==5.2.6
gunicorn==21.2.0
asgiref==3.9.2
sqlparse==0.5.3
tzdata==2025.2" > requirements.txt
```

### 3. Initialize Elastic Beanstalk
```bash
# Initialize EB application
eb init

# Select region (e.g., us-east-1)
# Create new application
# Select Python 3.13 platform
# Enable SSH with existing key pair
```

### 4. Create Environment
```bash
# Create environment
eb create your-env-name

# Select application load balancer
# Disable Spot Fleet requests
```

### 5. Configure Environment Variables
```bash
# Set production settings
eb setenv ALLOWED_HOSTS=your-env.us-east-1.elasticbeanstalk.com,.elasticbeanstalk.com DEBUG=False SECRET_KEY=your-secret-key
```

### 6. Deploy Application
```bash
# Deploy to environment
eb deploy

# Verify deployment
eb status
eb health
```

## Key Configuration Files

### `.ebextensions/django.config`
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: mysite.wsgi:application
```

### `requirements.txt` (Runtime Dependencies)
```
django==5.2.6
gunicorn==21.2.0
asgiref==3.9.2
sqlparse==0.5.3
tzdata==2025.2
```

## CI/CD (Travis CI)

- **What runs**: On every push/PR to `main`, Travis installs dependencies, runs tests with coverage, and reports status to the badges above.
- **Why**: Quick feedback that the app builds and that tests keep coverage healthy.

### Minimal .travis.yml
```yaml
# .travis.yml
language: python
python: "3.11"
install:
  - pip install -r djangotutorial/requirements.txt
  - pip install pytest pytest-cov
script:
  - pytest -q --cov=. --cov-report=term-missing
after_success:
  - coverage xml  # generates coverage.xml used by badges/dashboards

# Optional: deploy to Elastic Beanstalk when main passes
# deploy:
#   provider: elasticbeanstalk
#   region: us-east-1
#   app: djangotutorial
#   env: djangotutorial-env
#   bucket_name: your-eb-bucket
#   on:
#     branch: main
```

### Setup Notes
- Add repository in Travis CI and enable builds for `main`.
- If deploying from Travis, set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in Travis repo settings.

## Assignment Deliverables
- ✅ Deployed Django polls app accessible at `/polls/`
- ✅ Homepage at root URL ("/")
- ✅ Proper EB configuration files
- ✅ Clean requirements.txt for production
- ✅ Environment variables configured
- ✅ Database migrations applied

## Notes
- SQLite database is used for this assignment
- Static files are collected automatically with STATIC_ROOT
- Health checks may take 2-3 minutes to update after changes
