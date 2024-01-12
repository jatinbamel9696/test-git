import argparse
import logging
import os
import markdown
import re
import json
import requests
from urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth
from config.getconfig import getConfig

logging.basicConfig(level=logging.INFO)

def getConfig():
    # ... (same as before)

CONFIG = getConfig()

# ... (same as before)

def searchPages(login, password, title):
    # ... (same as before)

def deletePages(pagesIDList, login, password):
    # ... (same as before)

def createPage(title, content, parentPageID, login, password):
    # ... (same as before)

def attachFile(pageIdForFileAttaching, attachedFile, login, password):
    # ... (same as before)

def publishFolder(folder, login, password, parentPageID=None):
    # ... (same as before)

def publishReleaseToConfluence(login, password, release_notes_path):
    # Search for the Confluence page named "jatin-test"
    search_result = searchPages(login=login, password=password, title="jatin-test")

    # If the page exists, delete it
    if search_result:
        deletePages(pagesIDList=search_result, login=login, password=password)

    # Create a new Confluence page with release notes content
    release_notes_content = ""
    with open(release_notes_path, 'r', encoding="utf-8") as release_notes_file:
        release_notes_content = release_notes_file.read()

    # Create a new Confluence page with the release notes content
    createPage(title="jatin-test", content=markdown.markdown(release_notes_content, extensions=['markdown.extensions.tables', 'fenced_code']),
               parentPageID=None, login=login, password=password)

    # If do exist files to upload as attachments
    files_to_upload = []
    for entry in os.scandir(os.path.dirname(release_notes_path)):
        if entry.is_file() and entry.name.lower().endswith('.md'):
            with open(entry.path, 'r', encoding="utf-8") as md_file:
                for line in md_file:
                    # Search for images in each line and ignore http/https image links
                    result = re.findall("\A!\[.*]\((?!http)(.*)\)", line)
                    if bool(result):
                        result = str(result).split('\'')[1]
                        result = str(result).split('/')[-1]
                        logging.debug("Found file for attaching: " + result)
                        files_to_upload.append(result)

    # If there are files to upload, attach them to the page
    if files_to_upload:
        for file in files_to_upload:
            image_path = os.path.join(os.path.dirname(release_notes_path), file)
            if os.path.isfile(image_path):
                logging.info("Attaching file: " + image_path + "  to the page: jatin-test")
                with open(image_path, 'rb') as attached_file:
                    attachFile(pageIdForFileAttaching=search_result[0],
                               attachedFile=attached_file,
                               login=login,
                               password=password)
            else:
                logging.error("File: " + str(image_path) + "  not found. Nothing to attach")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--login', help='Login with "" is mandatory', required=True)
    parser.add_argument('--password', help='Password with "" is mandatory', required=True)
    parser.add_argument('--release-notes', help='Path to release notes file', required=True)
    args = parser.parse_args()
    input_arguments = vars(args)

    publishReleaseToConfluence(login=input_arguments['login'], password=input_arguments['password'],
                               release_notes_path=input_arguments['release_notes'])
