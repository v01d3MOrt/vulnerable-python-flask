import os
import requests
from bs4 import BeautifulSoup

# Fetch environment variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
OWNER = os.getenv('REPO_OWNER')
REPO = os.getenv('REPO_NAME')

# Check if environment variables are set
if not GITHUB_TOKEN or not OWNER or not REPO:
    raise ValueError("Please set the GITHUB_TOKEN, REPO_OWNER, and REPO_NAME environment variables.")

# GitHub API endpoint for code scanning alerts
API_URL = f'https://api.github.com/repos/{OWNER}/{REPO}/code-scanning/alerts'

# Define the headers for the request
headers = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': f'token {GITHUB_TOKEN}',
}

def fetch_high_severity_alerts():
    high_severity_alerts = []
    page = 1

    while True:
        # Make the API request
        response = requests.get(API_URL, headers=headers, params={'page': page, 'per_page': 100})
        response.raise_for_status()
        alerts = response.json()

        # Filter alerts with severity "high" or "critical"
        for alert in alerts:
            if alert['rule']['security_severity_level'] in ['high', 'critical']:
                high_severity_alerts.append(alert)

        # Check if there are more pages
        if 'Link' in response.headers:
            links = response.headers['Link'].split(',')
            if not any('rel="next"' in link for link in links):
                break
        else:
            break

        page += 1

    return high_severity_alerts

def get_exploitability_likelihood(cwe_id):
    url = f"https://cwe.mitre.org/data/definitions/{cwe_id}.html"
    response = requests.get(url)
    if response.status_code != 200:
        return "Unknown"

    soup = BeautifulSoup(response.content, 'html.parser')
    likelihood = soup.find(text="Likelihood of Exploit")
    if likelihood:
        return likelihood.find_next('td').text.strip()
    return "Unknown"

if __name__ == '__main__':
    alerts = fetch_high_severity_alerts()
    print(f"Found {len(alerts)} high or critical severity alerts.")
    for alert in alerts:
        description = alert['rule']['description']
        severity = alert['rule']['security_severity_level']
        cwe_id = alert['rule']['id']
        exploitability = get_exploitability_likelihood(cwe_id)
        print(f"- {description} (Severity: {severity}, CWE: {cwe_id}, Likelihood of Exploitability: {exploitability})")
