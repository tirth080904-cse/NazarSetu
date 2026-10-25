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
    """Renders the top branding, Streetverse tagline, language pills, and officer link."""
    tagline = t("streetverse_tagline", lang)

    col1, col2 = st.columns([0.62, 0.38])
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
        top_ctrl1, top_ctrl2, top_ctrl3 = st.columns([0.45, 0.30, 0.25])
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
            if st.button("🛡️ Officer", use_container_width=True, key="btn_open_officer"):
                st.session_state.street_active_view = "officer"
                st.rerun()

        with top_ctrl3:
            if st.button("🏛️ Classic", use_container_width=True, key="btn_toggle_classic"):
                st.session_state.view_mode = "classic"
                st.rerun()


def render_floating_capsule(active_view: str, lang: str = "en"):
    """
    Renders the central Floating Command Capsule:
    [ 🗺️ Explore ] [ 📸 Report ] [ 🔍 Track ] [ 🤖 Ask AI ] [ 📖 Stories ]
    """
    c_explore = t("capsule_explore", lang)
    c_report = t("capsule_report", lang)
    c_track = t("capsule_track", lang)
    c_ask = t("capsule_ask_ai", lang)
    c_stories = t("capsule_stories", lang)

    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button(c_explore, use_container_width=True, type="primary" if active_view == "street" else "secondary", key="capsule_btn_explore"):
            st.session_state.street_active_view = "street"
            st.session_state.selected_hotspot = None
            st.rerun()

    with col2:
        if st.button(c_report, use_container_width=True, type="primary" if active_view == "report" else "secondary", key="capsule_btn_report"):
            st.session_state.street_active_view = "report"
            st.rerun()

    with col3:
        if st.button(c_track, use_container_width=True, type="primary" if active_view == "track" else "secondary", key="capsule_btn_track"):
            st.session_state.street_active_view = "track"
            st.rerun()

    with col4:
        if st.button(c_ask, use_container_width=True, type="primary" if active_view == "companion" else "secondary", key="capsule_btn_ask"):
            st.session_state.street_active_view = "companion"
            st.rerun()

    with col5:
        if st.button(c_stories, use_container_width=True, type="primary" if active_view == "stories" else "secondary", key="capsule_btn_stories"):
            st.session_state.street_active_view = "stories"
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
        cities = list(tools.SUPPORTED_LOCALITIES.keys())
        default_city = st.session_state.get("sample_city", "Bengaluru")
        c_idx = cities.index(default_city) if default_city in cities else 0
        selected_city = st.selectbox("Municipal City", options=cities, index=c_idx, key="inv_sel_city")

        localities = tools.SUPPORTED_LOCALITIES.get(selected_city, [])
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
        search_clicked = st.button("🔍 Find Story", type="primary", use_container_width=True)

    st.caption("Quick Demo Stories:")
    p_c1, p_c2, p_c3 = st.columns(3)
    if p_c1.button("🕳️ NS-DEMO-A101B202 (Road)", use_container_width=True):
        entered_id = "NS-DEMO-A101B202"
        st.session_state.tracking_search_id = entered_id
        st.rerun()
    if p_c2.button("🗑️ NS-DEMO-C303D404 (Waste)", use_container_width=True):
        entered_id = "NS-DEMO-C303D404"
        st.session_state.tracking_search_id = entered_id
        st.rerun()
    if p_c3.button("💡 NS-DEMO-E505F606 (Lighting)", use_container_width=True):
        entered_id = "NS-DEMO-E505F606"
        st.session_state.tracking_search_id = entered_id
        st.rerun()

    complaint = database.get_complaint(entered_id)
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

    # CivicTwin Resolution Inspection
    st.markdown("---")
    st.markdown("### ♊ CivicTwin Before & After Physical Verification")
    st.caption("Inspect physical repair quality side-by-side before closing municipal records.")

    tw_col1, tw_col2 = st.columns(2)
    sample_dir = Path(__file__).resolve().parent / "data" / "samples"
    before_file = sample_dir / "sample_pothole.jpg"
    after_file = sample_dir / "sample_resolved_pothole.jpg"

    with tw_col1:
        st.markdown("**Original Incident Photo**")
        if before_file.exists():
            st.image(str(before_file), caption="Before: Unrepaired Defect", use_column_width=True)

    with tw_col2:
        st.markdown("**Post-Repair Verification Proof**")
        if after_file.exists():
            st.image(str(after_file), caption="After: Repaired Surface", use_column_width=True)

    if before_file.exists() and after_file.exists():
        if st.button("🚀 Run CivicTwin Verification Inspection", type="primary", use_container_width=True, key="btn_run_twin"):
            with open(before_file, "rb") as f1, open(after_file, "rb") as f2:
                v_res = vision.verify_civictwin(f1.read(), f2.read(), original_issue=complaint["issue_type"])
            
            st.markdown(f"""
                <div style="background: #FAF3E8; border: 2px solid #83A98A; border-radius: 14px; padding: 18px; margin-top: 14px;">
                    <div style="font-weight: 700; color: #047857; font-size: 1.1rem;">
                        Inspection Score: {int(v_res.get('verification_score', 0.95) * 100)}% • Repair Verified: {'YES' if v_res.get('resolved') else 'NO'}
                    </div>
                    <p style="font-size: 0.9rem; color: #243B63; margin-top: 6px;">
                        {v_res.get('delta_detected', 'Surface leveled successfully with minimal edge elevation.')}
                    </p>
                </div>
            """, unsafe_allow_html=True)


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


def render_neighborhood_stories(lang: str = "en"):
    """
    Renders Neighborhood Stories:
    Explores supported localities (Indiranagar, Bandra West, Connaught Place, Satellite, Kothrud)
    with grounded SQLite telemetry and short stories.
    """
    st.markdown("""
        <div style="margin-bottom: 1rem;">
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 700; color: #D96C48;">
                NEIGHBORHOOD STORIES
            </span>
            <h2 style="font-family: 'Fraunces', serif; font-size: 2rem; color: #243B63; margin: 0;">
                📖 Localized Civic Memory & Progress
            </h2>
            <p style="color: #64748B; font-size: 0.92rem; margin-top: 4px;">
                Explore real community telemetry grounded strictly in authentic municipal database rows.
            </p>
        </div>
    """, unsafe_allow_html=True)

    stats = database.get_neighborhood_pulse_stats()
    summary = stats.get("ai_neighborhood_summary", "Telemetry loaded.")

    st.markdown(f"""
        <div style="background: #FAF3E8; border: 1.5px solid #DFCAB0; border-radius: 16px; padding: 20px; margin-bottom: 20px;">
            <strong style="color: #D96C48; font-size: 0.84rem; text-transform: uppercase;">Civic Intelligence Synthesis:</strong>
            <p style="font-size: 0.95rem; color: #243B63; margin-top: 6px; line-height: 1.5;">{summary}</p>
        </div>
    """, unsafe_allow_html=True)

    all_complaints = database.list_complaints(limit=50)
    if all_complaints:
        st.markdown("#### 🏘️ Recent Community Complaint Dossiers")
        for c in all_complaints[:6]:
            st.markdown(f"""
                <div style="background: #FFFFFF; border: 1px solid #E8DAC6; border-radius: 12px; padding: 12px 18px; margin-bottom: 8px;">
                    <strong>{c['id']}</strong> • <em>{c['issue_type']}</em> at <strong>{c['locality']}, {c['city']}</strong>
                    <div style="font-size: 0.82rem; color: #64748B; margin-top: 2px;">{c['description']}</div>
                </div>
            """, unsafe_allow_html=True)


def render_discreet_officer_portal(lang: str = "en"):
    """
    Renders the discreet municipal administrator management console.
    Allows status updates, CivicTwin verification review, and audit trail inspection.
    """
    st.markdown("""
        <div style="margin-bottom: 1rem;">
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 700; color: #243B63;">
                MUNICIPAL OFFICER CONSOLE
            </span>
            <h2 style="font-family: 'Fraunces', serif; font-size: 2rem; color: #243B63; margin: 0;">
                🛡️ Civic Dispatch & Status Command
            </h2>
            <p style="color: #64748B; font-size: 0.92rem; margin-top: 4px;">
                Authorized municipal dashboard for complaint status transitions and CivicTwin confirmations.
            </p>
        </div>
    """, unsafe_allow_html=True)

    all_complaints = database.list_complaints(limit=100)
    if not all_complaints:
        st.info("No complaints found in the database.")
        return

    c_ids = [c["id"] for c in all_complaints]
    sel_id = st.selectbox("Select Complaint to Manage", options=c_ids, key="admin_sel_cid")

    complaint = database.get_complaint(sel_id)
    if complaint:
        st.markdown(f"""
            <div style="background: #FFFFFF; border: 1.5px solid #DFCAB0; border-radius: 14px; padding: 16px; margin: 12px 0;">
                <strong>Current Status:</strong> <span style="color: #D96C48; font-weight: 800;">{complaint.get('status')}</span><br>
                <strong>Issue:</strong> {complaint.get('issue_type')}<br>
                <strong>Department:</strong> {complaint.get('department')} ({complaint.get('ward')})<br>
                <strong>Locality:</strong> {complaint.get('locality')}, {complaint.get('city')}
            </div>
        """, unsafe_allow_html=True)

        new_status = st.selectbox("Update Status", options=VALID_STATUSES, index=VALID_STATUSES.index(complaint.get("status", "Reported")), key="admin_status_select")
        officer_notes = st.text_input("Officer Action Notes", value="Verified on-site by municipal assessment team.", key="admin_officer_notes")

        if st.button("💾 Commit Status Transition to SQLite", type="primary", key="btn_commit_admin"):
            success = database.update_complaint_status(sel_id, new_status, note=officer_notes)
            if success:
                st.success(f"Status for `{sel_id}` officially updated to **{new_status}**.")
                st.rerun()


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
        st.query_params.clear()

    if query_action == "track":
        st.session_state.street_active_view = "track"
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

    elif active_view == "track":
        render_repair_story(lang=st.session_state.lang)

    elif active_view == "companion":
        render_ai_companion_drawer(lang=st.session_state.lang)

    elif active_view == "stories":
        render_neighborhood_stories(lang=st.session_state.lang)

    elif active_view == "officer":
        render_discreet_officer_portal(lang=st.session_state.lang)

    # Floating Command Capsule (Navigation Bar)
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    render_floating_capsule(active_view, lang=st.session_state.lang)

    # Floating Real-Data Activity Indicator
    render_activity_pill(stats)
