import requests
import json
import os
import sys

# Set your Confluence details
confluence_url = "https://jatin-bamel.atlassian.net/wiki/rest/api/content"
page_id = "950287"  # Replace with your actual page_id
space_key = "testj3"

# Set your Confluence API token directly (for testing purposes)
api_token = "YOUR_CONFLUENCE_API_TOKEN"

# Create a Confluence REST API URL
api_url = f"{confluence_url}/{page_id}"

# Set the headers for authentication
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json",
}

# Get the current page content
response = requests.get(api_url, headers=headers)
page_data = response.json()

# Update the page content with release information
page_data["version"]["number"] += 1
page_data["title"] = "Release v1.0.0"
page_data["body"]["storage"]["value"] = "<p>Release notes for v1.0.0</p>"
page_data["body"]["storage"]["representation"] = "storage"

# Update the Confluence page
update_response = requests.put(api_url, headers=headers, json=page_data)

if update_response.status_code == 200:
    print("Confluence page updated successfully.")
else:
    print(f"Failed to update Confluence page. Status code: {update_response.status_code}")
    print(update_response.text)
