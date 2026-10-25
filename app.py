"""
NAZARSETU — STREETVERSE
The Autonomous Civic Intelligence & Action Platform.

Tagline: "Every Street Has a Story. Let's Change the Ending."

Complete Application-Wide Frontend Replacement:
- 🗺️ Explore City (Interactive 2.5D illustrated Indian neighborhood with live infrastructure signals)
- 📸 Report Issue (AI Photo Investigation Studio with multimodal vision & human affirmation)
- 🚀 AI Mission Control (Agent Workshop showcasing OBSERVE → ANALYZE → LOCATE → ROUTE → REGISTER)
- 🔍 Track Complaint (The Repair Story with 6 unfolding narrative chapters & AI assistant)
- ♊ CivicTwin (Transformation Studio with multimodal before/after inspection & municipal sign-off)
- 📊 Neighborhood Pulse (Localized civic memory & grounded SQLite telemetry)
- 🛡️ Civic Operations Studio (Municipal grievance administration & audit dispatch)
"""

import streamlit as st
import database
import streetverse

# Page Configuration - Single unified Streetverse interface
st.set_page_config(
    page_title="NazarSetu — Streetverse | Every Street Has a Story",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Seed database with demo records if empty
database.seed_demo_complaints()

# Initialize session state variables
if "lang" not in st.session_state:
    st.session_state.lang = "en"

if "street_active_view" not in st.session_state:
    st.session_state.street_active_view = "street"

# Render the single unified Streetverse frontend
streetverse.render_streetverse()
