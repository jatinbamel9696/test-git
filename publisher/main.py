import argparse
import logging
import requests
from config.getconfig import getConfig
from pagesController import deletePages, searchPages
from pagesPublisher import publishFolder

logging.basicConfig(level=logging.INFO)

# Parse arguments with LOGIN and PASSWORD for Confluence
parser = argparse.ArgumentParser()
parser.add_argument('--login', help='Login with "" is mandatory', required=True)
parser.add_argument('--password', help='Password with "" is mandatory', required=True)
parser.add_argument('--github-token', help='GitHub access token for authentication', required=True)
parser.add_argument('--confluence-page-title', help='Title of the Confluence page to update', required=True)
args = parser.parse_args()
input_arguments = vars(args)

CONFIG = getConfig()
logging.debug(CONFIG)

# GitHub API endpoint for releases
github_api_url = f"https://api.github.com/repos/{CONFIG['github_repo']}/releases"

# Make a request to GitHub API to get the list of releases
response = requests.get(github_api_url, headers={"Authorization": f"Bearer {input_arguments['github_token']}"})
releases = response.json()

# Check if there are new releases
if releases:
    logging.info(f"Found {len(releases)} releases on GitHub.")
    
    # Assuming the Confluence page already exists
    confluence_page_title = input_arguments['confluence_page_title']
    
    # Find the Confluence page by title
    confluence_pages = searchPages(login=input_arguments['login'], password=input_arguments['password'], title=confluence_page_title)
    
    if confluence_pages:
        confluence_page_id = confluence_pages[0]['id']
        logging.info(f"Found Confluence page with title '{confluence_page_title}' (ID: {confluence_page_id}).")
        
        # You may need to customize the following lines based on your Confluence page update logic
        # Example: updateConfluencePage(confluence_page_id, releases)
        
        # Update Confluence with the new release information
    else:
        logging.warning(f"No Confluence page found with title '{confluence_page_title}'.")
else:
    logging.info("No new releases found on GitHub.")
