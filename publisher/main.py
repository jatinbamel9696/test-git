import argparse
import logging
from config.getconfig import getConfig
from pagesController import searchPages, deletePages, createPage

logging.basicConfig(level=logging.INFO)

# Parse arguments with LOGIN and PASSWORD for Confluence
parser = argparse.ArgumentParser()
parser.add_argument('--login', help='Login with "" is mandatory', required=True)
parser.add_argument('--password', help='Password with "" is mandatory', required=True)
parser.add_argument('--release-notes', help='Path to release notes file', required=True)
args = parser.parse_args()
inputArguments = vars(args)

CONFIG = getConfig()

logging.debug(CONFIG)

# Search for the Confluence page named "jatin-test"
search_result = searchPages(login=inputArguments['login'], password=inputArguments['password'], title="jatin-test")

# If the page exists, delete it
if search_result:
    deletePages(pagesIDList=search_result, login=inputArguments['login'], password=inputArguments['password'])

# Create a new Confluence page with release notes content
release_notes_content = ""
with open(inputArguments['release_notes'], 'r', encoding="utf-8") as release_notes_file:
    release_notes_content = release_notes_file.read()

# Create a new Confluence page with the release notes content
createPage(title="jatin-test", content=release_notes_content, parentPageID=None,
           login=inputArguments['login'], password=inputArguments['password'])
