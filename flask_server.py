from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')  # Loads templates/index.html

@app.route('/run_recon', methods=['POST'])
def run_recon():
    data = request.get_json()
    target = data.get('target')

    if not target:
        return jsonify({'output': '❌ No target provided.'})

    try:
        # Run reconx/main.py with the given target
        recon_path = os.path.join('reconx', 'main.py')
        result = subprocess.check_output(['python', recon_path, target], stderr=subprocess.STDOUT)
        return jsonify({'output': result.decode()})

    except subprocess.CalledProcessError as e:
        return jsonify({'output': f"❌ Recon failed:\n{e.output.decode()}"} if e.output else "❌ Recon failed (no output)" )

    except Exception as e:
        return jsonify({'output': f"⚠️ Unexpected error: {str(e)}"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
