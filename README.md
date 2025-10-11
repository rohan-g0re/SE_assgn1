# Django Polls App - AWS Elastic Beanstalk Deployment

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
