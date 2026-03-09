import requests
from auth import get_installation_token


def comment_issue(repo, issue_number, comment):

    token = get_installation_token()

    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    data = {
        "body": comment
    }

    response = requests.post(url, json=data, headers=headers)

    print("GitHub API status:", response.status_code)