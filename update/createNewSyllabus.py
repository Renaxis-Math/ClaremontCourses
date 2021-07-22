from __future__ import print_function
import urllib3
import requests
import email, smtplib, ssl
import sqlite3
import convert_prereq
import convert_coreq
import random
import json
import math
import re
import ast 
import random
import time
import gzip
import shutil
from random import randint
from datetime import datetime
from bs4 import BeautifulSoup
from flask import Flask, render_template, send_from_directory, request, make_response, flash, redirect, url_for
from werkzeug.utils import secure_filename
import pickle
import os.path
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import google.oauth2.credentials
import google_auth_oauthlib.flow

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    cred = None
    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)
    service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        return service
    except:
        return None
def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

con = sqlite3.connect("claremontcourses.db", check_same_thread=False)
con.row_factory = sqlite3.Row

def getNewCourses():
    """
    Get a list of new course codes without syllabus link
    """
    cur = con.cursor()
    select = """
        SELECT code FROM temp_claremontcourses WHERE syllabus == "None"
    """
    codes = []
    selects = cur.execute(select)
    for select in selects:
        codes.append(select[0])
        con.commit()
    return codes

def createNewSyllabusLink(codeList):
    """
    Return a list of syllabu links based on a list of codes
    """
    newSyllabusLinks = []
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    for code in codeList:
        file_metadata = {
            'name': code,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': ['1MRMZnnMUtfboXihOradVZG3p3WllFXqe']
        }    
        file = service.files().create(body=file_metadata,
                                            fields='id').execute()
        print(file.get('id'))
        newSyllabusLinks.append((code, "https://drive.google.com/drive/folders/" + file.get('id')))
        time.sleep(5)
    return newSyllabusLinks

newCodes = getNewCourses()
newSyllabusLinks = createNewSyllabusLink(newCodes)
for code, newSyllabusLink in newSyllabusLinks:
    print(code, " ", newSyllabusLink)
    update = """
        UPDATE temp_claremontcourses SET syllabus = ? WHERE code == ?;
    """
    cur = con.cursor()
    cur.execute(update, (newSyllabusLink, code))
    con.commit()
