from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Call Ollama API
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:1b",
                "prompt": user_message,
                "stream": False
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            bot_response = result.get('response', 'No response received')
            return jsonify({'response': bot_response})
        else:
            return jsonify({'error': f'Ollama returned status code {response.status_code}'})
            
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Could not connect to Ollama. Make sure it\'s running on localhost:11434'})
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timed out'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)