from flask import Flask, request, jsonify
from transformers import pipeline
import os

app = Flask(__name__)

# Use a lightweight summarization model suitable for Render
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")


def summarize_text(text, max_chunk=1000):
    chunks = [text[i:i + max_chunk] for i in range(0, len(text), max_chunk)]
    summary = ""
    for chunk in chunks:
        result = summarizer(chunk, max_length=200, min_length=50, do_sample=False)
        summary += result[0]['summary_text'] + "\n\n"
    return summary.strip()

# Health check route
@app.route("/")
def home():
    return "✅ News Summarizer API is running!"

# Summarization endpoint
@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    summary = summarize_text(data["text"])
    return jsonify({"summary": summary})

# Render requires binding to 0.0.0.0 and a dynamic port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # 5000 is default for local
    app.run(host='0.0.0.0', port=port)
