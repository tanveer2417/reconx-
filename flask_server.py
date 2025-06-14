from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "✅ ReconX Flask Backend is running."

@app.route('/run_recon', methods=['POST'])
def run_recon():
    data = request.get_json()
    target = data.get('target')

    if not target:
        return jsonify({'output': '❌ No target provided.'})

    try:
        # Call your CLI tool from main.py here
        result = subprocess.check_output(['python', 'main.py', target])  # Use 'python' on Windows
        return jsonify({'output': result.decode()})
    
    except subprocess.CalledProcessError as e:
        return jsonify({'output': f"❌ Recon failed:\n{e.output.decode()}"} if e.output else "❌ Recon failed (no output)")
    
    except Exception as e:
        return jsonify({'output': f"⚠️ Unexpected error: {str(e)}"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
