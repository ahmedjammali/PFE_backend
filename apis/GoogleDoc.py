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
import json



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

def extract_tables(document):

    all_tables = []
    tables_titles = []
    for content in document.get('body').get('content'):
        if 'table' in content:
            table = content['table']
            table_data = {}
            headers = []
            content_rows = []
            
            for i, row in enumerate(table['tableRows']):
                for j, cell in enumerate(row['tableCells']):
                    cell_data = ''
                    for p in cell['content']:
                        cell_data += p['paragraph']['elements'][0]['textRun']['content']
                    if j == 0:  
                        headers.append(cell_data.strip())
                    elif headers and (j == 1): 
                        content_rows.append((headers[i], cell_data.strip()))
                    if j == 1 and i == 0 : 
                        title = cell_data.strip()
            table_data['headers'] = headers
            table_data['content'] = content_rows
            table_data['title'] = title
            tables_titles.append(title)
            all_tables.append(table_data)

    return all_tables  , tables_titles



SCOPES = ['https://www.googleapis.com/auth/drive']
current_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the absolute path to credentials.json
CREDS_FILE= os.path.join(current_dir, 'cred', 'credentials.json')

doc_blueprint = Blueprint('doc_api', __name__)

@doc_blueprint.route('/get_text', methods=['POST'])
def get_text():
    
    creds = None
    data = request.json  
    doc_id = extract_doc_id(data.get('doc_id'))
    cred_json = data.get('cred')
    print(doc_id)
    print(cred_json)
    if  cred_json is None or cred_json == "undefined"  :
        flow = InstalledAppFlow.from_client_secrets_file(
                        CREDS_FILE, SCOPES,redirect_uri='http://localhost')
        creds = flow.run_local_server(port=0)
        cred_json = flow.run_local_server(port=0).to_json()
        print("B")
    else : 
        cred_json = json.loads(cred_json)
        creds = Credentials.from_authorized_user_info(cred_json)
        cred_json = creds.to_json()
        print(creds)
        if not creds.valid:  
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                print("A")

    service = build('docs', 'v1', credentials=creds)

    try:
        document = service.documents().get(documentId=doc_id).execute()
        content  = extract_tables(document)

        return jsonify({'content': content,'creds' :cred_json})
    except Exception as e:
        error_message = f"Error retrieving document content: {e}"
        return jsonify({'error': error_message,'creds' : cred_json })
    
@doc_blueprint.route('/modify_doc', methods=['POST'])
def modify_doc():
    data = request.json  
    cred_json = data.get('cred')
    doc_id = extract_doc_id(data.get('doc_id'))
    table_title = request.json.get('table_title')
    table_header = request.json.get('table_header')
    new_content = request.json.get('new_content')

    cred_json = json.loads(cred_json)
    creds = Credentials.from_authorized_user_info(cred_json)

    service = build('docs', 'v1', credentials=creds)

    try:
        document = service.documents().get(documentId=doc_id).execute()
        for content in document.get('body').get('content'):
            if 'table' in content:
                table = content['table']
                table = content['table']
                table_start_index = content['startIndex']
                # Find the table based on its title in the first row, second column
                print("hello 1")

                # Find the table based on its title in the first row, second column
                for i, row in enumerate(table['tableRows']):
                    if len(row['tableCells']) > 1:
                        cell_content = row['tableCells'][1]['content'][0]['paragraph']['elements'][0]['textRun']['content'].strip()

                        if cell_content == table_title:
                            print("hello3")
                            # Find the target column based on the header
                            headers = [
                                row['tableCells'][0]['content'][0]['paragraph']['elements'][0]['textRun']['content'].strip()  # Extract text content from the first cell of each row
                                for row in table['tableRows']  # Iterate through each row of the table
                            ]
                            
                            # Check if the specified header exists in the table
                            print("hello4")
                            if table_header in headers:
                                target_column_index = headers.index(table_header)
                                # Update the content of the target cell
                                print("hello6")
                                row_index = i
                                print(row_index)
                                content_to_change =table['tableRows'][target_column_index]['tableCells'][1]
                                service.documents().batchUpdate(
                                        documentId=doc_id,
                                        body={'requests': [
                                            {
                                                    'deleteContentRange': {
                                                        'range': {
                                                            'startIndex': content_to_change['startIndex']+1,
                                                            'endIndex': content_to_change['endIndex']-1
                                                        }
                                                    }
                                            },
                                            {
                                                'insertText': {
                                                'location': {
                                                    'index': content_to_change['startIndex']+1
                                                },
                                                'text': new_content
                                              }
                                            }
                                        ]}
                                    ).execute()
                                return "Table updated successfully."
                            else:
                                return f'Header "{table_header}" not found in table "{table_title}"'
                                    
    


        return jsonify({'message':" Document updated successfully " })
    except Exception as e:
        error_message = f"Error updating document content: {e}"
        return jsonify({'error': error_message })


    













