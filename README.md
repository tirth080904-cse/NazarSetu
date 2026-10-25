# NazarSetu (नज़रसेतु) 🛡️
> **See the Problem. Bridge to Action.**  
> *From a single photograph to meaningful civic action — powered by autonomous AI agents.*

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/tirth080904-cse/NazarSetu)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template?template=https%3A%2F%2Fgithub.com%2Ftirth080904-cse%2FNazarSetu)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tirth080904-cse-nazarsetu-app-94zmc9.streamlit.app/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### 🌐 Live Cloud Web Application:
- **Render Cloud Service (Independent Cloud Host):** 👉 **[Deploy 1-Click to Render](https://render.com/deploy?repo=https://github.com/tirth080904-cse/NazarSetu)**
- **Railway Cloud App:** 👉 **[Deploy 1-Click to Railway](https://railway.app/template?template=https%3A%2F%2Fgithub.com%2Ftirth080904-cse%2FNazarSetu)**
- **Streamlit Cloud Web App:** 👉 **[Launch NazarSetu Live Web App](https://tirth080904-cse-nazarsetu-app-94zmc9.streamlit.app/)**

**Category:** Agentic AI / Smart Cities / Civic Intelligence & Autonomous Action  
**Edition:** Autonomous Civic Intelligence Platform (v2.0 Hackathon Edition)  
**Tech Stack:** Python 3.11+, Streamlit, OpenAI Multimodal API & Function Calling, SQLite, Pillow, Pandas, Altair, Zero-Dependency i18n

---

## 🌟 Overview

**NazarSetu (नज़रसेतु)** transforms ordinary civic complaint systems into an **autonomous civic intelligence loop**. Rather than functioning as a passive drop-box, NazarSetu actively diagnoses physical evidence, evaluates citizen safety impact, coordinates with municipal ward registers, executes genuine Python tool calls across a 10-stage timeline, and visually verifies physical repairs before closing tickets with human-in-the-loop governance.

---

## 🏗️ Architecture

```
nazarsetu/
├── app.py                  # Main Streamlit Web Application (7 Product Views)
├── agent.py                # Autonomous Agent Loop, Tool Calling & Action Trail
├── vision.py               # Multimodal Civic Intelligence Engine & CivicTwin Analyzer
├── tools.py                # 9 Autonomous Agent Tools (ward lookup, routing, duplicate check, pulse stats)
├── database.py             # SQLite Persistence, CivicTwin Verifications & Event Timelines
├── config.py               # Heuristics, Priority Rules, Citizen Impact Presets & Constants
├── components.py           # Smart City Command Center UI & SaaS Design System
├── i18n.py                 # Multilingual Accessibility Engine (English, Hindi, Gujarati)
├── data/
│   ├── demo_wards.csv      # Fictional Ward Jurisdiction Dataset
│   ├── nazarsetu.db        # SQLite Persistent Storage
│   └── samples/            # Pre-configured 1-Click Demo Scenarios (Pothole, Garbage, etc.)
├── tests/
│   ├── test_core.py        # 14 Core Automated Unit Tests
│   ├── test_demo_flow.py   # Full End-to-End Autonomous Lifecycle Test
│   └── test_enhancements.py# 7 Comprehensive Tests for New Intelligence Features
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Key Innovation Features

### 1. Civic Intelligence Engine
When a photograph is uploaded, the multimodal AI performs in-depth civic diagnostic reasoning:
- **Multimodal Severity Rating:** Low, Medium, High, and Critical tiers based on municipal engineering standards.
- **Projected Citizen Impact:** Evaluates dangers to pedestrians, two-wheelers, school children, and elderly residents.
- **Transparent Priority Decision Rationale:** Explains exactly why an issue received its priority based on documented safety heuristics.
- **Recommended Action Plan & SLA:** Specific technical guidance and target turnaround hours for the responsible department.

### 2. AI Civic Mission Control (10-Stage Pipeline)
A verifiable command center timeline tracking genuine model tool executions:
- **Stage 1:** Evidence Ingestion & Cryptographic SHA-256 Hashing
- **Stage 2:** Multimodal Civic Issue Classification
- **Stage 3:** Severity & Citizen Impact Evaluation
- **Stage 4:** Geographic Coordinate & Locality Verification
- **Stage 5:** Municipal Ward & Jurisdiction Lookup
- **Stage 6:** Operational Department Selection & Routing
- **Stage 7:** Smart Duplicate Shield Search
- **Stage 8:** Human-in-the-Loop Affirmative Authorization
- **Stage 9:** Persistent Database Registration (`NS-DEMO-XXXXXXXX`)
- **Stage 10:** Real-Time Lifecycle Tracking Activated

### 3. CivicTwin (Before & After Resolution Verification)
Eliminates false "resolved" claims:
- Inspects post-repair evidence photos side-by-side with initial complaint photos.
- Computes AI Verification Score, detection delta, and a 3-point quality assurance checklist (hazard cleared, surface leveled, debris removed).
- **Strict Human-in-the-Loop Governance:** AI verification is advisory; affirmative officer approval is mandatory before any ticket is formally closed.

### 4. Neighborhood Pulse (Grounded Municipal Telemetry)
- Real-time community health dashboard calculated **strictly from SQLite database records** (zero hallucinated statistics).
- 5 Live KPI cards: Total Filed, Active Pending, In Progress, Awaiting Verification, and Resolution Rate %.
- Interactive distribution charts by category and locality.
- Grounded AI Executive Summary summarizing verified neighborhood metrics.

### 5. Smart Duplicate Shield
- Matches image SHA-256 hashes and category/locality clusters against active complaints.
- Alerts citizens with existing Tracking IDs and lets them either link to the open ticket or file an independent incident.

### 6. 5-Stage Complaint Journey
Full visual lifecycle progression:
`Reported` ➔ `Assigned` ➔ `In Progress` ➔ `Awaiting Verification` ➔ `Resolved`

### 7. Multilingual Accessibility Engine
Native, high-performance dictionary translation engine with zero external dependencies supporting:
- **English** (`en`)
- **हिंदी / Hindi** (`hi`)
- **ગુજરાતી / Gujarati** (`gu`)

---

## 🛠️ Installation & Quickstart

### Prerequisites
- Python 3.11+
- Git

### 1. Setup Virtual Environment
```bash
git clone <repo-url> NazarSetu
cd NazarSetu

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Add your OpenAI API key for real vision & tool-calling agent capabilities:
```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```
> **Note on Fallback Mode:** If no API key is provided, NazarSetu automatically runs in **Offline Fallback Mode** with deterministic tool execution and local heuristic image analysis. All tools, databases, and UI workflows remain 100% operational!

### 3. Run Automated Tests
```bash
pytest tests/test_core.py -v
```
*(All 12 tests pass verifying routing, lookup, database persistence, timelines, duplicate guard, and error handling).*

### 4. Launch Application
```bash
streamlit run app.py
```
Open your browser to `http://localhost:8501`.

---

## ⏱️ 90-Second Hackathon Presentation Script

- **[0:00 - 0:15] The Hook:** *"Judges, everyday citizens see potholes, overflowing bins, and broken streetlights, but reporting them is frustrating, opaque, and often leads nowhere. Meet **NazarSetu** — See the Problem, Bridge to Action."*
- **[0:15 - 0:35] Scene 1: Autonomous Vision & Issue DNA:** *(Click '🕳️ Pothole' from the sidebar, then 'Analyze Issue').* *"A citizen simply uploads a photo. NazarSetu doesn't just describe the image. Our agent extracts **Issue DNA**: identifying deep crater depth, calculating High priority based on vehicular safety rules, and routing jurisdiction to the Indiranagar East ward."*
- **[0:35 - 0:50] Scene 2: Verifiable Agent Action Trail:** *(Scroll to the Action Trail).* *"Notice this isn't hardcoded text. The agent autonomously executed four real Python tools: `select_department`, `find_responsible_ward`, `check_duplicate`, and SHA-256 signature hashing. Every step is an auditable municipal event."*
- **[0:50 - 1:10] Scene 3: Confirmed Registration:** *(Check confirmation box, click 'Confirm & Register Complaint').* *"With explicit citizen consent, the agent registers the complaint in SQLite, generating tracking ID `NS-DEMO-XXXXXXXX`."*
- **[1:10 - 1:25] Scene 4: Conversational Tracking & Live Persistence:** *(Open 'Tracking Assistant' tab, click 'Check NS-DEMO-A101B202').* *"Citizens ask natural questions. The agent calls `get_complaint_status` to show a clean 3-stage progress bar."*
- **[1:25 - 1:30] Scene 5: The Punchline:** *(Open 'Admin Command Center', change status to 'Resolved', re-query in Tracking Assistant).* *"When the municipal team updates the status, the AI assistant immediately reflects it from the database. Real understanding. Real tool execution. Real civic impact."*

---

## ⚖️ Hackathon MVP Limitations & Disclaimers

1. **Fictional Ward Dataset:** Ward IDs (e.g. `DEMO-WARD-BLR-074`) and nodal officer names are demonstration fixtures and do not correspond to active municipal rosters.
2. **No Official Municipal Dispatch:** This prototype stores records locally in SQLite (`data/nazarsetu.db`). No government municipal APIs or emergency services were contacted.
3. **Tracking ID Format:** All generated tracking numbers use the prefix `NS-DEMO-` to avoid confusion with official municipal grievance numbers.
4. **Human-in-the-Loop:** Citizen review and affirmative confirmation are strictly enforced before any complaint is registered in the database.
