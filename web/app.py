from flask import Flask, render_template, request, jsonify
from core.ai_engine import AIEngine

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    task = data.get("message", "").strip()

    if not task:
        return jsonify({"error": "Message is required."}), 400

    try:
        engine = AIEngine()
        result = engine.generate(task)

        return jsonify({
            "categories": result["categories"],
            "answer": result["answer"]
        })

    except Exception as error:
        return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
