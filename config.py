"""
NazarSetu Configuration & Domain Constants.

Defines civic issue types, department routing rules, priority heuristics,
and demo ward dataset configurations.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Database
DB_PATH = DATA_DIR / "nazarsetu.db"

# Sample ward mapping CSV
DEMO_WARDS_CSV = DATA_DIR / "demo_wards.csv"

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()

# Tracking ID Prefix
COMPLAINT_ID_PREFIX = "NS-DEMO-"

# Supported Civic Issue Categories
SUPPORTED_CATEGORIES = [
    "Potholes and damaged roads",
    "Overflowing garbage",
    "Broken streetlights",
    "Waterlogging and drainage issues",
]

# Department Routing Mapping
DEPARTMENT_MAPPING = {
    "Potholes and damaged roads": "Roads & Infrastructure Department",
    "Overflowing garbage": "Solid Waste Management Department",
    "Broken streetlights": "Electrical & Public Lighting Department",
    "Waterlogging and drainage issues": "Stormwater & Drainage Department",
}

# Category Icons & Accents
CATEGORY_METADATA = {
    "Potholes and damaged roads": {
        "icon": "🕳️",
        "short_name": "Road Damage",
        "color": "#F4A340",
    },
    "Overflowing garbage": {
        "icon": "🗑️",
        "short_name": "Garbage",
        "color": "#E53E3E",
    },
    "Broken streetlights": {
        "icon": "💡",
        "short_name": "Streetlight",
        "color": "#DD6B20",
    },
    "Waterlogging and drainage issues": {
        "icon": "🌊",
        "short_name": "Drainage",
        "color": "#3182CE",
    },
}

# Complaint Lifecycle Statuses (5-Stage Journey)
STATUS_PENDING = "Pending"
STATUS_REPORTED = "Reported"
STATUS_ASSIGNED = "Assigned"
STATUS_IN_PROGRESS = "In Progress"
STATUS_AWAITING_VERIFICATION = "Awaiting Verification"
STATUS_RESOLVED = "Resolved"

# Full list of valid database statuses (maintains backward compatibility with tests)
VALID_STATUSES = [
    STATUS_PENDING,
    STATUS_REPORTED,
    STATUS_ASSIGNED,
    STATUS_IN_PROGRESS,
    STATUS_AWAITING_VERIFICATION,
    STATUS_RESOLVED,
]

# Canonical 5-Stage Visual Lifecycle Sequence
COMPLAINT_LIFECYCLE_STAGES = [
    STATUS_REPORTED,
    STATUS_ASSIGNED,
    STATUS_IN_PROGRESS,
    STATUS_AWAITING_VERIFICATION,
    STATUS_RESOLVED,
]
COMPLAINT_STAGES = COMPLAINT_LIFECYCLE_STAGES

# Priority and Severity Levels
SEVERITY_LEVELS = ["Low", "Medium", "High", "Critical"]
VALID_PRIORITIES = ["Low", "Medium", "High", "Critical"]

# Documented Priority Heuristic Rules with Critical tier
PRIORITY_RULES = {
    "Potholes and damaged roads": {
        "Critical": "Active cave-in or crater depth > 20cm spanning arterial corridor, imminent high-casualty hazard.",
        "High": "Severe crater depth > 10cm, spans active traffic lane, or poses immediate vehicular/two-wheeler hazard.",
        "Medium": "Moderate depression or broken asphalt creating traffic slowdowns.",
        "Low": "Surface gravel wear or minor road chipping without structural blockage.",
    },
    "Overflowing garbage": {
        "Critical": "Hazardous toxic/chemical dump, open burning waste emitting noxious smoke near sensitive zones.",
        "High": "Massive waste spill blocking sidewalk/roadway, severe biohazard, or active pest infestation.",
        "Medium": "Overfilled dumpster container with waste spilling into immediate perimeter.",
        "Low": "Isolated scattered dry waste or single uncollected bin.",
    },
    "Broken streetlights": {
        "Critical": "Exposed high-voltage live wires sparking, or fallen lighting pole blocking traffic carriageway.",
        "High": "Complete junction blackout on high-speed road or dark blind curve.",
        "Medium": "Complete unlit street lamp on pedestrian thoroughfare or residential street.",
        "Low": "Flickering bulb or timer desynchronization (lamp active during daytime).",
    },
    "Waterlogging and drainage issues": {
        "Critical": "Submerged highway underpass with rising water, breached electrical utility box, or flash flood zone.",
        "High": "Deep standing water (> 1 foot) stalling vehicles or breaching residential/commercial thresholds.",
        "Medium": "Clogged storm drain or persistent curb-side pooling impeding pedestrian movement.",
        "Low": "Slow-draining shallow puddle during normal monsoon conditions.",
    },
}

# Real-world Citizen Impact Heuristics
CITIZEN_IMPACT_PRESETS = {
    "Potholes and damaged roads": {
        "Critical": "Severe vehicle overturn hazard, fatal two-wheeler skidding risk, arterial transit gridlock.",
        "High": "Immediate two-wheeler spill hazard, vehicular rim/suspension damage, sudden braking collisions.",
        "Medium": "Traffic flow deceleration, localized congestion, minor vehicular jarring.",
        "Low": "Minor ride discomfort, loose pebble projectile hazard for pedestrians.",
    },
    "Overflowing garbage": {
        "Critical": "Severe respiratory toxicity, uncontrolled fire risk, medical/biohazard public exposure.",
        "High": "Vector-borne disease breeding (dengue/cholera), pedestrian forced onto vehicle lanes, foul odor.",
        "Medium": "Unpleasant olfactory environment, sidewalk littering, stray animal congregation.",
        "Low": "Aesthetic blight, localized scattered dry litter.",
    },
    "Broken streetlights": {
        "Critical": "Direct electrocution hazard, high-speed vehicle impact with unlit fallen infrastructure.",
        "High": "Compromised nocturnal pedestrian safety, heightened blind-spot crash vulnerability.",
        "Medium": "Pedestrian hesitation after dusk, reduced perimeter visibility for residents.",
        "Low": "Minor illumination shortfall, aesthetic irregularity.",
    },
    "Waterlogging and drainage issues": {
        "Critical": "Vehicle stall and passenger entrapment risk, sewage backflow contamination in homes.",
        "High": "Engine water ingestion hazard, hidden pothole submergence trap, pedestrian displacement.",
        "Medium": "Pedestrian foot-traffic detour, curbside accumulation, curb splashing.",
        "Low": "Minor puddle jumping requirement, damp pavement.",
    },
}

# Hackathon Demo Disclaimer
DEMO_DISCLAIMER = (
    "NazarSetu is an Agentic AI Civic Action prototype built for demonstration. "
    "Ward assignments are mapped against fictional demo datasets. "
    "No municipal departments were officially contacted. ID format: NS-DEMO-XXXXXXXX."
)
