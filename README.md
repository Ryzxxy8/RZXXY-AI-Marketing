# 🚀 RZXXY AI Marketing Assistant

An AI-powered marketing assistant designed to simplify marketing research, content creation, copywriting, email marketing, advertising, and sales strategy.

<p align="center">
  <strong>CREATE · INNOVATE · GROW</strong>
</p>

---

## ✨ Overview

RZXXY AI Marketing Assistant is an intelligent marketing toolkit designed to support marketers, entrepreneurs, content creators, and businesses.

## 🌟 Features

### 🤖 AI Marketing Assistant
- AI-powered marketing assistance
- Gemini AI provider integration
- Category-based AI responses
- Marketing research support
- Content and copywriting assistance

### 📈 Marketing Resources
- Marketing knowledge base
- Email marketing guidance
- Facebook Ads knowledge
- Lead magnet resources
- Sales letter resources

### 💻 Interactive Web Dashboard
- Modern neon-inspired interface
- Animated welcome intro
- Custom RZXXY branding
- SVG logo and favicon
- Demo Mode
- Chat history management
- English and Myanmar language switch
- Dashboard statistics

### 🧪 Development
- Python-based application
- Flask web interface
- Automated tests
- Modular project structure

## 🖥️ Project Structure

```text
RZXXY-AI-Marketing/
├── config/
├── core/
├── knowledge/
├── tests/
├── web/
│   ├── static/
│   │   └── images/
│   │       ├── rzxxy-logo.svg
│   │       └── favicon.svg
│   └── templates/
│       └── index.html
├── .env.example
├── .gitignore
├── main.py
└── requirements.txt
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Ryzxxy8/RZXXY-AI-Marketing.git
cd RZXXY-AI-Marketing
pip install -r requirements.txt
```

## 🔑 Configuration

1. Create a local `.env` file using `.env.example` as a reference.
2. Add your Gemini API key to `GEMINI_API_KEY` if you want to enable Gemini integration.
3. Keep API keys and passwords private. Never commit the real `.env` file.

Demo Mode can be used locally without connecting an AI provider.

## ▶️ Run the Web Dashboard

Start the local Flask application:

```bash
python3 -m flask --app web.app run --host 127.0.0.1 --port 5000
```

Open `http://127.0.0.1:5000` in your browser.

## 🛡️ Security Configuration

The development server binds to loopback and does not require login by default. Before exposing the application publicly, configure all of the following in the deployment environment:

- `APP_ENV=production`
- `APP_USERNAME` — a non-default login name
- `APP_PASSWORD` — a long, unique password
- `ALLOWED_HOSTS` — comma-separated exact hostnames for the deployment (do not include URL schemes or paths)
- `GEMINI_API_KEY` — keep the provider key server-side only
- `RATELIMIT_STORAGE_URI` — use a shared Redis URL when running multiple workers or instances

The application refuses to start in production mode if `APP_PASSWORD` or `ALLOWED_HOSTS` is missing. The dashboard and API use HTTP Basic Authentication when credentials are configured. Public deployments must use HTTPS; terminate TLS at a trusted hosting platform or reverse proxy. Do not expose Flask's development server to the internet.

The chat API enforces a request-body limit, a message-length limit, JSON validation, and a default limit of 10 requests per minute per client IP. The default `memory://` rate-limit store is process-local; use shared storage for multi-worker deployments. Configure trusted-proxy handling and edge-level request limits in the hosting environment rather than blindly trusting forwarded headers.

Security response headers include Content Security Policy, frame protection, MIME sniffing protection, Referrer Policy, and a restrictive Permissions Policy. The current dashboard uses inline CSS and JavaScript, so the CSP retains `unsafe-inline` for those two directives; move those assets to separate files before tightening the policy further.

## 🧪 Run Tests

```bash
python3 -m unittest discover -s tests -v
```

## 🛠️ Technology Stack

- Python
- Flask
- Flask-Limiter
- HTML5, CSS3, JavaScript, SVG
- Gemini AI integration
- Git & GitHub

## 📌 Project Status

Current Version: V2.2

Status: Active Development

## 👨‍💻 Developer

RZXXY

GitHub: @Ryzxxy8

Project: RZXXY AI Marketing

---

<p align="center">
  <strong>RZXXY AI MARKETING</strong><br>
  CREATE · INNOVATE · GROW
</p>
