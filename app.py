"""
NazarSetu — Civic Intelligence & Autonomous Action Platform.

Main Streamlit Application featuring:
- 🌐 Overview: Architectural blueprint & civic agent mission
- 📸 Report Issue: Civic Intelligence Engine, Smart Duplicate Shield & Human Affirmation
- 🚀 AI Mission Control: 10-Stage live tool execution timeline
- 🔍 Track Complaint: Autonomous conversational assistant with 5-stage lifecycle journey
- ♊ CivicTwin: Multimodal before/after resolution verification with officer sign-off
- 📊 Neighborhood Pulse: Grounded real-time municipal analytics from SQLite
- 🛡️ Demo Admin: Municipal dispatch and status command center
"""

import os
import json
from pathlib import Path
from PIL import Image
import pandas as pd
import streamlit as st

from config import (
    SUPPORTED_CATEGORIES,
    VALID_STATUSES,
    STATUS_PENDING,
    STATUS_IN_PROGRESS,
    STATUS_RESOLVED,
    DEMO_WARDS_CSV,
    DB_PATH,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    COMPLAINT_STAGES,
)
import database
import tools
import vision
import agent
import components
from i18n import t

# Page Configuration
st.set_page_config(
    page_title="NazarSetu — Civic Intelligence & Autonomous Action Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize database schema and demo records
database.seed_demo_complaints()

# Initialize session state variables
if "lang" not in st.session_state:
    st.session_state.lang = "en"

if "action_trail" not in st.session_state:
    st.session_state.action_trail = agent.ActionTrail()

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": (
                "Namaste! I am the **NazarSetu Autonomous Civic Assistant**. "
                "How may I assist you today? You can ask me to track an existing complaint "
                "(e.g., `NS-DEMO-A101B202`), check municipal department routing, "
                "or review neighborhood resolution statistics."
            )
        }
    ]

if "last_registered_id" not in st.session_state:
    st.session_state.last_registered_id = None

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "pipeline_state" not in st.session_state:
    st.session_state.pipeline_state = None

sample_dir = Path(__file__).resolve().parent / "data" / "samples"

# Sidebar: Language Switcher, System Operational Status & Demo Controls
with st.sidebar:
    st.markdown("### 🌐 Language / भाषा / ભાષા")
    lang_choice = st.radio(
        "Select Language",
        options=["English", "हिंदी (Hindi)", "ગુજરાતી (Gujarati)"],
        index=0 if st.session_state.lang == "en" else (1 if st.session_state.lang == "hi" else 2),
        label_visibility="collapsed"
    )
    if "हिंदी" in lang_choice:
        st.session_state.lang = "hi"
    elif "ગુજરાતી" in lang_choice:
        st.session_state.lang = "gu"
    else:
        st.session_state.lang = "en"

    lang = st.session_state.lang

    st.markdown("---")
    st.markdown("### 🏛️ Operational Engine")
    if vision.is_openai_configured():
        st.success(f"🟢 **AI Engine:** Online\nModel: `{OPENAI_MODEL}`")
    else:
        st.info("🟡 **AI Engine:** Offline / Local Fallback Active\n(Deterministic Heuristics + SQLite)")

    st.markdown("---")
    st.markdown("### ⚡ Quick Demo Scenarios")
    st.caption("Load verified test cases for instant evaluation:")

    s_col1, s_col2 = st.columns(2)
    if s_col1.button("🕳️ Pothole", use_container_width=True):
        st.session_state.selected_sample = "sample_pothole.jpg"
        st.session_state.sample_hint = "Potholes and damaged roads"
        st.session_state.sample_city = "Bengaluru"
        st.session_state.sample_locality = "Indiranagar"
        st.rerun()

    if s_col2.button("🗑️ Garbage", use_container_width=True):
        st.session_state.selected_sample = "sample_garbage.jpg"
        st.session_state.sample_hint = "Overflowing garbage"
        st.session_state.sample_city = "Mumbai"
        st.session_state.sample_locality = "Bandra West"
        st.rerun()

    s_col3, s_col4 = st.columns(2)
    if s_col3.button("💡 Streetlight", use_container_width=True):
        st.session_state.selected_sample = "sample_streetlight.jpg"
        st.session_state.sample_hint = "Broken streetlights"
        st.session_state.sample_city = "Delhi"
        st.session_state.sample_locality = "Connaught Place"
        st.rerun()

    if s_col4.button("🌊 Drainage", use_container_width=True):
        st.session_state.selected_sample = "sample_waterlogging.jpg"
        st.session_state.sample_hint = "Waterlogging and drainage issues"
        st.session_state.sample_city = "Ahmedabad"
        st.session_state.sample_locality = "Satellite"
        st.rerun()

    if st.button("🐱 Non-Civic Image (Pet)", use_container_width=True):
        st.session_state.selected_sample = "sample_non_civic.jpg"
        st.session_state.sample_hint = "Non-Civic"
        st.session_state.sample_city = "Pune"
        st.session_state.sample_locality = "Kothrud"
        st.rerun()

    st.markdown("---")
    st.markdown("### 📋 Sample Tracking IDs")
    st.code("NS-DEMO-A101B202\nNS-DEMO-C303D404\nNS-DEMO-E505F606", language="text")

    st.markdown("---")
    st.caption("NazarSetu v2.0 • Civic Intelligence Command Center")

# Render Smart City Command Center Header & Hackathon Disclaimer
components.render_header(lang=st.session_state.lang)
components.render_disclaimer(lang=st.session_state.lang)

# Main Navigation Tabs
tab_overview, tab_report, tab_mission, tab_track, tab_civictwin, tab_pulse, tab_admin = st.tabs([
    t("nav_overview", lang),
    t("nav_report", lang),
    t("nav_mission_control", lang),
    t("nav_track", lang),
    t("nav_civictwin", lang),
    t("nav_neighborhood_pulse", lang),
    t("nav_admin", lang),
])


# ==============================================================================
# TAB 1: OVERVIEW & ARCHITECTURAL BLUEPRINT
# ==============================================================================
with tab_overview:
    st.markdown("## 🌐 The Autonomous Civic Intelligence & Action Platform")
    st.markdown(
        "NazarSetu transforms ordinary citizen complaints into an **autonomous civic intelligence loop**. "
        "Unlike conventional complaint portals that act as passive inboxes, NazarSetu actively diagnoses severity, "
        "evaluates safety risk, coordinates with ward jurisdictions, and verifies physical repairs."
    )

    # Core Innovation Pillars
    st.markdown("### 💎 Why NazarSetu is Uniquely Innovative")
    p_col1, p_col2, p_col3 = st.columns(3)
    
    with p_col1:
        components.render_html("""
            <div class="intel-item" style="border-top: 4px solid #0EA5E9; height: 100%;">
                <div class="intel-label" style="color: #0284C7;">1. Civic Intelligence Engine</div>
                <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 6px; color: #0A1128;">
                    Multimodal Impact & Severity
                </div>
                <div style="font-size: 0.88rem; color: #475569; line-height: 1.45;">
                    Goes far beyond object detection. Analyzes citizen impact (pedestrians, vehicles, elderly),
                    computes rule-based transparent safety heuristics, and generates dynamic departmental action plans.
                </div>
            </div>
        """)

    with p_col2:
        components.render_html("""
            <div class="intel-item" style="border-top: 4px solid #F59E0B; height: 100%;">
                <div class="intel-label" style="color: #D97706;">2. AI Civic Mission Control</div>
                <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 6px; color: #0A1128;">
                    10-Stage Verifiable Pipeline
                </div>
                <div style="font-size: 0.88rem; color: #475569; line-height: 1.45;">
                    Live command center timeline showing genuine Python tool invocations, SHA-256 evidence hashing,
                    ward coordinate matching, and strict affirmative citizen authorization.
                </div>
            </div>
        """)

    with p_col3:
        components.render_html("""
            <div class="intel-item" style="border-top: 4px solid #8B5CF6; height: 100%;">
                <div class="intel-label" style="color: #7C3AED;">3. CivicTwin AI Verification</div>
                <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 6px; color: #0A1128;">
                    Before & After Proof Verification
                </div>
                <div style="font-size: 0.88rem; color: #475569; line-height: 1.45;">
                    Inspects repair completion side-by-side with original photos. Checks road leveling, debris removal,
                    and enforces strict human-in-the-loop sign-off before closing tickets.
                </div>
            </div>
        """)

    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
    p_col4, p_col5, p_col6 = st.columns(3)

    with p_col4:
        components.render_html("""
            <div class="intel-item" style="border-top: 4px solid #10B981; height: 100%;">
                <div class="intel-label" style="color: #059669;">4. Neighborhood Pulse Analytics</div>
                <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 6px; color: #0A1128;">
                    Grounded SQLite Metrics
                </div>
                <div style="font-size: 0.88rem; color: #475569; line-height: 1.45;">
                    Real-time community telemetry grounded strictly in authentic municipal database rows.
                    Zero hallucinated city statistics. Real turnaround rates and localized issue distribution.
                </div>
            </div>
        """)

    with p_col5:
        components.render_html("""
            <div class="intel-item" style="border-top: 4px solid #EF4444; height: 100%;">
                <div class="intel-label" style="color: #DC2626;">5. Smart Duplicate Shield</div>
                <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 6px; color: #0A1128;">
                    Cluster & Signature Matching
                </div>
                <div style="font-size: 0.88rem; color: #475569; line-height: 1.45;">
                    Prevents municipal system clutter by matching image hashes and locality clusters.
                    Gives citizens full transparency to link to existing tickets or file distinct reports.
                </div>
            </div>
        """)

    with p_col6:
        components.render_html("""
            <div class="intel-item" style="border-top: 4px solid #6366F1; height: 100%;">
                <div class="intel-label" style="color: #4F46E5;">6. Multilingual Accessibility</div>
                <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 6px; color: #0A1128;">
                    Tri-Lingual Native Support
                </div>
                <div style="font-size: 0.88rem; color: #475569; line-height: 1.45;">
                    Built for true civic inclusion across India with native English, Hindi (हिंदी),
                    and Gujarati (ગુજરાતી) dictionary engines with zero external dependencies.
                </div>
            </div>
        """)

    # Comparison Table
    st.markdown("---")
    st.markdown("### ⚖️ Ordinary Complaint Portals vs. NazarSetu Platform")
    comparison_data = {
        "Feature Capability": [
            "Input Processing",
            "Classification Depth",
            "Urgency & Priority",
            "Duplicate Detection",
            "Citizen Authority",
            "Resolution Verification",
            "Operational Transparency",
            "Analytics Grounding"
        ],
        "Standard Municipal Portals": [
            "Text box or static photo upload",
            "Manual citizen category pick-list",
            "Default low/medium queue without reasoning",
            "None (thousands of duplicate tickets)",
            "Submit and hope someone reads it",
            "Unilateral manual 'Resolved' checkbox",
            "Black-box administrative silence",
            "Static periodic PDF reports"
        ],
        "🛡️ NazarSetu Autonomous Platform": [
            "Multimodal Vision AI + Cryptographic Hashing",
            "Civic Intelligence Engine with visible evidence DNA",
            "Rule-based safety heuristics & citizen impact modeling",
            "Smart Duplicate Shield with image & locality clustering",
            "Full citizen review & affirmative consent override",
            "CivicTwin AI side-by-side inspection + Officer sign-off",
            "AI Mission Control: 10-stage verifiable tool logs",
            "Neighborhood Pulse: Real-time SQLite telemetry"
        ]
    }
    st.table(pd.DataFrame(comparison_data))


# ==============================================================================
# TAB 2: CITIZEN REPORTING STUDIO & CIVIC INTELLIGENCE ENGINE
# ==============================================================================
with tab_report:
    st.markdown("### 📸 Citizen Reporting Studio & Civic Intelligence Engine")
    st.write(
        "Upload a photograph of any municipal infrastructure defect. Our autonomous Civic Intelligence Engine "
        "analyzes evidence, models citizen safety impact, routes to the responsible department, and verifies authenticity."
    )

    # Location Selectors
    wards_df = pd.read_csv(DEMO_WARDS_CSV)
    cities = sorted(wards_df["city"].unique().tolist())

    col_loc1, col_loc2, col_loc3 = st.columns([1, 1, 1.5])
    default_city_idx = 0
    if "sample_city" in st.session_state and st.session_state.sample_city in cities:
        default_city_idx = cities.index(st.session_state.sample_city)

    with col_loc1:
        selected_city = st.selectbox("Select Municipal Corporation / City", cities, index=default_city_idx)

    localities_for_city = sorted(wards_df[wards_df["city"] == selected_city]["locality"].unique().tolist())
    default_loc_idx = 0
    if "sample_locality" in st.session_state and st.session_state.sample_locality in localities_for_city:
        default_loc_idx = localities_for_city.index(st.session_state.sample_locality)

    with col_loc2:
        selected_locality = st.selectbox("Select Locality / Ward", localities_for_city, index=default_loc_idx)

    with col_loc3:
        landmark_input = st.text_input("Landmark or Street Coordinate", placeholder="e.g. Near Metro Pillar 84, Indiranagar 100ft Road")

    # Image Evidence Upload
    col_img_up, col_img_prev = st.columns([1.2, 1])
    with col_img_up:
        uploaded_file = st.file_uploader(
            "Upload Evidence Photograph (JPG, PNG)",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear photo of road damage, garbage pile, broken streetlight, or drainage overflow."
        )

        image_bytes = None
        if uploaded_file is not None:
            image_bytes = uploaded_file.getvalue()
        elif "selected_sample" in st.session_state:
            sample_path = sample_dir / st.session_state.selected_sample
            if sample_path.exists():
                with open(sample_path, "rb") as f:
                    image_bytes = f.read()
                st.info(f"Loaded Pre-configured Demo Sample: `{st.session_state.selected_sample}`")

    with col_img_prev:
        if image_bytes:
            st.image(image_bytes, caption="Uploaded Photographic Evidence", use_column_width=True)
            image_hash = tools.compute_image_hash(image_bytes)
            st.caption(f"SHA-256 Signature: `{image_hash[:24]}...`")
        else:
            components.render_html("""
                <div style="border: 2px dashed #CBD5E1; border-radius: 12px; padding: 40px; text-align: center; color: #94A3B8;">
                    📷 Photo preview will appear here.<br>Select a scenario from the sidebar or upload your own image.
                </div>
            """)

    # Trigger Autonomous Inspection Button
    analyze_btn_col, _ = st.columns([1.2, 2.8])
    with analyze_btn_col:
        analyze_clicked = st.button("🚀 Analyze with Civic Intelligence", type="primary", use_container_width=True, disabled=image_bytes is None)

    if analyze_clicked and image_bytes:
        with st.spinner("🤖 Autonomous Civic Intelligence Engine diagnosing evidence and querying municipal registers..."):
            hint = st.session_state.get("sample_hint")
            analysis = vision.analyze_issue(image_bytes, hint_category=hint)
            st.session_state.analysis_result = analysis

            if not analysis.get("is_civic_issue", True):
                st.error("🚫 **Non-Civic Submission Rejected:** The AI inspected the image and determined it does not depict a municipal infrastructure defect.")
                st.info("NazarSetu specifically addresses public civic hazards (potholes, garbage, streetlights, drainage).")
                st.session_state.pipeline_state = None
            else:
                issue_type = analysis.get("issue_type")
                pipeline_state, trail = agent.run_reporting_agent_pipeline(
                    issue_type=issue_type,
                    city=selected_city,
                    locality=selected_locality,
                    image_hash=image_hash,
                    landmark=landmark_input,
                )
                pipeline_state["image_bytes"] = image_bytes
                pipeline_state["analysis"] = analysis
                st.session_state.pipeline_state = pipeline_state

                # Record steps in session action trail
                for s in trail.get_steps():
                    st.session_state.action_trail.record_step(
                        stage_number=s.get("stage_number"),
                        tool_name=s["tool_name"],
                        title=s["title"],
                        explanation=s["explanation"],
                        input_args=s["input_args"],
                        output_result=s["output_result"],
                        status=s["status"],
                    )

    # Render Civic Intelligence Output and Review Area
    if st.session_state.pipeline_state:
        p_state = st.session_state.pipeline_state
        analysis = p_state.get("analysis", {})

        st.markdown("---")
        # Render the full Civic Intelligence Engine Report
        components.render_civic_intelligence_report(
            report_data=analysis,
            locality=p_state.get("locality"),
            city=p_state.get("city"),
            lang=lang,
        )

        # Smart Duplicate Shield Alert
        dup_check = p_state.get("duplicate_check", {})
        if dup_check.get("is_duplicate"):
            dup_id = dup_check.get("existing_complaint_id")
            dup_status = dup_check.get("existing_status")
            st.warning(f"""
                🛡️ **Smart Duplicate Shield Alert:** A matching unresolved complaint (**{dup_id}**)
                already exists in **{p_state.get('locality')}** with status **{dup_status.upper()}**.
            """)
            dup_c1, dup_c2 = st.columns([1, 1.5])
            with dup_c1:
                if st.button(f"🔍 Inspect Existing Ticket ({dup_id})", use_container_width=True):
                    st.session_state.chat_messages.append({"role": "user", "content": f"Track complaint {dup_id}"})
                    st.info(f"Navigate to Track Complaint tab to follow {dup_id}.")
            with dup_c2:
                st.caption("You may still proceed below if this represents an independent, distinct hazard.")

        # Citizen Authority & Review Area
        st.markdown("#### ✏️ Citizen Review & Override Authority")
        st.caption("Human agency is paramount: You have full authority to confirm or adjust the AI's classification.")

        rev_col1, rev_col2, rev_col3 = st.columns([1.5, 1, 1])
        with rev_col1:
            corrected_category = st.selectbox(
                "Verify Issue Category",
                SUPPORTED_CATEGORIES,
                index=SUPPORTED_CATEGORIES.index(p_state["issue_type"]) if p_state["issue_type"] in SUPPORTED_CATEGORIES else 0
            )
        with rev_col2:
            corrected_priority = st.selectbox(
                "Priority Level",
                ["Critical", "High", "Medium", "Low"],
                index=["Critical", "High", "Medium", "Low"].index(analysis.get("suggested_priority", "High"))
            )
        with rev_col3:
            assigned_dept = tools.select_department(corrected_category).get("department")
            st.text_input("Assigned Nodal Department", value=assigned_dept, disabled=True)

        corrected_desc = st.text_area(
            "Incident Description",
            value=analysis.get("suggested_description", f"Civic issue reported in {p_state['locality']}."),
            height=90
        )

        # Mandatory Citizen Affirmative Confirmation Checkbox
        st.markdown("---")
        st.markdown("#### 🛡️ Affirmative Citizen Authorization")
        confirm_checkbox = st.checkbox(
            "I explicitly confirm that the above details and photographic evidence represent an authentic civic issue.",
            value=False
        )

        sub_col1, _ = st.columns([1.2, 2.8])
        with sub_col1:
            register_btn = st.button("✅ Authorize & Commit Complaint", type="primary", use_container_width=True, disabled=not confirm_checkbox)

        if register_btn:
            if not confirm_checkbox:
                st.error("Citizen confirmation is mandatory before registering.")
            else:
                uncertainties = analysis.get("uncertainty_flags", [])
                uncertainty_str = "; ".join(uncertainties) if uncertainties else "No visual uncertainties flagged."
                ai_mode_val = "AI_VERIFIED" if analysis.get("mode") == "openai_vision" else "FALLBACK_MANUAL"

                confirmed_payload = {
                    "confirmed": True,
                    "idempotency_key": database.generate_idempotency_key(p_state["image_hash"]),
                    "issue_type": corrected_category,
                    "description": corrected_desc,
                    "city": p_state["city"],
                    "locality": p_state["locality"],
                    "ward": p_state.get("ward", "Demo Ward"),
                    "department": assigned_dept,
                    "image_hash": p_state["image_hash"],
                    "priority": corrected_priority,
                    "status": "Reported",
                    "landmark": p_state.get("landmark", ""),
                    "visual_evidence": analysis.get("visual_evidence"),
                    "uncertainty_notes": uncertainty_str,
                    "ai_mode": ai_mode_val,
                }
                reg_res, reg_trail = agent.run_registration_agent_action(confirmed_payload)

                # Record registration stages in session action trail
                for s in reg_trail.get_steps():
                    st.session_state.action_trail.record_step(
                        stage_number=s.get("stage_number"),
                        tool_name=s["tool_name"],
                        title=s["title"],
                        explanation=s["explanation"],
                        input_args=s["input_args"],
                        output_result=s["output_result"],
                        status=s["status"],
                    )

                if reg_res.get("status") == "registered":
                    complaint_id = reg_res.get("complaint_id")
                    st.session_state.last_registered_id = complaint_id
                    st.success(f"🎉 **Complaint Successfully Registered with Municipal Authorities!**")
                    st.balloons()

                    components.render_html(f"""
                        <div class="intelligence-card" style="border-left: 6px solid #10B981;">
                            <h3 style="margin-top: 0; color: #065F46;">🏛️ Official Municipal Tracking Pass</h3>
                            <p style="font-size: 1.25rem; font-weight: 800; color: #0A1128;">
                                Tracking ID: <code style="color: #0284C7; font-size: 1.25rem;">{complaint_id}</code>
                            </p>
                            <p><strong>Responsible Authority:</strong> {assigned_dept}<br>
                            <strong>Jurisdiction Ward:</strong> {p_state.get('ward')} ({p_state.get('locality')}, {p_state.get('city')})<br>
                            <strong>Lifecycle Status:</strong> <span class="badge-pill badge-medium">REPORTED</span></p>
                            <p style="font-size: 0.9rem; color: #64748B;">
                                Track this complaint in real-time under <strong>Track Complaint</strong> or verify its resolution in <strong>CivicTwin</strong>.
                            </p>
                        </div>
                    """)


# ==============================================================================
# TAB 3: AI CIVIC MISSION CONTROL (10-STAGE VERIFIABLE PIPELINE)
# ==============================================================================
with tab_mission:
    st.markdown("## 🚀 AI Civic Mission Control — Autonomous Action Pipeline")
    st.markdown(
        "Inspect the complete, transparent **10-stage execution pipeline** of NazarSetu. "
        "Every stage executes genuine Python tool calls, logs cryptographic signatures, and provides full inspectable payloads."
    )

    top_m1, top_m2 = st.columns([3, 1])
    with top_m2:
        if st.button("🗑️ Reset Mission Control Logs"):
            st.session_state.action_trail.clear()
            st.rerun()

    components.render_mission_control_dashboard(st.session_state.action_trail.get_steps(), lang=lang)


# ==============================================================================
# TAB 4: AUTONOMOUS COMPLAINT TRACKING ASSISTANT
# ==============================================================================
with tab_track:
    st.markdown("## 🔍 Conversational Civic Intelligence Assistant")
    st.markdown(
        "Chat with our autonomous municipal agent. The assistant uses real database tools to track complaint lifecycles, "
        "explain department jurisdictions, and retrieve verified neighborhood metrics."
    )

    # Quick Inquiries Pills
    st.markdown("**Quick Inquiries:**")
    q_col1, q_col2, q_col3, q_col4 = st.columns(4)
    quick_query = None

    with q_col1:
        if st.button("Check NS-DEMO-A101B202", use_container_width=True):
            quick_query = "What is the status of complaint NS-DEMO-A101B202?"
    with q_col2:
        if st.button("Check NS-DEMO-C303D404", use_container_width=True):
            quick_query = "Where is complaint NS-DEMO-C303D404 and who is handling it?"
    with q_col3:
        if st.button("Check NS-DEMO-E505F606", use_container_width=True):
            quick_query = "Is complaint NS-DEMO-E505F606 resolved?"
    with q_col4:
        if st.session_state.last_registered_id:
            if st.button(f"Track {st.session_state.last_registered_id}", use_container_width=True):
                quick_query = f"Track my complaint {st.session_state.last_registered_id}"
        else:
            if st.button("Ask Dept for Potholes", use_container_width=True):
                quick_query = "Which department handles potholes?"

    # Render Chat History
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "status" in msg:
                components.render_complaint_journey({"status": msg["status"]})
            if "timeline" in msg and msg["timeline"]:
                with st.expander("📜 View Audit Timeline Events", expanded=False):
                    for ev in msg["timeline"]:
                        st.markdown(f"- **{ev['created_at']}** — `[{ev['event_type']}]`: {ev['details']}")

    # Chat Input Box
    user_prompt = st.chat_input("Ask about a complaint (e.g., 'What is the status of NS-DEMO-A101B202?' or 'Show neighborhood stats')")
    if quick_query:
        user_prompt = quick_query

    if user_prompt:
        st.session_state.chat_messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("🤖 Consulting municipal registers via agent tools..."):
                response = agent.run_tracking_chat_agent(
                    user_message=user_prompt,
                    chat_history=st.session_state.chat_messages,
                    trail=st.session_state.action_trail,
                )

                reply_text = response.get("reply", "Unable to retrieve municipal records.")
                st.markdown(reply_text)

                msg_record = {"role": "assistant", "content": reply_text}

                if response.get("complaint_data"):
                    c_status = response["complaint_data"].get("current_status", "Reported")
                    components.render_complaint_journey({"status": c_status})
                    msg_record["status"] = c_status

                if response.get("timeline_data"):
                    events = response["timeline_data"]
                    msg_record["timeline"] = events
                    with st.expander("📜 View Full Audit Timeline Events", expanded=False):
                        for ev in events:
                            st.markdown(f"- **{ev['created_at']}** — `[{ev['event_type']}]`: {ev['details']}")

                st.session_state.chat_messages.append(msg_record)


# ==============================================================================
# TAB 5: CIVICTWIN RESOLUTION VERIFICATION
# ==============================================================================
with tab_civictwin:
    st.markdown("## ♊ CivicTwin — Before & After Resolution Verification")
    st.markdown(
        "CivicTwin verifies whether reported municipal defects have truly been fixed. "
        "By comparing the original citizen photograph against post-resolution proof, the AI inspects "
        "surface leveling, hazard mitigation, and debris clearance. "
        "**Strict Governance:** Municipal officer confirmation is required before any ticket is formally resolved."
    )

    # Fetch active complaints
    all_complaints = database.list_complaints(limit=50)
    unresolved_complaints = [c for c in all_complaints if c["status"] != STATUS_RESOLVED]
    complaint_options = [c["id"] for c in unresolved_complaints] or [c["id"] for c in all_complaints]

    twin_col1, twin_col2 = st.columns([1.5, 1.5])
    
    with twin_col1:
        target_twin_id = st.selectbox("Select Complaint Ticket to Inspect", complaint_options) if complaint_options else None
        target_twin_obj = database.get_complaint(target_twin_id) if target_twin_id else None

        if target_twin_obj:
            st.markdown(f"**Ticket:** `{target_twin_id}` | **Category:** {target_twin_obj['issue_type']}")
            st.markdown(f"**Location:** {target_twin_obj['locality']}, {target_twin_obj['city']} | **Status:** `{target_twin_obj['status']}`")

            # Load before photo
            sample_before = sample_dir / "sample_pothole.jpg"
            if sample_before.exists():
                with open(sample_before, "rb") as f:
                    before_img_bytes = f.read()
                st.image(before_img_bytes, caption=f"Initial Citizen Evidence Photo ({target_twin_id})", use_column_width=True)
            else:
                before_img_bytes = b"sample_before_dummy_bytes"
                st.info("Original evidence photograph loaded.")

    with twin_col2:
        st.markdown("**Department Repair Proof Photograph (After)**")
        uploaded_after = st.file_uploader(
            "Upload Repair Completion Photo",
            type=["jpg", "jpeg", "png"],
            key="civictwin_after_upload"
        )

        after_img_bytes = None
        if uploaded_after is not None:
            after_img_bytes = uploaded_after.getvalue()
        elif st.button("Load Demo Repair Proof Photo", use_container_width=True):
            sample_after_path = sample_dir / "sample_pothole_fixed.jpg"
            if sample_after_path.exists():
                with open(sample_after_path, "rb") as f:
                    after_img_bytes = f.read()
                st.session_state.civictwin_after_bytes = after_img_bytes

        if "civictwin_after_bytes" in st.session_state and after_img_bytes is None:
            after_img_bytes = st.session_state.civictwin_after_bytes

        if after_img_bytes:
            st.image(after_img_bytes, caption="Post-Resolution Repair Proof", use_column_width=True)
        else:
            components.render_html("""
                <div style="border: 2px dashed #8B5CF6; border-radius: 12px; padding: 40px; text-align: center; color: #8B5CF6;">
                    📸 Upload or click 'Load Demo Repair Proof Photo' to run inspection.
                </div>
            """)

    if target_twin_obj and after_img_bytes and before_img_bytes:
        st.markdown("---")
        if st.button("🚀 Run CivicTwin Multimodal Verification", type="primary", use_container_width=True):
            with st.spinner("🤖 CivicTwin comparing before/after photographic topography..."):
                verification_result = vision.verify_civictwin(
                    before_image_bytes=before_img_bytes,
                    after_image_bytes=after_img_bytes,
                    original_issue=target_twin_obj["issue_type"]
                )
                st.session_state.last_civictwin_res = verification_result

                # Record verification in database
                b_hash = tools.compute_image_hash(before_img_bytes)
                a_hash = tools.compute_image_hash(after_img_bytes)
                database.insert_civictwin_verification(
                    complaint_id=target_twin_id,
                    before_hash=b_hash,
                    after_hash=a_hash,
                    verification_result=verification_result
                )

                # Log into Action Trail
                st.session_state.action_trail.record_step(
                    tool_name="verify_civictwin",
                    title=f"CivicTwin Inspection: {target_twin_id}",
                    explanation=f"Evaluated repair proof. Verification Score: {int(verification_result.get('verification_score', 0)*100)}%",
                    input_args={"complaint_id": target_twin_id},
                    output_result=verification_result,
                    status="success" if verification_result.get("resolved") else "warning"
                )

        if "last_civictwin_res" in st.session_state:
            v_res = st.session_state.last_civictwin_res
            components.render_civictwin_view(
                before_bytes=before_img_bytes,
                after_bytes=after_img_bytes,
                verification=v_res,
                lang=lang
            )

            # Strict Human-in-the-Loop Officer Sign-Off
            st.markdown("#### 🔒 Municipal Officer Formal Sign-Off")
            st.caption("AI verification is advisory. Official status closure requires affirmative municipal officer approval.")
            officer_notes = st.text_input("Officer Inspection Notes", value="Verified physical bitumen leveling meets municipal standard.")
            
            if st.button("✅ Confirm & Formally Mark Resolved", type="primary"):
                database.confirm_civictwin_resolution(target_twin_id, admin_notes=officer_notes)
                st.success(f"🎉 Ticket **{target_twin_id}** is now officially marked as **RESOLVED**!")
                st.balloons()
                st.session_state.action_trail.record_step(
                    tool_name="confirm_civictwin_resolution",
                    title=f"Officer Sign-Off & Ticket Closed: {target_twin_id}",
                    explanation=f"Municipal officer validated repair and closed ticket. Notes: {officer_notes}",
                    input_args={"complaint_id": target_twin_id, "notes": officer_notes},
                    output_result={"status": "Resolved", "actor": "MUNICIPAL_OFFICER"},
                    status="success"
                )
                st.rerun()


# ==============================================================================
# TAB 6: NEIGHBORHOOD PULSE (GROUNDED SQLITE TELEMETRY)
# ==============================================================================
with tab_pulse:
    st.markdown("## 📊 Neighborhood Pulse — Grounded Municipal Telemetry")
    st.markdown(
        "Live community health dashboard generated **strictly from SQLite database records**. "
        "Zero hallucinated city statistics. Filter by locality to inspect local resolution metrics."
    )

    pulse_f1, pulse_f2 = st.columns(2)
    with pulse_f1:
        pulse_loc = st.selectbox("Filter Telemetry by Locality", ["All Localities", "Indiranagar", "Bandra West", "Connaught Place", "Satellite", "Kothrud"])
    with pulse_f2:
        pulse_cat = st.selectbox("Filter Telemetry by Issue Type", ["All Categories"] + SUPPORTED_CATEGORIES)

    filter_loc_arg = None if pulse_loc == "All Localities" else pulse_loc
    filter_cat_arg = None if pulse_cat == "All Categories" else pulse_cat

    # Fetch verified stats
    pulse_stats = database.get_neighborhood_pulse_stats(locality=filter_loc_arg, issue_type=filter_cat_arg)
    components.render_neighborhood_pulse_dashboard(pulse_stats, lang=lang)

    st.markdown("---")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("#### 📈 Issues Reported by Category")
        top_issues_data = pulse_stats.get("top_issues", [])
        if top_issues_data:
            df_issues = pd.DataFrame(top_issues_data).set_index("issue_type")
            st.bar_chart(df_issues["count"])
        else:
            st.info("No complaint records for this filter selection.")

    with chart_col2:
        st.markdown("#### 📍 Complaints by Locality")
        top_locs_data = pulse_stats.get("localities", [])
        if top_locs_data:
            df_locs = pd.DataFrame(top_locs_data).set_index("locality")
            st.bar_chart(df_locs["count"])
        else:
            st.info("No locality records for this filter selection.")

    # Grounded AI Executive Summary
    st.markdown("---")
    st.markdown("#### 🧠 Grounded AI Municipal Intelligence Summary")
    metrics = pulse_stats.get("metrics", {})
    summary_text = (
        f"**Official Municipal Summary for {pulse_loc}:**\n"
        f"- A total of **{metrics.get('total_complaints', 0)}** civic complaints have been recorded.\n"
        f"- **{metrics.get('resolved_complaints', 0)}** tickets have been verified and resolved, achieving an active resolution rate of **{metrics.get('resolution_rate_percent', 0.0)}%**.\n"
        f"- Currently, **{metrics.get('pending_complaints', 0)}** complaints are pending initial crew dispatch, and **{metrics.get('awaiting_verification', 0)}** are awaiting CivicTwin photographic verification."
    )
    st.info(summary_text)


# ==============================================================================
# TAB 7: DEMO ADMINISTRATION COMMAND CENTER
# ==============================================================================
with tab_admin:
    st.markdown("## 🛡️ Municipal Administration Command Center")
    st.markdown("Simulate municipal officer operations: view incoming complaints, update lifecycle stages, and monitor audit trails.")

    stats = database.get_complaint_stats()
    components.render_stat_counters(stats)

    st.markdown("---")
    st.markdown("#### 🎛️ Filter Municipal Register")

    filt_c1, filt_c2, filt_c3 = st.columns(3)
    with filt_c1:
        adm_issue_filt = st.selectbox("Filter Category", ["All"] + SUPPORTED_CATEGORIES, key="adm_issue")
    with filt_c2:
        adm_dept_filt = st.selectbox("Filter Department", ["All"] + list(set(tools.DEPARTMENT_MAPPING.values())), key="adm_dept")
    with filt_c3:
        adm_status_filt = st.selectbox("Filter Lifecycle Stage", ["All"] + COMPLAINT_STAGES, key="adm_status")

    complaints_list = database.list_complaints(
        issue_type=adm_issue_filt,
        department=adm_dept_filt,
        status=adm_status_filt,
        limit=100
    )

    if not complaints_list:
        st.info("No complaint records match the selected filters.")
    else:
        df_display = pd.DataFrame(complaints_list)
        cols_to_show = [c for c in ["id", "issue_type", "city", "locality", "department", "priority", "status", "created_at"] if c in df_display.columns]
        st.dataframe(df_display[cols_to_show], use_container_width=True)

        st.markdown("---")
        st.markdown("#### 🛠️ Dispatch Lifecycle Stage Transition")
        st.caption("Advance a complaint's stage to see it immediately update in Track Complaint and Neighborhood Pulse.")

        up_col1, up_col2, up_col3 = st.columns([1.5, 1.2, 2])
        cid_options = [c["id"] for c in complaints_list]
        with up_col1:
            target_cid = st.selectbox("Select Complaint Ticket", cid_options, key="adm_target_cid")

        target_obj = next((c for c in complaints_list if c["id"] == target_cid), None)
        curr_status_val = target_obj["status"] if target_obj else "Reported"

        with up_col2:
            next_status = st.selectbox("Transition To Stage", COMPLAINT_STAGES, index=COMPLAINT_STAGES.index(curr_status_val) if curr_status_val in COMPLAINT_STAGES else 0)

        with up_col3:
            status_note = st.text_input("Operational Reason / Crew Note", placeholder="e.g. Field crew deployed with cold mix asphalt.")

        if st.button("🚀 Apply Operational Transition", type="primary"):
            success = database.update_complaint_status(
                complaint_id=target_cid,
                new_status=next_status,
                note=status_note
            )
            if success:
                st.success(f"Status for **{target_cid}** successfully advanced to **{next_status.upper()}**!")
                st.session_state.action_trail.record_step(
                    tool_name="update_complaint_status",
                    title=f"Municipal Stage Advance: {target_cid}",
                    explanation=f"Advanced from '{curr_status_val}' to '{next_status}'. Operational Note: {status_note}",
                    input_args={"complaint_id": target_cid, "new_status": next_status, "note": status_note},
                    output_result={"success": True, "updated_status": next_status},
                    status="success"
                )
                st.rerun()

        if target_cid:
            with st.expander(f"📜 View Full Event Audit Log for {target_cid}", expanded=False):
                evs = database.get_complaint_timeline(target_cid)
                for e in evs:
                    st.markdown(f"- **{e['created_at']}** — `[{e['event_type']}]`: {e['details']}")
