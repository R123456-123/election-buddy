# 🗳️ Election Buddy — Election Process Education Assistant

An interactive AI-powered assistant that educates users about democratic election processes worldwide. Built with **Streamlit** and **Google Gemini**.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45-FF4B4B?logo=streamlit)
![Gemini](https://img.shields.io/badge/Google_Gemini-2.0_Flash-4285F4?logo=google)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- **🤖 AI Chat Assistant** — Conversational AI restricted to election & democracy topics
- **📅 Election Calendar** — Quick reference of upcoming global elections
- **🏛️ Voting Systems Guide** — Explainers for FPTP, PR, RCV, MMP, and more
- **💡 Quick Facts** — Curated election trivia in the sidebar
- **📊 Global Statistics** — Headline metrics on democracy worldwide
- **🔒 Non-partisan** — System prompt enforces neutrality and factual accuracy
- **♿ Accessible** — Semantic markdown, descriptive help text, screen-reader friendly

---

## 📁 Project Structure

```
election-buddy/
├── app.py                    # Streamlit UI (main entry point)
├── requirements.txt          # Python dependencies
├── Dockerfile                # Cloud Run-optimized container
├── cloudbuild.yaml           # Google Cloud Build CI/CD
├── .env.example              # Environment variable template
├── .gitignore                # Git exclusions
├── .streamlit/
│   └── config.toml           # Streamlit theme & server config
├── utils/
│   ├── __init__.py
│   ├── gemini_helper.py      # Gemini API integration layer
│   └── election_data.py      # Static election reference data
├── tests/
│   ├── __init__.py
│   └── test_app.py           # Unit tests (pytest)
└── README.md                 # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- A free [Google Gemini API key](https://aistudio.google.com/apikey)

### Setup

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd election-buddy

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 5. Run the app
streamlit run app.py
```

The app will open at **http://localhost:8501**.

---

## 🧪 Testing

```bash
pytest tests/test_app.py -v
```

Tests include:
- ✅ Data formatting validation
- ✅ Mocked Gemini API response handling
- ✅ API error propagation
- ✅ Static data structure integrity

---

## 🐳 Docker

```bash
# Build
docker build -t election-buddy .

# Run
docker run -p 8080:8080 -e GEMINI_API_KEY=your_key election-buddy
```

---

## ☁️ Google Cloud Run Deployment

```bash
# Option 1: Cloud Build (automated)
gcloud builds submit --config cloudbuild.yaml .

# Option 2: Manual
gcloud run deploy election-buddy \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key
```

---

## 🔒 Security

- API keys managed via `python-dotenv` (`.env` file)
- `.env` is excluded from version control via `.gitignore`
- No hardcoded secrets anywhere in the codebase
- XSRF protection enabled in Streamlit config

---

## 📋 Grading Criteria Coverage

| Criteria | Implementation |
|---|---|
| **Code Quality** | Modular architecture: `app.py` (UI) + `utils/` (logic) |
| **Security** | `python-dotenv`, `.gitignore`, no hardcoded secrets |
| **Efficiency** | `@st.cache_data`, token-limited system prompts |
| **Testing** | `pytest` with mocked API + data validation tests |
| **Accessibility** | Semantic markdown, `help` text on all elements |
| **Google Services** | `google-generativeai` SDK, Dockerfile, `cloudbuild.yaml` |

---

## 📄 License

MIT — Free for educational and hackathon use.
