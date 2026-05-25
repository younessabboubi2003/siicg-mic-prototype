import io
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

# ============================================================
# CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="SIICG — MIC | Executive Performance Cockpit",
    page_icon="assets/logo_mic.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PALETTE
# ============================================================
NAVY = "#1E2A44"
NAVY_2 = "#243B63"
GOLD = "#C8A96B"
TEAL = "#1F7A7A"
RED = "#B91C1C"
ORANGE = "#D97706"
GREEN = "#047857"
LIGHT = "#F7F8FA"
WHITE = "#FFFFFF"
GRAY = "#6B7280"
LGRAY = "#E5E7EB"
SOFT_BLUE = "#EAF3F8"

MIC_LOGO = "assets/logo_mic.png"
DEFAULT_FILE = "kpi_mic_sample.csv"

# ============================================================
# CSS — PREMIUM CONSULTING STYLE
# ============================================================
st.markdown(f"""
<style>
html, body, [class*="css"] {{
    font-family: 'Segoe UI', Arial, sans-serif;
}}

.main {{
    background-color: {LIGHT};
}}

.block-container {{
    padding: 0 2.6rem 2.5rem 2.6rem;
    max-width: 1380px;
}}

.header-band {{
    background: linear-gradient(90deg, {NAVY} 0%, {NAVY_2} 100%);
    padding: 18px 30px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 3px solid {GOLD};
    margin: -1.8rem -2.6rem 1.4rem -2.6rem;
}}

.header-left {{
    display: flex;
    align-items: center;
    gap: 18px;
}}

.header-logo {{
    height: 52px;
    object-fit: contain;
    background: white;
    border-radius: 6px;
    padding: 5px 12px;
}}

.header-title {{
    color: {WHITE};
    font-size: 22px;
    font-weight: 750;
    line-height: 1.15;
}}

.header-sub {{
    color: {GOLD};
    font-size: 12px;
    margin-top: 4px;
}}

.header-badge {{
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.25);
    color: {WHITE};
    font-size: 12px;
    font-weight: 600;
    padding: 8px 14px;
    border-radius: 999px;
}}

.method-box {{
    background: {SOFT_BLUE};
    border-left: 4px solid {TEAL};
    color: {NAVY};
    padding: 14px 18px;
    border-radius: 8px;
    margin: 0 0 1.2rem 0;
    font-size: 14px;
    line-height: 1.5;
}}

.section-title {{
    color: {NAVY};
    font-size: 17px;
    font-weight: 750;
    border-left: 4px solid {GOLD};
    padding-left: 12px;
    margin: 1.4rem 0 0.8rem 0;
}}

.exec-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 1.2rem;
}}

.exec-card {{
    background: {WHITE};
    border: 1px solid {LGRAY};
    border-radius: 12px;
    padding: 18px 18px;
    box-shadow: 0 2px 8px rgba(30,42,68,0.045);
}}

.exec-card .label {{
    font-size: 11px;
    color: {GRAY};
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 8px;
}}

.exec-card .value {{
    font-size: 30px;
    font-weight: 800;
    color: {NAVY};
    line-height: 1;
}}

.exec-card .sub {{
    font-size: 11px;
    color: {GRAY};
    margin-top: 7px;
}}

.exec-card.green {{ border-top: 3px solid {GREEN}; }}
.exec-card.orange {{ border-top: 3px solid {ORANGE}; }}
.exec-card.red {{ border-top: 3px solid {RED}; }}
.exec-card.gold {{ border-top: 3px solid {GOLD}; }}

.decision-card {{
    background: {WHITE};
    border: 1px solid {LGRAY};
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
    box-shadow: 0 1px 5px rgba(30,42,68,0.04);
}}

.decision-red {{ border-left: 5px solid {RED}; }}
.decision-orange {{ border-left: 5px solid {ORANGE}; }}
.decision-green {{ border-left: 5px solid {GREEN}; }}

.decision-title {{
    color: {NAVY};
    font-weight: 750;
    font-size: 13px;
}}

.decision-meta {{
    color: {GRAY};
    font-size: 12px;
    margin-top: 4px;
}}

.decision-action {{
    color: {NAVY};
    font-size: 12px;
    margin-top: 7px;
    background: #F9FAFB;
    padding: 7px 10px;
    border-radius: 6px;
}}

.gov-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 1rem;
}}

.gov-card {{
    background: {WHITE};
    border: 1px solid {LGRAY};
    border-radius: 10px;
    padding: 14px;
    text-align: center;
}}

.gov-card .gov-label {{
    font-size: 11px;
    color: {GRAY};
    text-transform: uppercase;
    font-weight: 700;
}}

.gov-card .gov-value {{
    color: {NAVY};
    font-size: 16px;
    font-weight: 750;
    margin-top: 6px;
}}

.assistant-panel {{
    background: {WHITE};
    border: 1px solid {LGRAY};
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(30,42,68,0.045);
    margin-top: 0.2rem;
}}

.assistant-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
}}

.assistant-title {{
    color: {NAVY};
    font-size: 15px;
    font-weight: 800;
}}

.assistant-badge {{
    background: #ECFDF5;
    color: {GREEN};
    border: 1px solid #A7F3D0;
    font-size: 10px;
    padding: 3px 8px;
    border-radius: 999px;
    font-weight: 800;
}}

.assistant-note {{
    background: #F8FAFC;
    color: {GRAY};
    border-left: 3px solid {GOLD};
    padding: 9px 10px;
    border-radius: 7px;
    font-size: 12px;
    margin-bottom: 12px;
    line-height: 1.45;
}}

.assistant-answer {{
    background: #F9FAFB;
    border: 1px solid {LGRAY};
    border-radius: 10px;
    padding: 12px;
    color: {NAVY};
    font-size: 13px;
    line-height: 1.55;
    margin-top: 10px;
}}

section[data-testid="stSidebar"] {{
    background: {NAVY} !important;
}}

section[data-testid="stSidebar"] * {{
    color: {WHITE} !important;
}}

section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stFileUploader label,
section[data-testid="stSidebar"] .stTextInput label {{
    color: {GOLD} !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}}

.sidebar-logo-wrap {{
    text-align: center;
    padding: 14px 0 8px 0;
    border-bottom: 1px solid rgba(200,169,107,0.35);
    margin-bottom: 16px;
}}

.sidebar-logo {{
    height: 48px;
    object-fit: contain;
    background: white;
    border-radius: 6px;
    padding: 5px 12px;
}}

.sidebar-doc-title {{
    color: {GOLD} !important;
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 12px;
    text-align: center;
}}

.stDownloadButton > button {{
    background: {NAVY} !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 650 !important;
    padding: 10px 18px !important;
}}

.stDownloadButton > button:hover {{
    background: {TEAL} !important;
}}

.footer {{
    margin-top: 2rem;
    padding: 12px 0;
    border-top: 1px solid {LGRAY};
    text-align: center;
    font-size: 11px;
    color: {GRAY};
}}

.stTextArea textarea {{
    font-family: 'Courier New', monospace;
    font-size: 12px;
    background: #F9FAFB;
    border: 1px solid {LGRAY};
    border-radius: 8px;
}}

[data-testid="stDataFrame"] {{
    border: 1px solid {LGRAY};
    border-radius: 10px;
    overflow: hidden;
}}

/* Sidebar input readability fix */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] select {{
    color: #1E2A44 !important;
    background-color: #FFFFFF !important;
}}

section[data-testid="stSidebar"] div[data-baseweb="select"] * {{
    color: #1E2A44 !important;
}}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
}}

section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {{
    background-color: #F8FAFC !important;
    border: 1px dashed #CBD5E1 !important;
}}

section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] * {{
    color: #1E2A44 !important;
}}

section[data-testid="stSidebar"] span[data-baseweb="tag"] {{
    border-radius: 8px !important;
    font-weight: 700 !important;
    color: white !important;
}}

.status-chip {{
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    color: white;
    font-size: 11px;
    font-weight: 800;
    margin: 2px 4px 2px 0;
}}
