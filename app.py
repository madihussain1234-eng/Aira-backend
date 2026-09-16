from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Aira Backend is running!"

@app.route("/api/aira", methods=["POST"])
def aira():
    try:
        data = request.get_json(silent=True) or {}
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"error": "Question is required"}), 400

        api_key = os.environ.get("OPENAI_API_KEY")

        if not api_key:
            return jsonify({"error": "OpenAI API key is not configured"}), 500

        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model="gpt-4o-mini",
            input=question
        )

        return jsonify({
            "answer": response.output_text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "_main_":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
