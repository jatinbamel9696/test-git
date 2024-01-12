import requests
import sys

def test_credentials(login, password):
    confluence_url = "https://jatin-bamel.atlassian.net/wiki/rest/api/"  # Replace with your Confluence instance URL

    try:
        response = requests.get(confluence_url, auth=(login, password))
        response.raise_for_status()

        # Check if the response contains expected data indicating successful authentication
        if "some_expected_data" in response.text:
            print("Credentials are valid.")
        else:
            print("Error: Unexpected response content.")
            sys.exit(1)

    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python test_credentials.py <login> <password>")
        sys.exit(1)

    test_credentials(login=sys.argv[1], password=sys.argv[2])
