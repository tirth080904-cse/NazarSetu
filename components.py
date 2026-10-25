"""
NazarSetu UI Components & Smart City Command Center Design System.

Provides custom CSS, Civic Intelligence Report cards, AI Mission Control timeline,
CivicTwin Before/After inspection, Neighborhood Pulse KPI displays, and 5-stage
Complaint Journey trackers with full multilingual accessibility.
"""

import json
import textwrap
from typing import Dict, Any, List, Optional
import streamlit as st
from config import CATEGORY_METADATA, DEMO_DISCLAIMER, COMPLAINT_STAGES
from i18n import t


CUSTOM_CSS = """
<style>
/* NazarSetu Smart City Command Center & SaaS Design System */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --navy-command: #0A1128;
    --navy-mid: #1E293B;
    --navy-light: #334155;
    --teal-glow: #0EA5E9;
    --teal-accent: #0284C7;
    --saffron-vibrant: #F59E0B;
    --saffron-light: #FEF3C7;
    --emerald-green: #10B981;
    --crimson-red: #EF4444;
    --purple-pulse: #8B5CF6;
    --card-bg: #FFFFFF;
    --card-hover: #F8FAFC;
    --text-primary: #0F172A;
    --text-secondary: #475569;
    --border-subtle: #E2E8F0;
    --border-highlight: #CBD5E1;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-primary);
}

/* Smart City Command Center Header */
.command-header {
    background: linear-gradient(135deg, #0A1128 0%, #0F172A 50%, #164E63 100%);
    padding: 1.8rem 2.2rem;
    border-radius: 16px;
    color: white;
    box-shadow: 0 12px 30px -8px rgba(10, 17, 40, 0.35);
    margin-bottom: 1.2rem;
    border-left: 6px solid var(--saffron-vibrant);
    position: relative;
    overflow: hidden;
}

.command-header::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(14, 165, 233, 0.15) 0%, transparent 70%);
    pointer-events: none;
}

.command-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(14, 165, 233, 0.18);
    border: 1px solid rgba(14, 165, 233, 0.45);
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: #38BDF8;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.command-title {
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 12px;
}

.command-tagline {
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--saffron-vibrant);
    margin: 4px 0 6px 0;
}

.command-subtitle {
    font-size: 0.92rem;
    color: #94A3B8;
    margin: 0;
    line-height: 1.45;
}

/* Disclaimer pill */
.disclaimer-banner {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 0.85rem;
    color: #1E40AF;
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1.2rem;
}

/* Civic Intelligence Report Card */
.intelligence-card {
    background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
    border: 2px solid #0EA5E9;
    border-radius: 18px;
    padding: 1.8rem;
    box-shadow: 0 10px 32px rgba(14, 165, 233, 0.12);
    margin-top: 1rem;
    margin-bottom: 1.5rem;
    position: relative;
}

.intelligence-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #E2E8F0;
    padding-bottom: 14px;
    margin-bottom: 16px;
    flex-wrap: wrap;
    gap: 10px;
}

.intelligence-title {
    font-size: 1.3rem;
    font-weight: 800;
    color: #0A1128;
    display: flex;
    align-items: center;
    gap: 10px;
}

.badge-pill {
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.badge-critical { background-color: #FEE2E2; color: #991B1B; border: 1.5px solid #F87171; }
.badge-high { background-color: #FEF3C7; color: #92400E; border: 1.5px solid #FBBF24; }
.badge-medium { background-color: #E0E7FF; color: #3730A3; border: 1.5px solid #A5B4FC; }
.badge-low { background-color: #ECFDF5; color: #065F46; border: 1.5px solid #6EE7B7; }

.intel-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
}

.intel-item {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 14px;
    transition: all 0.2s ease;
}

.intel-item:hover {
    border-color: #CBD5E1;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}

.intel-label {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    color: #64748B;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.intel-value {
    font-size: 0.95rem;
    font-weight: 600;
    color: #0F172A;
    line-height: 1.45;
}

.intel-highlight {
    background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
    border: 1px solid #86EFAC;
    border-radius: 12px;
    padding: 14px;
}

.intel-alert {
    background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
    border: 1px solid #FCD34D;
    border-radius: 12px;
    padding: 12px 14px;
    font-size: 0.85rem;
    color: #78350F;
    margin-top: 14px;
}

/* AI Mission Control 10-Stage Timeline */
.mission-stage-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #0EA5E9;
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 12px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
    position: relative;
    transition: all 0.2s;
}

.mission-stage-card:hover {
    box-shadow: 0 6px 16px rgba(14, 165, 233, 0.08);
}

.mission-stage-card.warning {
    border-left-color: #F59E0B;
}

.mission-stage-card.error {
    border-left-color: #EF4444;
}

.stage-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 6px;
    background: #0A1128;
    color: #38BDF8;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    margin-bottom: 4px;
}

.stage-title {
    font-size: 0.96rem;
    font-weight: 700;
    color: #0A1128;
    margin-bottom: 4px;
}

.stage-expl {
    font-size: 0.86rem;
    color: #475569;
    line-height: 1.4;
    margin-bottom: 6px;
}

.stage-meta {
    font-size: 0.74rem;
    font-family: 'JetBrains Mono', monospace;
    color: #64748B;
}

/* CivicTwin Comparison Box */
.civictwin-box {
    background: white;
    border: 2px solid #8B5CF6;
    border-radius: 16px;
    padding: 1.6rem;
    box-shadow: 0 10px 30px rgba(139, 92, 246, 0.08);
    margin-bottom: 1.5rem;
}

.civictwin-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #F1F5F9;
    padding-bottom: 12px;
    margin-bottom: 16px;
}

.civictwin-title {
    font-size: 1.25rem;
    font-weight: 800;
    color: #4C1D95;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* 5-Stage Complaint Journey */
.journey-tracker {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 8px;
    margin: 20px 0;
    position: relative;
}

.journey-node {
    background: white;
    border: 2px solid #CBD5E1;
    border-radius: 12px;
    padding: 10px;
    text-align: center;
    transition: all 0.3s;
}

.journey-node.active {
    border-color: #0EA5E9;
    background: #F0F9FF;
    box-shadow: 0 4px 12px rgba(14, 165, 233, 0.15);
}

.journey-node.completed {
    border-color: #10B981;
    background: #ECFDF5;
}

.journey-node .node-icon {
    font-size: 1.1rem;
    margin-bottom: 4px;
}

.journey-node .node-label {
    font-size: 0.76rem;
    font-weight: 700;
    color: #334155;
}

.journey-node.active .node-label {
    color: #0284C7;
}

.journey-node.completed .node-label {
    color: #059669;
}

/* Metric Pulse Cards */
.pulse-card {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 16px;
    text-align: center;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
    position: relative;
}

.pulse-card .metric-val {
    font-size: 2.1rem;
    font-weight: 800;
    color: #0A1128;
    line-height: 1;
    margin-bottom: 4px;
}

.pulse-card .metric-lbl {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    color: #64748B;
    letter-spacing: 0.05em;
}
</style>
"""


def render_html(html_str: str):
    """Safely dedent and render HTML in Streamlit without triggering Markdown indented code block formatting."""
    st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)


def render_header(lang: str = "en"):
    """Renders the top Smart City Command Center header."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    tagline = t("platform_tagline", lang)
    subtitle = t("platform_subtitle", lang)
    render_html(f"""
        <div class="command-header">
            <div class="command-badge">⚡ CIVIC INTELLIGENCE COMMAND CENTER v2.0 • AGENTIC SYSTEM ACTIVE</div>
            <div class="command-title">
                <span>🛡️ NazarSetu</span>
            </div>
            <div class="command-tagline">{tagline}</div>
            <div class="command-subtitle">{subtitle}</div>
        </div>
    """)


def render_disclaimer(lang: str = "en"):
    """Renders the hackathon prototype disclaimer banner."""
    render_html(f"""
        <div class="disclaimer-banner">
            <span style="font-size: 1.1rem;">ℹ️</span>
            <div><strong>{t('hackathon_disclaimer_title', lang)}:</strong> {DEMO_DISCLAIMER}</div>
        </div>
    """)


def render_civic_intelligence_report(
    report_data: Dict[str, Any],
    locality: str = "",
    city: str = "",
    lang: str = "en"
):
    """
    Renders the complete Civic Intelligence Engine Report:
    - Multimodal Severity (Low / Medium / High / Critical)
    - Projected Citizen Impact
    - Priority Decision Rationale
    - Recommended Department Action Plan
    - Visual Evidence & Confidence Score
    """
    problem = report_data.get("issue_type", "Potholes and damaged roads")
    severity = report_data.get("severity", "High")
    priority = report_data.get("suggested_priority", severity)
    citizen_impact = report_data.get("citizen_impact", "Impacting vehicular commute and pedestrian safety.")
    priority_rationale = report_data.get("priority_rationale", "Rule-based safety heuristic applied based on municipal guidelines.")
    action_plan = report_data.get("action_plan", "Dispatch repair engineer for site assessment.")
    evidence = report_data.get("visual_evidence", "Analyzed surface irregularity in road carriage.")
    confidence = report_data.get("confidence_score", 0.92)
    dept = report_data.get("recommended_department", "Roads & Infrastructure Department")
    sla = report_data.get("sla_hours", 48)
    uncertainties = report_data.get("uncertainty_flags", [])

    # Badge class
    s_lower = severity.lower()
    if "critical" in s_lower:
        badge_class = "badge-critical"
    elif "high" in s_lower:
        badge_class = "badge-high"
    elif "low" in s_lower:
        badge_class = "badge-low"
    else:
        badge_class = "badge-medium"

    meta = CATEGORY_METADATA.get(problem, {"icon": "📍", "color": "#0EA5E9"})
    location_str = f"{locality}, {city}" if (locality and city) else "Locality Selected"

    uncertainty_html = ""
    if uncertainties:
        flags_text = " • ".join(uncertainties)
        uncertainty_html = f"""
            <div class="intel-alert">
                ⚠️ <strong>Autonomous Safety Flag:</strong> {flags_text}
            </div>
        """

    html = f"""
    <div class="intelligence-card">
        <div class="intelligence-header">
            <div class="intelligence-title">
                <span>{meta['icon']} Civic Intelligence Report</span>
                <span style="font-size: 0.82rem; font-weight: 500; color: #64748B; margin-left: 8px;">
                    Model Confidence: <strong>{int(confidence * 100)}%</strong>
                </span>
            </div>
            <div style="display: flex; gap: 8px; align-items: center;">
                <span class="badge-pill {badge_class}">🚨 {severity} Severity</span>
                <span class="badge-pill" style="background: #0A1128; color: #38BDF8; border: 1px solid #38BDF8;">SLA: {sla}h</span>
            </div>
        </div>

        <div class="intel-grid">
            <div class="intel-item">
                <div class="intel-label">🏷️ Classified Civic Issue</div>
                <div class="intel-value"><strong>{problem}</strong></div>
            </div>
            <div class="intel-item">
                <div class="intel-label">📍 Geo-Locality Jurisdiction</div>
                <div class="intel-value">{location_str}</div>
            </div>
            <div class="intel-item" style="grid-column: span 2;">
                <div class="intel-label">👁️ Multimodal Visual Evidence</div>
                <div class="intel-value" style="font-size: 0.9rem; color: #334155;">{evidence}</div>
            </div>
            <div class="intel-item" style="grid-column: span 2;">
                <div class="intel-label">👥 Projected Citizen Impact</div>
                <div class="intel-value" style="font-size: 0.9rem; color: #1E293B;">{citizen_impact}</div>
            </div>
            <div class="intel-item" style="grid-column: span 2;">
                <div class="intel-label">⚖️ Safety Priority Rationale</div>
                <div class="intel-value" style="font-size: 0.88rem; color: #475569; font-style: italic;">
                    "{priority_rationale}"
                </div>
            </div>
            <div class="intel-highlight" style="grid-column: span 2;">
                <div class="intel-label" style="color: #065F46;">🛠️ Autonomous Action Plan & Nodal Target</div>
                <div class="intel-value" style="color: #064E3B; font-weight: 700;">
                    {action_plan} — <span style="text-decoration: underline;">{dept}</span>
                </div>
            </div>
        </div>
        {uncertainty_html}
    </div>
    """
    render_html(html)


def render_issue_dna(dna_data: Dict[str, Any], locality: str = "", city: str = ""):
    """Backward compatibility alias for render_civic_intelligence_report."""
    render_civic_intelligence_report(dna_data, locality=locality, city=city)


def render_mission_control_dashboard(steps: List[Dict[str, Any]], lang: str = "en"):
    """
    Renders the live 10-Stage AI Mission Control Pipeline:
    Displays each genuine Python tool execution with input parameters, output results,
    collapsible JSON inspection payloads, and transparent actor tracking.
    """
    if not steps:
        st.info("No autonomous agent actions recorded in this session yet.")
        return

    st.markdown("### 🚀 AI Civic Mission Control — Autonomous Action Trail")
    st.caption("Verifiable real-time event pipeline showing genuine tool calling, stage outputs, and human-in-the-loop sign-off.")

    for step in steps:
        stage_num = step.get("stage_number", step.get("step_number", 1))
        tool_name = step.get("tool_name", "tool")
        title = step.get("title", f"Stage {stage_num}: {tool_name}")
        expl = step.get("explanation", "")
        timestamp = step.get("timestamp", "")
        status = step.get("status", "success")
        output_result = step.get("output_result", {})
        input_args = step.get("input_args", {})

        icon = "✅"
        if status == "warning":
            icon = "⚠️"
        elif status == "error":
            icon = "❌"

        formatted_payload = json.dumps({
            "stage": stage_num,
            "tool": tool_name,
            "inputs": input_args,
            "outputs": output_result,
        }, indent=2)

        card_html = f"""
        <div class="mission-stage-card {status}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="stage-badge">STAGE {stage_num:02d} • <code>{tool_name}()</code></span>
                <span class="stage-meta">{timestamp}</span>
            </div>
            <div class="stage-title">{icon} {title}</div>
            <div class="stage-expl">{expl}</div>
        </div>
        """
        render_html(card_html)
        with st.expander(f"Inspect Stage {stage_num:02d} Tool Execution Payload (`{tool_name}`)", expanded=False):
            st.code(formatted_payload, language="json")


def render_action_trail(steps: List[Dict[str, Any]]):
    """Backward compatibility wrapper for render_mission_control_dashboard."""
    render_mission_control_dashboard(steps)


def render_civictwin_view(
    before_img,
    after_img,
    verification: Dict[str, Any],
    lang: str = "en"
):
    """
    Renders the CivicTwin Before & After Resolution Verification Interface.
    Shows side-by-side photos, verification metrics, delta detection, and admin sign-off warning.
    """
    score = verification.get("verification_score", 0.0)
    resolved = verification.get("resolved", False)
    summary = verification.get("summary", "Analysis completed.")
    checklist = verification.get("quality_checklist", {})
    delta = verification.get("delta_detected", "Resolution state examined.")

    status_badge = (
        '<span class="badge-pill badge-low">✅ REPAIR VERIFIED</span>'
        if resolved else
        '<span class="badge-pill badge-critical">⚠️ REPAIR INCOMPLETE</span>'
    )

    box_html = f"""
    <div class="civictwin-box">
        <div class="civictwin-header">
            <div class="civictwin-title">
                <span>♊ CivicTwin Autonomous Resolution Verification</span>
            </div>
            <div style="display: flex; gap: 8px; align-items: center;">
                {status_badge}
                <span class="badge-pill" style="background: #0A1128; color: #A78BFA; border: 1px solid #8B5CF6;">
                    Confidence: {int(score * 100)}%
                </span>
            </div>
        </div>

        <div style="margin-bottom: 14px;">
            <strong>Autonomous Inspection Delta:</strong>
            <p style="font-size: 0.95rem; color: #334155; margin-top: 4px; line-height: 1.45;">
                {delta}
            </p>
        </div>

        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 12px; margin-bottom: 12px;">
            <div style="font-size: 0.8rem; font-weight: 700; text-transform: uppercase; color: #64748B; margin-bottom: 6px;">
                Quality Assurance Checklist:
            </div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; font-size: 0.85rem;">
                <div>{'✅' if checklist.get('hazard_mitigated') else '❌'} Hazard Cleared</div>
                <div>{'✅' if checklist.get('surface_level_verified') else '❌'} Surface Leveled</div>
                <div>{'✅' if checklist.get('debris_cleared') else '❌'} Debris Removed</div>
            </div>
        </div>

        <div style="background: #FFFBEB; border: 1px solid #FCD34D; border-radius: 8px; padding: 10px 14px; font-size: 0.82rem; color: #92400E;">
            🔒 <strong>Strict Human-in-the-Loop Governance:</strong> CivicTwin AI analyzes photographic evidence,
            but administrative resolution is NEVER performed automatically. Municipal officer confirmation is mandatory.
        </div>
    </div>
    """
    render_html(box_html)


def render_complaint_journey(
    complaint: Dict[str, Any],
    events: Optional[List[Dict[str, Any]]] = None,
    lang: str = "en"
):
    """
    Renders the upgraded 5-Stage Complaint Journey:
    1. Reported ➔ 2. Assigned ➔ 3. In Progress ➔ 4. Awaiting Verification ➔ 5. Resolved
    """
    curr = complaint.get("status", "Reported")
    # Normalize
    if curr == "Pending":
        curr = "Reported"

    stage_order = ["Reported", "Assigned", "In Progress", "Awaiting Verification", "Resolved"]
    curr_idx = stage_order.index(curr) if curr in stage_order else 0

    icons = {
        "Reported": "📝",
        "Assigned": "🏛️",
        "In Progress": "🚧",
        "Awaiting Verification": "♊",
        "Resolved": "🎉",
    }

    nodes_html = []
    for idx, stage in enumerate(stage_order):
        if idx < curr_idx:
            cls = "journey-node completed"
            icon = "✅"
        elif idx == curr_idx:
            cls = "journey-node active"
            icon = icons.get(stage, "📍")
        else:
            cls = "journey-node"
            icon = icons.get(stage, "⚪")

        nodes_html.append(f"""
            <div class="{cls}">
                <div class="node-icon">{icon}</div>
                <div class="node-label">{stage}</div>
            </div>
        """)

    journey_html = f"""
    <div style="margin: 1.5rem 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <strong style="color: #0A1128; font-size: 0.95rem;">Official Complaint Lifecycle</strong>
            <span style="font-size: 0.8rem; font-family: 'JetBrains Mono', monospace; color: #64748B;">
                Current Stage: <strong style="color: #0284C7;">{curr.upper()}</strong>
            </span>
        </div>
        <div class="journey-tracker">
            {''.join(nodes_html)}
        </div>
    </div>
    """
    render_html(journey_html)


def render_status_tracker(current_status: str):
    """Backward compatibility wrapper for 3-stage or 5-stage tracker."""
    render_complaint_journey({"status": current_status})


def render_neighborhood_pulse_dashboard(stats: Dict[str, Any], lang: str = "en"):
    """Renders the top KPI metric cards for Neighborhood Pulse."""
    metrics = stats.get("metrics", {})
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        render_html(f"""
            <div class="pulse-card">
                <div class="metric-val">{metrics.get('total_complaints', 0)}</div>
                <div class="metric-lbl">Total Filed</div>
            </div>
        """)
    with col2:
        render_html(f"""
            <div class="pulse-card" style="border-top: 4px solid #F59E0B;">
                <div class="metric-val" style="color: #D97706;">{metrics.get('pending_complaints', 0)}</div>
                <div class="metric-lbl">Active Pending</div>
            </div>
        """)
    with col3:
        render_html(f"""
            <div class="pulse-card" style="border-top: 4px solid #3B82F6;">
                <div class="metric-val" style="color: #2563EB;">{metrics.get('in_progress_complaints', 0)}</div>
                <div class="metric-lbl">In Progress</div>
            </div>
        """)
    with col4:
        render_html(f"""
            <div class="pulse-card" style="border-top: 4px solid #8B5CF6;">
                <div class="metric-val" style="color: #7C3AED;">{metrics.get('awaiting_verification', 0)}</div>
                <div class="metric-lbl">Awaiting Twin</div>
            </div>
        """)
    with col5:
        render_html(f"""
            <div class="pulse-card" style="border-top: 4px solid #10B981;">
                <div class="metric-val" style="color: #059669;">{metrics.get('resolution_rate_percent', 0.0)}%</div>
                <div class="metric-lbl">Resolution Rate</div>
            </div>
        """)


def render_stat_counters(stats: Dict[str, int]):
    """Renders metric cards for the Admin Dashboard."""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_html(f"""
            <div class="pulse-card">
                <div class="metric-val">{stats.get('total', 0)}</div>
                <div class="metric-lbl">Total Reports</div>
            </div>
        """)
    with col2:
        render_html(f"""
            <div class="pulse-card" style="border-top: 4px solid #F59E0B;">
                <div class="metric-val" style="color: #D97706;">{stats.get('pending', 0)}</div>
                <div class="metric-lbl">Pending Action</div>
            </div>
        """)
    with col3:
        render_html(f"""
            <div class="pulse-card" style="border-top: 4px solid #3B82F6;">
                <div class="metric-val" style="color: #2563EB;">{stats.get('in_progress', 0)}</div>
                <div class="metric-lbl">In Progress</div>
            </div>
        """)
    with col4:
        render_html(f"""
            <div class="pulse-card" style="border-top: 4px solid #10B981;">
                <div class="metric-val" style="color: #059669;">{stats.get('resolved', 0)}</div>
                <div class="metric-lbl">Resolved</div>
            </div>
        """)
