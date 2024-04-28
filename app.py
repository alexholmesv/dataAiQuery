from flask import Flask, request, jsonify, render_template
import pandas as pd
import openai

app = Flask(__name__)

# Load CSV data
data = pd.read_csv('test.csv')

# OpenAI API key
openai.api_key = None

def generate_response(query):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=query,
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Homepage route
@app.route('/')
def home():
    return render_template('index.html')

# Query endpoint
@app.route('/query', methods=['GET'])
def query_data():
    query = request.args.get('query')
    if query:
        response = generate_response(query)
        return jsonify({'response': response})
    else:
        return jsonify({'error': 'No query provided'})

@app.route('/save-api-key', methods=['POST'])
def save_api_key():
    data = request.json
    openai.api_key = data.get('apiKey')
    return jsonify({'message': 'API key saved successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
