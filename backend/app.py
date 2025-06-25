from flask import Flask, request, jsonify
from flask_cors import CORS
from summarize import summarize_text

app = Flask(__name__)
CORS(app)
@app.route('/summarize', methods=['POST'])
def summarize_input():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    input_text = data['text']
    summary = summarize_text(input_text)
    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(debug=True)
