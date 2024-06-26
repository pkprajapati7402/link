from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Load Google Safe Browsing API key from environment variable
API_KEY = os.getenv('GOOGLE_SAFE_BROWSING_API_KEY')

@app.route('/analyze', methods=['POST'])
def analyze_url():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    safe_browsing_api_url = f'https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}'
    body = {
        'client': {
            'clientId': 'yourcompanyname',
            'clientVersion': '1.5.2'
        },
        'threatInfo': {
            'threatTypes': ['MALWARE', 'SOCIAL_ENGINEERING'],
            'platformTypes': ['WINDOWS'],
            'threatEntryTypes': ['URL'],
            'threatEntries': [
                {'url': url}
            ]
        }
    }

    response = requests.post(safe_browsing_api_url, json=body)
    if response.status_code != 200:
        return jsonify({'error': 'Error fetching data from Safe Browsing API'}), 500

    matches = response.json().get('matches', [])
    if matches:
        status = 'red'
        score = 0
    else:
        status = 'green'
        score = 100

    result = {
        'url': url,
        'score': score,
        'status': status
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
