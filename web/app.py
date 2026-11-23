from flask import Flask, render_template, request, jsonify
from core.ai_engine import AIEngine

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024  # Limit incoming request bodies to 16 KB.

MAX_MESSAGE_LENGTH = 5000


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify({"error": "Request body is too large."}), 413


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json."}), 415

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    message = data.get("message")
    if not isinstance(message, str):
        return jsonify({"error": "Message must be a string."}), 400

    task = message.strip()
    if not task:
        return jsonify({"error": "Message is required."}), 400

    if len(task) > MAX_MESSAGE_LENGTH:
        return jsonify({
            "error": f"Message must be {MAX_MESSAGE_LENGTH} characters or fewer."
        }), 413

    try:
        engine = AIEngine()
        result = engine.generate(task)

        return jsonify({
            "categories": result["categories"],
            "answer": result["answer"]
        })

    except Exception:
        app.logger.exception("Unexpected error while processing /api/chat")
        return jsonify({
            "error": "An internal server error occurred. Please try again later."
        }), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
