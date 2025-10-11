## CI/Travis Integration Answers

### GitHub repo + default branch
- Repo URL (owner/repo): `rohan-g0re/SE_assgn1`
- Default branch: `main`

### Travis CI hookup
- Travis CI enabled: No (not configured yet). OK to proceed with public `travis-ci.com`.

### EB target (for Travis deploy step)
- Application name: `djangotutorial`
- Environment name: `djangotutorial-env`
- Region: `us-east-1`

### AWS credentials for Travis deploy
- Create least-privilege IAM user and store `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in Travis repo settings: Yes

### Coveralls
- Coveralls project/token available: No
- OK to merge CI without coverage badge first and add token later: Yes

### Python version in CI
- Selected Python version: `3.13` (to match EB platform)

### Project paths (for CI commands)
- Confirmed: Yes
  - `manage.py` path: `djangotutorial/manage.py`
  - WSGI module: `mysite.wsgi`

### Minimal tests
- OK to add a smoke test (`tests/test_smoke.py`): Yes

### Badges & branch protection
- Target branch for badges and required status checks: `main`


