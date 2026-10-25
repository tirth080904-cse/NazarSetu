"""
End-to-End Live Demonstration Scenario Test.

Validates the complete 6-Scene Hackathon demonstration flow:
Scene 1: Upload / Load sample pothole photograph.
Scene 2: Vision AI Understanding -> Issue DNA generated.
Scene 3: Agent Takes Action -> Genuine Action Trail recorded.
Scene 4: Registration -> Confirmed insertion into SQLite, NS-DEMO-XXXXXXXX generated.
Scene 5: Live Tracking Assistant -> Chat query retrieves live record.
Scene 6: Demonstrate Persistence -> Admin updates status to 'In Progress',
         assistant immediately reflects the new status.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import DB_PATH
import database
import tools
import vision
import agent


def test_hackathon_demo_flow():
    # Scene 1: Load sample photograph
    sample_path = Path(__file__).resolve().parent.parent / "data" / "samples" / "sample_pothole.jpg"
    assert sample_path.exists(), "Sample pothole image must exist."
    with open(sample_path, "rb") as f:
        image_bytes = f.read()
    image_hash = tools.compute_image_hash(image_bytes)
    assert len(image_hash) == 64

    # Scene 2: AI Understanding (Issue DNA)
    analysis = vision.analyze_issue(image_bytes, hint_category="Potholes and damaged roads")
    assert analysis["is_civic_issue"] is True
    assert analysis["issue_type"] == "Potholes and damaged roads"
    assert "visual_evidence" in analysis
    assert analysis["suggested_priority"] in ["High", "Medium", "Low"]
    assert "recommended_action" in analysis

    # Scene 3: Agent Takes Action (Action Trail)
    city = "Bengaluru"
    locality = "Indiranagar"
    pipeline_state, trail = agent.run_reporting_agent_pipeline(
        issue_type=analysis["issue_type"],
        city=city,
        locality=locality,
        image_hash=image_hash,
        landmark="Near Metro Pillar 84"
    )
    steps = trail.get_steps()
    assert len(steps) >= 3
    tool_names = [s["tool_name"] for s in steps]
    assert "select_department" in tool_names
    assert "find_responsible_ward" in tool_names
    assert "check_duplicate" in tool_names
    assert pipeline_state["department"] == "Roads & Infrastructure Department"
    assert "Ward 74" in pipeline_state["ward"]

    # Scene 4: Registration with Explicit Confirmation
    confirmed_payload = {
        "confirmed": True,
        "issue_type": analysis["issue_type"],
        "description": analysis["suggested_description"],
        "city": city,
        "locality": locality,
        "ward": pipeline_state["ward"],
        "department": pipeline_state["department"],
        "image_hash": image_hash,
        "priority": analysis["suggested_priority"],
        "status": "Pending",
        "landmark": "Near Metro Pillar 84",
        "visual_evidence": analysis["visual_evidence"],
    }
    reg_res, reg_trail = agent.run_registration_agent_action(confirmed_payload, trail=trail)
    assert reg_res["status"] == "registered"
    complaint_id = reg_res["complaint_id"]
    assert complaint_id.startswith("NS-DEMO-")

    # Step is recorded in Action Trail
    all_reg_tools = [s["tool_name"] for s in reg_trail.get_steps()]
    assert "register_complaint" in all_reg_tools
    assert "activate_tracking_lifecycle" in all_reg_tools

    # Scene 5: Live Tracking Query
    user_query = f"Where is my complaint {complaint_id} and who is handling it?"
    tracking_res = agent.run_tracking_chat_agent(user_message=user_query)
    assert tracking_res["complaint_data"] is not None
    assert tracking_res["complaint_data"]["complaint_id"] == complaint_id
    assert tracking_res["complaint_data"]["current_status"] == "Pending"
    assert tracking_res["complaint_data"]["department"] == "Roads & Infrastructure Department"
    assert complaint_id in tracking_res["reply"]
    assert "PENDING" in tracking_res["reply"].upper()

    # Scene 6: Demonstrate Persistence (Admin Status Update & Re-Query)
    # Admin updates status to 'In Progress'
    update_ok = database.update_complaint_status(
        complaint_id=complaint_id,
        new_status="In Progress",
        note="Field maintenance crew dispatched with asphalt hot-mix."
    )
    assert update_ok is True

    # Immediate re-query through Tracking Assistant
    re_query = f"What is the updated status for {complaint_id}?"
    re_tracking_res = agent.run_tracking_chat_agent(user_message=re_query)
    assert re_tracking_res["complaint_data"] is not None
    assert re_tracking_res["complaint_data"]["current_status"] == "In Progress"
    assert "IN PROGRESS" in re_tracking_res["reply"].upper()

    # Scene 7: Step 5 - Show complaint reflected in Neighborhood Pulse
    pulse_stats = database.get_neighborhood_pulse_stats(locality=locality)
    assert pulse_stats["total_complaints"] >= 1
    assert "metrics" in pulse_stats
    assert pulse_stats["metrics"]["total_complaints"] >= 1

    # Scene 8: Step 8 & 9 - CivicTwin Before & After Resolution Verification
    after_path = Path(__file__).resolve().parent.parent / "data" / "samples" / "sample_pothole_fixed.jpg"
    assert after_path.exists(), "Sample repaired pothole photo must exist."
    with open(after_path, "rb") as f:
        after_bytes = f.read()

    civictwin_report = vision.verify_civictwin(
        before_bytes=image_bytes,
        after_bytes=after_bytes,
        issue_type="Potholes and damaged roads"
    )
    assert civictwin_report["appears_improved"] is True
    assert civictwin_report["repair_status"] == "Complete"
    assert "verification_score" in civictwin_report
    assert civictwin_report["verification_score"] > 0.8
    assert "quality_checklist" in civictwin_report

    # Insert CivicTwin report into database
    v_id = database.insert_civictwin_verification(
        complaint_id=complaint_id,
        before_hash=image_hash,
        after_hash=tools.compute_image_hash(after_bytes),
        verification_result=civictwin_report
    )
    assert v_id > 0

    # Scene 9: Human-in-the-Loop Municipal Officer Sign-Off
    resolve_ok = database.confirm_civictwin_resolution(
        target_id=complaint_id,
        admin_notes="Officer verified asphalt compaction and surface grade."
    )
    assert resolve_ok is True

    # Scene 10: Retrieve Updated Complaint Journey & Chat Assistant Reflection
    resolved_record = database.get_complaint(complaint_id)
    assert resolved_record["status"] == "Resolved"

    post_resolution_query = f"Is complaint {complaint_id} resolved?"
    final_tracking_res = agent.run_tracking_chat_agent(user_message=post_resolution_query)
    assert final_tracking_res["complaint_data"] is not None
    assert final_tracking_res["complaint_data"]["current_status"] == "Resolved"
    assert "RESOLVED" in final_tracking_res["reply"].upper()
