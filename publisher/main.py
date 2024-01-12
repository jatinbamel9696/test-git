import os
import argparse
import logging
import requests
from requests.auth import HTTPBasicAuth
from config.getconfig import getConfig

logging.basicConfig(level=logging.INFO)

def getConfig():
    # ... (same as before)

CONFIG = getConfig()

def searchPages(login, password, title):
    # ... (same as before)

def deletePages(pagesIDList, login, password):
    # ... (same as before)

def createPage(title, content, parentPageID, login, password):
    # ... (same as before)

def publishReleaseToConfluence(login, password, release_notes):
    # Search for the Confluence page
    search_result = searchPages(login=login, password=password, title=CONFIG["CONFLUENCE_PAGE_TITLE"])

    # If the page exists, delete it
    if search_result:
        deletePages(pagesIDList=search_result, login=login, password=password)

    # Create a new Confluence page with release notes content
    createPage(title=CONFIG["CONFLUENCE_PAGE_TITLE"],
               content=release_notes,
               parentPageID=CONFIG["CONFLUENCE_PARENT_PAGE_ID"],
               login=login,
               password=password)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--login', help='Login with "" is mandatory', required=True)
    parser.add_argument('--password', help='Password with "" is mandatory', required=True)
    parser.add_argument('--github-token', help='GitHub token for authentication', required=True)
    args = parser.parse_args()
    input_arguments = vars(args)

    # Fetch the latest release notes from GitHub
    headers = {'Authorization': f'token {input_arguments["github_token"]}'}
    response = requests.get(f'https://api.github.com/repos/your-username/your-repo/releases/latest', headers=headers)
    release_data = response.json()
    release_notes = release_data.get('body', '')

    # Publish release notes to Confluence
    publishReleaseToConfluence(login=input_arguments['login'],
                               password=input_arguments['password'],
                               release_notes=release_notes)
