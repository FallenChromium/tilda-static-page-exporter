import os
import requests
from flask import Flask, request
from dotenv.main import load_dotenv
from pathlib import Path

load_dotenv()

app = Flask(__name__)

TILDA_PUBLIC_KEY = os.environ.get('TILDA_PUBLIC_KEY')
TILDA_SECRET_KEY = os.environ.get('TILDA_SECRET_KEY')
LOCAL_PATH_PREFIX = os.environ.get('TILDA_STATIC_PATH_PREFIX', '')

def extract_project(project_id):
    # Send the getprojectinfo request and loop through the image array to save common files to the server
    project_info = requests.get(f'https://api.tildacdn.info/v1/getprojectinfo/?projectid={project_id}&publickey={TILDA_PUBLIC_KEY}&secretkey={TILDA_SECRET_KEY}')
    for image in project_info.json()['result']['images']:
        source_url = image['from']
        local_path = Path(LOCAL_PATH_PREFIX) / Path(image['to'])
        local_path.parent.mkdir(parents=True, exist_ok=True)
        save_file(source_url, local_path)
    
    # Send the getpageslist request and loop through the page list to export each page
    pages_list = requests.get(f'https://api.tildacdn.info/v1/getpageslist/?projectid={project_id}&publickey={TILDA_PUBLIC_KEY}&secretkey={TILDA_SECRET_KEY}')
    for page in pages_list.json()['result']:
        # Send the getpagefullexport request for each page and save the images, scripts, and styles used on the page to the server
        page_info = requests.get(f'https://api.tildacdn.info/v1/getpagefullexport/?projectid={project_id}&pageid={page["id"]}&publickey={TILDA_PUBLIC_KEY}&secretkey={TILDA_SECRET_KEY}')
        for image in page_info.json()['result']['images']:
            source_url = image['from']
            local_path = Path(LOCAL_PATH_PREFIX) / Path(image['to'])
            local_path.parent.mkdir(parents=True, exist_ok=True)
            save_file(source_url, local_path)
    
        for script in page_info.json()['result']['js']:
            source_url = script['from']
            local_path = Path(LOCAL_PATH_PREFIX) / Path(script['to'])
            local_path.parent.mkdir(parents=True, exist_ok=True)
            save_file(source_url, local_path)
    
        for style in page_info.json()['result']['css']:
            source_url = style['from']
            local_path = Path(LOCAL_PATH_PREFIX) / Path(style['to'])
            local_path.parent.mkdir(parents=True, exist_ok=True)
            save_file(source_url, local_path)
    
        # Create a new page file and fill it with the HTML content
        filename = page_info.json()['result']['filename']
        html_content = page_info.json()['result']['html']
        with open(Path(LOCAL_PATH_PREFIX) / filename, 'w') as f:
            f.write(html_content)

def save_file(source_url, local_path):
    # Download the file from the source URL and save it to the local path
    response = requests.get(source_url, stream=True)
    with open(local_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

@app.route('/webhook', methods=['GET'])
def handle_webhook():
    # Parse the query parameters from the webhook call
    project_id = request.args.get('projectid')

    # Log that a project extraction has been started
    logging.info(f'Starting extraction for project {project_id}')

    # Extract the project and its pages
    extract_project(project_id)

    # Log that the project extraction has finished
    logging.info(f'Finished extraction for project {project_id}')

    return 'OK'

if __name__ == '__main__':
    import sys
    extract_project(sys.argv[1])
