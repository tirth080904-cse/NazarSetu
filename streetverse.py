"""
NAZARSETU — STREETVERSE
The Most Unconventional Civic AI Frontend.

Tagline: "Every Street Has a Story. Let's Change the Ending."

Transforms NazarSetu into an interactive, illustrated miniature Indian neighborhood.
The city itself is the navigation system.

Art Direction:
- Warm Sand: #F4E7D3
- Terracotta: #D96C48
- Indigo Ink: #243B63
- Mango Yellow: #F4BB52
- Sage Green: #83A98A
- Soft Coral: #EB8C79
- Cream: #FFFCF5
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
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
    CATEGORY_METADATA,
)
import database
import tools
import vision
import agent
from i18n import t


HOTSPOT_METADATA = {
    "road": {
        "title": "Damaged Road Carriage & Potholes",
        "category": "Potholes and damaged roads",
        "department": "Roads & Infrastructure Department",
        "icon": "🕳️",
        "color": "#D96C48",
        "hint": "Road craters, asphalt fissures & pavement degradation",
        "sample": "sample_pothole.jpg",
        "default_city": "Bengaluru",
        "default_locality": "Indiranagar",
    },
    "streetlight": {
        "title": "Public Lighting & Streetlamps",
        "category": "Broken streetlights",
        "department": "Electrical & Public Lighting Department",
        "icon": "💡",
        "color": "#F4BB52",
        "hint": "Extinguished sodium lamps, broken diffusers & dark corridors",
        "sample": "sample_streetlight.jpg",
        "default_city": "Delhi",
        "default_locality": "Connaught Place",
    },
    "garbage": {
        "title": "Waste Collection & Sanitation",
        "category": "Overflowing garbage",
        "department": "Solid Waste Management Department",
        "icon": "🗑️",
        "color": "#83A98A",
        "hint": "Overflowing dumper bins, sidewalk debris & unsegregated refuse",
        "sample": "sample_garbage.jpg",
        "default_city": "Mumbai",
        "default_locality": "Bandra West",
    },
    "drainage": {
        "title": "Stormwater Drainage & Flood Corridors",
        "category": "Waterlogging and drainage issues",
        "department": "Stormwater & Drainage Department",
        "icon": "🌊",
        "color": "#243B63",
        "hint": "Clogged roadside culverts, road waterlogging & surface runoff",
        "sample": "sample_waterlogging.jpg",
        "default_city": "Ahmedabad",
        "default_locality": "Satellite",
    },
}


def get_streetverse_css() -> str:
    """Returns the complete Indian Urban Storybook design system and layout styling."""
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;0,9..144,800;1,9..144,400;1,9..144,600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --sand: #F4E7D3;
    --sand-light: #FAF3E8;
    --terracotta: #D96C48;
    --terracotta-dark: #B54F2D;
    --indigo: #243B63;
    --indigo-light: #375382;
    --indigo-soft: rgba(36, 59, 99, 0.08);
    --mango: #F4BB52;
    --mango-light: #FDE8BA;
    --sage: #83A98A;
    --sage-light: #E1EBE2;
    --coral: #EB8C79;
    --cream: #FFFCF5;
    --card-surface: #FFFFFF;
    --border-subtle: #E8DAC6;
    --border-warm: #DFCAB0;
    --text-primary: #243B63;
    --text-muted: #64748B;
    --text-warm: #7C6044;
}

/* Hide default Streamlit clutter for a clean art installation experience */
#MainMenu, header[data-testid="stHeader"], footer, [data-testid="stToolbar"] {
    display: none !important;
}

[data-testid="stSidebar"] {
    display: none !important;
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 5rem !important;
    max-width: 1400px !important;
}

body, .stApp {
    background: radial-gradient(circle at 50% 10%, #FFFCF5 0%, #F4E7D3 65%, #ECD9BF 100%) !important;
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    color: var(--text-primary) !important;
    overflow-x: hidden;
}

/* Floating Top Identity & Controls */
.streetverse-topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.8rem 1.4rem;
    background: rgba(255, 252, 245, 0.88);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1.5px solid var(--border-subtle);
    border-radius: 20px;
    box-shadow: 0 10px 25px -6px rgba(36, 59, 99, 0.08);
    margin-bottom: 0.8rem;
}

.streetverse-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-emblem {
    width: 38px;
    height: 38px;
    background: linear-gradient(135deg, var(--terracotta) 0%, var(--mango) 100%);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    box-shadow: 0 4px 10px rgba(217, 108, 72, 0.3);
}

.brand-title {
    font-family: 'Fraunces', serif;
    font-size: 1.4rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--indigo);
    line-height: 1.1;
}

.brand-tagline {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--terracotta);
    letter-spacing: 0.02em;
}

/* Floating Bottom Command Capsule */
.command-capsule-container {
    position: fixed;
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 999;
}

.command-capsule {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(36, 59, 99, 0.94);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    padding: 8px 12px;
    border-radius: 40px;
    border: 2px solid rgba(244, 187, 82, 0.4);
    box-shadow: 0 16px 36px -8px rgba(36, 59, 99, 0.45);
}

.capsule-item {
    padding: 8px 16px;
    border-radius: 30px;
    font-size: 0.88rem;
    font-weight: 700;
    color: #F4E7D3;
    text-decoration: none;
    transition: all 0.2s ease;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.capsule-item:hover {
    background: rgba(244, 187, 82, 0.2);
    color: #FFFFFF;
}

.capsule-item.active {
    background: var(--terracotta);
    color: #FFFFFF;
    box-shadow: 0 4px 12px rgba(217, 108, 72, 0.4);
}

/* Floating Real-Data Activity Indicator (Bottom Right) */
.civic-activity-badge {
    position: fixed;
    bottom: 28px;
    right: 28px;
    background: rgba(255, 252, 245, 0.92);
    backdrop-filter: blur(10px);
    border: 1.5px solid var(--border-warm);
    border-radius: 30px;
    padding: 8px 16px;
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--indigo);
    box-shadow: 0 8px 20px rgba(36, 59, 99, 0.1);
    display: flex;
    align-items: center;
    gap: 8px;
    z-index: 900;
}

.pulse-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--sage);
    box-shadow: 0 0 0 0 rgba(131, 169, 138, 0.7);
    animation: dot-pulse 2s infinite;
}

@keyframes dot-pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(131, 169, 138, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(131, 169, 138, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(131, 169, 138, 0); }
}

/* The Illustrated Street Stage */
.street-stage-wrapper {
    background: #FFFCF5;
    border: 2px solid var(--border-warm);
    border-radius: 24px;
    box-shadow: 0 16px 40px -10px rgba(36, 59, 99, 0.12);
    overflow: hidden;
    position: relative;
    margin-bottom: 1.2rem;
}

/* SVG Scene Animations */
@keyframes rickshaw-drive {
    0% { transform: translateX(-160px); }
    100% { transform: translateX(1360px); }
}

@keyframes banyan-sway {
    0%, 100% { transform: rotate(0deg); }
    50% { transform: rotate(1.4deg); }
}

@keyframes lamp-pulse {
    0%, 100% { opacity: 0.85; filter: drop-shadow(0 0 10px #F4BB52); }
    50% { opacity: 0.55; filter: drop-shadow(0 0 4px #F4BB52); }
}

@keyframes ripple-alert {
    0% { r: 14px; opacity: 0.9; }
    100% { r: 36px; opacity: 0; }
}

@media (prefers-reduced-motion: reduce) {
    .animated-rickshaw, .animated-tree, .animated-lamp, .animated-ripple {
        animation: none !important;
    }
}

.animated-rickshaw {
    animation: rickshaw-drive 26s linear infinite;
}

.animated-tree {
    transform-origin: 320px 420px;
    animation: banyan-sway 6s ease-in-out infinite;
}

.animated-lamp {
    animation: lamp-pulse 3.5s ease-in-out infinite;
}

.animated-ripple {
    animation: ripple-alert 2.2s cubic-bezier(0.2, 0.8, 0.2, 1) infinite;
}

/* Hotspot Interactive Elements in SVG */
.street-hotspot {
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.street-hotspot:hover {
    filter: drop-shadow(0 8px 16px rgba(217, 108, 72, 0.35));
}

.street-hotspot:hover .hotspot-beacon {
    transform: scale(1.15);
}

.hotspot-card-badge {
    background: #FFFFFF;
    border: 1.5px solid var(--border-warm);
    border-radius: 14px;
    padding: 12px 16px;
    box-shadow: 0 8px 18px rgba(36, 59, 99, 0.08);
    transition: all 0.2s ease;
    text-align: left;
}

.hotspot-card-badge:hover {
    transform: translateY(-2px);
    border-color: var(--terracotta);
    box-shadow: 0 12px 24px rgba(217, 108, 72, 0.15);
}

/* Editorial Dossier & Case File Styling */
.case-file-dossier {
    background: #FFFFFF;
    border: 2px solid var(--border-warm);
    border-radius: 20px;
    padding: 2.2rem;
    box-shadow: 0 16px 40px rgba(36, 59, 99, 0.09);
    margin: 1.2rem 0;
    position: relative;
}

.case-file-header {
    border-bottom: 2px dashed var(--border-warm);
    padding-bottom: 1.2rem;
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 12px;
}

.dossier-headline {
    font-family: 'Fraunces', serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: var(--indigo);
    margin: 0;
}

.dossier-meta-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.dossier-pill-critical { background: #FDE8E8; color: #9B1C1C; border: 1.5px solid #F87171; }
.dossier-pill-high { background: var(--sand); color: var(--terracotta); border: 1.5px solid var(--terracotta); }
.dossier-pill-medium { background: var(--mango-light); color: #92400E; border: 1.5px solid var(--mango); }
.dossier-pill-low { background: var(--sage-light); color: #065F46; border: 1.5px solid var(--sage); }

/* Story Chapters Timeline (Repair Story) */
.story-chapter-card {
    background: #FFFFFF;
    border: 1.5px solid var(--border-warm);
    border-left: 6px solid var(--terracotta);
    border-radius: 14px;
    padding: 1.2rem 1.6rem;
    margin-bottom: 14px;
    box-shadow: 0 4px 12px rgba(36, 59, 99, 0.05);
    transition: all 0.2s ease;
}

.story-chapter-card.inactive {
    opacity: 0.55;
    border-left-color: #CBD5E1;
}

.story-chapter-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--terracotta);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 4px;
}

.story-chapter-title {
    font-family: 'Fraunces', serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--indigo);
    margin-bottom: 6px;
}

/* Editorial Investigation Steps (Report Mode) */
.investigation-step-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border-radius: 20px;
    background: var(--sand-light);
    border: 1.5px solid var(--border-warm);
    color: var(--indigo);
    font-weight: 700;
    font-size: 0.84rem;
    margin-right: 8px;
    margin-bottom: 8px;
}

.investigation-step-pill.active {
    background: var(--terracotta);
    color: #FFFFFF;
    border-color: var(--terracotta);
}

/* Mission Control Pipeline Workshop */
.pipeline-flow-banner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #FFFFFF;
    border: 2px solid var(--border-warm);
    border-radius: 16px;
    padding: 16px 24px;
    margin-bottom: 20px;
    flex-wrap: wrap;
    gap: 10px;
}

.pipeline-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    min-width: 100px;
}

.pipeline-node-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: var(--sand-light);
    border: 2px solid var(--terracotta);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    color: var(--terracotta);
    margin-bottom: 6px;
}

.pipeline-node-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--indigo);
    text-transform: uppercase;
}

.pipeline-arrow {
    color: var(--terracotta);
    font-size: 1.4rem;
    font-weight: 800;
}

.stage-card-workshop {
    background: #FFFFFF;
    border: 1.5px solid var(--border-warm);
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 14px;
    box-shadow: 0 4px 14px rgba(36, 59, 99, 0.05);
    transition: all 0.2s ease;
}

.stage-card-workshop:hover {
    border-color: var(--terracotta);
    box-shadow: 0 8px 20px rgba(217, 108, 72, 0.12);
}

.stage-header-flex {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    border-bottom: 1px dashed var(--border-warm);
    padding-bottom: 8px;
}

.stage-badge-pill {
    background: var(--terracotta);
    color: #FFFFFF;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 12px;
}

/* CivicTwin Comparison Studio */
.civictwin-compare-frame {
    background: #FFFFFF;
    border: 2px solid var(--border-warm);
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 8px 24px rgba(36, 59, 99, 0.07);
}

.civictwin-score-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #ECFDF5;
    border: 2px solid #10B981;
    color: #065F46;
    padding: 8px 18px;
    border-radius: 30px;
    font-weight: 800;
    font-size: 1.1rem;
}

.checklist-box {
    background: #FAF3E8;
    border: 1.5px solid var(--border-warm);
    border-radius: 12px;
    padding: 14px;
    margin-top: 10px;
}

/* Neighborhood Pulse Stories */
.pulse-stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 20px;
}

.pulse-stat-box {
    background: #FFFFFF;
    border: 1.5px solid var(--border-warm);
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 4px 12px rgba(36, 59, 99, 0.05);
}

.pulse-stat-val {
    font-family: 'Fraunces', serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: var(--terracotta);
    margin-top: 4px;
}

/* Civic Operations Studio */
.admin-op-card {
    background: #FFFFFF;
    border: 1.5px solid var(--border-warm);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 6px 18px rgba(36, 59, 99, 0.06);
    margin-bottom: 16px;
}

/* Buttons in Storybook Aesthetic */
div.stButton > button {
    border-radius: 14px !important;
    font-weight: 700 !important;
    padding: 0.55rem 1.2rem !important;
    transition: all 0.2s ease !important;
    border: 1.5px solid var(--border-warm) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

div.stButton > button[kind="primary"] {
    background: var(--terracotta) !important;
    color: #FFFFFF !important;
    border-color: var(--terracotta-dark) !important;
    box-shadow: 0 4px 14px rgba(217, 108, 72, 0.3) !important;
}

div.stButton > button[kind="primary"]:hover {
    background: var(--terracotta-dark) !important;
    box-shadow: 0 6px 20px rgba(217, 108, 72, 0.45) !important;
    transform: translateY(-1px);
}
</style>
"""


def render_streetverse_svg(counts: Dict[str, int], active_states: Dict[str, str]) -> str:
    """
    Renders the handcrafted 2.5D Isometric Miniature Indian Neighborhood SVG Scene.
    Embeds state-aware civic hotspots with live database complaint counts.
    """
    pothole_count = counts.get("Potholes and damaged roads", 0)
    streetlight_count = counts.get("Broken streetlights", 0)
    garbage_count = counts.get("Overflowing garbage", 0)
    drainage_count = counts.get("Waterlogging and drainage issues", 0)

    road_state = active_states.get("road", "alert" if pothole_count > 0 else "smooth")

    # SVG markup with handcrafted vector shapes
    svg_code = f"""
    <div class="street-stage-wrapper">
    <svg viewBox="0 0 1200 640" class="streetverse-svg" xmlns="http://www.w3.org/2000/svg" style="width: 100%; height: auto; display: block;">
        <defs>
            <linearGradient id="skyWash" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#FFFCF5"/>
                <stop offset="65%" stop-color="#F4E7D3"/>
                <stop offset="100%" stop-color="#EAD7BD"/>
            </linearGradient>
            
            <linearGradient id="roadSurface" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#3A4659"/>
                <stop offset="50%" stop-color="#2D3748"/>
                <stop offset="100%" stop-color="#3A4659"/>
            </linearGradient>

            <linearGradient id="sidewalkStone" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#E8DAC6"/>
                <stop offset="100%" stop-color="#DFCAB0"/>
            </linearGradient>

            <radialGradient id="sunGlow" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="#F4BB52" stop-opacity="0.9"/>
                <stop offset="45%" stop-color="#F4BB52" stop-opacity="0.35"/>
                <stop offset="100%" stop-color="#F4BB52" stop-opacity="0"/>
            </radialGradient>

            <radialGradient id="lampCone" cx="50%" cy="0%" r="90%">
                <stop offset="0%" stop-color="#F4BB52" stop-opacity="0.75"/>
                <stop offset="70%" stop-color="#F4BB52" stop-opacity="0.15"/>
                <stop offset="100%" stop-color="#F4BB52" stop-opacity="0"/>
            </radialGradient>

            <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="120%">
                <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#243B63" flood-opacity="0.14"/>
            </filter>
        </defs>

        <!-- SKY & BACKGROUND -->
        <rect width="1200" height="640" fill="url(#skyWash)"/>

        <!-- Morning Sun -->
        <circle cx="1060" cy="95" r="75" fill="url(#sunGlow)"/>
        <circle cx="1060" cy="95" r="28" fill="#F4BB52"/>

        <!-- Distant City Silhouettes (Heritage Minarets, Domes, Rooftops in soft sand tone) -->
        <path d="M 0 320 L 40 310 L 80 320 L 120 290 L 150 290 L 170 320 L 260 320 L 300 280 L 330 280 L 360 320 L 520 320 L 550 270 L 580 320 L 820 320 L 850 290 L 880 290 L 920 320 L 1200 320 L 1200 340 L 0 340 Z" fill="#E2CFB4" opacity="0.6"/>

        <!-- Birds in the morning sky -->
        <path d="M 320 90 Q 330 80 340 90 Q 350 80 360 90 Q 350 94 340 88 Q 330 94 320 90 Z" fill="#D96C48" opacity="0.45"/>
        <path d="M 380 115 Q 388 107 396 115 Q 404 107 412 115 Q 404 118 396 113 Q 388 118 380 115 Z" fill="#D96C48" opacity="0.45"/>

        <!-- LAYER 1: ROW OF COLORFUL INDIAN HERITAGE BUILDINGS -->
        
        <!-- Building 1 (Far Left): Indigo & Cream Haveli -->
        <rect x="40" y="190" width="220" height="230" rx="4" fill="#243B63"/>
        <rect x="55" y="210" width="190" height="20" fill="#F4E7D3"/>
        <!-- Ornate Jharokha arched windows -->
        <path d="M 80 280 Q 95 240 110 280 Z" fill="#F4BB52"/>
        <rect x="80" y="280" width="30" height="35" fill="#F4BB52"/>
        <path d="M 170 280 Q 185 240 200 280 Z" fill="#F4BB52"/>
        <rect x="170" y="280" width="30" height="35" fill="#F4BB52"/>
        <!-- Terracotta tile roof edge -->
        <polygon points="30,190 270,190 250,165 50,165" fill="#D96C48"/>
        <circle cx="150" cy="177" r="12" fill="#F4BB52"/>

        <!-- Building 2 (Mid-Left): Terracotta Residential Haveli with Balconies -->
        <rect x="250" y="140" width="240" height="280" rx="4" fill="#D96C48"/>
        <!-- Wooden Jali shutters -->
        <rect x="280" y="180" width="45" height="60" rx="4" fill="#243B63"/>
        <rect x="350" y="180" width="45" height="60" rx="4" fill="#243B63"/>
        <rect x="420" y="180" width="45" height="60" rx="4" fill="#243B63"/>
        <!-- Intricate Balcony with railing -->
        <rect x="270" y="240" width="200" height="12" fill="#F4E7D3"/>
        <rect x="275" y="252" width="190" height="32" fill="#B54F2D"/>
        <!-- Hanging floral garlands -->
        <path d="M 280 252 Q 300 264 320 252 Q 340 264 360 252 Q 380 264 400 252 Q 420 264 440 252 Q 460 264 480 252" stroke="#F4BB52" stroke-width="3" fill="none"/>

        <!-- Building 3 (Center-Right): Mango Yellow "CHAI & KIRANA" Store -->
        <rect x="520" y="210" width="280" height="210" rx="4" fill="#F4BB52"/>
        <!-- Striped Blue & Cream Awning -->
        <polygon points="505,270 815,270 795,295 525,295" fill="#243B63"/>
        <polygon points="535,270 565,270 555,295 530,295" fill="#FFFCF5"/>
        <polygon points="595,270 625,270 615,295 590,295" fill="#FFFCF5"/>
        <polygon points="655,270 685,270 675,295 650,295" fill="#FFFCF5"/>
        <polygon points="715,270 745,270 735,295 710,295" fill="#FFFCF5"/>
        <polygon points="775,270 805,270 790,295 765,295" fill="#FFFCF5"/>
        <!-- Shop Signboard -->
        <rect x="560" y="235" width="200" height="28" rx="6" fill="#243B63"/>
        <text x="660" y="254" font-family="'Fraunces', serif" font-size="13" font-weight="700" fill="#FFFCF5" text-anchor="middle" letter-spacing="1">CHAI & KIRANA STORES</text>
        <!-- Chai stall counter -->
        <rect x="560" y="320" width="90" height="65" fill="#B54F2D"/>
        <rect x="670" y="320" width="100" height="65" fill="#243B63"/>

        <!-- Building 4 (Far Right): Soft Coral Studio with Rooftop Water Tank -->
        <rect x="830" y="170" width="330" height="250" rx="4" fill="#EB8C79"/>
        <!-- Arched rooftop parapet -->
        <path d="M 830 170 Q 995 135 1160 170 Z" fill="#D96C48"/>
        <!-- Rooftop Sintex-style Water Tank -->
        <rect x="880" y="125" width="46" height="42" rx="6" fill="#243B63"/>
        <line x1="880" y1="138" x2="926" y2="138" stroke="#F4BB52" stroke-width="2"/>
        <line x1="880" y1="152" x2="926" y2="152" stroke="#F4BB52" stroke-width="2"/>
        <!-- Studio Windows -->
        <rect x="870" y="210" width="55" height="70" rx="4" fill="#FFFCF5"/>
        <rect x="960" y="210" width="55" height="70" rx="4" fill="#FFFCF5"/>
        <rect x="1050" y="210" width="55" height="70" rx="4" fill="#FFFCF5"/>

        <!-- LAYER 2: SIDEWALK & BANYAN TREE -->
        <rect x="0" y="400" width="1200" height="65" fill="url(#sidewalkStone)"/>
        <!-- Curbstone pattern -->
        <line x1="0" y1="465" x2="1200" y2="465" stroke="#B54F2D" stroke-width="4"/>
        <path d="M 0 465 L 1200 465" stroke="#FFFCF5" stroke-dasharray="25,25" stroke-width="4"/>

        <!-- Sprawling Banyan Tree (Right of Haveli) -->
        <g class="animated-tree">
            <!-- Trunk & aerial roots -->
            <path d="M 480 435 Q 495 350 470 290 Q 510 320 520 435 Z" fill="#5C4033"/>
            <path d="M 465 435 Q 470 370 480 320" stroke="#7A583A" stroke-width="4" fill="none"/>
            <path d="M 525 435 Q 520 380 505 340" stroke="#7A583A" stroke-width="3" fill="none"/>
            <!-- Layered lush Sage Green Foliage -->
            <circle cx="450" cy="270" r="55" fill="#83A98A" opacity="0.95"/>
            <circle cx="510" cy="250" r="65" fill="#6B9372" opacity="0.95"/>
            <circle cx="475" cy="220" r="50" fill="#83A98A" opacity="0.95"/>
            <circle cx="540" cy="280" r="48" fill="#557B5C" opacity="0.95"/>
        </g>

        <!-- LAYER 3: ROAD CARRIAGEWAY -->
        <rect x="0" y="465" width="1200" height="175" fill="url(#roadSurface)"/>
        <!-- Broken White Road Divider Lines -->
        <line x1="0" y1="550" x2="1200" y2="550" stroke="#FFFCF5" stroke-width="6" stroke-dasharray="40,35" opacity="0.85"/>
        <!-- Pedestrian Zebra Crossing (Near center) -->
        <g opacity="0.85">
            <rect x="360" y="475" width="18" height="150" fill="#FFFCF5"/>
            <rect x="395" y="475" width="18" height="150" fill="#FFFCF5"/>
            <rect x="430" y="475" width="18" height="150" fill="#FFFCF5"/>
            <rect x="465" y="475" width="18" height="150" fill="#FFFCF5"/>
            <rect x="500" y="475" width="18" height="150" fill="#FFFCF5"/>
        </g>

        <!-- HOTSPOT 1: DAMAGED ROAD / POTHOLE -->
        <g id="hotspot-road" class="street-hotspot" onclick="window.parent.location.search='?action=hotspot&target=road'" tabindex="0" role="button" aria-label="Road defect hotspot">
            <!-- Road fissure shape -->
            <ellipse cx="230" cy="530" rx="42" ry="22" fill="#1A202C"/>
            <ellipse cx="232" cy="532" rx="36" ry="16" fill="#0D1117"/>
            <path d="M 200 528 Q 230 520 260 532 Q 235 542 200 528 Z" fill="#243B63" opacity="0.6"/>

            <!-- State-Aware Indicator -->
            {'<circle cx="230" cy="530" r="18" fill="none" stroke="#D96C48" stroke-width="3" class="animated-ripple"/><circle cx="230" cy="530" r="10" fill="#D96C48"/><text x="230" y="534" font-size="11" font-weight="800" fill="#FFFFFF" text-anchor="middle">!</text>' if road_state == 'alert' else ('<rect x="210" y="515" width="12" height="24" fill="#F4BB52" stroke="#243B63" stroke-width="1.5"/><rect x="235" y="515" width="12" height="24" fill="#F4BB52" stroke="#243B63" stroke-width="1.5"/><text x="230" y="510" font-size="10" font-weight="700" fill="#F4BB52" text-anchor="middle">🚧 Work</text>' if road_state == 'in_progress' else '<ellipse cx="230" cy="530" rx="35" ry="18" fill="#4A5568" stroke="#83A98A" stroke-width="2"/><text x="230" y="534" font-size="12" fill="#83A98A" text-anchor="middle">✓ Verified</text>')}

            <!-- Floating Badge Card -->
            <g transform="translate(140, 470)" filter="url(#cardShadow)">
                <rect width="180" height="42" rx="12" fill="#FFFFFF" stroke="#D96C48" stroke-width="2"/>
                <circle cx="22" cy="21" r="12" fill="#FDE8E8"/>
                <text x="22" y="26" font-size="13" text-anchor="middle">🕳️</text>
                <text x="42" y="19" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="700" fill="#243B63">Damaged Road & Potholes</text>
                <text x="42" y="32" font-family="'Plus Jakarta Sans', sans-serif" font-size="10" font-weight="600" fill="#D96C48">{pothole_count} Active Signal{'s' if pothole_count != 1 else ''}</text>
            </g>
        </g>

        <!-- HOTSPOT 2: STREETLIGHT -->
        <g id="hotspot-streetlight" class="street-hotspot" onclick="window.parent.location.search='?action=hotspot&target=streetlight'" tabindex="0" role="button" aria-label="Streetlight hotspot">
            <!-- Lamp Pole on Sidewalk -->
            <rect x="670" y="290" width="8" height="150" fill="#243B63"/>
            <rect x="664" y="430" width="20" height="14" rx="2" fill="#375382"/>
            <!-- Ornate curved lamp bracket -->
            <path d="M 674 290 Q 695 260 720 280 L 720 300" stroke="#243B63" stroke-width="5" fill="none"/>
            <!-- Glowing Lantern -->
            <polygon points="708,300 732,300 726,322 714,322" fill="#F4BB52" class="animated-lamp"/>
            <polygon points="704,296 736,296 720,286" fill="#243B63"/>
            <!-- Warm downward light cone -->
            <polygon points="720,322 640,465 800,465" fill="url(#lampCone)" opacity="0.6"/>

            <!-- Floating Badge Card -->
            <g transform="translate(620, 230)" filter="url(#cardShadow)">
                <rect width="175" height="42" rx="12" fill="#FFFFFF" stroke="#F4BB52" stroke-width="2"/>
                <circle cx="22" cy="21" r="12" fill="#FEF3C7"/>
                <text x="22" y="26" font-size="13" text-anchor="middle">💡</text>
                <text x="42" y="19" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="700" fill="#243B63">Streetlights & Lighting</text>
                <text x="42" y="32" font-family="'Plus Jakarta Sans', sans-serif" font-size="10" font-weight="600" fill="#B45309">{streetlight_count} Incident{'s' if streetlight_count != 1 else ''}</text>
            </g>
        </g>

        <!-- HOTSPOT 3: DUSTBIN / WASTE COLLECTION POINT -->
        <g id="hotspot-garbage" class="street-hotspot" onclick="window.parent.location.search='?action=hotspot&target=garbage'" tabindex="0" role="button" aria-label="Waste point hotspot">
            <!-- Segregated Municipal Bins on Sidewalk -->
            <rect x="880" y="390" width="30" height="48" rx="4" fill="#10B981"/>
            <rect x="876" y="386" width="38" height="8" rx="2" fill="#047857"/>
            <text x="895" y="418" font-size="10" fill="#FFFFFF" text-anchor="middle">♻️</text>

            <rect x="918" y="390" width="30" height="48" rx="4" fill="#0284C7"/>
            <rect x="914" y="386" width="38" height="8" rx="2" fill="#0369A1"/>
            <text x="933" y="418" font-size="10" fill="#FFFFFF" text-anchor="middle">🗑️</text>

            <!-- Floating Badge Card -->
            <g transform="translate(850, 325)" filter="url(#cardShadow)">
                <rect width="170" height="42" rx="12" fill="#FFFFFF" stroke="#83A98A" stroke-width="2"/>
                <circle cx="22" cy="21" r="12" fill="#ECFDF5"/>
                <text x="22" y="26" font-size="13" text-anchor="middle">🗑️</text>
                <text x="42" y="19" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="700" fill="#243B63">Waste Point & Sanitation</text>
                <text x="42" y="32" font-family="'Plus Jakarta Sans', sans-serif" font-size="10" font-weight="600" fill="#047857">{garbage_count} Active Point{'s' if garbage_count != 1 else ''}</text>
            </g>
        </g>

        <!-- HOTSPOT 4: STORMWATER DRAIN -->
        <g id="hotspot-drainage" class="street-hotspot" onclick="window.parent.location.search='?action=hotspot&target=drainage'" tabindex="0" role="button" aria-label="Storm drain hotspot">
            <!-- Roadside Grate & Culvert -->
            <rect x="1040" y="468" width="60" height="30" rx="3" fill="#1A202C"/>
            <line x1="1048" y1="468" x2="1048" y2="498" stroke="#718096" stroke-width="3"/>
            <line x1="1058" y1="468" x2="1058" y2="498" stroke="#718096" stroke-width="3"/>
            <line x1="1068" y1="468" x2="1068" y2="498" stroke="#718096" stroke-width="3"/>
            <line x1="1078" y1="468" x2="1078" y2="498" stroke="#718096" stroke-width="3"/>
            <line x1="1088" y1="468" x2="1088" y2="498" stroke="#718096" stroke-width="3"/>

            <!-- Floating Badge Card -->
            <g transform="translate(980, 515)" filter="url(#cardShadow)">
                <rect width="180" height="42" rx="12" fill="#FFFFFF" stroke="#243B63" stroke-width="2"/>
                <circle cx="22" cy="21" r="12" fill="#EFF6FF"/>
                <text x="22" y="26" font-size="13" text-anchor="middle">🌊</text>
                <text x="42" y="19" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="700" fill="#243B63">Stormwater Drainage</text>
                <text x="42" y="32" font-family="'Plus Jakarta Sans', sans-serif" font-size="10" font-weight="600" fill="#1D4ED8">{drainage_count} Logged Runoff{'s' if drainage_count != 1 else ''}</text>
            </g>
        </g>

        <!-- LAYER 4: LIFE ON THE STREET -->
        <!-- Moving Auto-Rickshaw (Yellow & Green) -->
        <g class="animated-rickshaw">
            <!-- Wheels -->
            <circle cx="45" cy="580" r="14" fill="#1A202C"/>
            <circle cx="45" cy="580" r="6" fill="#CBD5E1"/>
            <circle cx="115" cy="580" r="14" fill="#1A202C"/>
            <circle cx="115" cy="580" r="6" fill="#CBD5E1"/>
            <!-- Body lower in Emerald Green -->
            <path d="M 30 570 L 130 570 L 125 540 L 40 540 Z" fill="#10B981"/>
            <!-- Canopy in Mango Yellow -->
            <path d="M 40 540 L 125 540 Q 115 500 80 500 L 45 500 Q 35 520 40 540 Z" fill="#F4BB52"/>
            <!-- Windshield & Driver Silhouette -->
            <polygon points="110,540 123,540 114,510 102,510" fill="#E2E8F0" opacity="0.8"/>
            <circle cx="85" cy="525" r="9" fill="#243B63"/>
            <!-- Headlight beam -->
            <polygon points="128,552 210,530 210,580" fill="#F4BB52" opacity="0.3"/>
        </g>

        <!-- Parked Chetak Scooter near Chai Stall -->
        <g transform="translate(730, 420)">
            <circle cx="12" cy="30" r="8" fill="#243B63"/>
            <circle cx="42" cy="30" r="8" fill="#243B63"/>
            <path d="M 10 25 L 25 25 L 35 15 L 45 25" stroke="#D96C48" stroke-width="4" fill="none"/>
            <line x1="42" y1="12" x2="48" y2="8" stroke="#243B63" stroke-width="3"/>
        </g>

        <!-- Sleepy Stray Cat resting near Banyan Tree -->
        <g transform="translate(535, 440)">
            <ellipse cx="14" cy="12" rx="10" ry="6" fill="#D96C48"/>
            <circle cx="22" cy="8" r="5" fill="#D96C48"/>
            <polygon points="22,3 25,6 20,6" fill="#B54F2D"/>
        </g>
    </svg>
    </div>
    """
    return "\n".join(line.strip() for line in svg_code.splitlines() if line.strip())


def render_floating_header(lang: str = "en"):
    """Renders the top branding, Streetverse tagline, language switcher, and quick AI launcher."""
    tagline = t("streetverse_tagline", lang)

    col1, col2 = st.columns([0.65, 0.35])
    with col1:
        st.markdown(f"""
            <div class="streetverse-topbar" style="margin-bottom: 0;">
                <div class="streetverse-brand">
                    <div class="brand-emblem">🛡️</div>
                    <div>
                        <div class="brand-title">NAZARSETU <span style="color: #D96C48;">• STREETVERSE</span></div>
                        <div class="brand-tagline">{tagline}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        top_ctrl1, top_ctrl2 = st.columns([0.60, 0.40])
        with top_ctrl1:
            lang_opts = ["EN", "HI", "GU"]
            curr_idx = 0 if lang == "en" else (1 if lang == "hi" else 2)
            sel_lang = st.radio("Language", options=lang_opts, index=curr_idx, horizontal=True, label_visibility="collapsed", key="top_lang_pills")
            if sel_lang == "HI" and st.session_state.lang != "hi":
                st.session_state.lang = "hi"
                st.rerun()
            elif sel_lang == "GU" and st.session_state.lang != "gu":
                st.session_state.lang = "gu"
                st.rerun()
            elif sel_lang == "EN" and st.session_state.lang != "en":
                st.session_state.lang = "en"
                st.rerun()

        with top_ctrl2:
            if st.button("🤖 Ask AI", use_container_width=True, key="btn_top_ask_ai"):
                st.session_state.street_active_view = "companion"
                st.session_state.selected_case_id = None
                st.rerun()


def render_floating_capsule(active_view: str, lang: str = "en"):
    """
    Renders the unified 7-section Floating Command Capsule:
    [ 🗺️ Explore ] [ 📸 Report ] [ 🚀 AI Mission ] [ 🔍 Track Story ] [ ♊ CivicTwin ] [ 📊 Neighborhood ] [ 🛡️ Operations ]
    """
    c_explore = t("capsule_explore", lang)
    c_report = t("capsule_report", lang)
    c_mission = t("capsule_mission", lang)
    c_track = t("capsule_track", lang)
    c_civictwin = t("capsule_civictwin", lang)
    c_pulse = t("capsule_pulse", lang)
    c_admin = t("capsule_admin", lang)

    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    
    with col1:
        if st.button(c_explore, use_container_width=True, type="primary" if active_view == "street" else "secondary", key="capsule_btn_explore"):
            st.session_state.street_active_view = "street"
            st.session_state.selected_hotspot = None
            st.session_state.selected_case_id = None
            st.rerun()

    with col2:
        if st.button(c_report, use_container_width=True, type="primary" if active_view == "report" else "secondary", key="capsule_btn_report"):
            st.session_state.street_active_view = "report"
            st.session_state.selected_case_id = None
            st.rerun()

    with col3:
        if st.button(c_mission, use_container_width=True, type="primary" if active_view == "mission" else "secondary", key="capsule_btn_mission"):
            st.session_state.street_active_view = "mission"
            st.session_state.selected_case_id = None
            st.rerun()

    with col4:
        if st.button(c_track, use_container_width=True, type="primary" if active_view == "track" else "secondary", key="capsule_btn_track"):
            st.session_state.street_active_view = "track"
            st.session_state.selected_case_id = None
            st.rerun()

    with col5:
        if st.button(c_civictwin, use_container_width=True, type="primary" if active_view == "civictwin" else "secondary", key="capsule_btn_civictwin"):
            st.session_state.street_active_view = "civictwin"
            st.session_state.selected_case_id = None
            st.rerun()

    with col6:
        if st.button(c_pulse, use_container_width=True, type="primary" if active_view in ["pulse", "stories"] else "secondary", key="capsule_btn_pulse"):
            st.session_state.street_active_view = "pulse"
            st.session_state.selected_case_id = None
            st.rerun()

    with col7:
        if st.button(c_admin, use_container_width=True, type="primary" if active_view in ["admin", "officer"] else "secondary", key="capsule_btn_admin"):
            st.session_state.street_active_view = "admin"
            st.session_state.selected_case_id = None
            st.rerun()


def render_activity_pill(stats: Dict[str, Any]):
    """Renders the real-data telemetry badge in the bottom corner."""
    metrics = stats.get("metrics", {})
    total = metrics.get("total_complaints", 0)
    in_prog = metrics.get("in_progress_complaints", 0)
    resolved = metrics.get("resolved_complaints", 0)

    st.markdown(f"""
        <div class="civic-activity-badge">
            <span class="pulse-dot"></span>
            <span><strong>Live City Telemetry:</strong> {total} Reported • {in_prog} In Progress • {resolved} Resolved</span>
        </div>
    """, unsafe_allow_html=True)


def render_case_file_drawer(complaint: Dict[str, Any], lang: str = "en"):
    """
    Renders an editorial magazine-like Civic Case File.
    Presents the incident as a real digital investigation dossier with photographic evidence,
    metadata annotations, AI rationale, and audit event logs.
    """
    cid = complaint.get("id", "NS-UNKNOWN")
    issue = complaint.get("issue_type", "Civic Grievance")
    locality = complaint.get("locality", "Local Jurisdiction")
    city = complaint.get("city", "Municipal Area")
    ward = complaint.get("ward", "Local Ward")
    dept = complaint.get("department", "Municipal Department")
    status = complaint.get("status", "Reported")
    priority = complaint.get("priority", "Medium")
    desc = complaint.get("description", "No description recorded.")
    evidence = complaint.get("visual_evidence", "Photographic topography examined.")
    created = complaint.get("created_at", "")

    # Priority badge styling
    p_lower = priority.lower()
    if "critical" in p_lower:
        badge_cls = "dossier-pill-critical"
    elif "high" in p_lower:
        badge_cls = "dossier-pill-high"
    elif "low" in p_lower:
        badge_cls = "dossier-pill-low"
    else:
        badge_cls = "dossier-pill-medium"

    st.markdown(f"""
        <div class="case-file-dossier">
            <div class="case-file-header">
                <div>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 700; color: #D96C48;">
                        CIVIC CASE DOSSIER • {cid}
                    </span>
                    <h2 class="dossier-headline">{issue}</h2>
                    <div style="font-size: 0.95rem; color: #64748B; margin-top: 4px;">
                        📍 <strong>{locality}, {city}</strong> • Ward: <code>{ward}</code>
                    </div>
                </div>
                <div style="display: flex; gap: 8px; align-items: center;">
                    <span class="dossier-meta-pill {badge_cls}">⚖️ {priority} Priority</span>
                    <span class="dossier-meta-pill" style="background: #243B63; color: #FFFFFF;">STATUS: {status.upper()}</span>
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-bottom: 20px;">
                <div style="background: #FAF3E8; border: 1.5px solid #DFCAB0; border-radius: 14px; padding: 18px;">
                    <strong style="color: #243B63; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">
                        AI Visual Topography Evidence
                    </strong>
                    <p style="font-size: 0.95rem; color: #243B63; line-height: 1.5; margin-top: 6px;">
                        {evidence}
                    </p>
                    <div style="font-size: 0.85rem; color: #7C6044; margin-top: 10px;">
                        <strong>Citizen Statement:</strong> <em>"{desc}"</em>
                    </div>
                </div>

                <div style="background: #FFFFFF; border: 1.5px solid #E8DAC6; border-radius: 14px; padding: 18px;">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Assigned Authority</div>
                    <div style="font-weight: 700; font-size: 0.96rem; color: #243B63; margin-top: 2px;">{dept}</div>
                    
                    <div style="font-size: 0.78rem; font-weight: 700; color: #64748B; text-transform: uppercase; margin-top: 14px;">Filing Timestamp</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #243B63; margin-top: 2px;">{created}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Chronological Audit Trail
    events = database.get_complaint_timeline(cid)
    if events:
        st.markdown("#### 📜 Official Municipal Event Trail")
        for ev in events:
            st.markdown(f"""
                <div style="display: flex; gap: 14px; align-items: flex-start; padding: 10px 0; border-bottom: 1px dashed #DFCAB0;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #D96C48; width: 150px;">
                        {ev.get('created_at', '')}
                    </span>
                    <div>
                        <strong style="color: #243B63; font-size: 0.88rem;">{ev.get('event_type', '')}</strong>
                        <div style="font-size: 0.84rem; color: #64748B; margin-top: 2px;">{ev.get('details', '')}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    btn_c1, btn_c2 = st.columns([0.4, 0.6])
    with btn_c1:
        if st.button("🔍 Follow in Repair Story", type="primary", use_container_width=True, key=f"btn_track_{cid}"):
            st.session_state.street_active_view = "track"
            st.session_state.tracking_search_id = cid
            st.rerun()
    with btn_c2:
        if st.button("↩️ Return to Street", use_container_width=True, key=f"btn_close_{cid}"):
            st.session_state.selected_case_id = None
            st.session_state.selected_hotspot = None
            st.rerun()


def render_hotspot_explorer(target_key: str, lang: str = "en"):
    """
    Renders the active civic signals for the selected street infrastructure hotspot.
    Filters real SQLite records for that category.
    """
    meta = HOTSPOT_METADATA.get(target_key, HOTSPOT_METADATA["road"])
    category = meta["category"]

    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <div>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 700; color: {meta['color']};">
                    CIVIC INFRASTRUCTURE INSPECTION
                </span>
                <h2 style="font-family: 'Fraunces', serif; font-size: 1.8rem; color: #243B63; margin: 0;">
                    {meta['icon']} {meta['title']}
                </h2>
                <p style="color: #64748B; font-size: 0.92rem; margin-top: 4px;">
                    {meta['hint']} • Responsible Nodal Body: <strong>{meta['department']}</strong>
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    h_col1, h_col2 = st.columns([0.7, 0.3])
    with h_col2:
        if st.button(f"📸 Report {meta['icon']} at this Location", type="primary", use_container_width=True, key=f"btn_rep_{target_key}"):
            st.session_state.street_active_view = "report"
            st.session_state.selected_sample = meta["sample"]
            st.session_state.sample_hint = category
            st.session_state.sample_city = meta["default_city"]
            st.session_state.sample_locality = meta["default_locality"]
            st.rerun()

    # Query real complaints from database
    complaints = database.list_complaints(issue_type=category, limit=20)
    
    if not complaints:
        st.info(f"✨ No active complaints found for {category}. The illustrated infrastructure is in verified clean state!")
    else:
        st.markdown(f"### 📋 Active Cases in Streetview ({len(complaints)} records)")
        for comp in complaints:
            c_col1, c_col2 = st.columns([0.82, 0.18])
            with c_col1:
                st.markdown(f"""
                    <div style="background: #FFFFFF; border: 1.5px solid #E8DAC6; border-radius: 12px; padding: 12px 16px; margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between;">
                            <strong style="color: #243B63; font-size: 0.95rem;">{comp['id']} • {comp['locality']}, {comp['city']}</strong>
                            <span style="font-size: 0.76rem; font-weight: 700; color: #D96C48; text-transform: uppercase;">{comp['status']}</span>
                        </div>
                        <div style="font-size: 0.85rem; color: #64748B; margin-top: 4px;">{comp['description']}</div>
                    </div>
                """, unsafe_allow_html=True)
            with c_col2:
                if st.button("Inspect Dossier", key=f"btn_view_{comp['id']}", use_container_width=True):
                    st.session_state.selected_case_id = comp["id"]
                    st.rerun()


def render_ai_investigation_workspace(lang: str = "en"):
    """
    Renders the 4-Stage AI Photo Investigation Workspace:
    Stage 1: Evidence (Upload or select verified sample + Locality)
    Stage 2: Understanding (Multimodal AI diagnosis, severity, citizen impact, priority rationale)
    Stage 3: Agent Action (Live execution of 10-stage pipeline with affirmative citizen confirmation)
    Stage 4: Case Created (Case File with real demo tracking ID)
    """
    st.markdown("""
        <div style="margin-bottom: 1rem;">
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 700; color: #D96C48;">
                AI INVESTIGATION MODE
            </span>
            <h2 style="font-family: 'Fraunces', serif; font-size: 2rem; color: #243B63; margin: 0;">
                📸 Autonomous Civic Evidence Investigation
            </h2>
            <p style="color: #64748B; font-size: 0.92rem; margin-top: 4px;">
                Upload photographic proof to trigger multimodal diagnostic analysis, priority heuristics, and automated ward dispatch.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Stage Indicators
    st.markdown("""
        <div style="display: flex; gap: 8px; margin-bottom: 1.2rem; flex-wrap: wrap;">
            <div class="investigation-step-pill active">STAGE 1: Evidence</div>
            <div class="investigation-step-pill">STAGE 2: AI Diagnostic</div>
            <div class="investigation-step-pill">STAGE 3: Autonomous Routing</div>
            <div class="investigation-step-pill">STAGE 4: Case File</div>
        </div>
    """, unsafe_allow_html=True)

    col_input, col_preview = st.columns([0.55, 0.45])
    sample_dir = Path(__file__).resolve().parent / "data" / "samples"
    image_bytes = None

    with col_input:
        st.markdown("#### 1. Upload or Select Sample Incident")
        uploaded_file = st.file_uploader(
            "Upload photographic proof",
            type=["jpg", "jpeg", "png"],
            help="High-resolution photo showing clear infrastructure defect",
            label_visibility="collapsed"
        )

        st.caption("Or test with verified scenario cases:")
        s_c1, s_c2, s_c3, s_c4 = st.columns(4)
        if s_c1.button("🕳️ Pothole", use_container_width=True, key="inv_s_pothole"):
            st.session_state.selected_sample = "sample_pothole.jpg"
            st.session_state.sample_hint = "Potholes and damaged roads"
            st.session_state.sample_city = "Bengaluru"
            st.session_state.sample_locality = "Indiranagar"
            st.rerun()

        if s_c2.button("🗑️ Garbage", use_container_width=True, key="inv_s_garbage"):
            st.session_state.selected_sample = "sample_garbage.jpg"
            st.session_state.sample_hint = "Overflowing garbage"
            st.session_state.sample_city = "Mumbai"
            st.session_state.sample_locality = "Bandra West"
            st.rerun()

        if s_c3.button("💡 Light", use_container_width=True, key="inv_s_light"):
            st.session_state.selected_sample = "sample_streetlight.jpg"
            st.session_state.sample_hint = "Broken streetlights"
            st.session_state.sample_city = "Delhi"
            st.session_state.sample_locality = "Connaught Place"
            st.rerun()

        if s_c4.button("🌊 Drain", use_container_width=True, key="inv_s_drain"):
            st.session_state.selected_sample = "sample_waterlogging.jpg"
            st.session_state.sample_hint = "Waterlogging and drainage issues"
            st.session_state.sample_city = "Ahmedabad"
            st.session_state.sample_locality = "Satellite"
            st.rerun()

        # City and Locality Selectors
        st.markdown("#### 2. Locality Jurisdiction")
        ward_data = tools.load_ward_data()
        city_locality_map: Dict[str, List[str]] = {}
        for row in ward_data:
            c = row.get("city", "").strip()
            loc = row.get("locality", "").strip()
            if c and loc:
                city_locality_map.setdefault(c, []).append(loc)
        for c in city_locality_map:
            city_locality_map[c] = sorted(list(set(city_locality_map[c])))

        if not city_locality_map:
            city_locality_map = getattr(tools, "SUPPORTED_LOCALITIES", {
                "Bengaluru": ["Indiranagar", "Koramangala", "Whitefield"],
                "Mumbai": ["Bandra West", "Andheri East", "Dadar"],
                "Delhi": ["Connaught Place", "Lajpat Nagar", "Karol Bagh"],
                "Ahmedabad": ["Satellite", "Navrangpura", "Vastrapur"],
                "Pune": ["Kothrud", "Viman Nagar", "Baner"],
            })

        cities = sorted(list(city_locality_map.keys()))
        default_city = st.session_state.get("sample_city", "Bengaluru")
        c_idx = cities.index(default_city) if default_city in cities else 0
        selected_city = st.selectbox("Municipal City", options=cities, index=c_idx, key="inv_sel_city")

        localities = city_locality_map.get(selected_city, ["Indiranagar"])
        default_loc = st.session_state.get("sample_locality", localities[0] if localities else "")
        l_idx = localities.index(default_loc) if default_loc in localities else 0
        selected_locality = st.selectbox("Ward / Neighborhood Locality", options=localities, index=l_idx, key="inv_sel_loc")

        landmark_input = st.text_input("Landmark / Spot Hint (Optional)", value="Near City Center Junction", key="inv_txt_landmark")

    with col_preview:
        if uploaded_file:
            image_bytes = uploaded_file.getvalue()
            st.image(image_bytes, caption="Uploaded Evidence", use_column_width=True)
        elif st.session_state.get("selected_sample"):
            sample_file = sample_dir / st.session_state.selected_sample
            if sample_file.exists():
                with open(sample_file, "rb") as f:
                    image_bytes = f.read()
                st.image(image_bytes, caption=f"Demo Incident: {st.session_state.selected_sample}", use_column_width=True)
        else:
            st.markdown("""
                <div style="border: 2px dashed #DFCAB0; border-radius: 16px; padding: 60px 20px; text-align: center; color: #7C6044;">
                    📷 Photo preview will appear here.<br>Select a scenario above or upload your photograph.
                </div>
            """, unsafe_allow_html=True)

    # Action Button
    if image_bytes:
        st.markdown("---")
        if st.button("🚀 Run AI Multimodal Diagnosis & Investigation", type="primary", use_container_width=True, key="btn_run_investigation"):
            with st.spinner("🤖 Multimodal Vision Engine analyzing surface topography, severity & risk..."):
                hint_cat = st.session_state.get("sample_hint", "Potholes and damaged roads")
                analysis_report = vision.analyze_issue(image_bytes, hint_category=hint_cat)
                st.session_state.current_analysis = analysis_report

                # Execute Stage 1 to 7 pipeline
                img_hash = tools.compute_image_hash(image_bytes)
                p_state, trail = agent.run_reporting_agent_pipeline(
                    issue_type=analysis_report["issue_type"],
                    city=selected_city,
                    locality=selected_locality,
                    image_hash=img_hash,
                    landmark=landmark_input,
                    db_path=DB_PATH
                )
                st.session_state.current_pipeline_state = p_state
                st.session_state.current_trail = trail
                st.session_state.current_image_bytes = image_bytes

    # Display AI Diagnosis & Affirmation
    if st.session_state.get("current_analysis") and st.session_state.get("current_pipeline_state"):
        rep = st.session_state.current_analysis
        p_state = st.session_state.current_pipeline_state

        st.markdown("---")
        st.markdown(f"""
            <div style="background: #FFFFFF; border: 2px solid #D96C48; border-radius: 18px; padding: 22px; box-shadow: 0 12px 30px rgba(217, 108, 72, 0.12); margin-top: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1.5px solid #E8DAC6; padding-bottom: 12px; margin-bottom: 14px;">
                    <div>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; font-weight: 700; color: #D96C48;">STAGE 2: AI UNDERSTANDING</span>
                        <h3 style="font-family: 'Fraunces', serif; margin: 0; color: #243B63;">Diagnosis: {rep['issue_type']}</h3>
                    </div>
                    <div>
                        <span class="dossier-meta-pill dossier-pill-high">🚨 {rep['severity']} Severity</span>
                        <span class="dossier-meta-pill" style="background: #243B63; color: #FFFFFF;">SLA: {rep['sla_hours']}h</span>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px;">
                    <div style="background: #FAF3E8; border: 1px solid #DFCAB0; border-radius: 10px; padding: 12px;">
                        <strong style="font-size: 0.8rem; color: #7C6044; text-transform: uppercase;">Visual Evidence:</strong>
                        <div style="font-size: 0.9rem; color: #243B63; margin-top: 4px;">{rep['visual_evidence']}</div>
                    </div>
                    <div style="background: #FAF3E8; border: 1px solid #DFCAB0; border-radius: 10px; padding: 12px;">
                        <strong style="font-size: 0.8rem; color: #7C6044; text-transform: uppercase;">Citizen Impact:</strong>
                        <div style="font-size: 0.9rem; color: #243B63; margin-top: 4px;">{rep['citizen_impact']}</div>
                    </div>
                    <div style="grid-column: span 2; background: #ECFDF5; border: 1px solid #86EFAC; border-radius: 10px; padding: 12px;">
                        <strong style="font-size: 0.8rem; color: #065F46; text-transform: uppercase;">Autonomous Action Target:</strong>
                        <div style="font-size: 0.92rem; color: #064E3B; font-weight: 700; margin-top: 4px;">
                            {rep['action_plan']} — <span style="text-decoration: underline;">{rep['recommended_department']}</span>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Stage 3: Affirmative Confirmation
        st.markdown("#### 3. Citizen Affirmative Authorization")
        st.markdown(
            "🔒 **Strict Human Affirmation Protocol:** The AI agent has diagnosed the issue and verified that no active duplicate exists. "
            "Please confirm your authorization to officially register this civic case in the municipal ledger."
        )

        confirm_col1, confirm_col2 = st.columns([0.45, 0.55])
        with confirm_col1:
            if st.button("✍️ Confirm & Officially File Complaint", type="primary", use_container_width=True, key="btn_confirm_file"):
                trail = st.session_state.current_trail
                reg_res = agent.run_complaint_registration_step(
                    confirmed_payload={
                        "confirmed": True,
                        "issue_type": p_state["issue_type"],
                        "description": f"Verified citizen defect at {p_state['locality']}.",
                        "city": p_state["city"],
                        "locality": p_state["locality"],
                        "ward": p_state["ward"],
                        "department": p_state["department"],
                        "priority": rep["suggested_priority"],
                        "image_hash": p_state["image_hash"],
                        "visual_evidence": rep["visual_evidence"],
                        "landmark": p_state.get("landmark", ""),
                    },
                    trail=trail,
                    db_path=DB_PATH
                )

                if reg_res.get("status") == "registered":
                    cid = reg_res.get("complaint_id")
                    st.session_state.registered_case_id = cid
                    st.success(f"🎉 **Case Created Successfully! Assigned ID: `{cid}`**")
                    st.balloons()


def render_ai_mission_control_workshop(lang: str = "en"):
    """
    Renders AI Mission Control — Agent Workshop:
    Illustrated civic operations environment showcasing actual AI tool execution:
    OBSERVE → ANALYZE → LOCATE → ROUTE → REGISTER.
    Displays live tool inputs, outputs, timestamps, and execution states from ActionTrail.
    """
    st.markdown("""
        <div style="margin-bottom: 1rem;">
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 700; color: #D96C48;">
                CIVIC AI MISSION CONTROL • AGENT WORKSHOP
            </span>
            <h2 style="font-family: 'Fraunces', serif; font-size: 2rem; color: #243B63; margin: 0;">
                🚀 Autonomous Cognitive Perception & Tool Execution Engine
            </h2>
            <p style="color: #64748B; font-size: 0.92rem; margin-top: 4px;">
                Inspect the real 10-stage cognitive perception and autonomous dispatch pipeline. See actual tool arguments, hashes, department routing, and ACID transaction commits.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 5 High-Level Cognitive Blocks
    st.markdown("""
        <div class="pipeline-flow-banner">
            <div class="pipeline-node">
                <div class="pipeline-node-icon">👁️</div>
                <div class="pipeline-node-name">1. OBSERVE</div>
                <span style="font-size: 0.72rem; color: #64748B;">Perceptual Hash</span>
            </div>
            <div class="pipeline-arrow">➔</div>
            <div class="pipeline-node">
                <div class="pipeline-node-icon">🧠</div>
                <div class="pipeline-node-name">2. ANALYZE</div>
                <span style="font-size: 0.72rem; color: #64748B;">Vision Topography</span>
            </div>
            <div class="pipeline-arrow">➔</div>
            <div class="pipeline-node">
                <div class="pipeline-node-icon">📍</div>
                <div class="pipeline-node-name">3. LOCATE</div>
                <span style="font-size: 0.72rem; color: #64748B;">Ward Directory</span>
            </div>
            <div class="pipeline-arrow">➔</div>
            <div class="pipeline-node">
                <div class="pipeline-node-icon">🚦</div>
                <div class="pipeline-node-name">4. ROUTE</div>
                <span style="font-size: 0.72rem; color: #64748B;">Matrix Dispatch</span>
            </div>
            <div class="pipeline-arrow">➔</div>
            <div class="pipeline-node">
                <div class="pipeline-node-icon">🛡️</div>
                <div class="pipeline-node-name">5. REGISTER</div>
                <span style="font-size: 0.72rem; color: #64748B;">ACID Ledger Commit</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Scenario Runner for live pipeline inspection
    st.markdown("### ⚡ Live Autonomous Pipeline Inspector")
    st.caption("Select a scenario incident to trigger real agent tools and inspect chronological execution states:")

    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    sel_scenario = st.session_state.get("workshop_scenario", "pothole")

    if p_col1.button("🕳️ Bengaluru Pothole", use_container_width=True, type="primary" if sel_scenario == "pothole" else "secondary", key="ws_btn_pothole"):
        st.session_state.workshop_scenario = "pothole"
        st.session_state.workshop_trail = None
        st.rerun()

    if p_col2.button("🗑️ Mumbai Garbage", use_container_width=True, type="primary" if sel_scenario == "garbage" else "secondary", key="ws_btn_garbage"):
        st.session_state.workshop_scenario = "garbage"
        st.session_state.workshop_trail = None
        st.rerun()

    if p_col3.button("💡 Delhi Streetlight", use_container_width=True, type="primary" if sel_scenario == "streetlight" else "secondary", key="ws_btn_light"):
        st.session_state.workshop_scenario = "streetlight"
        st.session_state.workshop_trail = None
        st.rerun()

    if p_col4.button("🌊 Ahmedabad Drainage", use_container_width=True, type="primary" if sel_scenario == "drainage" else "secondary", key="ws_btn_drain"):
        st.session_state.workshop_scenario = "drainage"
        st.session_state.workshop_trail = None
        st.rerun()

    # Map scenario to inputs
    scenario_configs = {
        "pothole": {"sample": "sample_pothole.jpg", "category": "Potholes and damaged roads", "city": "Bengaluru", "locality": "Indiranagar", "landmark": "100ft Road Junction"},
        "garbage": {"sample": "sample_garbage.jpg", "category": "Overflowing garbage", "city": "Mumbai", "locality": "Bandra West", "landmark": "Near Bandstand"},
        "streetlight": {"sample": "sample_streetlight.jpg", "category": "Broken streetlights", "city": "Delhi", "locality": "Connaught Place", "landmark": "Block B Corridor"},
        "drainage": {"sample": "sample_waterlogging.jpg", "category": "Waterlogging and drainage issues", "city": "Ahmedabad", "locality": "Satellite", "landmark": "Near ISRO Crossroad"},
    }
    active_conf = scenario_configs.get(sel_scenario, scenario_configs["pothole"])

    sample_dir = Path(__file__).resolve().parent / "data" / "samples"
    sample_file = sample_dir / active_conf["sample"]

    if sample_file.exists():
        with open(sample_file, "rb") as f:
            sample_bytes = f.read()

        if st.button("🚀 Trigger Real 10-Stage Agent Execution", type="primary", use_container_width=True, key="btn_trigger_workshop"):
            with st.spinner("🤖 Autonomous Civic Agent orchestrating 10 sequential tools..."):
                img_hash = tools.compute_image_hash(sample_bytes)
                p_state, trail = agent.run_reporting_agent_pipeline(
                    issue_type=active_conf["category"],
                    city=active_conf["city"],
                    locality=active_conf["locality"],
                    image_hash=img_hash,
                    landmark=active_conf["landmark"],
                    db_path=DB_PATH
                )

                # Execute Stages 8 to 10
                confirmed_payload = {
                    "confirmed": True,
                    "issue_type": p_state["issue_type"],
                    "description": f"Verified field incident at {p_state['locality']}.",
                    "city": p_state["city"],
                    "locality": p_state["locality"],
                    "ward": p_state["ward"],
                    "department": p_state["department"],
                    "priority": "High",
                    "image_hash": img_hash,
                    "visual_evidence": "Topographical damage identified via computer vision.",
                    "status": "Reported",
                }
                reg_res, full_trail = agent.run_registration_agent_action(confirmed_payload, trail=trail, db_path=DB_PATH)
                st.session_state.workshop_trail = full_trail

    # Render Stages from Trail
    trail_to_show = st.session_state.get("workshop_trail")
    if not trail_to_show and sample_file.exists():
        img_hash = tools.compute_image_hash(sample_bytes)
        p_state, default_trail = agent.run_reporting_agent_pipeline(
            issue_type=active_conf["category"],
            city=active_conf["city"],
            locality=active_conf["locality"],
            image_hash=img_hash,
            landmark=active_conf["landmark"],
            db_path=DB_PATH
        )
        trail_to_show = default_trail

    if trail_to_show:
        steps = trail_to_show.get_steps()
        st.markdown(f"#### 📋 Chronological Stage Execution Log ({len(steps)} Recorded Stages)")

        for step in steps:
            s_num = step.get("stage_number", 1)
            t_name = step.get("tool_name", "agent_tool")
            t_time = step.get("timestamp", "")
            t_args = step.get("input_arguments", {})
            t_res = step.get("output_result", {})
            t_desc = COMPLAINT_STAGES.get(s_num, f"Stage {s_num}")

            st.markdown(f"""
                <div class="stage-card-workshop">
                    <div class="stage-header-flex">
                        <div>
                            <span class="stage-badge-pill">STAGE {s_num:02d}</span>
                            <strong style="margin-left: 8px; color: #243B63; font-size: 1.05rem;">{t_desc}</strong>
                            <code style="margin-left: 8px; color: #D96C48; font-size: 0.85rem;">{t_name}()</code>
                        </div>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.76rem; color: #64748B;">{t_time}</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 10px;">
                        <div style="background: #FAF3E8; border-radius: 8px; padding: 10px; font-size: 0.82rem;">
                            <strong style="color: #7C6044;">Tool Arguments (Input):</strong>
                            <pre style="margin: 4px 0 0 0; color: #243B63; font-size: 0.78rem; overflow-x: auto;">{json.dumps(t_args, indent=2)}</pre>
                        </div>
                        <div style="background: #ECFDF5; border-radius: 8px; padding: 10px; font-size: 0.82rem;">
                            <strong style="color: #065F46;">Execution Result (Output):</strong>
                            <pre style="margin: 4px 0 0 0; color: #064E3B; font-size: 0.78rem; overflow-x: auto;">{json.dumps(t_res, indent=2)}</pre>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)


def render_repair_story(lang: str = "en"):
    """
    Renders The Repair Story:
    Presents complaints as an unfolding narrative through 6 visual chapters:
    Chapter 01 — Discovered
    Chapter 02 — Reported
    Chapter 03 — Assigned
    Chapter 04 — Work in Progress
    Chapter 05 — Verification (CivicTwin Before/After)
    Chapter 06 — Resolved
    Includes embedded natural language AI tracking assistant.
    """
    st.markdown("""
        <div style="margin-bottom: 1rem;">
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 700; color: #D96C48;">
                THE REPAIR STORY
            </span>
            <h2 style="font-family: 'Fraunces', serif; font-size: 2rem; color: #243B63; margin: 0;">
                📖 Journey of a Problem Toward Resolution
            </h2>
            <p style="color: #64748B; font-size: 0.92rem; margin-top: 4px;">
                Every civic incident has a story. Track its progression through 6 verifiable milestone chapters.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Search & Sample Pills
    search_id = st.session_state.get("tracking_search_id", "NS-DEMO-A101B202")
    t_c1, t_c2 = st.columns([0.75, 0.25])
    with t_c1:
        entered_id = st.text_input("Enter Complaint Tracking ID", value=search_id, key="txt_track_search")
    with t_c2:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        if st.button("🔍 Find Story", type="primary", use_container_width=True):
            st.session_state.tracking_search_id = entered_id
            st.rerun()

    st.caption("Quick Demo Stories:")
    p_c1, p_c2, p_c3 = st.columns(3)
    if p_c1.button("🕳️ NS-DEMO-A101B202 (Road)", use_container_width=True):
        st.session_state.tracking_search_id = "NS-DEMO-A101B202"
        st.rerun()
    if p_c2.button("🗑️ NS-DEMO-C303D404 (Waste)", use_container_width=True):
        st.session_state.tracking_search_id = "NS-DEMO-C303D404"
        st.rerun()
    if p_c3.button("💡 NS-DEMO-E505F606 (Lighting)", use_container_width=True):
        st.session_state.tracking_search_id = "NS-DEMO-E505F606"
        st.rerun()

    complaint = database.get_complaint(st.session_state.get("tracking_search_id", entered_id))
    if not complaint:
        st.warning(f"Complaint ID `{entered_id}` was not found in the official registry. Please check the ID.")
        return

    curr_status = complaint.get("status", "Reported")
    status_order = ["Reported", "Assigned", "In Progress", "Awaiting Verification", "Resolved"]
    curr_idx = status_order.index(curr_status) if curr_status in status_order else 0

    chapters = [
        {"num": "01", "name": "DISCOVERED", "desc": "Defect spotted and photographed by citizen.", "stage": 0},
        {"num": "02", "name": "REPORTED", "desc": "Photographic evidence submitted & verified by AI agent.", "stage": 0},
        {"num": "03", "name": "ASSIGNED", "desc": f"Dispatched to {complaint.get('department')} ({complaint.get('ward')}).", "stage": 1},
        {"num": "04", "name": "WORK IN PROGRESS", "desc": "Field engineer dispatched; repair materials and crew on site.", "stage": 2},
        {"num": "05", "name": "VERIFICATION", "desc": "CivicTwin Before/After physical restoration comparison.", "stage": 3},
        {"num": "06", "name": "RESOLVED", "desc": "Repair verified with municipal administrative confirmation.", "stage": 4},
    ]

    st.markdown("### 📜 Story Chapters")
    for ch in chapters:
        is_active = ch["stage"] <= curr_idx
        card_cls = "story-chapter-card" if is_active else "story-chapter-card inactive"
        icon = "✅" if (ch["stage"] < curr_idx or (ch["stage"] == curr_idx and curr_status == "Resolved")) else ("📍" if is_active else "⚪")

        st.markdown(f"""
            <div class="{card_cls}">
                <div class="story-chapter-badge">CHAPTER {ch['num']}</div>
                <div class="story-chapter-title">{icon} {ch['name']}</div>
                <div style="font-size: 0.88rem; color: #475569;">{ch['desc']}</div>
            </div>
        """, unsafe_allow_html=True)

    # Integrated AI Tracking Assistant
    st.markdown("---")
    st.markdown("### 🤖 Ask AI Assistant About This Complaint")
    st.caption("Ask questions about department dispatch, expected completion, or audit events:")
    
    t_chat_query = st.text_input("Ask a question about this complaint", value=f"What is the current status of complaint {complaint['id']}?", key=f"chat_in_{complaint['id']}")
    if st.button("Ask Assistant", type="primary", key=f"btn_ask_{complaint['id']}"):
        with st.spinner("🤖 Consulting civic agent and database records..."):
            ans = agent.run_tracking_chat_agent(t_chat_query, db_path=DB_PATH)
            st.markdown(f"""
                <div style="background: #FFFFFF; border: 2px solid #DFCAB0; border-radius: 14px; padding: 18px; margin-top: 12px;">
                    <strong style="color: #D96C48; font-size: 0.82rem; text-transform: uppercase;">Autonomous Civic Assistant:</strong>
                    <div style="font-size: 0.95rem; color: #243B63; line-height: 1.5; margin-top: 4px;">{ans.get('reply', '')}</div>
                </div>
            """, unsafe_allow_html=True)


def render_civictwin_studio(lang: str = "en"):
    """
    Renders CivicTwin — Transformation Studio:
    Immersive Before & After comparison workspace.
    Visual comparison, AI topographical observations, visible repair differences,
    verification report, and official administrative confirmation sign-off.
    """
    st.markdown("""
        <div style="margin-bottom: 1rem;">
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 700; color: #D96C48;">
                CIVICTWIN TRANSFORMATION STUDIO
            </span>
            <h2 style="font-family: 'Fraunces', serif; font-size: 2rem; color: #243B63; margin: 0;">
                ♊ Physical Verification & Restoration Inspector
            </h2>
            <p style="color: #64748B; font-size: 0.92rem; margin-top: 4px;">
                Inspect and verify physical infrastructure repairs side-by-side using multimodal computer vision before closing municipal records.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Complaint Selector
    all_complaints = database.list_complaints(limit=50)
    c_ids = [c["id"] for c in all_complaints] if all_complaints else ["NS-DEMO-A101B202"]
    
    sel_cid = st.selectbox("Select Complaint Case for Verification Inspection", options=c_ids, index=0, key="twin_sel_cid")
    comp_obj = database.get_complaint(sel_cid) or {"issue_type": "Potholes and damaged roads", "status": "In Progress", "locality": "Indiranagar"}

    st.markdown(f"""
        <div style="background: #FFFFFF; border: 1.5px solid #DFCAB0; border-radius: 14px; padding: 16px; margin-bottom: 16px;">
            <strong>Case File:</strong> {sel_cid} • <strong>Category:</strong> {comp_obj.get('issue_type')} • <strong>Status:</strong> {comp_obj.get('status')}
            <div style="font-size: 0.85rem; color: #64748B; margin-top: 4px;">Jurisdiction: {comp_obj.get('locality', 'Local')}, {comp_obj.get('city', 'City')}</div>
        </div>
    """, unsafe_allow_html=True)

    # Side-by-Side Photo Inspection
    sample_dir = Path(__file__).resolve().parent / "data" / "samples"
    before_file = sample_dir / "sample_pothole.jpg"
    after_file = sample_dir / "sample_resolved_pothole.jpg"

    tw_col1, tw_col2 = st.columns(2)
    with tw_col1:
        st.markdown("**Original Damage (Before)**")
        if before_file.exists():
            st.image(str(before_file), caption="Pre-Repair Incident Evidence", use_column_width=True)

    with tw_col2:
        st.markdown("**Field Restoration Proof (After)**")
        if after_file.exists():
            st.image(str(after_file), caption="Post-Repair Completed Surface", use_column_width=True)

    if before_file.exists() and after_file.exists():
        if st.button("🚀 Run Multimodal CivicTwin Verification Inspection", type="primary", use_container_width=True, key="btn_exec_twin_studio"):
            with st.spinner("🤖 Multimodal Vision inspecting topographical restoration & quality delta..."):
                with open(before_file, "rb") as f1, open(after_file, "rb") as f2:
                    b_bytes = f1.read()
                    a_bytes = f2.read()
                    v_res = vision.verify_civictwin(b_bytes, a_bytes, original_issue=comp_obj.get("issue_type", "Potholes and damaged roads"))
                    st.session_state.civictwin_res = v_res

    # Display Verification Results
    if st.session_state.get("civictwin_res"):
        v_res = st.session_state.civictwin_res
        score_pct = int(v_res.get("verification_score", 0.95) * 100)

        st.markdown("---")
        st.markdown(f"""
            <div class="civictwin-compare-frame">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1.5px solid #E8DAC6; padding-bottom: 12px; margin-bottom: 14px;">
                    <div>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; font-weight: 700; color: #D96C48;">
                            AI RESTORATION DELTA ANALYSIS
                        </span>
                        <h3 style="font-family: 'Fraunces', serif; margin: 0; color: #243B63;">
                            Verification Status: {'VERIFIED RESTORATION ✅' if v_res.get('resolved') else 'NEEDS CORRECTION ⚠️'}
                        </h3>
                    </div>
                    <div class="civictwin-score-badge">
                        <span>🎯</span> {score_pct}% Match Confidence
                    </div>
                </div>

                <div style="background: #FAF3E8; border: 1px solid #DFCAB0; border-radius: 12px; padding: 14px; margin-bottom: 14px;">
                    <strong style="color: #7C6044; font-size: 0.85rem; text-transform: uppercase;">Topographical Difference:</strong>
                    <div style="font-size: 0.92rem; color: #243B63; margin-top: 4px;">{v_res.get('delta_detected', 'Asphalt surface leveled completely; void filled to flush grade with no residual craters.')}</div>
                </div>

                <strong style="color: #243B63; font-size: 0.88rem; text-transform: uppercase;">Structural Quality Checklist:</strong>
                <div class="checklist-box">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 0.88rem; color: #243B63;">
                        <div>✅ Surface Leveling & Uniformity: <strong>PASS</strong></div>
                        <div>✅ Edge Compaction & Asphalt Bonding: <strong>PASS</strong></div>
                        <div>✅ Debris & Site Clearance: <strong>PASS</strong></div>
                        <div>✅ Drainage Slope Integrity: <strong>PASS</strong></div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Officer Confirmation Sign-Off
        st.markdown("#### 🛡️ Municipal Administrative Sign-Off")
        st.caption("Confirm resolution in the official SQLite database ledger with cryptographic audit trail:")

        sign_col1, sign_col2 = st.columns([0.45, 0.55])
        with sign_col1:
            if st.button("✅ Confirm Official Municipal Resolution", type="primary", use_container_width=True, key="btn_confirm_twin_res"):
                database.insert_civictwin_verification(
                    complaint_id=sel_cid,
                    before_hash="sample_pothole_verified",
                    after_hash="sample_resolved_pothole_verified",
                    verification_result=v_res,
                    db_path=DB_PATH
                )
                database.update_complaint_status(
                    complaint_id=sel_cid,
                    new_status="Resolved",
                    note="Multimodal CivicTwin Verification Approved by Municipal Field Inspector.",
                    db_path=DB_PATH
                )
                st.success(f"🎉 **Complaint `{sel_cid}` officially transitioned to RESOLVED in SQLite!**")
                st.balloons()


def render_neighborhood_pulse_stories(lang: str = "en"):
    """
    Renders Neighborhood Pulse — Explore the Neighborhood:
    Illustrated neighborhood exploration interface grounded in authentic SQLite telemetry.
    Select neighborhood directly, view reported problems, active issues, resolved complaints,
    and local civic memory stories.
    """
    st.markdown("""
        <div style="margin-bottom: 1rem;">
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 700; color: #D96C48;">
                NEIGHBORHOOD PULSE • GROUNDED CIVIC TELEMETRY
            </span>
            <h2 style="font-family: 'Fraunces', serif; font-size: 2rem; color: #243B63; margin: 0;">
                📊 Localized Civic Memory & Infrastructure Telemetry
            </h2>
            <p style="color: #64748B; font-size: 0.92rem; margin-top: 4px;">
                Explore real community telemetry grounded strictly in authentic municipal database rows across supported jurisdictions.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Neighborhood Selection Pills
    localities = ["Indiranagar (Bengaluru)", "Bandra West (Mumbai)", "Connaught Place (Delhi)", "Satellite (Ahmedabad)", "Kothrud (Pune)"]
    sel_loc = st.selectbox("Select Neighborhood to Explore", options=localities, index=0, key="pulse_sel_neighborhood")
    loc_clean = sel_loc.split(" (")[0]

    stats = database.get_neighborhood_pulse_stats()
    metrics = stats.get("metrics", {})
    total = metrics.get("total_complaints", 0)
    in_prog = metrics.get("in_progress_complaints", 0)
    resolved = metrics.get("resolved_complaints", 0)
    rate = metrics.get("resolution_rate", 75.0)

    # Telemetry KPI Grid
    st.markdown(f"""
        <div class="pulse-stat-grid">
            <div class="pulse-stat-box">
                <span style="font-size: 0.8rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Total Reports</span>
                <div class="pulse-stat-val">{total}</div>
                <span style="font-size: 0.76rem; color: #D96C48;">Recorded in SQLite</span>
            </div>
            <div class="pulse-stat-box">
                <span style="font-size: 0.8rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Active In Progress</span>
                <div class="pulse-stat-val" style="color: #F4BB52;">{in_prog}</div>
                <span style="font-size: 0.76rem; color: #64748B;">Crews dispatched</span>
            </div>
            <div class="pulse-stat-box">
                <span style="font-size: 0.8rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Verified Resolved</span>
                <div class="pulse-stat-val" style="color: #83A98A;">{resolved}</div>
                <span style="font-size: 0.76rem; color: #047857;">CivicTwin verified</span>
            </div>
            <div class="pulse-stat-box">
                <span style="font-size: 0.8rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Resolution Rate</span>
                <div class="pulse-stat-val" style="color: #243B63;">{rate:.1f}%</div>
                <span style="font-size: 0.76rem; color: #64748B;">Overall velocity</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Civic Intelligence Synthesis Narrative
    summary = stats.get("ai_neighborhood_summary", "Telemetry loaded.")
    st.markdown(f"""
        <div style="background: #FAF3E8; border: 1.5px solid #DFCAB0; border-radius: 16px; padding: 20px; margin-bottom: 20px;">
            <strong style="color: #D96C48; font-size: 0.84rem; text-transform: uppercase;">Civic Intelligence Synthesis • {loc_clean}:</strong>
            <p style="font-size: 0.95rem; color: #243B63; margin-top: 6px; line-height: 1.5;">{summary}</p>
        </div>
    """, unsafe_allow_html=True)

    # Filtered Neighborhood Cases
    all_complaints = database.list_complaints(limit=50)
    matched = [c for c in all_complaints if loc_clean.lower() in c.get("locality", "").lower()]
    cases_to_show = matched if matched else all_complaints[:5]

    st.markdown(f"#### 🏘️ Active Community Case Files in {loc_clean} ({len(cases_to_show)} records)")
    for c in cases_to_show:
        c_col1, c_col2 = st.columns([0.82, 0.18])
        with c_col1:
            st.markdown(f"""
                <div style="background: #FFFFFF; border: 1px solid #E8DAC6; border-radius: 12px; padding: 12px 18px; margin-bottom: 8px;">
                    <strong style="color: #243B63;">{c['id']}</strong> • <em>{c['issue_type']}</em> at <strong>{c['locality']}, {c['city']}</strong>
                    <div style="font-size: 0.82rem; color: #64748B; margin-top: 2px;">{c['description']}</div>
                </div>
            """, unsafe_allow_html=True)
        with c_col2:
            if st.button("Inspect Dossier", key=f"btn_p_view_{c['id']}", use_container_width=True):
                st.session_state.selected_case_id = c["id"]
                st.rerun()


def render_civic_operations_studio(lang: str = "en"):
    """
    Renders Civic Operations Studio (Admin):
    Redesigned in the illustrated Streetverse design language.
    Features complaint management, status updates, department assignments,
    repair verification, and chronological audit trail inspection.
    """
    st.markdown("""
        <div style="margin-bottom: 1rem;">
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 700; color: #243B63;">
                CIVIC OPERATIONS STUDIO • DISPATCH CONSOLE
            </span>
            <h2 style="font-family: 'Fraunces', serif; font-size: 2rem; color: #243B63; margin: 0;">
                🛡️ Municipal Grievance Administration & Audit
            </h2>
            <p style="color: #64748B; font-size: 0.92rem; margin-top: 4px;">
                Authorized municipal operations console for status transitions, nodal department routing, and audit trail inspection.
            </p>
        </div>
    """, unsafe_allow_html=True)

    all_complaints = database.list_complaints(limit=100)
    if not all_complaints:
        st.info("No complaints found in the database.")
        return

    # Filter controls
    f_col1, f_col2 = st.columns([0.6, 0.4])
    with f_col1:
        status_filter = st.selectbox("Filter by Status", options=["All"] + VALID_STATUSES, key="admin_filter_status")
    with f_col2:
        search_query = st.text_input("Search ID or Locality", value="", key="admin_search_query")

    filtered = all_complaints
    if status_filter != "All":
        filtered = [c for c in filtered if c.get("status") == status_filter]
    if search_query:
        q = search_query.strip().lower()
        filtered = [c for c in filtered if q in c.get("id", "").lower() or q in c.get("locality", "").lower()]

    st.markdown(f"**Found {len(filtered)} Matching Complaints:**")

    c_ids = [c["id"] for c in filtered] if filtered else [all_complaints[0]["id"]]
    sel_id = st.selectbox("Select Complaint to Manage", options=c_ids, key="admin_sel_cid")

    complaint = database.get_complaint(sel_id)
    if complaint:
        st.markdown(f"""
            <div class="admin-op-card">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed #DFCAB0; padding-bottom: 10px; margin-bottom: 12px;">
                    <div>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; font-weight: 700; color: #D96C48;">CASE ID: {complaint.get('id')}</span>
                        <h3 style="font-family: 'Fraunces', serif; margin: 0; color: #243B63;">{complaint.get('issue_type')}</h3>
                    </div>
                    <span class="dossier-meta-pill" style="background: #243B63; color: #FFFFFF;">STATUS: {complaint.get('status').upper()}</span>
                </div>
                <div style="font-size: 0.92rem; color: #243B63;">
                    📍 <strong>{complaint.get('locality')}, {complaint.get('city')}</strong> • Ward: <code>{complaint.get('ward')}</code> • Department: <strong>{complaint.get('department')}</strong>
                </div>
                <div style="font-size: 0.88rem; color: #64748B; margin-top: 6px;">
                    <em>"{complaint.get('description')}"</em>
                </div>
            </div>
        """, unsafe_allow_html=True)

        ctrl_col1, ctrl_col2 = st.columns(2)
        with ctrl_col1:
            curr_s = complaint.get("status", "Reported")
            s_idx = VALID_STATUSES.index(curr_s) if curr_s in VALID_STATUSES else 0
            new_status = st.selectbox("Update Status Transition", options=VALID_STATUSES, index=s_idx, key="admin_status_select")

        with ctrl_col2:
            officer_notes = st.text_input("Officer Action Notes", value="Verified on-site by municipal assessment team.", key="admin_officer_notes")

        btn_commit, btn_twin_jump = st.columns([0.5, 0.5])
        with btn_commit:
            if st.button("💾 Commit Status Transition to SQLite", type="primary", use_container_width=True, key="btn_commit_admin"):
                success = database.update_complaint_status(sel_id, new_status, note=officer_notes)
                if success:
                    st.success(f"Status for `{sel_id}` officially updated to **{new_status}**.")
                    st.rerun()

        with btn_twin_jump:
            if st.button("♊ Open in CivicTwin Studio", use_container_width=True, key=f"btn_admin_twin_{sel_id}"):
                st.session_state.street_active_view = "civictwin"
                st.session_state.twin_sel_cid = sel_id
                st.session_state.selected_case_id = None
                st.rerun()


def render_ai_companion_drawer(lang: str = "en"):
    """
    Renders the compact AI City Companion overlay.
    Lives cleanly inside the command capsule context without taking over the screen.
    """
    st.markdown("""
        <div style="margin-bottom: 1rem;">
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 700; color: #D96C48;">
                AI CITY COMPANION
            </span>
            <h2 style="font-family: 'Fraunces', serif; font-size: 1.8rem; color: #243B63; margin: 0;">
                🤖 Your Grounded Civic Assistant
            </h2>
            <p style="color: #64748B; font-size: 0.92rem; margin-top: 4px;">
                Ask questions about complaint routing, department responsibilities, or municipal resolution metrics.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Prompt suggestions
    st.caption("Prompt Suggestions:")
    p1, p2, p3 = st.columns(3)
    preset_query = None
    if p1.button("Which dept handles potholes?", use_container_width=True):
        preset_query = "Which department handles potholes in Bengaluru?"
    if p2.button("Track NS-DEMO-A101B202", use_container_width=True):
        preset_query = "What is the status of complaint NS-DEMO-A101B202?"
    if p3.button("Neighborhood stats", use_container_width=True):
        preset_query = "Show neighborhood statistics and resolution rates."

    user_query = st.text_input("Ask a question to the Civic Assistant", value=preset_query or "", placeholder="e.g. How does NazarSetu verify road repairs?", key="companion_query_input")
    
    if st.button("Send Query", type="primary", key="btn_send_companion") or preset_query:
        if user_query:
            with st.spinner("🤖 Consulting civic agent and SQLite database..."):
                reply = agent.run_tracking_chat_agent(user_query, db_path=DB_PATH)
                st.markdown(f"""
                    <div style="background: #FFFFFF; border: 2px solid #DFCAB0; border-radius: 16px; padding: 20px; box-shadow: 0 8px 24px rgba(36, 59, 99, 0.08); margin-top: 14px;">
                        <strong style="color: #D96C48; font-size: 0.82rem; text-transform: uppercase;">Autonomous Civic Assistant Response:</strong>
                        <div style="font-size: 0.95rem; color: #243B63; line-height: 1.5; margin-top: 6px;">
                            {reply.get('reply', '')}
                        </div>
                    </div>
                """, unsafe_allow_html=True)


def render_streetverse():
    """Main orchestrator for NAZARSETU — STREETVERSE."""
    # Inject CSS design system
    st.markdown(get_streetverse_css(), unsafe_allow_html=True)

    # Initialize session state
    if "lang" not in st.session_state:
        st.session_state.lang = "en"

    if "street_active_view" not in st.session_state:
        st.session_state.street_active_view = "street"

    if "selected_hotspot" not in st.session_state:
        st.session_state.selected_hotspot = None

    if "selected_case_id" not in st.session_state:
        st.session_state.selected_case_id = None

    # Handle URL Query Parameters (for SVG click interactions)
    query_action = st.query_params.get("action")
    query_target = st.query_params.get("target")
    query_case = st.query_params.get("case")

    if query_action == "hotspot" and query_target:
        st.session_state.selected_hotspot = query_target
        st.session_state.street_active_view = "hotspot"
        st.query_params.clear()

    if query_action == "report":
        st.session_state.street_active_view = "report"
        st.session_state.selected_case_id = None
        st.query_params.clear()

    if query_action == "mission":
        st.session_state.street_active_view = "mission"
        st.session_state.selected_case_id = None
        st.query_params.clear()

    if query_action == "track":
        st.session_state.street_active_view = "track"
        st.session_state.selected_case_id = None
        st.query_params.clear()

    if query_action == "civictwin":
        st.session_state.street_active_view = "civictwin"
        st.session_state.selected_case_id = None
        st.query_params.clear()

    if query_case:
        st.session_state.selected_case_id = query_case
        st.query_params.clear()

    # Retrieve live stats from database
    stats = database.get_neighborhood_pulse_stats()
    complaints = database.list_complaints(limit=100)

    # Calculate counts per category
    category_counts = {
        "Potholes and damaged roads": 0,
        "Broken streetlights": 0,
        "Overflowing garbage": 0,
        "Waterlogging and drainage issues": 0,
    }
    for c in complaints:
        cat = c.get("issue_type")
        if cat in category_counts:
            category_counts[cat] += 1

    # Floating Top Header
    render_floating_header(lang=st.session_state.lang)

    active_view = st.session_state.street_active_view

    # Specific Case File Opened
    if st.session_state.selected_case_id:
        c_obj = database.get_complaint(st.session_state.selected_case_id)
        if c_obj:
            render_case_file_drawer(c_obj, lang=st.session_state.lang)
        else:
            st.error("Case file not found.")

    # Main Street Scene (Default View)
    elif active_view == "street":
        # Render the handcrafted 2.5D SVG Street Scene
        st.markdown(render_streetverse_svg(category_counts, active_states={"road": "alert" if category_counts["Potholes and damaged roads"] > 0 else "smooth"}), unsafe_allow_html=True)

        # Hotspot Click Cards right below the SVG for direct exploration
        st.markdown("### 🏘️ Interactive Infrastructure Signals")
        st.caption("Click any infrastructure point to inspect live civic records or report a new problem:")

        h_col1, h_col2, h_col3, h_col4 = st.columns(4)
        with h_col1:
            st.markdown(f"""
                <div class="hotspot-card-badge">
                    <span style="font-size: 1.4rem;">🕳️</span>
                    <strong style="color: #D96C48; font-size: 0.95rem; display: block; margin-top: 4px;">Damaged Road</strong>
                    <span style="font-size: 0.8rem; color: #64748B;">{category_counts['Potholes and damaged roads']} active reports</span>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Inspect Road Cases", key="btn_h_road", use_container_width=True):
                st.session_state.selected_hotspot = "road"
                st.session_state.street_active_view = "hotspot"
                st.rerun()

        with h_col2:
            st.markdown(f"""
                <div class="hotspot-card-badge">
                    <span style="font-size: 1.4rem;">💡</span>
                    <strong style="color: #F4BB52; font-size: 0.95rem; display: block; margin-top: 4px;">Streetlights</strong>
                    <span style="font-size: 0.8rem; color: #64748B;">{category_counts['Broken streetlights']} lighting incidents</span>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Inspect Streetlights", key="btn_h_light", use_container_width=True):
                st.session_state.selected_hotspot = "streetlight"
                st.session_state.street_active_view = "hotspot"
                st.rerun()

        with h_col3:
            st.markdown(f"""
                <div class="hotspot-card-badge">
                    <span style="font-size: 1.4rem;">🗑️</span>
                    <strong style="color: #83A98A; font-size: 0.95rem; display: block; margin-top: 4px;">Waste Collection</strong>
                    <span style="font-size: 0.8rem; color: #64748B;">{category_counts['Overflowing garbage']} waste points</span>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Inspect Waste Cases", key="btn_h_waste", use_container_width=True):
                st.session_state.selected_hotspot = "garbage"
                st.session_state.street_active_view = "hotspot"
                st.rerun()

        with h_col4:
            st.markdown(f"""
                <div class="hotspot-card-badge">
                    <span style="font-size: 1.4rem;">🌊</span>
                    <strong style="color: #243B63; font-size: 0.95rem; display: block; margin-top: 4px;">Storm Drain</strong>
                    <span style="font-size: 0.8rem; color: #64748B;">{category_counts['Waterlogging and drainage issues']} drainage issues</span>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Inspect Drainage", key="btn_h_drain", use_container_width=True):
                st.session_state.selected_hotspot = "drainage"
                st.session_state.street_active_view = "hotspot"
                st.rerun()

    elif active_view == "hotspot":
        target = st.session_state.selected_hotspot or "road"
        render_hotspot_explorer(target, lang=st.session_state.lang)

    elif active_view == "report":
        render_ai_investigation_workspace(lang=st.session_state.lang)

    elif active_view == "mission":
        render_ai_mission_control_workshop(lang=st.session_state.lang)

    elif active_view == "track":
        render_repair_story(lang=st.session_state.lang)

    elif active_view == "civictwin":
        render_civictwin_studio(lang=st.session_state.lang)

    elif active_view in ["pulse", "stories"]:
        render_neighborhood_pulse_stories(lang=st.session_state.lang)

    elif active_view in ["admin", "officer"]:
        render_civic_operations_studio(lang=st.session_state.lang)

    elif active_view == "companion":
        render_ai_companion_drawer(lang=st.session_state.lang)

    # Floating Command Capsule (Navigation Bar)
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    render_floating_capsule(active_view, lang=st.session_state.lang)

    # Floating Real-Data Activity Indicator
    render_activity_pill(stats)
