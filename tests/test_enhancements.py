"""
Comprehensive Automated Test Suite for NazarSetu Enhancements.

Validates:
1. Civic Intelligence Engine analysis (severity, citizen impact, priority rationale, action plan).
2. 10-stage AI Civic Mission Control pipeline.
3. CivicTwin Before & After Resolution Verification engine and database lifecycle.
4. Neighborhood Pulse grounded SQLite telemetry calculation.
5. Multilingual accessibility engine (English, Hindi, Gujarati).
6. Smart Duplicate Shield matching.
7. Natural language autonomous assistant routing.
"""

import sys
import tempfile
from pathlib import Path
import pytest

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import (
    SUPPORTED_CATEGORIES,
    COMPLAINT_STAGES,
    PRIORITY_RULES,
    CITIZEN_IMPACT_PRESETS,
)
import database
import tools
import vision
import agent
import components
from i18n import t, TRANSLATIONS


@pytest.fixture
def temp_db():
    """Create an isolated temporary SQLite database for tests."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        temp_path = Path(f.name)
    database.init_db(temp_path)
    yield temp_path
    import gc
    gc.collect()
    for ext in ["", "-wal", "-shm"]:
        p = Path(str(temp_path) + ext)
        if p.exists():
            try:
                p.unlink(missing_ok=True)
            except Exception:
                pass


# 1. Test Civic Intelligence Engine Analysis
def test_civic_intelligence_engine_report():
    sample_path = Path(__file__).resolve().parent.parent / "data" / "samples" / "sample_pothole.jpg"
    assert sample_path.exists()
    with open(sample_path, "rb") as f:
        img_bytes = f.read()

    report = vision.analyze_issue(img_bytes, hint_category="Potholes and damaged roads")
    assert report["is_civic_issue"] is True
    assert report["issue_type"] == "Potholes and damaged roads"
    assert report["severity"] in ["Critical", "High", "Medium", "Low"]
    assert "citizen_impact" in report
    assert len(report["citizen_impact"]) > 10
    assert "priority_rationale" in report
    assert "action_plan" in report
    assert report["recommended_department"] == "Roads & Infrastructure Department"
    assert report["sla_hours"] > 0


# 2. Test 10-Stage AI Civic Mission Control Pipeline
def test_ten_stage_mission_control_pipeline(temp_db):
    sample_path = Path(__file__).resolve().parent.parent / "data" / "samples" / "sample_garbage.jpg"
    with open(sample_path, "rb") as f:
        img_bytes = f.read()
    img_hash = tools.compute_image_hash(img_bytes)

    # Stages 1 to 7
    pipeline_state, trail = agent.run_reporting_agent_pipeline(
        issue_type="Overflowing garbage",
        city="Mumbai",
        locality="Bandra West",
        image_hash=img_hash,
        landmark="Near Bandstand",
        db_path=temp_db
    )
    steps_initial = trail.get_steps()
    assert len(steps_initial) == 7
    stages_initial = [s.get("stage_number") for s in steps_initial]
    assert stages_initial == [1, 2, 3, 4, 5, 6, 7]

    # Stages 8 to 10 upon user confirmation
    confirmed_payload = {
        "confirmed": True,
        "issue_type": "Overflowing garbage",
        "description": "Severe garbage spill near residential pavement.",
        "city": "Mumbai",
        "locality": "Bandra West",
        "ward": pipeline_state["ward"],
        "department": pipeline_state["department"],
        "image_hash": img_hash,
        "priority": "High",
        "status": "Reported",
    }
    reg_res, reg_trail = agent.run_registration_agent_action(confirmed_payload, trail=trail, db_path=temp_db)
    assert reg_res["status"] == "registered"
    all_steps = reg_trail.get_steps()
    assert len(all_steps) == 10
    all_stages = [s.get("stage_number") for s in all_steps]
    assert all_stages == list(range(1, 11))


# 3. Test CivicTwin Before & After Verification Engine
def test_civictwin_verification_and_resolution(temp_db):
    # Insert a sample complaint into temp_db
    cid = database.insert_complaint({
        "confirmed": True,
        "issue_type": "Potholes and damaged roads",
        "description": "Deep asphalt trench on main road.",
        "city": "Bengaluru",
        "locality": "Indiranagar",
        "ward": "Ward 74",
        "department": "Roads & Infrastructure Department",
        "image_hash": "dummy_before_hash_123456",
        "priority": "High",
        "status": "In Progress",
    }, db_path=temp_db)

    # Run CivicTwin verification
    before_bytes = b"sample_road_pothole_bytes"
    after_bytes = b"sample_road_fixed_bytes"
    twin_res = vision.verify_civictwin(before_bytes, after_bytes, original_issue="Potholes and damaged roads")

    assert "verification_score" in twin_res
    assert twin_res["verification_score"] > 0.5
    assert "delta_detected" in twin_res
    assert "quality_checklist" in twin_res

    # Store verification in database
    v_id = database.insert_civictwin_verification(
        complaint_id=cid,
        before_hash="dummy_before_hash_123456",
        after_hash="dummy_after_hash_654321",
        verification_result=twin_res,
        db_path=temp_db
    )
    assert v_id > 0

    # Human-in-the-loop confirmation
    ok = database.confirm_civictwin_resolution(cid, admin_notes="Officer verified repair.", db_path=temp_db)
    assert ok is True

    # Verify status changed to Resolved
    comp = database.get_complaint(cid, db_path=temp_db)
    assert comp["status"] == "Resolved"


# 4. Test Neighborhood Pulse Telemetry Calculation
def test_neighborhood_pulse_telemetry(temp_db):
    # Register 3 complaints in temp_db
    c1 = database.insert_complaint({
        "confirmed": True,
        "issue_type": "Potholes and damaged roads",
        "city": "Bengaluru",
        "locality": "Indiranagar",
        "ward": "Ward 74",
        "department": "Roads & Infrastructure Department",
        "image_hash": "hash_1",
        "priority": "High",
        "status": "Reported",
    }, db_path=temp_db)

    c2 = database.insert_complaint({
        "confirmed": True,
        "issue_type": "Potholes and damaged roads",
        "city": "Bengaluru",
        "locality": "Indiranagar",
        "ward": "Ward 74",
        "department": "Roads & Infrastructure Department",
        "image_hash": "hash_2",
        "priority": "High",
        "status": "Resolved",
    }, db_path=temp_db)

    stats = database.get_neighborhood_pulse_stats(locality="Indiranagar", db_path=temp_db)
    metrics = stats["metrics"]
    assert metrics["total_complaints"] >= 2
    assert metrics["resolved_complaints"] >= 1
    assert metrics["resolution_rate_percent"] >= 50.0
    assert len(stats["top_issues"]) >= 1


# 5. Test Multilingual Accessibility Engine
def test_multilingual_translations():
    keys = ["nav_overview", "nav_report", "nav_mission_control", "nav_civictwin", "nav_neighborhood_pulse"]
    for k in keys:
        en_val = t(k, "en")
        hi_val = t(k, "hi")
        gu_val = t(k, "gu")

        assert en_val != ""
        assert hi_val != ""
        assert gu_val != ""
        assert hi_val != en_val  # Verified distinct Hindi translation
        assert gu_val != en_val  # Verified distinct Gujarati translation

    # Fallback to key if unknown
    assert t("non_existent_key_xyz", "en") == "non_existent_key_xyz"


# 6. Test Smart Duplicate Shield Tool
def test_smart_duplicate_shield(temp_db):
    # Register initial complaint
    cid = database.insert_complaint({
        "confirmed": True,
        "issue_type": "Broken streetlights",
        "city": "Delhi",
        "locality": "Connaught Place",
        "ward": "Ward 12",
        "department": "Electrical & Energy Department",
        "image_hash": "unique_lamp_hash_112233",
        "priority": "Medium",
        "status": "Reported",
    }, db_path=temp_db)

    # Check duplicate with same hash
    dup_res = tools.check_duplicate(
        issue_type="Broken streetlights",
        locality="Connaught Place",
        image_hash="unique_lamp_hash_112233",
        db_path=temp_db
    )
    assert dup_res["is_duplicate"] is True
    assert dup_res["existing_complaint_id"] == cid
    assert dup_res["match_type"] == "exact_image_hash"


# 7. Test Autonomous Tracking Agent Natural Language Queries
def test_tracking_agent_natural_language_queries():
    # Department routing query
    res_dept = agent.run_tracking_chat_agent("Which department handles waterlogging?")
    assert "Stormwater & Drainage Department" in res_dept["reply"]

    # Statistics query
    res_stats = agent.run_tracking_chat_agent("What are the neighborhood statistics?")
    assert "Neighborhood Pulse Live Statistics" in res_stats["reply"]

    # Search query
    res_search = agent.run_tracking_chat_agent("Show pending complaints")
    assert "complaints" in res_search["reply"].lower()


# 8. Test Dynamic Light/Dark Themes and HTML Sanitization
def test_theme_and_html_rendering_sanitization(monkeypatch):
    light_css = components.get_custom_css("light")
    dark_css = components.get_custom_css("dark")

    assert "#F8FAFC" in light_css
    assert "#FFFFFF" in light_css
    assert "#0A0F1D" in dark_css
    assert "#131E32" in dark_css

    # Test render_html sanitizes leading indentation and empty lines
    captured = []
    if hasattr(components.st, "html"):
        monkeypatch.setattr(components.st, "html", lambda s: captured.append(s))
    else:
        monkeypatch.setattr(components.st, "markdown", lambda s, unsafe_allow_html=False: captured.append(s))

    test_raw_html = """
        <div class="intelligence-card">
            <div class="intelligence-header">Title</div>

            <div class="intel-grid">
                <div class="intel-item">Item</div>
            </div>
        </div>
    """
    components.render_html(test_raw_html)
    assert len(captured) == 1
    rendered = captured[0]
    # Ensure no line starts with 4+ spaces of indentation (which triggers Markdown code block)
    for line in rendered.splitlines():
        assert not line.startswith("    "), f"Indented line found: {line}"
        assert not line.startswith("\t"), f"Tabbed line found: {line}"
    assert '<div class="intel-grid">' in rendered
    assert '<div class="intel-item">Item</div>' in rendered

