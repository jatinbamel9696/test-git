import os
import requests
import json

def fetch_latest_release(owner, repo):
    headers = {'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'}
    response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/releases/latest', headers=headers)

    if response.status_code == 200:
        release_data = response.json()
        return release_data
    else:
        print(f"Failed to fetch GitHub release. Status code: {response.status_code}")
        return None

if __name__ == "__main__":
    repo_owner, repo_name = os.getenv("GITHUB_REPOSITORY").split()

    latest_release = fetch_latest_release(repo_owner, repo_name)

    if latest_release:
        print("Latest Release Information:")
        print(f"Name: {latest_release.get('name')}")
        print(f"Tag: {latest_release.get('tag_name')}")
        print(f"Commits Since Last Release: {latest_release.get('commits')}")
    else:
        print("Failed to fetch the latest release.")
