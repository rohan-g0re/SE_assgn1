# 🚀 COMPREHENSIVE DEPLOYMENT PLAN: Django on AWS Elastic Beanstalk

> **Based on TestDriven.io Guide & AWS Best Practices**  
> **Target**: Complete Django polls app deployment with production-grade configuration

---

## 📋 PRE-DEPLOYMENT CHECKLIST

### ✅ Phase 0: Prerequisites & Environment Setup

#### 0.1 AWS Account Setup
- [ ] **Create AWS Account** (if not already done)
  - Go to https://aws.amazon.com/
  - Complete account verification
  - Set up billing information
  - **CRITICAL**: Set up billing alerts (CloudWatch → Billing → Create alarm at $5)

#### 0.2 Local Development Environment
- [ ] **Install Python 3.12+** (recommended)
- [ ] **Install uv package manager**
  ```bash
  # Windows PowerShell:
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  
  # macOS/Linux:
  curl -LsSf https://astral.sh/uv/install.sh | sh
  
  # Or via pip:
  pip install uv
  ```

#### 0.3 AWS CLI Configuration
- [ ] **Install AWS CLI v2**
  ```bash
  # Windows (using MSI installer)
  # Download from: https://aws.amazon.com/cli/
  
  # macOS (using Homebrew)
  brew install awscli
  
  # Linux
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip awscliv2.zip
  sudo ./aws/install
  ```

- [ ] **Configure AWS CLI**
  ```bash
  aws configure
  # Enter your AWS Access Key ID
  # Enter your AWS Secret Access Key
  # Enter your default region (e.g., us-east-1)
  # Enter your default output format (json)
  ```

---

## 🏗️ PHASE 1: LOCAL DEVELOPMENT & TESTING

### 1.1 Project Structure Setup
```bash
# Navigate to your project directory
cd D:\STUFF\NYU_Coursework\SE\Django_x_AWS_EB

# Create virtual environment with uv
uv venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 1.2 Django Application Development
- [ ] **Install Django and dependencies**
  ```bash
  uv pip install "django>=5.2,<6.0"
  uv pip install gunicorn
  uv pip install psycopg2-binary  # For PostgreSQL support
  uv pip install boto3  # For AWS S3 integration
  uv pip install django-storages  # For S3 static files
  ```

- [ ] **Complete Django Tutorial Parts 1-4**
  - Part 1: Project setup and basic views
  - Part 2: Database models and admin
  - Part 3: Views and templates
  - Part 4: Forms and generic views

### 1.3 Local Testing & Validation
- [ ] **Run local development server**
  ```bash
  cd djangotutorial
  python manage.py runserver
  ```
- [ ] **Test all functionality**
  - Create sample polls via admin
  - Test voting functionality
  - Verify all URLs work correctly
- [ ] **Take screenshots** of working application

### 1.4 Generate Requirements
- [ ] **Create requirements.txt**
  ```bash
  uv pip freeze > requirements.txt
  ```

- [ ] **Commit Phase 1**
  ```bash
  git add .
  git commit -m "Phase 1: Complete Django polls app locally"
  git tag phase1-complete
  ```

---

## ⚙️ PHASE 2: PRODUCTION CONFIGURATION

### 2.1 Update Django Settings for Production

#### 2.1.1 Modify `djangotutorial/mysite/settings.py`
```python
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-REPLACE-WITH-NEW-KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Production ALLOWED_HOSTS
ALLOWED_HOSTS = [
    '.elasticbeanstalk.com',
    '.amazonaws.com',
    'localhost',
    '127.0.0.1',
    # Add your custom domain here if you have one
]

# Database configuration for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('RDS_DB_NAME', 'pollsdb'),
        'USER': os.environ.get('RDS_USERNAME', 'postgres'),
        'PASSWORD': os.environ.get('RDS_PASSWORD', ''),
        'HOST': os.environ.get('RDS_HOSTNAME', 'localhost'),
        'PORT': os.environ.get('RDS_PORT', '5432'),
    }
}

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# AWS S3 Configuration (for static files in production)
if not DEBUG:
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    
    # Static files
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    
    # Media files
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
```

#### 2.1.2 Update `INSTALLED_APPS`
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls.apps.PollsConfig',
    'storages',  # Add this for S3 support
]
```

### 2.2 Create Elastic Beanstalk Configuration Files

#### 2.2.1 Create `.ebextensions/01_packages.config`
```yaml
packages:
  yum:
    git: []
    postgresql-devel: []
    gcc: []
```

#### 2.2.2 Create `.ebextensions/02_python.config`
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: djangotutorial.mysite.wsgi:application
  aws:elasticbeanstalk:application:environment:
    DJANGO_SETTINGS_MODULE: djangotutorial.mysite.settings
    DEBUG: 'False'
    SECRET_KEY: 'your-super-secret-key-change-this-in-production'
    ALLOWED_HOSTS: '.elasticbeanstalk.com,.amazonaws.com'
```

#### 2.2.3 Create `.ebextensions/03_django.config`
```yaml
container_commands:
  01_migrate:
    command: "source /var/app/venv/*/bin/activate && python djangotutorial/manage.py migrate --noinput"
    leader_only: true
  02_collectstatic:
    command: "source /var/app/venv/*/bin/activate && python djangotutorial/manage.py collectstatic --noinput"
  03_createsuperuser:
    command: "source /var/app/venv/*/bin/activate && echo 'from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username=\"admin\").exists() or User.objects.create_superuser(\"admin\", \"admin@example.com\", \"admin123\")' | python djangotutorial/manage.py shell"
    leader_only: true
```

#### 2.2.4 Create `.ebextensions/04_nginx.config`
```yaml
files:
  "/etc/nginx/conf.d/proxy.conf":
    mode: "000644"
    owner: root
    group: root
    content: |
      client_max_body_size 20M;
      proxy_connect_timeout 60s;
      proxy_send_timeout 60s;
      proxy_read_timeout 60s;
```

### 2.3 Create Application Entry Point

#### 2.3.1 Create `application.py` in project root
```python
import os
import sys
import django
from django.core.wsgi import get_wsgi_application

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangotutorial.mysite.settings')

# Initialize Django
django.setup()

# Get WSGI application
application = get_wsgi_application()
```

### 2.4 Update Requirements File
```bash
# Update requirements.txt with all necessary packages
uv pip freeze > requirements.txt
```

### 2.5 Test Local Configuration
- [ ] **Test migrations locally**
  ```bash
  cd djangotutorial
  python manage.py migrate
  python manage.py collectstatic
  ```

- [ ] **Commit Phase 2**
  ```bash
  git add .
  git commit -m "Phase 2: Production configuration for Elastic Beanstalk"
  git tag phase2-ready-for-eb
  ```

---

## 🔧 PHASE 3: AWS ELASTIC BEANSTALK CLI SETUP

### 3.1 Install Elastic Beanstalk CLI
```bash
# Install EB CLI using uv
uv pip install --upgrade awsebcli

# Verify installation
eb --version
```

### 3.2 Initialize Elastic Beanstalk Application
```bash
# Navigate to project root
cd D:\STUFF\NYU_Coursework\SE\Django_x_AWS_EB

# Initialize EB application
eb init -p python-3.12 polls-app

# Follow the prompts:
# - Select region (e.g., us-east-1)
# - Create new application or select existing
# - Create new environment or select existing
# - Create SSH key pair if prompted
```

### 3.3 Configure SSH Key (if needed)
```bash
# If you need to create a new SSH key
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
# Save to default location
# Add to SSH agent
ssh-add ~/.ssh/id_rsa
```

### 3.4 Verify Configuration
- [ ] **Check `.elasticbeanstalk/config.yml` exists**
- [ ] **Commit EB configuration**
  ```bash
  git add .elasticbeanstalk/
  git commit -m "Phase 3: Elastic Beanstalk CLI configuration"
  git tag phase3-eb-cli-configured
  ```

---

## 🚀 PHASE 4: FIRST CLOUD DEPLOYMENT

### 4.1 Create Elastic Beanstalk Environment
```bash
# Create environment with specific configuration
eb create polls-env \
  --instance-type t3.micro \
  --platform-version "Python 3.12" \
  --region us-east-1 \
  --timeout 20
```

### 4.2 Monitor Deployment
```bash
# Watch deployment logs in real-time
eb logs --stream

# Check environment health
eb health

# Get environment status
eb status
```

### 4.3 Verify Deployment
- [ ] **Wait for health status to turn GREEN**
- [ ] **Open application in browser**
  ```bash
  eb open
  ```
- [ ] **Test polls application**
  - Navigate to `/polls/`
  - Create sample polls via admin
  - Test voting functionality

### 4.4 Document Deployment
- [ ] **Capture screenshots** of working application
- [ ] **Save deployment logs**
  ```bash
  mkdir -p deployment_artifacts
  eb logs > deployment_artifacts/initial_logs.txt
  ```
- [ ] **Update README.md** with live URL
- [ ] **Commit Phase 4**
  ```bash
  git add .
  git commit -m "Phase 4: First successful cloud deployment"
  git tag phase4-first-deploy
  ```

---

## 🛡️ PHASE 5: OPERATIONAL SAFEGUARDS

### 5.1 AWS VPC Configuration
- [ ] **Check Default VPC**
  - Go to AWS Console → VPC
  - Verify default VPC exists
  - If not, create default VPC
  - Take screenshot

### 5.2 Billing Alerts Setup
- [ ] **Create Billing Alarm**
  - Go to CloudWatch → Billing
  - Create alarm for estimated charges
  - Set threshold to $5.00
  - Configure email notifications
  - Take screenshot

### 5.3 Security Groups Review
- [ ] **Review EB Security Groups**
  - Go to EC2 → Security Groups
  - Verify EB security groups
  - Ensure only necessary ports are open

### 5.4 Environment Variables Setup
- [ ] **Set Production Environment Variables**
  ```bash
  # Set via EB CLI
  eb setenv SECRET_KEY="your-production-secret-key"
  eb setenv DEBUG="False"
  eb setenv ALLOWED_HOSTS=".elasticbeanstalk.com,.amazonaws.com"
  ```

### 5.5 Commit Safeguards
- [ ] **Document safeguards in README**
- [ ] **Commit Phase 5**
  ```bash
  git add .
  git commit -m "Phase 5: Operational safeguards implemented"
  git tag phase5-safeguards
  ```

---

## 🎯 PHASE 6: ADVANCED CONFIGURATION (OPTIONAL)

### 6.1 Database Migration to RDS (Optional)
- [ ] **Create RDS PostgreSQL Instance**
  - Go to RDS → Create database
  - Choose PostgreSQL
  - Select free tier eligible
  - Configure security groups

- [ ] **Update Environment Variables**
  ```bash
  eb setenv RDS_DB_NAME="pollsdb"
  eb setenv RDS_USERNAME="postgres"
  eb setenv RDS_PASSWORD="your-password"
  eb setenv RDS_HOSTNAME="your-rds-endpoint"
  eb setenv RDS_PORT="5432"
  ```

### 6.2 S3 Static Files Configuration (Optional)
- [ ] **Create S3 Bucket**
  - Go to S3 → Create bucket
  - Configure for static website hosting

- [ ] **Set S3 Environment Variables**
  ```bash
  eb setenv AWS_STORAGE_BUCKET_NAME="your-bucket-name"
  eb setenv AWS_S3_REGION_NAME="us-east-1"
  ```

### 6.3 Custom Domain Setup (Optional)
- [ ] **Register Domain** (if desired)
- [ ] **Configure Route 53**
- [ ] **Set up SSL Certificate** via ACM
- [ ] **Update ALLOWED_HOSTS**

---

## 📦 PHASE 7: FINAL SUBMISSION PACKAGE

### 7.1 Repository Finalization
- [ ] **Ensure all files are committed**
  ```bash
  git status
  git add .
  git commit -m "Final submission package"
  ```

### 7.2 Create Comprehensive README
- [ ] **Include all required sections:**
  - Project overview
  - Local setup instructions
  - Deployment instructions
  - Environment variables table
  - Screenshots and links
  - Troubleshooting guide

### 7.3 Final Testing
- [ ] **Test all functionality**
- [ ] **Verify all links work**
- [ ] **Check all screenshots are clear**

### 7.4 Create Release Tag
```bash
# Create final release tag
git tag v1.0-submission

# Push all tags to remote
git push origin --tags
```

### 7.5 Submission
- [ ] **Submit GitHub repository URL**
- [ ] **Submit Elastic Beanstalk application URL**
- [ ] **Include any additional documentation**

---

## 🔍 TROUBLESHOOTING GUIDE

### Common Issues & Solutions

#### Issue: Deployment Fails with Database Errors
**Solution:**
```bash
# Check database configuration
eb logs --stream

# Verify environment variables
eb printenv

# Re-run migrations
eb ssh
source /var/app/venv/*/bin/activate
python djangotutorial/manage.py migrate
```

#### Issue: Static Files Not Loading
**Solution:**
```bash
# Check static files configuration
eb logs --stream

# Verify collectstatic ran
eb ssh
ls -la /var/app/current/staticfiles/
```

#### Issue: Application Not Accessible
**Solution:**
```bash
# Check health status
eb health

# Verify security groups
# Go to EC2 → Security Groups
# Ensure HTTP (80) and HTTPS (443) are open
```

#### Issue: Environment Variables Not Working
**Solution:**
```bash
# Set environment variables
eb setenv VARIABLE_NAME="value"

# Verify variables are set
eb printenv

# Restart environment
eb restart
```

---

## 📊 SUCCESS METRICS

### ✅ Deployment Checklist
- [ ] Django polls app running locally
- [ ] All Django tutorial parts completed
- [ ] Production configuration implemented
- [ ] Elastic Beanstalk environment created
- [ ] Application deployed successfully
- [ ] Health status is GREEN
- [ ] Application accessible via EB URL
- [ ] All functionality working in cloud
- [ ] Billing alerts configured
- [ ] VPC properly configured
- [ ] Repository properly documented
- [ ] All phases tagged and committed

### 🎯 Final Deliverables
1. **Live Elastic Beanstalk URL** (e.g., `http://polls-env.elasticbeanstalk.com/polls/`)
2. **Public GitHub Repository** with complete code and documentation
3. **Screenshots** of working application
4. **Deployment logs** and artifacts
5. **Comprehensive README** with setup instructions

---

## 🚀 EXTRA CREDIT OPPORTUNITIES

### GitHub Actions CI/CD Pipeline
```yaml
# .github/workflows/deploy.yml
name: Deploy to Elastic Beanstalk
on:
  push:
    branches: [ main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to EB
      uses: einaregilsson/beanstalk-deploy@v20
      with:
        aws_access_key: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws_secret_key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        application_name: polls-app
        environment_name: polls-env
        region: us-east-1
        version_label: ${{ github.sha }}
```

### Advanced Monitoring
- CloudWatch custom metrics
- Application performance monitoring
- Log aggregation and analysis

### Security Enhancements
- WAF (Web Application Firewall) configuration
- Enhanced security headers
- Database encryption at rest

---

**🎉 CONGRATULATIONS!**  
Upon completion of all phases, you will have successfully deployed a production-ready Django application to AWS Elastic Beanstalk with proper configuration, monitoring, and documentation.
