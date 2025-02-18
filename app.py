import os
import requests
from flask import Flask, render_template, request, jsonify
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get API keys from environment variables
API_KEYS = [
    os.getenv('REMOVE_BG_API_KEY_1'),
    os.getenv('REMOVE_BG_API_KEY_2'),
    os.getenv('REMOVE_BG_API_KEY_3'),
    os.getenv('REMOVE_BG_API_KEY_4'),
    os.getenv('REMOVE_BG_API_KEY_5'),
    os.getenv('REMOVE_BG_API_KEY_6'),
]

API_ENDPOINT = 'https://api.remove.bg/v1.0/removebg'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files.get('image')
    if not uploaded_file:
        return jsonify({'error': 'No image uploaded'}), 400

    input_image = uploaded_file.read()

    valid_api_key_found = False

    for api_key in API_KEYS:
        if not api_key:
            continue  # Skip if API key is missing

        valid_api_key_found = True

        try:
            response = requests.post(
                API_ENDPOINT,
                files={'image_file': ('image.png', input_image, 'image/png')},
                data={'size': 'auto'},
                headers={'X-Api-Key': api_key}
            )

            if response.status_code == 200:
                output_image = response.content

                # Convert images to base64
                original_image_base64 = base64.b64encode(input_image).decode('utf-8')
                modified_image_base64 = base64.b64encode(output_image).decode('utf-8')

                return jsonify({
                    'original_image': f'data:image/png;base64,{original_image_base64}',
                    'background_removed_image': f'data:image/png;base64,{modified_image_base64}'
                })

            print(f"API failed (Key: {api_key[:4]}...): {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

    if not valid_api_key_found:
        return jsonify({'error': 'No valid API keys found'}), 500

    return jsonify({'error': 'All API keys failed to process the image'}), 500

if __name__ == '__main__':
    app.run(debug=True)