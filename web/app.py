import logging
import os
import secrets
from urllib.parse import urlsplit

from flask import Flask, jsonify, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.exceptions import BadRequest

from core.ai_engine import AIEngine


APP_ENV = os.getenv("APP_ENV", "development").strip().lower()
APP_USERNAME = os.getenv("APP_USERNAME", "admin")
APP_PASSWORD = os.getenv("APP_PASSWORD", "")
ALLOWED_HOSTS = {
    host.strip().lower()
    for host in os.getenv("ALLOWED_HOSTS", "").split(",")
    if host.strip()
}

if APP_ENV == "production":
    if not APP_PASSWORD:
        raise RuntimeError("APP_PASSWORD must be configured in production.")
    if not ALLOWED_HOSTS:
        raise RuntimeError("ALLOWED_HOSTS must be configured in production.")

app = Flask(__name__)
app.config.update(
    MAX_CONTENT_LENGTH=64 * 1024,
    AUTH_ENABLED=bool(APP_PASSWORD),
    APP_USERNAME=APP_USERNAME,
    APP_PASSWORD=APP_PASSWORD,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri=os.getenv("RATELIMIT_STORAGE_URI", "memory://"),
    headers_enabled=True,
)


@app.before_request
def enforce_request_security():
    allowed_hosts = app.config["ALLOWED_HOSTS"]
    if allowed_hosts:
        hostname = (urlsplit("//{}".format(request.host)).hostname or "").lower()
        if hostname not in allowed_hosts:
            return jsonify({"error": "Invalid host."}), 400

    if app.config["AUTH_ENABLED"]:
        credentials = request.authorization
        supplied_username = (credentials.username if credentials else "") or ""
        supplied_password = (credentials.password if credentials else "") or ""
        valid_username = secrets.compare_digest(
            supplied_username.encode("utf-8"),
            app.config["APP_USERNAME"].encode("utf-8"),
        )
        valid_password = secrets.compare_digest(
            supplied_password.encode("utf-8"),
            app.config["APP_PASSWORD"].encode("utf-8"),
        )
        if not (valid_username and valid_password):
            return (
                jsonify({"error": "Authentication required."}),
                401,
                {"WWW-Authenticate": 'Basic realm="RZXXY AI Marketing"'},
            )


@app.after_request
def add_security_headers(response):
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault(
        "Permissions-Policy",
        "camera=(), microphone=(), geolocation=()",
    )
    # The current dashboard uses inline CSS and JavaScript; retain those while
    # blocking plugins, framing, and external resource injection.
    response.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "connect-src 'self'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'none'",
    )
    return response


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify({"error": "Request body is too large."}), 413


@app.errorhandler(429)
def rate_limit_exceeded(_error):
    return jsonify({"error": "Too many requests. Please try again later."}), 429


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
@limiter.limit(os.getenv("CHAT_RATE_LIMIT", "10 per minute"))
def chat():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json."}), 415

    try:
        data = request.get_json()
    except BadRequest:
        return jsonify({"error": "Invalid JSON request body."}), 400

    if not isinstance(data, dict):
        return jsonify({"error": "JSON body must be an object."}), 400

    task = data.get("message")
    if not isinstance(task, str):
        return jsonify({"error": "Message must be a string."}), 400

    task = task.strip()
    if not task:
        return jsonify({"error": "Message is required."}), 400
    if len(task) > 12000:
        return jsonify({"error": "Message exceeds the 12000-character limit."}), 400

    try:
        result = AIEngine().generate(task)
        categories = result.get("categories")
        answer = result.get("answer")
        if not isinstance(categories, list) or not isinstance(answer, str):
            raise ValueError("AI provider returned an invalid response shape.")

        return jsonify({
            "categories": categories,
            "answer": answer,
        })
    except Exception:
        app.logger.exception("AI chat request failed")
        return jsonify({
            "error": "The AI service could not complete this request. Check the server configuration and logs."
        }), 502


if __name__ == "__main__":
    # Keep the development server bound to loopback. Use a production WSGI
    # server (for example, Gunicorn) behind HTTPS for public deployments.
    app.run(host="127.0.0.1", port=5000, debug=False)
