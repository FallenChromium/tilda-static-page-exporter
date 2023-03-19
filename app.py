import os
import requests
from flask import Flask, request
from dotenv.main import load_dotenv
from pathlib import Path

load_dotenv()

app = Flask(__name__)

TILDA_PUBLIC_KEY = os.environ.get('TILDA_PUBLIC_KEY')
TILDA_SECRET_KEY = os.environ.get('TILDA_SECRET_KEY')
LOCAL_PATH_PREFIX = os.environ.get('LOCAL_PATH_PREFIX', '')

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    # Parse the JSON payload from the webhook call
    payload = request.get_json()

    # Send the getprojectinfo request and loop through the image array to save common files to the server
    project_info = requests.get(f'https://api.tilda.cc/v1/projects/getprojectinfo/?projectid={payload["projectid"]}&publickey={TILDA_PUBLIC_KEY}&secretkey={TILDA_SECRET_KEY}')
    for image in project_info.json()['images']:
        source_url = image['from']
        local_path = LOCAL_PATH_PREFIX + image['to']
        save_image(source_url, local_path)

    # Send the getpageslist request and loop through the page list to export each page
    pages_list = requests.get(f'https://api.tilda.cc/v1/pages/getpageslist/?projectid={payload["projectid"]}&publickey={TILDA_PUBLIC_KEY}&secretkey={TILDA_SECRET_KEY}')
    for page in pages_list.json():
        # Send the getpagefullexport request for each page and save the images, scripts, and styles used on the page to the server
        page_info = requests.get(f'https://api.tilda.cc/v1/pages/getpagefullexport/?pageid={page["id"]}&projectid={payload["projectid"]}&publickey={TILDA_PUBLIC_KEY}&secretkey={TILDA_SECRET_KEY}')
        for image in page_info.json()['images']:
            source_url = image['from']
            local_path = LOCAL_PATH_PREFIX + image['to']
            save_image(source_url, local_path)

        for script in page_info.json()['js']:
            source_url = script['from']
            local_path = LOCAL_PATH_PREFIX + script['to']
            save_script(source_url, local_path)

        for style in page_info.json()['css']:
            source_url = style['from']
            local_path = LOCAL_PATH_PREFIX + style['to']
            save_style(source_url, local_path)

        # Create a new page file and fill it with the HTML content
        filename = page_info.json()['filename']
        html_content = page_info.json()['html']
        create_page_file(filename, html_content)

    return 'OK'

def save_image(source_url, local_path):
    # Download the image from the source URL and save it to the local path
    response = requests.get(source_url)
    with open(local_path, 'wb') as f:
        f.write(response.content)

def save_script(source_url, local_path):
    # Download the script from the source URL and save it to the local path
    response = requests.get(source_url)
    with open(local_path, 'w') as f:
        f.write(response.text)

def save_style(source_url, local_path):
    # Download the style from the source URL and save it to the local path
    response = requests.get(source_url)
    with open(local_path, 'w') as f:
        f.write(response.text)

def create_page_file(filename, html_content):
    # Create a new page file with the given filename and fill it with the HTML content
    with open(filename, 'w') as f:
        f.write(html_content)

if __name__ == '__main__':
    app.run(debug=True)
