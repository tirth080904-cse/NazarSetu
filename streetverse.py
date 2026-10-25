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

.admin-control-bar {
    background: #FFFFFF;
    border: 1.5px solid var(--border-warm);
    border-radius: 16px;
    padding: 18px 24px;
    margin-bottom: 20px;
    box-shadow: 0 6px 18px rgba(36, 59, 99, 0.05);
}

/* Page Hero Container across all sections */
.storybook-page-hero {
    background: linear-gradient(135deg, rgba(255, 252, 245, 0.98) 0%, rgba(244, 231, 211, 0.92) 100%);
    border: 2px solid var(--border-warm);
    border-radius: 22px;
    padding: 24px 30px;
    margin-bottom: 24px;
    box-shadow: 0 12px 32px -8px rgba(36, 59, 99, 0.08);
    position: relative;
    overflow: hidden;
}

.storybook-page-hero::after {
    content: "";
    position: absolute;
    top: -30px;
    right: -30px;
    width: 140px;
    height: 140px;
    background: radial-gradient(circle, rgba(244, 187, 82, 0.28) 0%, rgba(244, 187, 82, 0) 70%);
    border-radius: 50%;
    pointer-events: none;
}

.hero-tagline-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    font-weight: 800;
    color: var(--terracotta);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(217, 108, 72, 0.1);
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid rgba(217, 108, 72, 0.25);
    margin-bottom: 8px;
}

.hero-page-title {
    font-family: 'Fraunces', serif !important;
    font-size: 2.1rem !important;
    font-weight: 800 !important;
    color: var(--indigo) !important;
    margin: 0 !important;
    line-height: 1.15 !important;
}

.hero-page-desc {
    color: #64748B !important;
    font-size: 0.96rem !important;
    margin-top: 6px !important;
    margin-bottom: 0 !important;
    max-width: 900px;
    line-height: 1.5;
}

/* Photographic Evidence Frame */
.polaroid-frame {
    background: #FFFFFF;
    border: 2px solid var(--border-warm);
    border-radius: 18px;
    padding: 16px;
    box-shadow: 0 14px 32px rgba(36, 59, 99, 0.1);
    position: relative;
    text-align: center;
}

.polaroid-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.76rem;
    font-weight: 700;
    color: var(--terracotta);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px dashed var(--border-warm);
    padding-top: 8px;
}

/* Interactive Workshop Terminals */
.terminal-window {
    background: #0F172A;
    border: 2px solid #334155;
    border-radius: 12px;
    overflow: hidden;
    margin-top: 6px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
}

.terminal-header {
    background: #1E293B;
    padding: 6px 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #334155;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #94A3B8;
}

.terminal-dots {
    display: flex;
    gap: 5px;
}

.terminal-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

.terminal-body {
    padding: 10px 14px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #E2E8F0;
    overflow-x: auto;
    max-height: 240px;
    line-height: 1.45;
}

/* Storybook Form Controls Overrides */
div[data-baseweb="input"] > div, div[data-baseweb="base-input"] {
    background: #FFFDF8 !important;
    border: 1.5px solid var(--border-warm) !important;
    border-radius: 12px !important;
    color: var(--indigo) !important;
    transition: all 0.2s ease !important;
}

div[data-baseweb="input"] > div:focus-within, div[data-baseweb="base-input"]:focus-within {
    border-color: var(--terracotta) !important;
    box-shadow: 0 0 0 3px rgba(217, 108, 72, 0.2) !important;
}

div[data-baseweb="input"] input {
    color: var(--indigo) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.92rem !important;
}

div[data-baseweb="select"] > div {
    background: #FFFDF8 !important;
    border: 1.5px solid var(--border-warm) !important;
    border-radius: 12px !important;
    color: var(--indigo) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    transition: all 0.2s ease !important;
}

div[data-baseweb="select"] > div:hover {
    border-color: var(--terracotta) !important;
}

div[data-baseweb="popover"], ul[role="listbox"] {
    background: #FFFDF8 !important;
    border: 1.5px solid var(--border-warm) !important;
    border-radius: 14px !important;
    box-shadow: 0 14px 34px rgba(36, 59, 99, 0.16) !important;
}

li[role="option"] {
    color: var(--indigo) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    border-radius: 8px !important;
    margin: 2px 4px !important;
}

li[role="option"]:hover, li[aria-selected="true"] {
    background: var(--sand-light) !important;
    color: var(--terracotta) !important;
    font-weight: 700 !important;
}

[data-testid="stFileUploadDropzone"] {
    background: rgba(255, 252, 245, 0.85) !important;
    border: 2px dashed var(--terracotta) !important;
    border-radius: 18px !important;
    padding: 24px 16px !important;
    transition: all 0.2s ease !important;
}

[data-testid="stFileUploadDropzone"]:hover {
    background: var(--sand-light) !important;
    border-color: var(--terracotta-dark) !important;
}

[data-testid="stFileUploadDropzone"] button {
    background: var(--terracotta) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
}

div[data-testid="stAlert"] {
    border-radius: 14px !important;
    border: 1.5px solid var(--border-warm) !important;
    background: #FFFDF8 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: var(--indigo) !important;
}

/* Headings and Code */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Fraunces', serif !important;
    color: var(--indigo) !important;
}

code {
    background: var(--sand-light) !important;
    color: var(--terracotta) !important;
    font-family: 'JetBrains Mono', monospace !important;
    padding: 2px 6px !important;
    border-radius: 6px !important;
    border: 1px solid var(--border-warm) !important;
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

div.stButton > button:not([kind="primary"]) {
    background: #FFFDF8 !important;
    color: var(--indigo) !important;
    border: 1.5px solid var(--border-warm) !important;
    box-shadow: 0 3px 10px rgba(36, 59, 99, 0.04) !important;
}

div.stButton > button:not([kind="primary"]):hover {
    background: var(--sand-light) !important;
    border-color: var(--terracotta) !important;
    color: var(--terracotta) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 14px rgba(217, 108, 72, 0.14) !important;
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


def render_streetverse_svg(counts: Dict[str, int], active_states: Dict[str, str], lang: str = "en") -> str:
    """
    Renders the handcrafted 2.5D Isometric Miniature Indian Neighborhood SVG Scene.
    Embeds state-aware civic hotspots with live database complaint counts.
    """
    pothole_count = counts.get("Potholes and damaged roads", 0)
    streetlight_count = counts.get("Broken streetlights", 0)
    garbage_count = counts.get("Overflowing garbage", 0)
    drainage_count = counts.get("Waterlogging and drainage issues", 0)

    road_state = active_states.get("road", "alert" if pothole_count > 0 else "smooth")

    title_road = t("hotspot_road_title", lang)
    title_light = t("hotspot_light_title", lang)
    title_waste = t("hotspot_waste_title", lang)
    title_drain = t("hotspot_drain_title", lang)
    work_label = "Work" if lang == "en" else t("In Progress", lang)
    verified_label = "Verified" if lang == "en" else t("Resolved", lang)

    if lang == "en":
        sub_road = f"Active Signal{'s' if pothole_count != 1 else ''}"
        sub_light = f"Incident{'s' if streetlight_count != 1 else ''}"
        sub_waste = f"Active Point{'s' if garbage_count != 1 else ''}"
        sub_drain = f"Logged Runoff{'s' if drainage_count != 1 else ''}"
    else:
        sub_road = t("active_reports_sub", lang)
        sub_light = t("lighting_incidents_sub", lang)
        sub_waste = t("waste_points_sub", lang)
        sub_drain = t("drainage_issues_sub", lang)

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
            {'<circle cx="230" cy="530" r="18" fill="none" stroke="#D96C48" stroke-width="3" class="animated-ripple"/><circle cx="230" cy="530" r="10" fill="#D96C48"/><text x="230" y="534" font-size="11" font-weight="800" fill="#FFFFFF" text-anchor="middle">!</text>' if road_state == 'alert' else (f'<rect x="210" y="515" width="12" height="24" fill="#F4BB52" stroke="#243B63" stroke-width="1.5"/><rect x="235" y="515" width="12" height="24" fill="#F4BB52" stroke="#243B63" stroke-width="1.5"/><text x="230" y="510" font-size="10" font-weight="700" fill="#F4BB52" text-anchor="middle">🚧 {work_label}</text>' if road_state == 'in_progress' else f'<ellipse cx="230" cy="530" rx="35" ry="18" fill="#4A5568" stroke="#83A98A" stroke-width="2"/><text x="230" y="534" font-size="12" fill="#83A98A" text-anchor="middle">✓ {verified_label}</text>')}

            <!-- Floating Badge Card -->
            <g transform="translate(140, 470)" filter="url(#cardShadow)">
                <rect width="180" height="42" rx="12" fill="#FFFFFF" stroke="#D96C48" stroke-width="2"/>
                <circle cx="22" cy="21" r="12" fill="#FDE8E8"/>
                <text x="22" y="26" font-size="13" text-anchor="middle">🕳️</text>
                <text x="42" y="19" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="700" fill="#243B63">{title_road}</text>
                <text x="42" y="32" font-family="'Plus Jakarta Sans', sans-serif" font-size="10" font-weight="600" fill="#D96C48">{pothole_count} {sub_road}</text>
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
                <text x="42" y="19" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="700" fill="#243B63">{title_light}</text>
                <text x="42" y="32" font-family="'Plus Jakarta Sans', sans-serif" font-size="10" font-weight="600" fill="#B45309">{streetlight_count} {sub_light}</text>
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
                <text x="42" y="19" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="700" fill="#243B63">{title_waste}</text>
                <text x="42" y="32" font-family="'Plus Jakarta Sans', sans-serif" font-size="10" font-weight="600" fill="#047857">{garbage_count} {sub_waste}</text>
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
                <text x="42" y="19" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="700" fill="#243B63">{title_drain}</text>
                <text x="42" y="32" font-family="'Plus Jakarta Sans', sans-serif" font-size="10" font-weight="600" fill="#1D4ED8">{drainage_count} {sub_drain}</text>
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
            if st.button(t("btn_ask_ai", lang), use_container_width=True, key="btn_top_ask_ai"):
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


def render_activity_pill(stats: Dict[str, Any], lang: str = "en"):
    """Renders the real-data telemetry badge in the bottom corner."""
    metrics = stats.get("metrics", {})
    total = metrics.get("total_complaints", 0)
    in_prog = metrics.get("in_progress_complaints", 0)
    resolved = metrics.get("resolved_complaints", 0)
    lbl_telem = t("live_telemetry", lang)
    lbl_rep = t("Reported", lang)
    lbl_prog = t("In Progress", lang)
    lbl_res = t("Resolved", lang)

    st.markdown(f"""
        <div class="civic-activity-badge">
            <span class="pulse-dot"></span>
            <span><strong>{lbl_telem}:</strong> {total} {lbl_rep} • {in_prog} {lbl_prog} • {resolved} {lbl_res}</span>
        </div>
    """, unsafe_allow_html=True)


def render_case_file_drawer(complaint: Dict[str, Any], lang: str = "en"):
    """
    Renders an editorial magazine-like Civic Case File.
    Presents the incident as a real digital investigation dossier with photographic evidence,
    metadata annotations, AI rationale, and audit event logs.
    """
    cid = complaint.get("id", "NS-UNKNOWN")
    issue = t(complaint.get("issue_type", "Civic Grievance"), lang)
    locality = t(complaint.get("locality", "Local Jurisdiction"), lang)
    city = t(complaint.get("city", "Municipal Area"), lang)
    ward = complaint.get("ward", "Local Ward")
    dept = t(complaint.get("department", "Municipal Department"), lang)
    status = complaint.get("status", "Reported")
    status_label = t(status, lang)
    priority = complaint.get("priority", "Medium")
    priority_label = t(priority, lang)
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

    dossier_tag = t("case_dossier_tag", lang)
    ward_lbl = t("ward_label", lang)
    status_lbl = t("status_label", lang)
    evi_lbl = t("ai_topography_evidence", lang)
    stmt_lbl = t("citizen_statement", lang)
    auth_lbl = t("assigned_authority", lang)
    time_lbl = t("filing_timestamp", lang)

    st.markdown(f"""
        <div class="case-file-dossier">
            <div class="case-file-header">
                <div>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 700; color: #D96C48;">
                        {dossier_tag} • {cid}
                    </span>
                    <h2 class="dossier-headline">{issue}</h2>
                    <div style="font-size: 0.95rem; color: #64748B; margin-top: 4px;">
                        📍 <strong>{locality}, {city}</strong> • {ward_lbl}: <code>{ward}</code>
                    </div>
                </div>
                <div style="display: flex; gap: 8px; align-items: center;">
                    <span class="dossier-meta-pill {badge_cls}">⚖️ {priority_label}</span>
                    <span class="dossier-meta-pill" style="background: #243B63; color: #FFFFFF;">{status_lbl.upper()}: {status_label.upper()}</span>
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-bottom: 20px;">
                <div style="background: #FAF3E8; border: 1.5px solid #DFCAB0; border-radius: 14px; padding: 18px;">
                    <strong style="color: #243B63; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">
                        {evi_lbl}
                    </strong>
                    <p style="font-size: 0.95rem; color: #243B63; line-height: 1.5; margin-top: 6px;">
                        {evidence}
                    </p>
                    <div style="font-size: 0.85rem; color: #7C6044; margin-top: 10px;">
                        <strong>{stmt_lbl}</strong> <em>"{desc}"</em>
                    </div>
                </div>

                <div style="background: #FFFFFF; border: 1.5px solid #E8DAC6; border-radius: 14px; padding: 18px;">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #64748B; text-transform: uppercase;">{auth_lbl}</div>
                    <div style="font-weight: 700; font-size: 0.96rem; color: #243B63; margin-top: 2px;">{dept}</div>
                    
                    <div style="font-size: 0.78rem; font-weight: 700; color: #64748B; text-transform: uppercase; margin-top: 14px;">{time_lbl}</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #243B63; margin-top: 2px;">{created}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Chronological Audit Trail
    events = database.get_complaint_timeline(cid)
    if events:
        st.markdown(f"#### 📜 {t('official_event_trail', lang)}")
        st.markdown('<div style="background: #FFFFFF; border: 1.5px solid #DFCAB0; border-radius: 16px; padding: 14px 20px; margin-bottom: 18px; box-shadow: 0 4px 14px rgba(36, 59, 99, 0.04);">', unsafe_allow_html=True)
        for ev in events:
            st.markdown(f"""
                <div style="display: flex; gap: 14px; align-items: flex-start; padding: 10px 0; border-bottom: 1px dashed #DFCAB0;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #D96C48; width: 160px; font-weight: 600;">
                        ⏱️ {ev.get('created_at', '')}
                    </span>
                    <div>
                        <strong style="color: #243B63; font-size: 0.9rem;">{t(ev.get('event_type', ''), lang)}</strong>
                        <div style="font-size: 0.85rem; color: #64748B; margin-top: 2px;">{ev.get('details', '')}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    btn_c1, btn_c2 = st.columns([0.4, 0.6])
    with btn_c1:
        if st.button(t("btn_follow_repair_story", lang), type="primary", use_container_width=True, key=f"btn_track_{cid}"):
            st.session_state.street_active_view = "track"
            st.session_state.tracking_search_id = cid
            st.rerun()
    with btn_c2:
        if st.button(t("btn_return_street", lang), use_container_width=True, key=f"btn_close_{cid}"):
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
    c_title = t(meta["title"], lang)
    c_hint = t(meta["hint"], lang)
    c_dept = t(meta["department"], lang)
    tag_insp = t("hotspot_inspect_tag", lang)
    lbl_nodal = t("responsible_nodal_body", lang)
    btn_report_lbl = t("report_at_location", lang)

    st.markdown(f"""
        <div class="storybook-page-hero">
            <div class="hero-tagline-badge" style="color: {meta['color']}; border-color: {meta['color']};">
                {meta['icon']} {tag_insp} • {lbl_nodal}: {c_dept}
            </div>
            <h1 class="hero-page-title">{c_title}</h1>
            <p class="hero-page-desc">{c_hint}</p>
        </div>
    """, unsafe_allow_html=True)

    h_col1, h_col2 = st.columns([0.7, 0.3])
    with h_col2:
        if st.button(f"{btn_report_lbl} {meta['icon']}", type="primary", use_container_width=True, key=f"btn_rep_{target_key}"):
            st.session_state.street_active_view = "report"
            st.session_state.selected_sample = meta["sample"]
            st.session_state.sample_hint = category
            st.session_state.sample_city = meta["default_city"]
            st.session_state.sample_locality = meta["default_locality"]
            st.rerun()

    # Query real complaints from database
    complaints = database.list_complaints(issue_type=category, limit=20)
    
    if not complaints:
        st.info(f"{t('no_active_complaints', lang)}")
    else:
        st.markdown(f"### 📋 {t('active_cases_heading', lang)} ({len(complaints)})")
        for comp in complaints:
            c_col1, c_col2 = st.columns([0.82, 0.18])
            with c_col1:
                st.markdown(f"""
                    <div style="background: #FFFFFF; border: 1.5px solid #E8DAC6; border-radius: 12px; padding: 12px 16px; margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between;">
                            <strong style="color: #243B63; font-size: 0.95rem;">{comp['id']} • {t(comp['locality'], lang)}, {t(comp['city'], lang)}</strong>
                            <span style="font-size: 0.76rem; font-weight: 700; color: #D96C48; text-transform: uppercase;">{t(comp['status'], lang)}</span>
                        </div>
                        <div style="font-size: 0.85rem; color: #64748B; margin-top: 4px;">{comp['description']}</div>
                    </div>
                """, unsafe_allow_html=True)
            with c_col2:
                if st.button(t("btn_inspect_dossier", lang), key=f"btn_view_{comp['id']}", use_container_width=True):
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
    tag_inv = t("inv_tag", lang)
    head_inv = t("inv_headline", lang)
    desc_inv = t("inv_desc", lang)
    p1 = t("stage_1_pill", lang)
    p2 = t("stage_2_pill", lang)
    p3 = t("stage_3_pill", lang)
    p4 = t("stage_4_pill", lang)

    # Streetverse Page Hero
    st.markdown(f"""
        <div class="storybook-page-hero">
            <div class="hero-tagline-badge">🔍 {tag_inv}</div>
            <h1 class="hero-page-title">{head_inv}</h1>
            <p class="hero-page-desc">{desc_inv}</p>
        </div>
    """, unsafe_allow_html=True)

    # Stage Indicators
    st.markdown(f"""
        <div style="display: flex; gap: 8px; margin-bottom: 1.4rem; flex-wrap: wrap;">
            <div class="investigation-step-pill active">{p1}</div>
            <div class="investigation-step-pill">{p2}</div>
            <div class="investigation-step-pill">{p3}</div>
            <div class="investigation-step-pill">{p4}</div>
        </div>
    """, unsafe_allow_html=True)

    col_input, col_preview = st.columns([0.55, 0.45])
    sample_dir = Path(__file__).resolve().parent / "data" / "samples"
    image_bytes = None

    with col_input:
        st.markdown(f"#### 📸 {t('upload_heading', lang)}")
        uploaded_file = st.file_uploader(
            t("upload_label", lang),
            type=["jpg", "jpeg", "png"],
            help="High-resolution photo showing clear infrastructure defect",
            label_visibility="collapsed"
        )

        st.caption(t("test_cases_label", lang))
        s_c1, s_c2, s_c3, s_c4 = st.columns(4)
        if s_c1.button(f"🕳️ {t('scenario_pothole', lang)}", use_container_width=True, key="inv_s_pothole"):
            st.session_state.selected_sample = "sample_pothole.jpg"
            st.session_state.sample_hint = "Potholes and damaged roads"
            st.session_state.sample_city = "Bengaluru"
            st.session_state.sample_locality = "Indiranagar"
            st.rerun()

        if s_c2.button(f"🗑️ {t('scenario_garbage', lang)}", use_container_width=True, key="inv_s_garbage"):
            st.session_state.selected_sample = "sample_garbage.jpg"
            st.session_state.sample_hint = "Overflowing garbage"
            st.session_state.sample_city = "Mumbai"
            st.session_state.sample_locality = "Bandra West"
            st.rerun()

        if s_c3.button(f"💡 {t('scenario_light', lang)}", use_container_width=True, key="inv_s_light"):
            st.session_state.selected_sample = "sample_streetlight.jpg"
            st.session_state.sample_hint = "Broken streetlights"
            st.session_state.sample_city = "Delhi"
            st.session_state.sample_locality = "Connaught Place"
            st.rerun()

        if s_c4.button(f"🌊 {t('scenario_drain', lang)}", use_container_width=True, key="inv_s_drain"):
            st.session_state.selected_sample = "sample_waterlogging.jpg"
            st.session_state.sample_hint = "Waterlogging and drainage issues"
            st.session_state.sample_city = "Ahmedabad"
            st.session_state.sample_locality = "Satellite"
            st.rerun()

        # City and Locality Selectors
        st.markdown(f"#### 📍 {t('locality_heading', lang)}")
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
        selected_city = st.selectbox(t("city_select_label", lang), options=cities, index=c_idx, key="inv_sel_city")

        localities = city_locality_map.get(selected_city, ["Indiranagar"])
        default_loc = st.session_state.get("sample_locality", localities[0] if localities else "")
        l_idx = localities.index(default_loc) if default_loc in localities else 0
        selected_locality = st.selectbox(t("ward_select_label", lang), options=localities, index=l_idx, key="inv_sel_loc")

        landmark_input = st.text_input(t("landmark_label", lang), value="Near City Center Junction", key="inv_txt_landmark")

    with col_preview:
        if uploaded_file:
            image_bytes = uploaded_file.getvalue()
            st.markdown('<div class="polaroid-frame">', unsafe_allow_html=True)
            st.image(image_bytes, caption="Uploaded Evidence", use_column_width=True)
            st.markdown(f"""
                <div class="polaroid-badge">
                    <span>EVIDENCE DOSSIER</span>
                    <span>LIVE UPLOAD</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif st.session_state.get("selected_sample"):
            sample_file = sample_dir / st.session_state.selected_sample
            if sample_file.exists():
                with open(sample_file, "rb") as f:
                    image_bytes = f.read()
                st.markdown('<div class="polaroid-frame">', unsafe_allow_html=True)
                st.image(image_bytes, caption=f"Demo Incident: {st.session_state.selected_sample}", use_column_width=True)
                st.markdown(f"""
                    <div class="polaroid-badge">
                        <span>ARCHIVED EVIDENCE</span>
                        <span>{st.session_state.get('sample_city', 'URBAN')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="polaroid-frame" style="padding: 48px 20px;">
                    <div style="font-size: 2.4rem; margin-bottom: 10px;">📷</div>
                    <div style="font-family: 'Fraunces', serif; font-size: 1.15rem; color: #243B63; font-weight: 700;">
                        {t('photo_placeholder', lang)}
                    </div>
                    <div style="font-size: 0.85rem; color: #7C6044; margin-top: 6px;">
                        Select a test incident or upload camera footage to begin AI investigation.
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Action Button
    if image_bytes:
        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
        if st.button(t("btn_run_investigation", lang), type="primary", use_container_width=True, key="btn_run_investigation"):
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
        s2_tag = t("stage_2_tag", lang)
        diag_lbl = t("diagnosis_label", lang)
        sev_lbl = t("severity_label", lang)
        sla_lbl = t("sla_label", lang)
        vis_lbl = t("visual_evidence_label", lang)
        imp_lbl = t("citizen_impact_title", lang)
        act_lbl = t("action_target_label", lang)
        diag_val = t(rep['issue_type'], lang)
        sev_val = t(rep['severity'], lang)
        dept_val = t(rep['recommended_department'], lang)

        st.markdown(f"""
            <div style="background: #FFFFFF; border: 2px solid #D96C48; border-radius: 18px; padding: 22px; box-shadow: 0 12px 30px rgba(217, 108, 72, 0.12); margin-top: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1.5px solid #E8DAC6; padding-bottom: 12px; margin-bottom: 14px;">
                    <div>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; font-weight: 700; color: #D96C48;">{s2_tag}</span>
                        <h3 style="font-family: 'Fraunces', serif; margin: 0; color: #243B63;">{diag_lbl}: {diag_val}</h3>
                    </div>
                    <div>
                        <span class="dossier-meta-pill dossier-pill-high">🚨 {sev_val} {sev_lbl}</span>
                        <span class="dossier-meta-pill" style="background: #243B63; color: #FFFFFF;">{sla_lbl}: {rep['sla_hours']}h</span>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px;">
                    <div style="background: #FAF3E8; border: 1px solid #DFCAB0; border-radius: 10px; padding: 12px;">
                        <strong style="font-size: 0.8rem; color: #7C6044; text-transform: uppercase;">{vis_lbl}</strong>
                        <div style="font-size: 0.9rem; color: #243B63; margin-top: 4px;">{rep['visual_evidence']}</div>
                    </div>
                    <div style="background: #FAF3E8; border: 1px solid #DFCAB0; border-radius: 10px; padding: 12px;">
                        <strong style="font-size: 0.8rem; color: #7C6044; text-transform: uppercase;">{imp_lbl}</strong>
                        <div style="font-size: 0.9rem; color: #243B63; margin-top: 4px;">{rep['citizen_impact']}</div>
                    </div>
                    <div style="grid-column: span 2; background: #ECFDF5; border: 1px solid #86EFAC; border-radius: 10px; padding: 12px;">
                        <strong style="font-size: 0.8rem; color: #065F46; text-transform: uppercase;">{act_lbl}</strong>
                        <div style="font-size: 0.92rem; color: #064E3B; font-weight: 700; margin-top: 4px;">
                            {rep['action_plan']} — <span style="text-decoration: underline;">{dept_val}</span>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Stage 3: Affirmative Confirmation
        st.markdown(f"#### ⚖️ {t('human_affirmation_heading', lang)}")
        st.markdown(t("human_affirmation_text", lang))

        confirm_col1, confirm_col2 = st.columns([0.45, 0.55])
        with confirm_col1:
            if st.button(t("btn_confirm_file", lang), type="primary", use_container_width=True, key="btn_confirm_file"):
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
                    st.success(f"{t('case_created_success', lang)} `{cid}`")
                    st.balloons()

    # Stage 4: Case Created Docket
    if st.session_state.get("registered_case_id"):
        cid = st.session_state.registered_case_id
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%); border: 2px solid #059669; border-radius: 18px; padding: 22px; margin-top: 20px; box-shadow: 0 10px 25px rgba(5, 150, 105, 0.12);">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; font-weight: 700; color: #065F46;">STAGE 04 • {p4}</span>
                        <h3 style="font-family: 'Fraunces', serif; color: #064E3B; margin: 4px 0 0 0;">🎉 {t('case_created_success', lang)}: <code>{cid}</code></h3>
                    </div>
                    <span style="background: #059669; color: #FFFFFF; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; font-weight: 700; padding: 4px 12px; border-radius: 20px;">
                        CIVIC LEDGER SEALED
                    </span>
                </div>
                <p style="font-size: 0.9rem; color: #065F46; margin: 8px 0 0 0;">
                    Your complaint has been permanently registered and autonomously routed to the nodal department. Follow the full resolution story below.
                </p>
            </div>
        """, unsafe_allow_html=True)

        post_c1, post_c2 = st.columns(2)
        with post_c1:
            if st.button(t("btn_follow_repair_story", lang), type="primary", use_container_width=True, key="btn_post_track"):
                st.session_state.street_active_view = "track"
                st.session_state.tracking_search_id = cid
                st.rerun()
        with post_c2:
            if st.button(t("btn_return_street", lang), use_container_width=True, key="btn_post_street"):
                st.session_state.street_active_view = "street"
                st.rerun()


def render_ai_mission_control_workshop(lang: str = "en"):
    """
    Renders AI Mission Control — Agent Workshop:
    Illustrated civic operations environment showcasing actual AI tool execution:
    OBSERVE → ANALYZE → LOCATE → ROUTE → REGISTER.
    Displays live tool inputs, outputs, timestamps, and execution states from ActionTrail.
    """
    m_tag = t("mission_tag", lang)
    m_head = t("mission_headline", lang)
    m_desc = t("mission_desc", lang)

    st.markdown(f"""
        <div class="storybook-page-hero">
            <div class="hero-tagline-badge">⚡ {m_tag}</div>
            <h1 class="hero-page-title">{m_head}</h1>
            <p class="hero-page-desc">{m_desc}</p>
        </div>
    """, unsafe_allow_html=True)

    # 5 High-Level Cognitive Blocks
    st.markdown(f"""
        <div class="pipeline-flow-banner">
            <div class="pipeline-node">
                <div class="pipeline-node-icon">👁️</div>
                <div class="pipeline-node-name">{t("node_observe", lang)}</div>
                <span style="font-size: 0.72rem; color: #64748B;">{t("node_observe_sub", lang)}</span>
            </div>
            <div class="pipeline-arrow">➔</div>
            <div class="pipeline-node">
                <div class="pipeline-node-icon">🧠</div>
                <div class="pipeline-node-name">{t("node_analyze", lang)}</div>
                <span style="font-size: 0.72rem; color: #64748B;">{t("node_analyze_sub", lang)}</span>
            </div>
            <div class="pipeline-arrow">➔</div>
            <div class="pipeline-node">
                <div class="pipeline-node-icon">📍</div>
                <div class="pipeline-node-name">{t("node_locate", lang)}</div>
                <span style="font-size: 0.72rem; color: #64748B;">{t("node_locate_sub", lang)}</span>
            </div>
            <div class="pipeline-arrow">➔</div>
            <div class="pipeline-node">
                <div class="pipeline-node-icon">🚦</div>
                <div class="pipeline-node-name">{t("node_route", lang)}</div>
                <span style="font-size: 0.72rem; color: #64748B;">{t("node_route_sub", lang)}</span>
            </div>
            <div class="pipeline-arrow">➔</div>
            <div class="pipeline-node">
                <div class="pipeline-node-icon">🛡️</div>
                <div class="pipeline-node-name">{t("node_register", lang)}</div>
                <span style="font-size: 0.72rem; color: #64748B;">{t("node_register_sub", lang)}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Scenario Runner for live pipeline inspection
    st.markdown(f"### ⚙️ {t('pipeline_inspector_title', lang)}")
    st.caption(t("pipeline_inspector_desc", lang))

    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    sel_scenario = st.session_state.get("workshop_scenario", "pothole")

    if p_col1.button(f"🕳️ {t('scenario_bengaluru_pothole', lang)}", use_container_width=True, type="primary" if sel_scenario == "pothole" else "secondary", key="ws_btn_pothole"):
        st.session_state.workshop_scenario = "pothole"
        st.session_state.workshop_trail = None
        st.rerun()

    if p_col2.button(f"🗑️ {t('scenario_mumbai_garbage', lang)}", use_container_width=True, type="primary" if sel_scenario == "garbage" else "secondary", key="ws_btn_garbage"):
        st.session_state.workshop_scenario = "garbage"
        st.session_state.workshop_trail = None
        st.rerun()

    if p_col3.button(f"💡 {t('scenario_delhi_light', lang)}", use_container_width=True, type="primary" if sel_scenario == "streetlight" else "secondary", key="ws_btn_light"):
        st.session_state.workshop_scenario = "streetlight"
        st.session_state.workshop_trail = None
        st.rerun()

    if p_col4.button(f"🌊 {t('scenario_ahmedabad_drain', lang)}", use_container_width=True, type="primary" if sel_scenario == "drainage" else "secondary", key="ws_btn_drain"):
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

        if st.button(t("btn_trigger_pipeline", lang), type="primary", use_container_width=True, key="btn_trigger_workshop"):
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
        st.markdown(f"#### 📜 {t('execution_log_title', lang)} ({len(steps)})")

        for step in steps:
            s_num = step.get("stage_number", 1)
            t_name = step.get("tool_name", "agent_tool")
            t_time = step.get("timestamp", "")
            t_args = step.get("input_arguments", {})
            t_res = step.get("output_result", {})
            raw_desc = COMPLAINT_STAGES.get(s_num, f"Stage {s_num}")
            t_desc = t(raw_desc, lang)

            st.markdown(f"""
                <div class="stage-card-workshop">
                    <div class="stage-header-flex">
                        <div>
                            <span class="stage-badge-pill">STAGE {s_num:02d}</span>
                            <strong style="margin-left: 8px; color: #243B63; font-size: 1.05rem;">{t_desc}</strong>
                            <code style="margin-left: 8px; color: #D96C48; font-size: 0.85rem;">{t_name}()</code>
                        </div>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.76rem; color: #64748B;">⏱️ {t_time}</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 10px;">
                        <div class="terminal-window">
                            <div class="terminal-header">
                                <div class="terminal-dots">
                                    <span class="terminal-dot" style="background: #EF4444;"></span>
                                    <span class="terminal-dot" style="background: #F59E0B;"></span>
                                    <span class="terminal-dot" style="background: #10B981;"></span>
                                </div>
                                <span>INPUT_PAYLOAD.json</span>
                            </div>
                            <div class="terminal-body"><pre style="margin: 0; background: transparent !important; padding: 0 !important; border: none !important; color: #E2E8F0;">{json.dumps(t_args, indent=2)}</pre></div>
                        </div>
                        <div class="terminal-window">
                            <div class="terminal-header">
                                <div class="terminal-dots">
                                    <span class="terminal-dot" style="background: #EF4444;"></span>
                                    <span class="terminal-dot" style="background: #F59E0B;"></span>
                                    <span class="terminal-dot" style="background: #10B981;"></span>
                                </div>
                                <span style="color: #34D399;">OUTPUT_TELEMETRY.json</span>
                            </div>
                            <div class="terminal-body"><pre style="margin: 0; background: transparent !important; padding: 0 !important; border: none !important; color: #34D399;">{json.dumps(t_res, indent=2)}</pre></div>
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
    st.markdown(f"""
        <div class="storybook-page-hero">
            <div class="hero-tagline-badge">📖 {t('story_tag', lang)}</div>
            <h1 class="hero-page-title">{t('story_headline', lang)}</h1>
            <p class="hero-page-desc">{t('story_desc', lang)}</p>
        </div>
    """, unsafe_allow_html=True)

    # Search & Sample Registry Bar
    st.markdown('<div class="admin-control-bar">', unsafe_allow_html=True)
    search_id = st.session_state.get("tracking_search_id", "NS-DEMO-A101B202")
    t_c1, t_c2 = st.columns([0.75, 0.25])
    with t_c1:
        entered_id = st.text_input(t("enter_tracking_id", lang), value=search_id, key="txt_track_search")
    with t_c2:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        if st.button(t("btn_find_story", lang), type="primary", use_container_width=True):
            st.session_state.tracking_search_id = entered_id
            st.rerun()

    st.caption(t("quick_demo_stories", lang))
    p_c1, p_c2, p_c3 = st.columns(3)
    if p_c1.button(f"🕳️ {t('demo_road_story', lang)}", use_container_width=True):
        st.session_state.tracking_search_id = "NS-DEMO-A101B202"
        st.rerun()
    if p_c2.button(f"🗑️ {t('demo_waste_story', lang)}", use_container_width=True):
        st.session_state.tracking_search_id = "NS-DEMO-C303D404"
        st.rerun()
    if p_c3.button(f"💡 {t('demo_light_story', lang)}", use_container_width=True):
        st.session_state.tracking_search_id = "NS-DEMO-E505F606"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    complaint = database.get_complaint(st.session_state.get("tracking_search_id", entered_id))
    if not complaint:
        st.warning(f"{t('complaint_not_found', lang)} ({entered_id})")
        return

    curr_status = complaint.get("status", "Reported")
    status_order = ["Reported", "Assigned", "In Progress", "Awaiting Verification", "Resolved"]
    curr_idx = status_order.index(curr_status) if curr_status in status_order else 0

    dept_tr = t(complaint.get('department', 'Municipal Authority'), lang)
    cat_tr = t(complaint.get('issue_type', 'Infrastructure Issue'), lang)
    loc_tr = t(complaint.get('locality', 'Local'), lang)
    city_tr = t(complaint.get('city', 'Metro'), lang)
    status_tr = t(curr_status, lang)

    # Active Incident Story Dossier
    prog_pct = min(100, int(((curr_idx + 1) / len(status_order)) * 100))
    st.markdown(f"""
        <div style="background: #FFFFFF; border: 2px solid #DFCAB0; border-radius: 18px; padding: 22px; margin: 18px 0; box-shadow: 0 10px 28px rgba(36, 59, 99, 0.07);">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1.5px dashed #DFCAB0; padding-bottom: 12px; margin-bottom: 14px; flex-wrap: wrap; gap: 8px;">
                <div>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; font-weight: 700; color: #D96C48;">STORY DOSSIER • {complaint.get('id')}</span>
                    <h3 style="font-family: 'Fraunces', serif; color: #243B63; margin: 2px 0 0 0;">{cat_tr}</h3>
                </div>
                <div>
                    <span class="dossier-meta-pill" style="background: #243B63; color: #FFFFFF; font-size: 0.82rem;">{t('status_label', lang)}: {status_tr.upper()}</span>
                </div>
            </div>
            <div style="font-size: 0.92rem; color: #243B63;">
                📍 <strong>{loc_tr}, {city_tr}</strong> • {t('ward_label', lang)}: <code>{complaint.get('ward')}</code> • {t('assigned_authority', lang)}: <strong>{dept_tr}</strong>
            </div>
            <div style="margin-top: 14px;">
                <div style="display: flex; justify-content: space-between; font-size: 0.78rem; font-weight: 700; color: #64748B; margin-bottom: 4px;">
                    <span>RESOLUTION NARRATIVE ARC</span>
                    <span>{prog_pct}% COMPLETE</span>
                </div>
                <div style="height: 8px; background: #FAF3E8; border-radius: 10px; overflow: hidden; border: 1px solid #DFCAB0;">
                    <div style="height: 100%; width: {prog_pct}%; background: linear-gradient(90deg, #F4BB52 0%, #D96C48 100%); border-radius: 10px;"></div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    chapters = [
        {"num": "01", "name": t("ch1_title", lang), "desc": t("ch1_desc", lang), "stage": 0},
        {"num": "02", "name": t("ch2_title", lang), "desc": t("ch2_desc", lang), "stage": 0},
        {"num": "03", "name": t("ch3_title", lang), "desc": f"{t('ch3_desc', lang)} ({dept_tr}, {complaint.get('ward')}).", "stage": 1},
        {"num": "04", "name": t("ch4_title", lang), "desc": t("ch4_desc", lang), "stage": 2},
        {"num": "05", "name": t("ch5_title", lang), "desc": t("ch5_desc", lang), "stage": 3},
        {"num": "06", "name": t("ch6_title", lang), "desc": t("ch6_desc", lang), "stage": 4},
    ]

    st.markdown(f"### 📚 {t('story_chapters_title', lang)}")
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
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style="background: #FFFFFF; border: 2px solid #DFCAB0; border-radius: 18px; padding: 22px; box-shadow: 0 8px 24px rgba(36, 59, 99, 0.06);">
            <div class="hero-tagline-badge">🤖 CITY COMPANION DIALOGUE</div>
            <h3 style="font-family: 'Fraunces', serif; color: #243B63; margin: 4px 0 0 0;">{t('ask_ai_complaint_title', lang)}</h3>
            <p style="font-size: 0.88rem; color: #64748B; margin: 4px 0 14px 0;">{t('ask_ai_complaint_caption', lang)}</p>
    """, unsafe_allow_html=True)
    
    t_chat_query = st.text_input(t("ask_ai_complaint_title", lang), value=f"What is the current status of complaint {complaint['id']}?", key=f"chat_in_{complaint['id']}", label_visibility="collapsed")
    if st.button(t("btn_ask_assistant", lang), type="primary", key=f"btn_ask_{complaint['id']}"):
        with st.spinner("🤖 Consulting civic agent and database records..."):
            ans = agent.run_tracking_chat_agent(t_chat_query, db_path=DB_PATH)
            st.markdown(f"""
                <div style="background: #FAF3E8; border: 1.5px solid #DFCAB0; border-radius: 14px; padding: 18px; margin-top: 14px;">
                    <strong style="color: #D96C48; font-size: 0.82rem; text-transform: uppercase;">{t('assistant_reply_label', lang)}:</strong>
                    <div style="font-size: 0.95rem; color: #243B63; line-height: 1.5; margin-top: 6px;">{ans.get('reply', '')}</div>
                </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_civictwin_studio(lang: str = "en"):
    """
    Renders CivicTwin — Transformation Studio:
    Immersive Before & After comparison workspace.
    Visual comparison, AI topographical observations, visible repair differences,
    verification report, and official administrative confirmation sign-off.
    """
    st.markdown(f"""
        <div class="storybook-page-hero">
            <div class="hero-tagline-badge">🏛️ {t('twin_tag', lang)}</div>
            <h1 class="hero-page-title">{t('twin_headline', lang)}</h1>
            <p class="hero-page-desc">{t('twin_desc', lang)}</p>
        </div>
    """, unsafe_allow_html=True)

    # Complaint Selector Bar
    st.markdown('<div class="admin-control-bar">', unsafe_allow_html=True)
    all_complaints = database.list_complaints(limit=50)
    c_ids = [c["id"] for c in all_complaints] if all_complaints else ["NS-DEMO-A101B202"]
    
    sel_cid = st.selectbox(t("twin_select_label", lang), options=c_ids, index=0, key="twin_sel_cid")
    comp_obj = database.get_complaint(sel_cid) or {"issue_type": "Potholes and damaged roads", "status": "In Progress", "locality": "Indiranagar"}

    cat_tr = t(comp_obj.get('issue_type', 'Potholes and damaged roads'), lang)
    status_tr = t(comp_obj.get('status', 'In Progress'), lang)
    loc_tr = t(comp_obj.get('locality', 'Local'), lang)
    city_tr = t(comp_obj.get('city', 'City'), lang)

    st.markdown(f"""
        <div style="font-size: 0.95rem; color: #243B63; margin-top: 10px;">
            <strong>{t('case_dossier_tag', lang)}:</strong> <code>{sel_cid}</code> • <strong>{t('diagnosis_label', lang)}:</strong> {cat_tr} • <strong>{t('status_label', lang)}:</strong> <span class="dossier-meta-pill dossier-pill-medium">{status_tr.upper()}</span>
            <div style="font-size: 0.85rem; color: #64748B; margin-top: 4px;">📍 {loc_tr}, {city_tr}</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Side-by-Side Photo Inspection
    sample_dir = Path(__file__).resolve().parent / "data" / "samples"
    before_file = sample_dir / "sample_pothole.jpg"
    after_file = sample_dir / "sample_resolved_pothole.jpg"

    tw_col1, tw_col2 = st.columns(2)
    with tw_col1:
        st.markdown('<div class="polaroid-frame">', unsafe_allow_html=True)
        if before_file.exists():
            st.image(str(before_file), caption=t("before_photo_label", lang), use_column_width=True)
        st.markdown(f"""
            <div class="polaroid-badge" style="color: #DC2626;">
                <span>⚠️ {t('before_photo_label', lang)}</span>
                <span>ORIGINAL DEFECT</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tw_col2:
        st.markdown('<div class="polaroid-frame">', unsafe_allow_html=True)
        if after_file.exists():
            st.image(str(after_file), caption=t("after_photo_label", lang), use_column_width=True)
        st.markdown(f"""
            <div class="polaroid-badge" style="color: #059669;">
                <span>✅ {t('after_photo_label', lang)}</span>
                <span>COMPLETION EVIDENCE</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if before_file.exists() and after_file.exists():
        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
        if st.button(t("btn_run_twin_studio", lang), type="primary", use_container_width=True, key="btn_exec_twin_studio"):
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
        status_badge = t('verified_badge', lang) if v_res.get('resolved') else t('needs_correction_badge', lang)

        st.markdown("---")
        st.markdown(f"""
            <div class="civictwin-compare-frame">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1.5px solid #E8DAC6; padding-bottom: 14px; margin-bottom: 16px; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; font-weight: 700; color: #D96C48;">
                            {t('ai_delta_tag', lang)}
                        </span>
                        <h3 style="font-family: 'Fraunces', serif; margin: 0; color: #243B63;">
                            {t('status_label', lang)}: {status_badge}
                        </h3>
                    </div>
                    <div class="civictwin-score-badge">
                        <span>🎯</span> {score_pct}% {t('match_confidence', lang)}
                    </div>
                </div>

                <div style="background: #FAF3E8; border: 1px solid #DFCAB0; border-radius: 12px; padding: 14px; margin-bottom: 16px;">
                    <strong style="color: #7C6044; font-size: 0.85rem; text-transform: uppercase;">{t('topography_diff_label', lang)}</strong>
                    <div style="font-size: 0.92rem; color: #243B63; margin-top: 4px; line-height: 1.5;">{v_res.get('delta_detected', 'Asphalt surface leveled completely; void filled to flush grade with no residual craters.')}</div>
                </div>

                <strong style="color: #243B63; font-size: 0.88rem; text-transform: uppercase;">📋 {t('checklist_title', lang)}</strong>
                <div class="checklist-box">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.88rem; color: #243B63;">
                        <div>✅ {t('check_1', lang)}</div>
                        <div>✅ {t('check_2', lang)}</div>
                        <div>✅ {t('check_3', lang)}</div>
                        <div>✅ {t('check_4', lang)}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Officer Confirmation Sign-Off
        st.markdown(f"#### ✍️ {t('admin_signoff_title', lang)}")
        st.caption(t("admin_signoff_desc", lang))

        sign_col1, sign_col2 = st.columns([0.45, 0.55])
        with sign_col1:
            if st.button(t("btn_confirm_resolution", lang), type="primary", use_container_width=True, key="btn_confirm_twin_res"):
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
                st.success(f"🎉 **Complaint `{sel_cid}` {t('resolution_committed_success', lang)}**")
                st.balloons()


def render_neighborhood_pulse_stories(lang: str = "en"):
    """
    Renders Neighborhood Pulse — Explore the Neighborhood:
    Illustrated neighborhood exploration interface grounded in authentic SQLite telemetry.
    Select neighborhood directly, view reported problems, active issues, resolved complaints,
    and local civic memory stories.
    """
    st.markdown(f"""
        <div class="storybook-page-hero">
            <div class="hero-tagline-badge">🏘️ {t('pulse_tag', lang)}</div>
            <h1 class="hero-page-title">{t('pulse_headline', lang)}</h1>
            <p class="hero-page-desc">{t('pulse_desc', lang)}</p>
        </div>
    """, unsafe_allow_html=True)

    # Neighborhood Selection Bar
    st.markdown('<div class="admin-control-bar">', unsafe_allow_html=True)
    localities = ["Indiranagar (Bengaluru)", "Bandra West (Mumbai)", "Connaught Place (Delhi)", "Satellite (Ahmedabad)", "Kothrud (Pune)"]
    sel_loc = st.selectbox(t("select_neighborhood_label", lang), options=localities, index=0, key="pulse_sel_neighborhood")
    loc_clean = sel_loc.split(" (")[0]
    st.markdown('</div>', unsafe_allow_html=True)

    stats = database.get_neighborhood_pulse_stats()
    metrics = stats.get("metrics", {})
    total = metrics.get("total_complaints", 0)
    in_prog = metrics.get("in_progress_complaints", 0)
    resolved = metrics.get("resolved_complaints", 0)
    rate = metrics.get("resolution_rate", 75.0)

    # Telemetry KPI Grid
    st.markdown(f"""
        <div class="pulse-stat-grid">
            <div class="pulse-stat-box" style="border-top: 4px solid var(--terracotta);">
                <span style="font-size: 0.8rem; color: #64748B; font-weight: 700; text-transform: uppercase;">📋 {t('total_reports', lang)}</span>
                <div class="pulse-stat-val">{total}</div>
                <span style="font-size: 0.76rem; color: #D96C48; font-weight: 600;">{t('recorded_in_sqlite', lang)}</span>
            </div>
            <div class="pulse-stat-box" style="border-top: 4px solid var(--mango);">
                <span style="font-size: 0.8rem; color: #64748B; font-weight: 700; text-transform: uppercase;">🚧 {t('active_in_progress', lang)}</span>
                <div class="pulse-stat-val" style="color: #D97706;">{in_prog}</div>
                <span style="font-size: 0.76rem; color: #64748B; font-weight: 600;">{t('crews_dispatched', lang)}</span>
            </div>
            <div class="pulse-stat-box" style="border-top: 4px solid var(--sage);">
                <span style="font-size: 0.8rem; color: #64748B; font-weight: 700; text-transform: uppercase;">✅ {t('verified_resolved', lang)}</span>
                <div class="pulse-stat-val" style="color: #059669;">{resolved}</div>
                <span style="font-size: 0.76rem; color: #047857; font-weight: 600;">{t('civictwin_verified', lang)}</span>
            </div>
            <div class="pulse-stat-box" style="border-top: 4px solid var(--indigo);">
                <span style="font-size: 0.8rem; color: #64748B; font-weight: 700; text-transform: uppercase;">⚡ {t('resolution_rate', lang)}</span>
                <div class="pulse-stat-val" style="color: #243B63;">{rate:.1f}%</div>
                <span style="font-size: 0.76rem; color: #64748B; font-weight: 600;">{t('overall_velocity', lang)}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Civic Intelligence Synthesis Narrative
    summary = stats.get("ai_neighborhood_summary", "Telemetry loaded.")
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FFFDF8 0%, #FAF3E8 100%); border: 2px solid #DFCAB0; border-radius: 18px; padding: 22px 26px; margin-bottom: 22px; box-shadow: 0 8px 24px rgba(36, 59, 99, 0.05); position: relative;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1.5px dashed #DFCAB0; padding-bottom: 10px; margin-bottom: 12px; flex-wrap: wrap; gap: 6px;">
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 800; color: #D96C48; text-transform: uppercase; letter-spacing: 0.08em;">
                    📰 {t('civic_intelligence_synthesis', lang)} • {loc_clean}
                </span>
                <span style="font-size: 0.75rem; color: #64748B; font-weight: 700;">AUTONOMOUS AI SYNTHESIS</span>
            </div>
            <p style="font-size: 0.96rem; color: #243B63; margin: 0; line-height: 1.6; font-style: italic;">"{summary}"</p>
        </div>
    """, unsafe_allow_html=True)

    # Filtered Neighborhood Cases
    all_complaints = database.list_complaints(limit=50)
    matched = [c for c in all_complaints if loc_clean.lower() in c.get("locality", "").lower()]
    cases_to_show = matched if matched else all_complaints[:5]

    st.markdown(f"#### 🏘️ {t('active_community_cases', lang)} {loc_clean} ({len(cases_to_show)})")
    for c in cases_to_show:
        c_col1, c_col2 = st.columns([0.82, 0.18])
        with c_col1:
            st.markdown(f"""
                <div style="background: #FFFFFF; border: 1.5px solid #E8DAC6; border-radius: 14px; padding: 14px 18px; margin-bottom: 10px; box-shadow: 0 4px 12px rgba(36, 59, 99, 0.04);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong style="color: #243B63; font-size: 0.98rem;">{c['id']}</strong>
                        <span class="dossier-meta-pill dossier-pill-medium">{t(c['status'], lang).upper()}</span>
                    </div>
                    <div style="font-size: 0.92rem; color: #D96C48; font-weight: 700; margin-top: 4px;">
                        {t(c['issue_type'], lang)} at <strong>{t(c['locality'], lang)}, {t(c['city'], lang)}</strong>
                    </div>
                    <div style="font-size: 0.84rem; color: #64748B; margin-top: 4px;">{c['description']}</div>
                </div>
            """, unsafe_allow_html=True)
        with c_col2:
            st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
            if st.button(t("btn_inspect_dossier", lang), key=f"btn_p_view_{c['id']}", use_container_width=True):
                st.session_state.selected_case_id = c["id"]
                st.rerun()


def render_civic_operations_studio(lang: str = "en"):
    """
    Renders Civic Operations Studio (Admin):
    Redesigned in the illustrated Streetverse design language.
    Features complaint management, status updates, department assignments,
    repair verification, and chronological audit trail inspection.
    """
    st.markdown(f"""
        <div class="storybook-page-hero">
            <div class="hero-tagline-badge">🛡️ {t('admin_tag', lang)}</div>
            <h1 class="hero-page-title">{t('admin_headline', lang)}</h1>
            <p class="hero-page-desc">{t('admin_desc', lang)}</p>
        </div>
    """, unsafe_allow_html=True)

    all_complaints = database.list_complaints(limit=100)
    if not all_complaints:
        st.info("No complaints found in the database.")
        return

    # Filter controls in Storybook Control Bar
    st.markdown('<div class="admin-control-bar">', unsafe_allow_html=True)
    f_col1, f_col2 = st.columns([0.6, 0.4])
    with f_col1:
        status_filter = st.selectbox(t("filter_status_label", lang), options=["All"] + VALID_STATUSES, key="admin_filter_status")
    with f_col2:
        search_query = st.text_input(t("search_id_locality", lang), value="", key="admin_search_query")
    st.markdown('</div>', unsafe_allow_html=True)

    filtered = all_complaints
    if status_filter != "All":
        filtered = [c for c in filtered if c.get("status") == status_filter]
    if search_query:
        q = search_query.strip().lower()
        filtered = [c for c in filtered if q in c.get("id", "").lower() or q in c.get("locality", "").lower()]

    st.markdown(f"**📋 {t('found_matching_complaints', lang)} {len(filtered)}**")

    c_ids = [c["id"] for c in filtered] if filtered else [all_complaints[0]["id"]]
    sel_id = st.selectbox(t("select_complaint_manage", lang), options=c_ids, key="admin_sel_cid")

    complaint = database.get_complaint(sel_id)
    if complaint:
        c_issue = t(complaint.get('issue_type', ''), lang)
        c_status = t(complaint.get('status', ''), lang)
        c_loc = t(complaint.get('locality', ''), lang)
        c_city = t(complaint.get('city', ''), lang)
        c_dept = t(complaint.get('department', ''), lang)

        st.markdown(f"""
            <div class="admin-op-card">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1.5px dashed #DFCAB0; padding-bottom: 12px; margin-bottom: 14px; flex-wrap: wrap; gap: 8px;">
                    <div>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; font-weight: 700; color: #D96C48;">CASE ID: {complaint.get('id')}</span>
                        <h3 style="font-family: 'Fraunces', serif; margin: 2px 0 0 0; color: #243B63;">{c_issue}</h3>
                    </div>
                    <span class="dossier-meta-pill" style="background: #243B63; color: #FFFFFF; font-size: 0.82rem;">{t('status_label', lang)}: {c_status.upper()}</span>
                </div>
                <div style="font-size: 0.92rem; color: #243B63;">
                    📍 <strong>{c_loc}, {c_city}</strong> • {t('ward_label', lang)}: <code>{complaint.get('ward')}</code> • {t('assigned_authority', lang)}: <strong>{c_dept}</strong>
                </div>
                <div style="font-size: 0.88rem; color: #64748B; margin-top: 8px; background: #FAF3E8; padding: 10px 14px; border-radius: 10px; border: 1px solid #DFCAB0;">
                    <em>"{complaint.get('description')}"</em>
                </div>
            </div>
        """, unsafe_allow_html=True)

        ctrl_col1, ctrl_col2 = st.columns(2)
        with ctrl_col1:
            curr_s = complaint.get("status", "Reported")
            s_idx = VALID_STATUSES.index(curr_s) if curr_s in VALID_STATUSES else 0
            new_status = st.selectbox(t("update_status_transition", lang), options=VALID_STATUSES, index=s_idx, key="admin_status_select")

        with ctrl_col2:
            officer_notes = st.text_input(t("officer_action_notes", lang), value="Verified on-site by municipal assessment team.", key="admin_officer_notes")

        btn_commit, btn_twin_jump = st.columns([0.5, 0.5])
        with btn_commit:
            if st.button(t("btn_commit_status", lang), type="primary", use_container_width=True, key="btn_commit_admin"):
                success = database.update_complaint_status(sel_id, new_status, note=officer_notes)
                if success:
                    st.success(f"Status for `{sel_id}` officially updated to **{t(new_status, lang)}**.")
                    st.rerun()

        with btn_twin_jump:
            if st.button(t("btn_open_twin_studio", lang), use_container_width=True, key=f"btn_admin_twin_{sel_id}"):
                st.session_state.street_active_view = "civictwin"
                st.session_state.twin_sel_cid = sel_id
                st.session_state.selected_case_id = None
                st.rerun()


def render_ai_companion_drawer(lang: str = "en"):
    """
    Renders the compact AI City Companion overlay.
    Lives cleanly inside the command capsule context without taking over the screen.
    """
    st.markdown(f"""
        <div class="storybook-page-hero">
            <div class="hero-tagline-badge">🤖 {t('companion_tag', lang)}</div>
            <h1 class="hero-page-title">{t('companion_headline', lang)}</h1>
            <p class="hero-page-desc">{t('companion_desc', lang)}</p>
        </div>
    """, unsafe_allow_html=True)

    # Prompt suggestions
    st.caption(t("prompt_suggestions_label", lang))
    p1, p2, p3 = st.columns(3)
    preset_query = None
    pr1 = t("prompt_1", lang)
    pr2 = t("prompt_2", lang)
    pr3 = t("prompt_3", lang)

    if p1.button(pr1, use_container_width=True):
        preset_query = "Which department handles potholes in Bengaluru?"
    if p2.button(pr2, use_container_width=True):
        preset_query = "What is the status of complaint NS-DEMO-A101B202?"
    if p3.button(pr3, use_container_width=True):
        preset_query = "Show neighborhood statistics and resolution rates."

    user_query = st.text_input(t("companion_headline", lang), value=preset_query or "", placeholder=t("ask_assistant_placeholder", lang), key="companion_query_input")
    
    if st.button(t("btn_send_query", lang), type="primary", key="btn_send_companion") or preset_query:
        if user_query:
            with st.spinner("🤖 Consulting civic agent and SQLite database..."):
                reply = agent.run_tracking_chat_agent(user_query, db_path=DB_PATH)
                st.markdown(f"""
                    <div style="background: #FFFFFF; border: 2px solid #DFCAB0; border-radius: 16px; padding: 20px; box-shadow: 0 8px 24px rgba(36, 59, 99, 0.08); margin-top: 14px;">
                        <strong style="color: #D96C48; font-size: 0.82rem; text-transform: uppercase;">{t('assistant_reply_label', lang)}:</strong>
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
        st.markdown(render_streetverse_svg(category_counts, active_states={"road": "alert" if category_counts["Potholes and damaged roads"] > 0 else "smooth"}, lang=st.session_state.lang), unsafe_allow_html=True)

        lang = st.session_state.lang
        st.markdown(f"### 🏘️ {t('street_signals_title', lang)}")
        st.caption(t("street_signals_desc", lang))

        h_col1, h_col2, h_col3, h_col4 = st.columns(4)
        with h_col1:
            st.markdown(f"""
                <div class="hotspot-card-badge">
                    <span style="font-size: 1.4rem;">🕳️</span>
                    <strong style="color: #D96C48; font-size: 0.95rem; display: block; margin-top: 4px;">{t('hotspot_road_title', lang)}</strong>
                    <span style="font-size: 0.8rem; color: #64748B;">{category_counts['Potholes and damaged roads']} {t('active_reports_sub', lang)}</span>
                </div>
            """, unsafe_allow_html=True)
            if st.button(t("hotspot_road_btn", lang), key="btn_h_road", use_container_width=True):
                st.session_state.selected_hotspot = "road"
                st.session_state.street_active_view = "hotspot"
                st.rerun()

        with h_col2:
            st.markdown(f"""
                <div class="hotspot-card-badge">
                    <span style="font-size: 1.4rem;">💡</span>
                    <strong style="color: #F4BB52; font-size: 0.95rem; display: block; margin-top: 4px;">{t('hotspot_light_title', lang)}</strong>
                    <span style="font-size: 0.8rem; color: #64748B;">{category_counts['Broken streetlights']} {t('lighting_incidents_sub', lang)}</span>
                </div>
            """, unsafe_allow_html=True)
            if st.button(t("hotspot_light_btn", lang), key="btn_h_light", use_container_width=True):
                st.session_state.selected_hotspot = "streetlight"
                st.session_state.street_active_view = "hotspot"
                st.rerun()

        with h_col3:
            st.markdown(f"""
                <div class="hotspot-card-badge">
                    <span style="font-size: 1.4rem;">🗑️</span>
                    <strong style="color: #83A98A; font-size: 0.95rem; display: block; margin-top: 4px;">{t('hotspot_waste_title', lang)}</strong>
                    <span style="font-size: 0.8rem; color: #64748B;">{category_counts['Overflowing garbage']} {t('waste_points_sub', lang)}</span>
                </div>
            """, unsafe_allow_html=True)
            if st.button(t("hotspot_waste_btn", lang), key="btn_h_waste", use_container_width=True):
                st.session_state.selected_hotspot = "garbage"
                st.session_state.street_active_view = "hotspot"
                st.rerun()

        with h_col4:
            st.markdown(f"""
                <div class="hotspot-card-badge">
                    <span style="font-size: 1.4rem;">🌊</span>
                    <strong style="color: #243B63; font-size: 0.95rem; display: block; margin-top: 4px;">{t('hotspot_drain_title', lang)}</strong>
                    <span style="font-size: 0.8rem; color: #64748B;">{category_counts['Waterlogging and drainage issues']} {t('drainage_issues_sub', lang)}</span>
                </div>
            """, unsafe_allow_html=True)
            if st.button(t("hotspot_drain_btn", lang), key="btn_h_drain", use_container_width=True):
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
    render_activity_pill(stats, lang=st.session_state.lang)
