# test_credentials.py
import requests
import sys

def test_credentials(login, password):
    confluence_url = "https://jatin-bamel.atlassian.net/wiki/rest/api/"  # Replace with your Confluence instance URL

    try:
        response = requests.get(confluence_url, auth=(login, password))
        response.raise_for_status()
        print("Credentials are valid.")
    except requests.exceptions.HTTPError as err:
        print(f"Error: {err}")
        sys.exit(1)

if __name__ == "__main__":
    test_credentials(login=sys.argv[1], password=sys.argv[2])
