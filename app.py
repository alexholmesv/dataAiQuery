from flask import Flask, request, jsonify, render_template
import pandas as pd
import openai

app = Flask(__name__)

#Habilitar el auto reload
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Cargar CSV de pryeba
data = pd.read_csv('test.csv')

# API Key OpenAI. NO SE PUEDE HARDCODEAR.
openai.api_key = ""

def generate_response(query):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=query,
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Endpoints
@app.route('/query', methods=['GET', "POST"])
def index():
    if request.method == 'POST':
        query = request.form.get('query')
        if query:

            response = generate_response(query)
            return render_template('index.html', response=response, query=query)
        else:
            return render_template('index.html', error='No query provided')



# Homepage route
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/save-api-key', methods=['POST'])
def save_api_key():
    data = request.json
    openai.api_key = data.get('apiKey')
    return jsonify({'message': 'API key saved successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
