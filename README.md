# Python Vuln App

Vulnerable app and github action run bandit scan. It has script to fetch issues from code scanning


## How to run 

1. Install Poetry https://python-poetry.org/docs/
2. To start the application `poetry run python app.py`
3. To run the bandit scan `poetry run bandit -r app.py`

## Fetch the issues from Github code scanning 


```bash
export GITHUB_TOKEN='your_personal_access_token'
export REPO_OWNER='repo_owner'
export REPO_NAME='repo_name'
```

### Run the script

`poetry run python fetch_high_severity_alerts.py`


