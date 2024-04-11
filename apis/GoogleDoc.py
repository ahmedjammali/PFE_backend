from flask import Flask, render_template, request,session, redirect, url_for , Blueprint , jsonify
from openai import OpenAI
import docx
from docx.shared import Pt
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
from docx import Document
import re



def extract_doc_id(url):
    pattern = r'/document/d/([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)

    if match:
        return match.group(1)
    else:

        return None
    
def extract_paragraph_text(doc_content):
    text = ""
    for content in doc_content:
        if 'paragraph' in content:
            elements = content['paragraph']['elements']
            for element in elements:
                if 'textRun' in element:
                    text += element['textRun']['content']
                text += '\n' 
    return text



SCOPES = ['https://www.googleapis.com/auth/drive']
current_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the absolute path to credentials.json
CREDS_FILE= os.path.join(current_dir, 'cred', 'credentials.json')

doc_blueprint = Blueprint('doc_api', __name__)

@doc_blueprint.route('/get_text', methods=['POST'])
def get_text():
    
    creds = None
    data = request.json  
    doc_id = data.get('doc_id')
    doc_id = extract_doc_id(doc_id)
    print(doc_id)

    flow = InstalledAppFlow.from_client_secrets_file(
                CREDS_FILE, SCOPES,redirect_uri='http://localhost')
    creds = flow.run_local_server(port=0)
    cred_json = flow.run_local_server(port=0).to_json()

    service = build('docs', 'v1', credentials=creds)


    try:
        document = service.documents().get(documentId=doc_id).execute()
        content = document.get('body').get('content')
        text = extract_paragraph_text(content)
        return jsonify({'content': text, 'creds' :cred_json})
    except Exception as e:
        error_message = f"Error retrieving document content: {e}"
        return jsonify({'error': error_message})
    








def extract_doc_id(url):
    pattern = r'/document/d/([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)

    if match:
        return match.group(1)
    else:

        return None





# @app.route('/get_text', methods=['POST'])
# def get_text():
#     doc_link = request.form.get('doc_link')

#     creds = None
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json',SCOPES)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 CREDS_FILE, SCOPES,redirect_uri='http://localhost')
#             creds = flow.run_local_server(port=0)
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())

#     service = build('docs', 'v1', credentials=creds)
#     try:
#         document = service.documents().get(documentId=doc_link).execute()
#         table_data = get_table_data(document)
#         headers=get_table_headers(document)
#         session['headers'] =  headers
#         session['text'] = table_data
        
#         return render_template('index.html', table_data=table_data, headers=headers)

#     except Exception as e:
#         error_message = f"Error retrieving document: {e}"
#         return render_template('index.html', error_message=error_message)