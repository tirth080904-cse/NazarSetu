# 🚀 NazarSetu Deployment Guide

This guide details how to deploy **NazarSetu** across various environments: locally on Windows/macOS/Linux, in Docker containers, and on free/cloud hosting platforms like Streamlit Community Cloud and Render.

---

## 📋 Table of Contents
1. [Local Deployment (Windows / macOS / Linux)](#1-local-deployment)
2. [Streamlit Community Cloud (Recommended Free Cloud Hosting)](#2-streamlit-community-cloud-recommended-free)
3. [Docker & Docker Compose Deployment](#3-docker--docker-compose-deployment)
4. [Render Web Service Deployment](#4-render-web-service-deployment)
5. [Hugging Face Spaces Deployment](#5-hugging-face-spaces-deployment)
6. [Configuration & Environment Variables](#6-configuration--environment-variables)

---

## 1. Local Deployment

### Windows (1-Click Run)
Simply double-click `run.bat` or open PowerShell in the project directory and run:
```powershell
.\run.bat
```
This script automatically:
- Creates the Python virtual environment (`venv`) if not present.
- Installs and upgrades required dependencies.
- Generates `.env` from template if missing.
- Launches Streamlit and opens `http://localhost:8501`.

### macOS / Linux
Open terminal in the project directory and run:
```bash
chmod +x start.sh
./start.sh
```

### Manual Local Step-by-Step
```bash
# 1. Create and activate virtual environment
python -m venv venv

# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Or Windows CMD:
.\venv\Scripts\activate.bat
# Linux/macOS:
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Run tests to verify setup
pytest tests/ -v

# 4. Launch Streamlit
streamlit run app.py
```
App will be accessible at: `http://localhost:8501`.

---

## 2. Streamlit Community Cloud (Recommended Free)

Streamlit Community Cloud is the fastest, completely free way to host NazarSetu with a public shareable URL.

### Steps:
1. **Push your code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Deploy NazarSetu"
   git remote add origin https://github.com/YOUR_USERNAME/NazarSetu.git
   git branch -M main
   git push -u origin main
   ```
2. Navigate to [share.streamlit.io](https://share.streamlit.io) and log in with GitHub.
3. Click **"New app"**.
4. Select your repository: `YOUR_USERNAME/NazarSetu`.
5. Branch: `main`.
6. Main file path: `app.py`.
7. Expand **"Advanced settings..."**:
   - Python version: `3.11` (or `3.12`)
   - Under **Secrets**, optionally add your OpenAI API key:
     ```toml
     OPENAI_API_KEY = "sk-..."
     OPENAI_MODEL = "gpt-4o-mini"
     ```
     *(If omitted, NazarSetu runs automatically in Offline Fallback Mode!)*
8. Click **"Deploy!"**.
Your app will be live with a custom URL such as `https://nazarsetu.streamlit.app` in under 2 minutes!

---

## 3. Docker & Docker Compose Deployment

NazarSetu includes a multi-stage, hardened production `Dockerfile` with healthcheck and persistent SQLite storage.

### Using Docker Compose (Simplest):
```bash
docker compose up -d --build
```
- The app will start on `http://localhost:8501`.
- Database records in `data/` persist on the host machine across container restarts.
- View container logs:
  ```bash
  docker compose logs -f
  ```
- Stop container:
  ```bash
  docker compose down
  ```

### Using Raw Docker:
```bash
# Build image
docker build -t nazarsetu:latest .

# Run container with volume mount for persistent data
docker run -d -p 8501:8501 -v $(pwd)/data:/app/data --name nazarsetu nazarsetu:latest
```

---

## 4. Render Web Service Deployment

The repository includes a ready-to-use `render.yaml` configuration.

1. Create a free account at [render.com](https://render.com).
2. Connect your GitHub repository.
3. Choose **"New Web Service"** and select the NazarSetu repository.
4. Render will auto-detect the configuration:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
5. Under **Environment Variables**, optionally provide `OPENAI_API_KEY`.
6. Click **Deploy**.

---

## 5. Hugging Face Spaces Deployment

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces) and click **"Create new Space"**.
2. Select **Streamlit** as the Space SDK.
3. Connect your GitHub repo or push code via Git.
4. In Space **Settings** -> **Variables and secrets**, add `OPENAI_API_KEY` (if desired).
5. The Space will automatically build and launch!

---

## 6. Configuration & Environment Variables

| Variable | Default | Purpose |
| :--- | :--- | :--- |
| `OPENAI_API_KEY` | *(blank)* | Enables live OpenAI GPT-4o Multimodal Vision & function calling. If empty, runs in offline fallback mode. |
| `OPENAI_MODEL` | `gpt-4o-mini` | Model identifier for OpenAI agent reasoning. |
| `STREAMLIT_SERVER_PORT` | `8501` | Port on which the web server listens. |
| `STREAMLIT_SERVER_ADDRESS` | `0.0.0.0` | Host IP binding. |
| `STREAMLIT_SERVER_HEADLESS` | `true` | Headless mode for production deployment. |

---

## 🛡️ Healthcheck & Audit
- Streamlit health probe: `http://localhost:8501/_stcore/health`
- Database location: `data/nazarsetu.db` (auto-initialized with WAL mode, foreign keys, and indexes).
- Automated test suite: `pytest tests/ -v`
