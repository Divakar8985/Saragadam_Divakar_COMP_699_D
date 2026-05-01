import streamlit as st
import sqlite3
import ast
import json
import hashlib
import os
import math
import statistics
import csv
import io
import re
from datetime import datetime, timedelta
from collections import defaultdict
import copy
import logging
import time
import random

logging.basicConfig(level=logging.INFO)

DB_PATH = "secureintent.db"

DARK_BG = "#080C14"
CARD_BG = "#0D1321"
CARD_BORDER = "#1A2540"
ACCENT_PRIMARY = "#00D4FF"
ACCENT_SECONDARY = "#7B61FF"
ACCENT_DANGER = "#FF4C6A"
ACCENT_SUCCESS = "#00E5A0"
ACCENT_WARNING = "#FFB84C"
TEXT_PRIMARY = "#F0F4FF"
TEXT_SECONDARY = "#8899BB"
TEXT_MUTED = "#445577"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
    --bg: #080C14;
    --card: #0D1321;
    --card-2: #111827;
    --border: #1A2540;
    --border-2: #243050;
    --accent: #00D4FF;
    --accent-2: #7B61FF;
    --danger: #FF4C6A;
    --success: #00E5A0;
    --warn: #FFB84C;
    --text: #F0F4FF;
    --text-2: #8899BB;
    --text-3: #445577;
    --glow: 0 0 40px rgba(0,212,255,0.15);
    --glow-2: 0 0 60px rgba(123,97,255,0.12);
    --shadow: 0 8px 32px rgba(0,0,0,0.6);
    --shadow-2: 0 24px 64px rgba(0,0,0,0.8);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse 80% 60% at 50% 0%, rgba(0,212,255,0.04) 0%, transparent 70%),
                radial-gradient(ellipse 60% 40% at 80% 80%, rgba(123,97,255,0.05) 0%, transparent 60%),
                #080C14 !important;
    min-height: 100vh;
}

[data-testid="stSidebar"] { display: none !important; }
[data-testid="stSidebarNav"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

[data-testid="stHeader"] {
    background: transparent !important;
    backdrop-filter: none !important;
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

.stButton > button {
    background: linear-gradient(135deg, rgba(0,212,255,0.12) 0%, rgba(123,97,255,0.08) 100%) !important;
    border: 1px solid rgba(0,212,255,0.3) !important;
    color: var(--accent) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    padding: 0.6rem 1.4rem !important;
    border-radius: 8px !important;
    transition: all 0.25s cubic-bezier(0.4,0,0.2,1) !important;
    letter-spacing: 0.02em !important;
    cursor: pointer !important;
    backdrop-filter: blur(8px) !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0,212,255,0.22) 0%, rgba(123,97,255,0.18) 100%) !important;
    border-color: rgba(0,212,255,0.6) !important;
    box-shadow: 0 0 20px rgba(0,212,255,0.25), 0 4px 16px rgba(0,0,0,0.4) !important;
    transform: translateY(-1px) !important;
    color: #ffffff !important;
}

.stButton > button:active { transform: translateY(0) !important; }

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div,
.stMultiSelect > div > div > div {
    background: rgba(13,19,33,0.9) !important;
    border: 1px solid var(--border-2) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    border-radius: 8px !important;
    transition: border-color 0.2s !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(0,212,255,0.5) !important;
    box-shadow: 0 0 0 2px rgba(0,212,255,0.1) !important;
    outline: none !important;
}

.stSelectbox > div > div { border: 1px solid var(--border-2) !important; border-radius: 8px !important; }
.stSelectbox [data-baseweb="select"] { background: rgba(13,19,33,0.9) !important; }
.stSelectbox [data-baseweb="select"] > div { background: transparent !important; color: var(--text) !important; }

label, .stTextInput label, .stTextArea label, .stSelectbox label,
.stNumberInput label, .stSlider label, .stMultiSelect label,
[data-testid="stWidgetLabel"] {
    color: var(--text-2) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    margin-bottom: 6px !important;
}

.stNumberInput > div > div > input {
    background: rgba(13,19,33,0.9) !important;
    border: 1px solid var(--border-2) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

.stSlider > div > div > div > div {
    background: var(--accent) !important;
}

[data-testid="stMetricValue"] {
    color: var(--accent) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 2rem !important;
}

[data-testid="stMetricLabel"] {
    color: var(--text-2) !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

[data-testid="stMetricDelta"] { font-size: 0.78rem !important; }

.stDataFrame { background: transparent !important; }
.stDataFrame > div { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; overflow: hidden !important; }

[data-testid="stExpander"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    margin-bottom: 8px !important;
}

[data-testid="stExpander"] summary {
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
}

.stAlert { border-radius: 10px !important; border: none !important; }

div[data-testid="stVerticalBlock"] > div { padding: 0 !important; }

.stTab { background: transparent !important; }
[data-testid="stTabs"] [role="tablist"] {
    background: rgba(13,19,33,0.7) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    border: 1px solid var(--border) !important;
    gap: 2px !important;
}

[data-testid="stTabs"] [role="tab"] {
    background: transparent !important;
    color: var(--text-2) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s !important;
    border: none !important;
}

[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(123,97,255,0.1)) !important;
    color: var(--accent) !important;
    border: 1px solid rgba(0,212,255,0.25) !important;
}

.stCheckbox > label { color: var(--text-2) !important; }
.stCheckbox > label > span { color: var(--text) !important; font-size: 0.9rem !important; }

[data-testid="stRadio"] label { color: var(--text-2) !important; }
[data-testid="stRadio"] > div > label { color: var(--text) !important; }

div.stForm { background: transparent !important; border: none !important; }
div.stForm > div { background: transparent !important; }

[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #00D4FF, #7B61FF) !important;
    border: none !important;
    color: #080C14 !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.75rem 2rem !important;
    border-radius: 10px !important;
    width: 100% !important;
    transition: all 0.25s !important;
    text-transform: uppercase !important;
}

[data-testid="stFormSubmitButton"] > button:hover {
    filter: brightness(1.1) !important;
    box-shadow: 0 0 30px rgba(0,212,255,0.4), 0 8px 24px rgba(0,0,0,0.5) !important;
    transform: translateY(-2px) !important;
}

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--card); }
::-webkit-scrollbar-thumb { background: var(--border-2); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

.stMarkdown p { color: var(--text-2) !important; font-size: 0.9rem !important; line-height: 1.7 !important; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: var(--text) !important; font-family: 'Syne', sans-serif !important; }

[data-testid="stCodeBlock"] {
    background: rgba(8,12,20,0.9) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

.element-container { margin-bottom: 0 !important; }

div[data-testid="column"] { padding: 0 4px !important; }

.stSuccess { background: rgba(0,229,160,0.1) !important; border: 1px solid rgba(0,229,160,0.3) !important; color: var(--success) !important; border-radius: 10px !important; }
.stError { background: rgba(255,76,106,0.1) !important; border: 1px solid rgba(255,76,106,0.3) !important; color: var(--danger) !important; border-radius: 10px !important; }
.stWarning { background: rgba(255,184,76,0.1) !important; border: 1px solid rgba(255,184,76,0.3) !important; color: var(--warn) !important; border-radius: 10px !important; }
.stInfo { background: rgba(0,212,255,0.08) !important; border: 1px solid rgba(0,212,255,0.2) !important; color: var(--accent) !important; border-radius: 10px !important; }

[data-testid="stMultiSelect"] > div { background: rgba(13,19,33,0.9) !important; border: 1px solid var(--border-2) !important; border-radius: 8px !important; }
[data-testid="stMultiSelect"] span[data-baseweb="tag"] { background: rgba(0,212,255,0.15) !important; border: 1px solid rgba(0,212,255,0.3) !important; color: var(--accent) !important; }

hr { border-color: var(--border) !important; opacity: 0.5 !important; }

.stProgress > div > div > div { background: linear-gradient(90deg, var(--accent), var(--accent-2)) !important; }
</style>
"""

def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def card(content, padding="24px", border_color=None, glow=False, height=None):
    bc = border_color or "#1A2540"
    glow_style = "box-shadow: 0 0 40px rgba(0,212,255,0.12), 0 8px 32px rgba(0,0,0,0.6);" if glow else "box-shadow: 0 8px 32px rgba(0,0,0,0.5);"
    h = f"height:{height};" if height else ""
    
    clean_content = str(content).replace('\n', ' ')
    
    html = f"""
    <div style="background:linear-gradient(145deg,#0D1321,#0A111E);
                border:1px solid {bc};
                border-radius:16px;
                padding:{padding};
                {glow_style}
                {h}
                position:relative;
                overflow:hidden;
                transition:all 0.3s;">
        <div style="position:absolute;top:0;left:0;right:0;height:1px;
                    background:linear-gradient(90deg,transparent,rgba(0,212,255,0.3),transparent);"></div>
        {clean_content}
    </div>
    """.replace('\n', ' ')
    
    st.markdown(html, unsafe_allow_html=True)
    return ""

def metric_card(label, value, delta=None, color="#00D4FF", icon=""):
    delta_html = ""
    if delta is not None:
        dc = "#00E5A0" if delta >= 0 else "#FF4C6A"
        ds = "+" if delta >= 0 else ""
        delta_html = f'<div style="color:{dc};font-size:0.75rem;font-weight:500;margin-top:4px;">{ds}{delta}%</div>'
    return f"""
    <div style="background:linear-gradient(145deg,#0D1321,#0A111E);
                border:1px solid #1A2540;border-radius:16px;padding:24px;
                box-shadow:0 8px 32px rgba(0,0,0,0.5);
                position:relative;overflow:hidden;transition:transform 0.2s;
                cursor:default;">
        <div style="position:absolute;top:0;left:0;right:0;height:2px;
                    background:linear-gradient(90deg,transparent,{color}44,transparent);"></div>
        <div style="position:absolute;top:-20px;right:-20px;width:80px;height:80px;
                    background:radial-gradient(circle,{color}18,transparent 70%);border-radius:50%;"></div>
        <div style="font-size:1.4rem;margin-bottom:8px;">{icon}</div>
        <div style="color:#8899BB;font-size:0.72rem;font-weight:500;letter-spacing:0.08em;
                    text-transform:uppercase;margin-bottom:8px;font-family:'DM Sans',sans-serif;">{label}</div>
        <div style="color:{color};font-size:2rem;font-weight:700;
                    font-family:'Syne',sans-serif;line-height:1;">{value}</div>
        {delta_html}
    </div>
    """

def status_badge(status):
    colors = {
        "Approved": ("#00E5A0", "rgba(0,229,160,0.12)"),
        "Rejected": ("#FF4C6A", "rgba(255,76,106,0.12)"),
        "Needs Revision": ("#FFB84C", "rgba(255,184,76,0.12)"),
        "Pending": ("#8899BB", "rgba(136,153,187,0.12)"),
        "Draft": ("#7B61FF", "rgba(123,97,255,0.12)"),
        "Submitted": ("#00D4FF", "rgba(0,212,255,0.12)"),
        "Evaluated": ("#00E5A0", "rgba(0,229,160,0.12)"),
    }
    c, bg = colors.get(status, ("#8899BB", "rgba(136,153,187,0.12)"))
    return f"""<span style="background:{bg};color:{c};border:1px solid {c}44;
               padding:3px 10px;border-radius:20px;font-size:0.72rem;
               font-weight:600;letter-spacing:0.06em;text-transform:uppercase;
               font-family:'DM Sans',sans-serif;">{status}</span>"""

def risk_gauge_html(score):
    if score < 30:
        color = "#00E5A0"
        level = "LOW"
    elif score < 60:
        color = "#FFB84C"
        level = "MEDIUM"
    else:
        color = "#FF4C6A"
        level = "HIGH"
    pct = min(score, 100)
    return f"""
    <div style="text-align:center;padding:10px 0;">
        <div style="position:relative;width:140px;height:70px;margin:0 auto 8px;">
            <svg viewBox="0 0 140 70" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;">
                <defs>
                    <linearGradient id="rg{score}" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" style="stop-color:#00E5A0"/>
                        <stop offset="50%" style="stop-color:#FFB84C"/>
                        <stop offset="100%" style="stop-color:#FF4C6A"/>
                    </linearGradient>
                </defs>
                <path d="M10 65 A60 60 0 0 1 130 65" fill="none" stroke="#1A2540" stroke-width="10" stroke-linecap="round"/>
                <path d="M10 65 A60 60 0 0 1 130 65" fill="none" stroke="url(#rg{score})" stroke-width="10"
                      stroke-linecap="round" stroke-dasharray="{pct*1.885} 188.5" opacity="0.9"/>
                <text x="70" y="62" text-anchor="middle" fill="{color}"
                      font-size="18" font-weight="700" font-family="Syne,sans-serif">{score}</text>
            </svg>
        </div>
        <div style="color:{color};font-size:0.72rem;font-weight:700;letter-spacing:0.15em;">{level} RISK</div>
    </div>
    """

def page_header(title, subtitle=None, breadcrumb=None):
    bc = f'<div style="color:#445577;font-size:0.78rem;margin-bottom:12px;font-family:JetBrains Mono,monospace;letter-spacing:0.05em;">{breadcrumb}</div>' if breadcrumb else ""
    sub = f'<div style="color:#8899BB;font-size:0.95rem;margin-top:6px;font-weight:300;">{subtitle}</div>' if subtitle else ""
    return f"""
    <div style="padding:32px 32px 0 32px;margin-bottom:24px;">
        {bc}
        <h1 style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:700;
                   color:#F0F4FF;line-height:1.2;letter-spacing:-0.02em;margin:0;">{title}</h1>
        {sub}
        <div style="width:48px;height:3px;background:linear-gradient(90deg,#00D4FF,#7B61FF);
                    border-radius:2px;margin-top:14px;"></div>
    </div>
    """

def section_header(title, subtitle=None):
    sub = f'<div style="color:#8899BB;font-size:0.82rem;margin-top:4px;">{subtitle}</div>' if subtitle else ""
    return f"""
    <div style="margin-bottom:18px;">
        <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:600;color:#F0F4FF;">{title}</div>
        {sub}
    </div>
    """

def top_navbar(user_name=None, user_role=None):
    user_section = ""
    if user_name:
        role_color = {
            "Author": "#00D4FF", "Analyst": "#7B61FF",
            "Admin": "#FFB84C", "Auditor": "#00E5A0"
        }.get(user_role, "#8899BB")
        user_section = f"""
        <div style="display:flex;align-items:center;gap:12px;">
            <div style="background:linear-gradient(135deg,{role_color}22,{role_color}11);
                        border:1px solid {role_color}33;border-radius:8px;
                        padding:6px 14px;">
                <span style="color:{role_color};font-size:0.72rem;font-weight:600;letter-spacing:0.08em;
                             text-transform:uppercase;">{user_role}</span>
            </div>
            <div style="width:36px;height:36px;background:linear-gradient(135deg,{role_color},{role_color}88);
                        border-radius:50%;display:flex;align-items:center;justify-content:center;
                        font-family:'Syne',sans-serif;font-weight:700;font-size:0.85rem;color:#080C14;">
                {user_name[0].upper()}
            </div>
            <div>
                <div style="color:#F0F4FF;font-size:0.88rem;font-weight:500;line-height:1.2;">{user_name}</div>
                <div style="color:#445577;font-size:0.72rem;">Authenticated</div>
            </div>
        </div>
        """
    return f"""
    <div style="background:rgba(8,12,20,0.95);border-bottom:1px solid #1A2540;
                padding:14px 32px;display:flex;justify-content:space-between;align-items:center;
                position:sticky;top:0;z-index:100;backdrop-filter:blur(20px);
                box-shadow:0 4px 24px rgba(0,0,0,0.5);">
        <div style="display:flex;align-items:center;gap:16px;">
            <div style="width:32px;height:32px;position:relative;">
                <svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
                    <polygon points="16,2 30,10 30,22 16,30 2,22 2,10" fill="none" stroke="#00D4FF" stroke-width="1.5"/>
                    <polygon points="16,7 25,12 25,20 16,25 7,20 7,12" fill="rgba(0,212,255,0.08)" stroke="#7B61FF" stroke-width="1"/>
                    <circle cx="16" cy="16" r="4" fill="#00D4FF"/>
                    <line x1="16" y1="2" x2="16" y2="7" stroke="#00D4FF" stroke-width="1.5"/>
                    <line x1="16" y1="25" x2="16" y2="30" stroke="#00D4FF" stroke-width="1.5"/>
                </svg>
            </div>
            <div>
                <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:1rem;
                            color:#F0F4FF;letter-spacing:-0.01em;">SecureIntent</div>
                <div style="font-size:0.65rem;color:#445577;letter-spacing:0.1em;
                            text-transform:uppercase;font-family:'JetBrains Mono',monospace;">
                    Governance Platform</div>
            </div>
        </div>
        <div style="display:flex;align-items:center;gap:8px;">
            <div style="width:6px;height:6px;background:#00E5A0;border-radius:50%;
                        box-shadow:0 0 6px #00E5A0;animation:pulse 2s infinite;"></div>
            <div style="color:#445577;font-size:0.72rem;font-family:'JetBrains Mono',monospace;">
                OFFLINE SECURE</div>
        </div>
        {user_section}
    </div>
    <style>@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:0.4}}}}</style>
    """

def side_nav(current_page, role):
    nav_items = get_nav_items(role)
    items_html = ""
    for item in nav_items:
        is_active = item["page"] == current_page
        active_style = """background:linear-gradient(135deg,rgba(0,212,255,0.12),rgba(123,97,255,0.08));
                         border-color:rgba(0,212,255,0.25);color:#00D4FF;""" if is_active else ""
        items_html += f"""
        <div style="padding:4px 0;">
            <div style="display:flex;align-items:center;gap:12px;padding:10px 16px;
                        border-radius:10px;border:1px solid transparent;cursor:pointer;
                        transition:all 0.2s;color:#8899BB;font-size:0.875rem;font-weight:500;
                        {active_style}" onclick="void(0)">
                <span style="font-size:1rem;width:20px;text-align:center;">{item['icon']}</span>
                <span>{item['label']}</span>
                {'<div style="width:4px;height:4px;background:#00D4FF;border-radius:50%;margin-left:auto;"></div>' if is_active else ''}
            </div>
        </div>
        """
    return f"""
    <div style="width:220px;background:rgba(8,12,20,0.8);border-right:1px solid #1A2540;
                padding:24px 16px;min-height:calc(100vh - 65px);
                backdrop-filter:blur(20px);">
        <div style="color:#445577;font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;
                    margin-bottom:16px;padding:0 6px;font-family:'JetBrains Mono',monospace;">
            Navigation</div>
        {items_html}
    </div>
    """

def get_nav_items(role):
    base = [{"page": "dashboard", "label": "Dashboard", "icon": "◈"}]
    if role in ["Author", "Admin"]:
        base += [
            {"page": "create_task", "label": "Create Task", "icon": "⊕"},
            {"page": "my_tasks", "label": "My Tasks", "icon": "◫"},
        ]
    if role in ["Analyst", "Admin"]:
        base += [
            {"page": "evaluate", "label": "Evaluate Tasks", "icon": "◎"},
            {"page": "risk_analysis", "label": "Risk Analysis", "icon": "◬"},
        ]
    if role in ["Admin"]:
        base += [
            {"page": "governance_rules", "label": "Governance Rules", "icon": "◈"},
            {"page": "policy_impact", "label": "Policy Impact", "icon": "◑"},
        ]
    if role in ["Auditor", "Admin"]:
        base += [
            {"page": "audit_logs", "label": "Audit Logs", "icon": "◳"},
            {"page": "reports", "label": "Reports", "icon": "◰"},
        ]
    return base

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL,
        status TEXT DEFAULT 'Active',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS automation_tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT NOT NULL,
        intent TEXT NOT NULL,
        business_purpose TEXT NOT NULL,
        owner_id INTEGER,
        state TEXT DEFAULT 'Draft',
        privilege_level TEXT DEFAULT 'User',
        timing_window TEXT DEFAULT 'Business Hours',
        resource_limit TEXT DEFAULT 'Low',
        risk_score REAL DEFAULT 0,
        decision TEXT DEFAULT 'Pending',
        created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(owner_id) REFERENCES users(user_id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS scripts (
        script_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER,
        script_name TEXT,
        script_content TEXT,
        language TEXT DEFAULT 'Python',
        FOREIGN KEY(task_id) REFERENCES automation_tasks(task_id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS task_dependencies (
        dependency_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER,
        depends_on_task_id INTEGER,
        relation_type TEXT DEFAULT 'Sequential',
        FOREIGN KEY(task_id) REFERENCES automation_tasks(task_id),
        FOREIGN KEY(depends_on_task_id) REFERENCES automation_tasks(task_id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS governance_rules (
        rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
        rule_name TEXT NOT NULL,
        rule_type TEXT NOT NULL,
        rule_definition TEXT,
        weight INTEGER DEFAULT 10,
        is_active INTEGER DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS evaluation_reports (
        report_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER,
        risk_score REAL,
        decision TEXT,
        explanation TEXT,
        violations TEXT,
        static_findings TEXT,
        evaluated_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        evaluated_by INTEGER,
        FOREIGN KEY(task_id) REFERENCES automation_tasks(task_id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS audit_logs (
        audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER,
        action_type TEXT,
        action_by INTEGER,
        action_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        remarks TEXT,
        FOREIGN KEY(task_id) REFERENCES automation_tasks(task_id),
        FOREIGN KEY(action_by) REFERENCES users(user_id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS state_transitions (
        transition_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER,
        from_state TEXT,
        to_state TEXT,
        transitioned_by INTEGER,
        transition_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        notes TEXT,
        FOREIGN KEY(task_id) REFERENCES automation_tasks(task_id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS rule_version_history (
        version_id INTEGER PRIMARY KEY AUTOINCREMENT,
        rule_id INTEGER,
        changed_by INTEGER,
        change_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        old_definition TEXT,
        new_definition TEXT,
        change_notes TEXT
    )""")
    conn.commit()
    seed_defaults(conn, c)
    conn.close()

def seed_defaults(conn, c):
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        default_users = [
            ("Divakar Saragadam", "divakar", hash_pwd("admin123"), "Admin"),
            ("Ravi Kumar", "ravi", hash_pwd("analyst123"), "Analyst"),
            ("Priya Singh", "priya", hash_pwd("author123"), "Author"),
            ("Alex Chen", "alex", hash_pwd("auditor123"), "Auditor"),
        ]
        c.executemany("INSERT INTO users (full_name,username,password_hash,role) VALUES(?,?,?,?)", default_users)
    c.execute("SELECT COUNT(*) FROM governance_rules")
    if c.fetchone()[0] == 0:
        rules = [
            ("Least Privilege Enforcement", "Privilege", "Penalize Admin-level tasks heavily", 25, 1),
            ("Execution Timing Control", "Timing", "Night execution outside business hours triggers penalty", 20, 1),
            ("Sensitive Import Detection", "Script", "OS, subprocess, shutil imports flagged", 30, 1),
            ("Unsafe Function Detection", "Script", "eval(), exec() usage penalized", 25, 1),
            ("Dependency Chain Risk", "Dependency", "Tasks with 3+ dependencies scored higher risk", 15, 1),
            ("Ownership Accountability", "Ownership", "Unowned tasks flagged automatically", 10, 1),
            ("Resource Overallocation", "Resource", "High resource tasks reviewed", 12, 1),
            ("Script Syntax Validation", "Script", "Scripts with syntax errors flagged", 10, 1),
        ]
        c.executemany("INSERT INTO governance_rules (rule_name,rule_type,rule_definition,weight,is_active) VALUES(?,?,?,?,?)", rules)
    c.execute("SELECT COUNT(*) FROM automation_tasks")
    if c.fetchone()[0] == 0:
        seed_tasks = [
            ("Database Night Backup", "Automated nightly database backup", "Ensure data recovery in case of failure", 2, "Evaluated", "Admin", "Night", "High", 85, "Rejected"),
            ("Log Rotation Script", "Rotate application logs weekly", "Prevent disk overflow from logs", 3, "Evaluated", "User", "Business Hours", "Low", 18, "Approved"),
            ("User Account Audit", "Audit inactive user accounts quarterly", "Compliance with security policy", 2, "Evaluated", "User", "Business Hours", "Medium", 42, "Needs Revision"),
            ("File Transfer Automation", "Move processed files to archive", "Operational efficiency", 3, "Draft", "User", "Business Hours", "Low", 0, "Pending"),
            ("System Health Monitor", "Check CPU and memory every 5 min", "Proactive infrastructure monitoring", 2, "Evaluated", "Admin", "Night", "Medium", 55, "Needs Revision"),
        ]
        for t in seed_tasks:
            c.execute("""INSERT INTO automation_tasks
                (task_name,intent,business_purpose,owner_id,state,privilege_level,timing_window,resource_limit,risk_score,decision)
                VALUES(?,?,?,?,?,?,?,?,?,?)""", t)
    conn.commit()

def hash_pwd(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def get_db():
    return sqlite3.connect(DB_PATH)

def db_fetch(query, params=()):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def db_fetchone(query, params=()):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(query, params)
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def db_exec(query, params=()):
    conn = get_db()
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    lid = c.lastrowid
    conn.close()
    return lid

def log_action(task_id, action_type, user_id, remarks=""):
    db_exec("INSERT INTO audit_logs (task_id,action_type,action_by,remarks) VALUES(?,?,?,?)",
            (task_id, action_type, user_id, remarks))

def record_transition(task_id, from_state, to_state, user_id, notes=""):
    db_exec("INSERT INTO state_transitions (task_id,from_state,to_state,transitioned_by,notes) VALUES(?,?,?,?,?)",
            (task_id, from_state, to_state, user_id, notes))

def authenticate(username, password):
    user = db_fetchone("SELECT * FROM users WHERE username=? AND status='Active'", (username,))
    if user and user["password_hash"] == hash_pwd(password):
        return user
    return None

def register_user(full_name, username, password, role):
    existing = db_fetchone("SELECT user_id FROM users WHERE username=?", (username,))
    if existing:
        return False, "Username already taken."
    db_exec("INSERT INTO users (full_name,username,password_hash,role) VALUES(?,?,?,?)",
            (full_name, username, hash_pwd(password), role))
    return True, "Account created successfully."

class StaticAnalyzer:
    SENSITIVE_IMPORTS = {"os", "subprocess", "shutil", "ctypes", "socket", "sys",
                         "paramiko", "ftplib", "smtplib", "requests", "urllib"}
    UNSAFE_FUNCTIONS = {"eval", "exec", "compile", "globals", "locals", "__import__"}
    FILE_OPS = {"open", "write", "read", "delete", "remove", "rmdir", "makedirs"}
    PRIVILEGE_OPS = {"chmod", "chown", "setuid", "setgid", "getpwnam"}

    @classmethod
    def analyze(cls, script_content):
        findings = []
        details = []
        try:
            tree = ast.parse(script_content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        name = alias.name.split(".")[0]
                        if name in cls.SENSITIVE_IMPORTS:
                            findings.append("Sensitive Import")
                            details.append(f"Sensitive module imported: '{name}'")
                if isinstance(node, ast.ImportFrom):
                    if node.module:
                        mod = node.module.split(".")[0]
                        if mod in cls.SENSITIVE_IMPORTS:
                            findings.append("Sensitive Import")
                            details.append(f"Sensitive module from-imported: '{node.module}'")
                if isinstance(node, ast.Call):
                    func_name = ""
                    if isinstance(node.func, ast.Name):
                        func_name = node.func.id
                    elif isinstance(node.func, ast.Attribute):
                        func_name = node.func.attr
                    if func_name in cls.UNSAFE_FUNCTIONS:
                        findings.append("Unsafe Function")
                        details.append(f"Unsafe function call detected: '{func_name}()'")
                    if func_name in cls.FILE_OPS:
                        findings.append("File Operation")
                        details.append(f"File operation detected: '{func_name}()'")
                    if func_name in cls.PRIVILEGE_OPS:
                        findings.append("Privilege Operation")
                        details.append(f"Privilege operation: '{func_name}()'")
        except SyntaxError as e:
            findings.append("Syntax Error")
            details.append(f"Script has syntax error: {str(e)}")
        except Exception as e:
            findings.append("Parse Error")
            details.append(f"Could not parse script: {str(e)}")
        return findings, details

class RiskEngine:
    @staticmethod
    def calculate(task, findings, active_rules):
        score = 0
        violations = []
        rule_map = {r["rule_name"]: r for r in active_rules}

        if task["privilege_level"] == "Admin":
            w = rule_map.get("Least Privilege Enforcement", {}).get("weight", 25)
            score += w
            violations.append(f"Admin privilege requested (+{w} pts)")
        elif task["privilege_level"] == "Elevated":
            score += 12
            violations.append("Elevated privilege requested (+12 pts)")

        if task["timing_window"] == "Night":
            w = rule_map.get("Execution Timing Control", {}).get("weight", 20)
            score += w
            violations.append(f"Night-time execution window (+{w} pts)")
        elif task["timing_window"] == "Weekend":
            score += 10
            violations.append("Weekend execution scheduled (+10 pts)")

        deps = db_fetch("SELECT * FROM task_dependencies WHERE task_id=?", (task["task_id"],))
        if len(deps) > 2:
            w = rule_map.get("Dependency Chain Risk", {}).get("weight", 15)
            score += w
            violations.append(f"Excessive dependencies ({len(deps)}) (+{w} pts)")
        elif len(deps) > 0:
            score += 5
            violations.append(f"Dependencies present ({len(deps)}) (+5 pts)")

        if task["resource_limit"] == "High":
            w = rule_map.get("Resource Overallocation", {}).get("weight", 12)
            score += w
            violations.append(f"High resource consumption (+{w} pts)")

        for f in findings:
            if f == "Sensitive Import":
                w = rule_map.get("Sensitive Import Detection", {}).get("weight", 30)
                score += w
                violations.append(f"Sensitive import in script (+{w} pts)")
            elif f == "Unsafe Function":
                w = rule_map.get("Unsafe Function Detection", {}).get("weight", 25)
                score += w
                violations.append(f"Unsafe function detected (+{w} pts)")
            elif f == "Syntax Error":
                w = rule_map.get("Script Syntax Validation", {}).get("weight", 10)
                score += w
                violations.append(f"Script syntax error (+{w} pts)")
            elif f == "File Operation":
                score += 8
                violations.append("File operation in script (+8 pts)")
            elif f == "Privilege Operation":
                score += 15
                violations.append("Privilege operation in script (+15 pts)")

        if not task.get("owner_id"):
            w = rule_map.get("Ownership Accountability", {}).get("weight", 10)
            score += w
            violations.append(f"No owner assigned (+{w} pts)")

        return min(score, 100), violations

    @staticmethod
    def get_decision(score):
        if score >= 60:
            return "Rejected"
        elif score >= 30:
            return "Needs Revision"
        return "Approved"

def render_login_register():
    st.markdown(f"""
    <div style="min-height:100vh;display:flex;align-items:center;justify-content:center;
                background:radial-gradient(ellipse 100% 80% at 50% 0%,rgba(0,212,255,0.06) 0%,transparent 60%),
                radial-gradient(ellipse 80% 60% at 20% 100%,rgba(123,97,255,0.07) 0%,transparent 60%),
                #080C14;">
        <div style="width:100%;max-width:480px;padding:20px;">
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;margin-bottom:40px;">
        <div style="width:64px;height:64px;margin:0 auto 20px;position:relative;">
            <svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;">
                <defs>
                    <linearGradient id="hg" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#00D4FF"/>
                        <stop offset="100%" style="stop-color:#7B61FF"/>
                    </linearGradient>
                </defs>
                <polygon points="32,4 60,20 60,44 32,60 4,44 4,20" fill="none" stroke="url(#hg)" stroke-width="2"/>
                <polygon points="32,12 52,23 52,41 32,52 12,41 12,23" fill="rgba(0,212,255,0.06)" stroke="#7B61FF" stroke-width="1"/>
                <circle cx="32" cy="32" r="8" fill="url(#hg)" opacity="0.9"/>
                <circle cx="32" cy="32" r="4" fill="#080C14"/>
                <circle cx="32" cy="32" r="2" fill="#00D4FF"/>
            </svg>
        </div>
        <div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;
                    color:#F0F4FF;letter-spacing:-0.03em;">SecureIntent</div>
        <div style="color:#445577;font-size:0.75rem;letter-spacing:0.2em;
                    text-transform:uppercase;margin-top:6px;font-family:'JetBrains Mono',monospace;">
            Cybersecurity Governance Platform</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Sign In", "Register"])

    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Authenticate")
            if submitted:
                if not username or not password:
                    st.error("All fields required.")
                else:
                    user = authenticate(username, password)
                    if user:
                        st.session_state.user = user
                        st.session_state.page = "dashboard"
                        log_action(None, "Login", user["user_id"], f"User {username} logged in")
                        st.rerun()
                    else:
                        st.error("Invalid credentials or inactive account.")

        st.markdown("""
        <div style="margin-top:20px;padding:16px;background:rgba(0,212,255,0.04);
                    border:1px solid rgba(0,212,255,0.1);border-radius:12px;">
            <div style="color:#445577;font-size:0.72rem;letter-spacing:0.08em;
                        text-transform:uppercase;margin-bottom:10px;font-family:'JetBrains Mono',monospace;">
                Demo Credentials</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
                <div style="padding:8px 12px;background:rgba(0,212,255,0.06);border-radius:8px;">
                    <div style="color:#00D4FF;font-size:0.7rem;font-weight:600;">ADMIN</div>
                    <div style="color:#8899BB;font-size:0.75rem;font-family:'JetBrains Mono',monospace;">divakar / admin123</div>
                </div>
                <div style="padding:8px 12px;background:rgba(123,97,255,0.06);border-radius:8px;">
                    <div style="color:#7B61FF;font-size:0.7rem;font-weight:600;">ANALYST</div>
                    <div style="color:#8899BB;font-size:0.75rem;font-family:'JetBrains Mono',monospace;">ravi / analyst123</div>
                </div>
                <div style="padding:8px 12px;background:rgba(0,229,160,0.06);border-radius:8px;">
                    <div style="color:#00E5A0;font-size:0.7rem;font-weight:600;">AUTHOR</div>
                    <div style="color:#8899BB;font-size:0.75rem;font-family:'JetBrains Mono',monospace;">priya / author123</div>
                </div>
                <div style="padding:8px 12px;background:rgba(255,184,76,0.06);border-radius:8px;">
                    <div style="color:#FFB84C;font-size:0.7rem;font-weight:600;">AUDITOR</div>
                    <div style="color:#8899BB;font-size:0.75rem;font-family:'JetBrains Mono',monospace;">alex / auditor123</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        with st.form("register_form"):
            full_name = st.text_input("Full Name", placeholder="Your full name")
            new_username = st.text_input("Username", placeholder="Choose a username")
            new_password = st.text_input("Password", type="password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
            role = st.selectbox("Role", ["Author", "Analyst", "Auditor"])
            reg_submitted = st.form_submit_button("Create Account")
            if reg_submitted:
                if not all([full_name, new_username, new_password, confirm_password]):
                    st.error("All fields are required.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    ok, msg = register_user(full_name, new_username, new_password, role)
                    if ok:
                        st.success(msg + " You may now sign in.")
                    else:
                        st.error(msg)

    st.markdown("</div></div>", unsafe_allow_html=True)

def render_dashboard():
    user = st.session_state.user
    role = user["role"]

    total_tasks = db_fetchone("SELECT COUNT(*) as cnt FROM automation_tasks")["cnt"]
    approved = db_fetchone("SELECT COUNT(*) as cnt FROM automation_tasks WHERE decision='Approved'")["cnt"]
    rejected = db_fetchone("SELECT COUNT(*) as cnt FROM automation_tasks WHERE decision='Rejected'")["cnt"]
    pending = db_fetchone("SELECT COUNT(*) as cnt FROM automation_tasks WHERE state='Draft' OR state='Submitted'")["cnt"]
    needs_rev = db_fetchone("SELECT COUNT(*) as cnt FROM automation_tasks WHERE decision='Needs Revision'")["cnt"]
    avg_risk = db_fetchone("SELECT AVG(risk_score) as avg FROM automation_tasks WHERE risk_score > 0")["avg"] or 0
    active_rules = db_fetchone("SELECT COUNT(*) as cnt FROM governance_rules WHERE is_active=1")["cnt"]
    total_users = db_fetchone("SELECT COUNT(*) as cnt FROM users")["cnt"]

    st.markdown(page_header("Governance Dashboard",
        f"Welcome back, {user['full_name']}. Platform status: operational.",
        f"SecureIntent / Dashboard"), unsafe_allow_html=True)

    st.markdown('<div style="padding:0 32px;">', unsafe_allow_html=True)

    cols = st.columns(4)
    with cols[0]:
        st.markdown(metric_card("Total Tasks", total_tasks, icon="◫", color="#00D4FF"), unsafe_allow_html=True)
    with cols[1]:
        st.markdown(metric_card("Approved", approved, icon="◎", color="#00E5A0"), unsafe_allow_html=True)
    with cols[2]:
        st.markdown(metric_card("Rejected", rejected, icon="◬", color="#FF4C6A"), unsafe_allow_html=True)
    with cols[3]:
        st.markdown(metric_card("Avg Risk Score", f"{avg_risk:.1f}", icon="◈", color="#FFB84C"), unsafe_allow_html=True)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    cols2 = st.columns([2, 1])

    with cols2[0]:
        recent_tasks = db_fetch("""
            SELECT t.*, u.full_name as owner_name
            FROM automation_tasks t
            LEFT JOIN users u ON t.owner_id = u.user_id
            ORDER BY t.updated_date DESC LIMIT 8
        """)
        html = section_header("Recent Tasks", "Latest automation submissions and their governance status")
        html += """<div style="display:flex;flex-direction:column;gap:8px;">"""
        for t in recent_tasks:
            bar_color = "#00E5A0" if t["decision"] == "Approved" else \
                        "#FF4C6A" if t["decision"] == "Rejected" else \
                        "#FFB84C" if t["decision"] == "Needs Revision" else "#7B61FF"
            risk_w = min(t["risk_score"], 100)
            priv_c = "#FF4C6A" if t["privilege_level"] == "Admin" else \
                     "#FFB84C" if t["privilege_level"] == "Elevated" else "#8899BB"
            html += f"""
            <div style="background:linear-gradient(145deg,#0D1321,#0A111E);
                        border:1px solid #1A2540;border-radius:12px;
                        padding:14px 16px;transition:all 0.2s;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
                    <div>
                        <div style="color:#F0F4FF;font-size:0.9rem;font-weight:500;
                                    font-family:'Syne',sans-serif;">{t['task_name']}</div>
                        <div style="color:#445577;font-size:0.75rem;margin-top:2px;
                                    font-family:'JetBrains Mono',monospace;">
                            ID #{t['task_id']} &nbsp;·&nbsp; {t['owner_name'] or 'Unassigned'}
                            &nbsp;·&nbsp; <span style="color:{priv_c};">{t['privilege_level']}</span>
                        </div>
                    </div>
                    {status_badge(t['decision'])}
                </div>
                <div style="display:flex;align-items:center;gap:10px;">
                    <div style="flex:1;height:3px;background:#1A2540;border-radius:2px;overflow:hidden;">
                        <div style="width:{risk_w}%;height:100%;background:{bar_color};
                                    border-radius:2px;transition:width 0.5s;"></div>
                    </div>
                    <div style="color:{bar_color};font-size:0.72rem;font-weight:600;
                                width:32px;text-align:right;">{t['risk_score']:.0f}</div>
                </div>
            </div>
            """
        html += "</div>"
        st.markdown(card(html, padding="20px"), unsafe_allow_html=True)

    with cols2[1]:
        st.markdown(section_header("Platform Status", "Live governance metrics"), unsafe_allow_html=True)

        gauge_html = risk_gauge_html(int(avg_risk))
        st.markdown(card(f"""
        <div style="text-align:center;margin-bottom:4px;">
            <div style="color:#8899BB;font-size:0.72rem;letter-spacing:0.08em;
                        text-transform:uppercase;margin-bottom:8px;">Average Risk Index</div>
            {gauge_html}
        </div>
        """, padding="16px"), unsafe_allow_html=True)

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

        stat_items = [
            ("Active Rules", active_rules, "#7B61FF"),
            ("Pending Review", pending, "#00D4FF"),
            ("Needs Revision", needs_rev, "#FFB84C"),
            ("Platform Users", total_users, "#00E5A0"),
        ]
        for label, val, color in stat_items:
            st.markdown(f"""
            <div style="background:rgba(13,19,33,0.8);border:1px solid #1A2540;
                        border-radius:10px;padding:12px 16px;margin-bottom:8px;
                        display:flex;justify-content:space-between;align-items:center;">
                <div style="color:#8899BB;font-size:0.8rem;">{label}</div>
                <div style="color:{color};font-family:'Syne',sans-serif;
                            font-weight:700;font-size:1.1rem;">{val}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

        decision_breakdown = db_fetch("""
            SELECT decision, COUNT(*) as cnt FROM automation_tasks
            WHERE decision != 'Pending' GROUP BY decision
        """)
        if decision_breakdown:
            total_dec = sum(d["cnt"] for d in decision_breakdown)
            dec_colors = {"Approved": "#00E5A0", "Rejected": "#FF4C6A", "Needs Revision": "#FFB84C"}
            donut_html = """
            <div style="text-align:center;margin-bottom:8px;">
                <div style="color:#8899BB;font-size:0.72rem;letter-spacing:0.08em;
                            text-transform:uppercase;margin-bottom:12px;">Decision Breakdown</div>
                <svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" style="width:100px;height:100px;margin:0 auto;display:block;">
            """
            offset = 0
            r = 40
            circ = 2 * math.pi * r
            for d in decision_breakdown:
                pct = d["cnt"] / total_dec if total_dec else 0
                dash = pct * circ
                color = dec_colors.get(d["decision"], "#8899BB")
                donut_html += f"""
                <circle cx="60" cy="60" r="{r}" fill="none" stroke="{color}" stroke-width="18"
                        stroke-dasharray="{dash:.1f} {circ:.1f}"
                        stroke-dashoffset="-{offset:.1f}" opacity="0.85"/>
                """
                offset += dash
            donut_html += """<circle cx="60" cy="60" r="26" fill="#080C14"/>
                <text x="60" y="55" text-anchor="middle" fill="#F0F4FF" font-size="12"
                      font-weight="700" font-family="Syne,sans-serif">Tasks</text>
                <text x="60" y="68" text-anchor="middle" fill="#8899BB" font-size="9"
                      font-family="DM Sans,sans-serif">evaluated</text>
                </svg>
                <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:10px;">
            """
            for d in decision_breakdown:
                color = dec_colors.get(d["decision"], "#8899BB")
                donut_html += f"""
                <div style="display:flex;align-items:center;gap:5px;">
                    <div style="width:8px;height:8px;background:{color};border-radius:2px;"></div>
                    <div style="color:#8899BB;font-size:0.7rem;">{d['decision']}</div>
                    <div style="color:{color};font-size:0.7rem;font-weight:600;">({d['cnt']})</div>
                </div>
                """
            donut_html += "</div></div>"
            st.markdown(card(donut_html, padding="16px"), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

def render_create_task():
    user = st.session_state.user
    st.markdown(page_header("Create Automation Task",
        "Define a new automation task for governance evaluation.",
        "SecureIntent / Create Task"), unsafe_allow_html=True)

    st.markdown('<div style="padding:0 32px;">', unsafe_allow_html=True)

    cols = st.columns([2, 1])

    with cols[0]:
        st.markdown(section_header("Task Definition", "Provide complete task information for UR-1 through UR-7"), unsafe_allow_html=True)
        with st.form("create_task_form"):
            task_name = st.text_input("Task Name *", placeholder="e.g. Nightly Database Backup")
            intent = st.text_area("Declared Intent *", placeholder="What is this task designed to do?", height=90)
            business_purpose = st.text_area("Business Purpose *", placeholder="Why is this task necessary for the organization?", height=90)

            st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
            st.markdown("""<div style="color:#8899BB;font-size:0.8rem;letter-spacing:0.05em;
                            text-transform:uppercase;margin-bottom:8px;">Execution Context</div>""", unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                privilege_level = st.selectbox("Privilege Level *", ["User", "Elevated", "Admin"])
            with c2:
                timing_window = st.selectbox("Execution Window *", ["Business Hours", "Night", "Weekend", "Anytime"])
            with c3:
                resource_limit = st.selectbox("Resource Usage *", ["Low", "Medium", "High"])

            st.markdown("""<div style="color:#8899BB;font-size:0.8rem;letter-spacing:0.05em;
                            text-transform:uppercase;margin:12px 0 8px;">Python Script (Optional)</div>""", unsafe_allow_html=True)
            script_name = st.text_input("Script Filename", placeholder="e.g. backup_script.py")
            script_content = st.text_area("Script Content", placeholder="Paste your Python script here...", height=120)

            all_tasks = db_fetch("SELECT task_id, task_name FROM automation_tasks WHERE task_id != -1")
            dep_options = {f"#{t['task_id']} - {t['task_name']}": t["task_id"] for t in all_tasks}
            selected_deps = st.multiselect("Task Dependencies (Optional)", list(dep_options.keys()))

            submitted = st.form_submit_button("Create Task")

            if submitted:
                if not task_name.strip() or not intent.strip() or not business_purpose.strip():
                    st.error("Task Name, Intent, and Business Purpose are required.")
                else:
                    task_id = db_exec("""INSERT INTO automation_tasks
                        (task_name,intent,business_purpose,owner_id,state,privilege_level,timing_window,resource_limit)
                        VALUES(?,?,?,?,?,?,?,?)""",
                        (task_name.strip(), intent.strip(), business_purpose.strip(),
                         user["user_id"], "Draft", privilege_level, timing_window, resource_limit))

                    if script_content.strip():
                        sname = script_name.strip() or "script.py"
                        db_exec("INSERT INTO scripts (task_id,script_name,script_content) VALUES(?,?,?)",
                                (task_id, sname, script_content.strip()))

                    for dep_label in selected_deps:
                        dep_id = dep_options[dep_label]
                        db_exec("INSERT INTO task_dependencies (task_id,depends_on_task_id) VALUES(?,?)",
                                (task_id, dep_id))

                    log_action(task_id, "Task Created", user["user_id"],
                               f"Task '{task_name}' created with {privilege_level} privilege")
                    record_transition(task_id, "None", "Draft", user["user_id"], "Task created")
                    st.success(f"Task '**{task_name}**' created successfully. Task ID: #{task_id}")

    with cols[1]:
        st.markdown(section_header("Governance Guide", "Best practices for task creation"), unsafe_allow_html=True)
        tips = [
            ("#00E5A0", "Use minimum required privilege level to reduce risk score."),
            ("#00D4FF", "Schedule tasks during business hours when possible."),
            ("#7B61FF", "Avoid importing os, subprocess, or shutil unless essential."),
            ("#FFB84C", "Document intent clearly to help analysts evaluate the task."),
            ("#FF4C6A", "Never use eval() or exec() in automation scripts."),
        ]
        tips_html = ""
        for color, tip in tips:
            tips_html += f"""
            <div style="display:flex;gap:10px;margin-bottom:12px;align-items:flex-start;">
                <div style="width:6px;height:6px;background:{color};border-radius:50%;
                            margin-top:6px;flex-shrink:0;box-shadow:0 0 6px {color}77;"></div>
                <div style="color:#8899BB;font-size:0.82rem;line-height:1.5;">{tip}</div>
            </div>
            """
        st.markdown(card(tips_html, padding="20px"), unsafe_allow_html=True)

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

        risk_table_html = """
        <div style="margin-bottom:8px;color:#8899BB;font-size:0.72rem;letter-spacing:0.08em;
                    text-transform:uppercase;">Risk Scoring Guide</div>
        """
        score_items = [
            ("Admin Privilege", "+25 pts", "#FF4C6A"),
            ("Night Execution", "+20 pts", "#FFB84C"),
            ("Sensitive Import", "+30 pts", "#FF4C6A"),
            ("Unsafe Function", "+25 pts", "#FF4C6A"),
            ("3+ Dependencies", "+15 pts", "#FFB84C"),
            ("High Resources", "+12 pts", "#FFB84C"),
        ]
        for label, pts, color in score_items:
            risk_table_html += f"""
            <div style="display:flex;justify-content:space-between;padding:6px 0;
                        border-bottom:1px solid #1A2540;">
                <div style="color:#8899BB;font-size:0.78rem;">{label}</div>
                <div style="color:{color};font-size:0.78rem;font-weight:600;
                            font-family:'JetBrains Mono',monospace;">{pts}</div>
            </div>
            """
        threshold_html = risk_table_html + """
        <div style="margin-top:12px;padding:10px;background:rgba(0,212,255,0.05);
                    border:1px solid rgba(0,212,255,0.1);border-radius:8px;">
            <div style="color:#8899BB;font-size:0.72rem;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:6px;">Decision Thresholds</div>
            <div style="color:#00E5A0;font-size:0.78rem;">0-29 → Approved</div>
            <div style="color:#FFB84C;font-size:0.78rem;">30-59 → Needs Revision</div>
            <div style="color:#FF4C6A;font-size:0.78rem;">60+ → Rejected</div>
        </div>
        """
        st.markdown(card(threshold_html, padding="16px"), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

def render_my_tasks():
    user = st.session_state.user
    st.markdown(page_header("My Tasks",
        "View, manage and submit your automation task submissions.",
        "SecureIntent / My Tasks"), unsafe_allow_html=True)

    st.markdown('<div style="padding:0 32px;">', unsafe_allow_html=True)

    tasks = db_fetch("""
        SELECT t.*, u.full_name as owner_name
        FROM automation_tasks t
        LEFT JOIN users u ON t.owner_id = u.user_id
        WHERE t.owner_id = ?
        ORDER BY t.updated_date DESC
    """, (user["user_id"],))

    if not tasks:
        st.markdown(card("""
        <div style="text-align:center;padding:40px;">
            <div style="font-size:2.5rem;margin-bottom:12px;opacity:0.3;">◫</div>
            <div style="color:#8899BB;font-size:0.95rem;">No tasks created yet.</div>
            <div style="color:#445577;font-size:0.82rem;margin-top:4px;">Create your first automation task to get started.</div>
        </div>
        """, padding="0px"), unsafe_allow_html=True)
    else:
        filter_col, _ = st.columns([2, 3])
        with filter_col:
            state_filter = st.selectbox("Filter by Status", ["All", "Draft", "Submitted", "Evaluated"])

        filtered = tasks if state_filter == "All" else [t for t in tasks if t["state"] == state_filter]

        for t in filtered:
            scripts = db_fetch("SELECT * FROM scripts WHERE task_id=?", (t["task_id"],))
            deps = db_fetch("""SELECT d.*, at.task_name as dep_name FROM task_dependencies d
                              JOIN automation_tasks at ON d.depends_on_task_id = at.task_id
                              WHERE d.task_id=?""", (t["task_id"],))

            with st.expander(f"  #{t['task_id']}  {t['task_name']}  —  {t['state']}", expanded=False):
                ec1, ec2, ec3 = st.columns(3)
                with ec1:
                    st.markdown(f"""
                    <div style="background:rgba(13,19,33,0.8);border:1px solid #1A2540;
                                border-radius:10px;padding:14px;">
                        <div style="color:#445577;font-size:0.7rem;text-transform:uppercase;
                                    letter-spacing:0.08em;margin-bottom:6px;">State</div>
                        {status_badge(t['state'])}
                    </div>""", unsafe_allow_html=True)
                with ec2:
                    st.markdown(f"""
                    <div style="background:rgba(13,19,33,0.8);border:1px solid #1A2540;
                                border-radius:10px;padding:14px;">
                        <div style="color:#445577;font-size:0.7rem;text-transform:uppercase;
                                    letter-spacing:0.08em;margin-bottom:6px;">Decision</div>
                        {status_badge(t['decision'])}
                    </div>""", unsafe_allow_html=True)
                with ec3:
                    risk_color = "#00E5A0" if t["risk_score"] < 30 else \
                                 "#FFB84C" if t["risk_score"] < 60 else "#FF4C6A"
                    st.markdown(f"""
                    <div style="background:rgba(13,19,33,0.8);border:1px solid #1A2540;
                                border-radius:10px;padding:14px;">
                        <div style="color:#445577;font-size:0.7rem;text-transform:uppercase;
                                    letter-spacing:0.08em;margin-bottom:4px;">Risk Score</div>
                        <div style="color:{risk_color};font-family:'Syne',sans-serif;
                                    font-size:1.4rem;font-weight:700;">{t['risk_score']:.0f}</div>
                    </div>""", unsafe_allow_html=True)

                st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

                d1, d2 = st.columns(2)
                with d1:
                    st.markdown(f"""
                    <div style="color:#8899BB;font-size:0.75rem;font-weight:500;
                                letter-spacing:0.06em;text-transform:uppercase;margin-bottom:4px;">Intent</div>
                    <div style="color:#F0F4FF;font-size:0.88rem;line-height:1.6;">{t['intent']}</div>
                    """, unsafe_allow_html=True)
                with d2:
                    st.markdown(f"""
                    <div style="color:#8899BB;font-size:0.75rem;font-weight:500;
                                letter-spacing:0.06em;text-transform:uppercase;margin-bottom:4px;">Business Purpose</div>
                    <div style="color:#F0F4FF;font-size:0.88rem;line-height:1.6;">{t['business_purpose']}</div>
                    """, unsafe_allow_html=True)

                st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

                ctx_html = f"""
                <div style="display:flex;gap:12px;flex-wrap:wrap;">
                    <div style="background:rgba(0,212,255,0.07);border:1px solid rgba(0,212,255,0.15);
                                border-radius:8px;padding:8px 14px;">
                        <div style="color:#445577;font-size:0.68rem;text-transform:uppercase;letter-spacing:0.06em;">Privilege</div>
                        <div style="color:#00D4FF;font-size:0.88rem;font-weight:500;">{t['privilege_level']}</div>
                    </div>
                    <div style="background:rgba(123,97,255,0.07);border:1px solid rgba(123,97,255,0.15);
                                border-radius:8px;padding:8px 14px;">
                        <div style="color:#445577;font-size:0.68rem;text-transform:uppercase;letter-spacing:0.06em;">Timing</div>
                        <div style="color:#7B61FF;font-size:0.88rem;font-weight:500;">{t['timing_window']}</div>
                    </div>
                    <div style="background:rgba(255,184,76,0.07);border:1px solid rgba(255,184,76,0.15);
                                border-radius:8px;padding:8px 14px;">
                        <div style="color:#445577;font-size:0.68rem;text-transform:uppercase;letter-spacing:0.06em;">Resource</div>
                        <div style="color:#FFB84C;font-size:0.88rem;font-weight:500;">{t['resource_limit']}</div>
                    </div>
                    <div style="background:rgba(0,229,160,0.07);border:1px solid rgba(0,229,160,0.15);
                                border-radius:8px;padding:8px 14px;">
                        <div style="color:#445577;font-size:0.68rem;text-transform:uppercase;letter-spacing:0.06em;">Scripts</div>
                        <div style="color:#00E5A0;font-size:0.88rem;font-weight:500;">{len(scripts)}</div>
                    </div>
                    <div style="background:rgba(136,153,187,0.07);border:1px solid rgba(136,153,187,0.15);
                                border-radius:8px;padding:8px 14px;">
                        <div style="color:#445577;font-size:0.68rem;text-transform:uppercase;letter-spacing:0.06em;">Dependencies</div>
                        <div style="color:#8899BB;font-size:0.88rem;font-weight:500;">{len(deps)}</div>
                    </div>
                </div>
                """
                st.markdown(ctx_html, unsafe_allow_html=True)

                if deps:
                    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                    dep_names = ", ".join([f"#{d['depends_on_task_id']} {d['dep_name']}" for d in deps])
                    st.markdown(f"""
                    <div style="color:#8899BB;font-size:0.75rem;margin-top:6px;">
                        <span style="color:#445577;text-transform:uppercase;letter-spacing:0.06em;font-size:0.68rem;">
                            Dependencies:</span> {dep_names}</div>
                    """, unsafe_allow_html=True)

                report = db_fetchone("SELECT * FROM evaluation_reports WHERE task_id=? ORDER BY evaluated_date DESC LIMIT 1",
                                     (t["task_id"],))
                if report and report.get("explanation"):
                    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div style="background:rgba(0,212,255,0.04);border:1px solid rgba(0,212,255,0.1);
                                border-radius:10px;padding:14px;">
                        <div style="color:#00D4FF;font-size:0.72rem;font-weight:600;letter-spacing:0.08em;
                                    text-transform:uppercase;margin-bottom:8px;">Decision Explanation</div>
                        <div style="color:#8899BB;font-size:0.85rem;line-height:1.6;">{report['explanation']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

                btn1, btn2, btn3 = st.columns([1, 1, 2])
                if t["state"] in ["Draft", "Rejected", "Evaluated"] and t["decision"] in ["Pending", "Rejected", "Needs Revision"]:
                    with btn1:
                        if st.button("Submit for Review", key=f"submit_{t['task_id']}"):
                            old_state = t["state"]
                            db_exec("UPDATE automation_tasks SET state='Submitted', updated_date=? WHERE task_id=?",
                                    (datetime.now(), t["task_id"]))
                            log_action(t["task_id"], "Task Submitted", user["user_id"], "Submitted for governance evaluation")
                            record_transition(t["task_id"], old_state, "Submitted", user["user_id"])
                            st.success("Task submitted for evaluation.")
                            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

def render_evaluate():
    user = st.session_state.user
    st.markdown(page_header("Evaluate Tasks",
        "Perform governance evaluation, risk scoring, and static analysis.",
        "SecureIntent / Evaluate Tasks"), unsafe_allow_html=True)

    st.markdown('<div style="padding:0 32px;">', unsafe_allow_html=True)

    tasks = db_fetch("""
        SELECT t.*, u.full_name as owner_name
        FROM automation_tasks t
        LEFT JOIN users u ON t.owner_id = u.user_id
        WHERE t.state = 'Submitted'
        ORDER BY t.updated_date DESC
    """)

    if not tasks:
        st.markdown(card("""
        <div style="text-align:center;padding:40px;">
            <div style="font-size:2.5rem;margin-bottom:12px;opacity:0.3;">◎</div>
            <div style="color:#8899BB;font-size:0.95rem;">No tasks pending evaluation.</div>
        </div>
        """, padding="0px"), unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background:rgba(0,212,255,0.05);border:1px solid rgba(0,212,255,0.15);
                    border-radius:10px;padding:12px 16px;margin-bottom:20px;display:flex;align-items:center;gap:12px;">
            <div style="width:8px;height:8px;background:#00D4FF;border-radius:50%;
                        box-shadow:0 0 8px #00D4FF;"></div>
            <div style="color:#8899BB;font-size:0.85rem;">
                <span style="color:#00D4FF;font-weight:600;">{len(tasks)}</span> task(s) awaiting governance evaluation
            </div>
        </div>
        """, unsafe_allow_html=True)

        active_rules = db_fetch("SELECT * FROM governance_rules WHERE is_active=1")

        for t in tasks:
            scripts = db_fetch("SELECT * FROM scripts WHERE task_id=?", (t["task_id"],))
            priv_color = "#FF4C6A" if t["privilege_level"] == "Admin" else \
                         "#FFB84C" if t["privilege_level"] == "Elevated" else "#00E5A0"

            task_html = f"""
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px;">
                <div>
                    <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:600;color:#F0F4FF;">
                        {t['task_name']}
                        <span style="font-size:0.75rem;color:#445577;font-family:'JetBrains Mono',monospace;
                                     font-weight:400;margin-left:10px;">#{t['task_id']}</span>
                    </div>
                    <div style="color:#8899BB;font-size:0.82rem;margin-top:4px;">
                        Owner: <span style="color:#F0F4FF;">{t['owner_name'] or 'Unassigned'}</span>
                        &nbsp;·&nbsp; Privilege: <span style="color:{priv_color};">{t['privilege_level']}</span>
                        &nbsp;·&nbsp; Window: <span style="color:#7B61FF;">{t['timing_window']}</span>
                    </div>
                </div>
                {status_badge(t['state'])}
            </div>
            <div style="color:#8899BB;font-size:0.85rem;margin-bottom:12px;">
                <strong style="color:#F0F4FF;">Intent:</strong> {t['intent']}</div>
            <div style="color:#8899BB;font-size:0.85rem;">
                <strong style="color:#F0F4FF;">Purpose:</strong> {t['business_purpose']}</div>
            """
            st.markdown(card(task_html, padding="20px"), unsafe_allow_html=True)

            all_findings = []
            all_details = []
            if scripts:
                for sc in scripts:
                    findings, details = StaticAnalyzer.analyze(sc["script_content"])
                    all_findings.extend(findings)
                    all_details.extend(details)

            score, violations = RiskEngine.calculate(t, all_findings, active_rules)
            decision = RiskEngine.get_decision(score)

            dec_color = "#00E5A0" if decision == "Approved" else \
                        "#FF4C6A" if decision == "Rejected" else "#FFB84C"

            preview_cols = st.columns(4)
            with preview_cols[0]:
                st.markdown(f"""
                <div style="background:linear-gradient(145deg,#0D1321,#0A111E);
                            border:1px solid #1A2540;border-radius:12px;padding:16px;text-align:center;">
                    <div style="color:#8899BB;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">Risk Score</div>
                    <div style="color:{dec_color};font-family:'Syne',sans-serif;font-size:2rem;font-weight:700;">{score}</div>
                </div>""", unsafe_allow_html=True)
            with preview_cols[1]:
                st.markdown(f"""
                <div style="background:linear-gradient(145deg,#0D1321,#0A111E);
                            border:1px solid #1A2540;border-radius:12px;padding:16px;text-align:center;">
                    <div style="color:#8899BB;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">Decision</div>
                    <div style="margin-top:4px;">{status_badge(decision)}</div>
                </div>""", unsafe_allow_html=True)
            with preview_cols[2]:
                st.markdown(f"""
                <div style="background:linear-gradient(145deg,#0D1321,#0A111E);
                            border:1px solid #1A2540;border-radius:12px;padding:16px;text-align:center;">
                    <div style="color:#8899BB;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">Script Issues</div>
                    <div style="color:#FFB84C;font-family:'Syne',sans-serif;font-size:2rem;font-weight:700;">{len(all_findings)}</div>
                </div>""", unsafe_allow_html=True)
            with preview_cols[3]:
                st.markdown(f"""
                <div style="background:linear-gradient(145deg,#0D1321,#0A111E);
                            border:1px solid #1A2540;border-radius:12px;padding:16px;text-align:center;">
                    <div style="color:#8899BB;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">Violations</div>
                    <div style="color:#FF4C6A;font-family:'Syne',sans-serif;font-size:2rem;font-weight:700;">{len(violations)}</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

            if violations or all_details:
                viol_html = ""
                for v in violations:
                    viol_html += f"""<div style="display:flex;gap:8px;align-items:flex-start;margin-bottom:8px;">
                        <div style="color:#FF4C6A;font-size:0.7rem;margin-top:3px;">▸</div>
                        <div style="color:#8899BB;font-size:0.82rem;">{v}</div>
                    </div>"""
                for d in all_details:
                    viol_html += f"""<div style="display:flex;gap:8px;align-items:flex-start;margin-bottom:8px;">
                        <div style="color:#FFB84C;font-size:0.7rem;margin-top:3px;">▸</div>
                        <div style="color:#8899BB;font-size:0.82rem;">{d}</div>
                    </div>"""
                exp_content = f"""
                <div style="color:#00D4FF;font-size:0.72rem;font-weight:600;letter-spacing:0.08em;
                            text-transform:uppercase;margin-bottom:12px;">Analysis Details</div>
                {viol_html}
                """
                st.markdown(card(exp_content, padding="16px", border_color="#243050"), unsafe_allow_html=True)

            btn_c1, btn_c2, _ = st.columns([1, 1, 2])
            with btn_c1:
                if st.button(f"Confirm & Submit Decision", key=f"eval_{t['task_id']}"):
                    explanation = f"Task evaluated with risk score {score}/100. Decision: {decision}. "
                    if violations:
                        explanation += "Policy violations: " + "; ".join(violations[:3]) + ". "
                    if all_details:
                        explanation += "Script issues: " + "; ".join(all_details[:3]) + "."

                    report_id = db_exec("""INSERT INTO evaluation_reports
                        (task_id,risk_score,decision,explanation,violations,static_findings,evaluated_by)
                        VALUES(?,?,?,?,?,?,?)""",
                        (t["task_id"], score, decision, explanation,
                         json.dumps(violations), json.dumps(all_details), user["user_id"]))

                    old_state = t["state"]
                    db_exec("""UPDATE automation_tasks
                        SET state='Evaluated', risk_score=?, decision=?, updated_date=?
                        WHERE task_id=?""",
                        (score, decision, datetime.now(), t["task_id"]))

                    log_action(t["task_id"], "Task Evaluated", user["user_id"],
                               f"Decision: {decision}, Risk: {score}")
                    record_transition(t["task_id"], "Submitted", "Evaluated", user["user_id"],
                                     f"Governance decision: {decision}")
                    st.success(f"Task #{t['task_id']} evaluated. Decision: **{decision}** (Score: {score})")
                    st.rerun()

            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

def render_risk_analysis():
    user = st.session_state.user
    st.markdown(page_header("Risk Analysis",
        "Compare risk scores across tasks and identify high-risk automation.",
        "SecureIntent / Risk Analysis"), unsafe_allow_html=True)

    st.markdown('<div style="padding:0 32px;">', unsafe_allow_html=True)

    tasks = db_fetch("""
        SELECT t.*, u.full_name as owner_name
        FROM automation_tasks t
        LEFT JOIN users u ON t.owner_id = u.user_id
        WHERE t.risk_score > 0
        ORDER BY t.risk_score DESC
    """)

    if not tasks:
        st.info("No evaluated tasks available for risk analysis.")
    else:
        avg = sum(t["risk_score"] for t in tasks) / len(tasks)
        high_risk = [t for t in tasks if t["risk_score"] >= 60]
        med_risk = [t for t in tasks if 30 <= t["risk_score"] < 60]
        low_risk = [t for t in tasks if t["risk_score"] < 30]

        rc = st.columns(4)
        with rc[0]:
            st.markdown(metric_card("Total Evaluated", len(tasks), color="#00D4FF", icon="◫"), unsafe_allow_html=True)
        with rc[1]:
            st.markdown(metric_card("High Risk", len(high_risk), color="#FF4C6A", icon="◬"), unsafe_allow_html=True)
        with rc[2]:
            st.markdown(metric_card("Medium Risk", len(med_risk), color="#FFB84C", icon="◑"), unsafe_allow_html=True)
        with rc[3]:
            st.markdown(metric_card("Average Score", f"{avg:.1f}", color="#7B61FF", icon="◈"), unsafe_allow_html=True)

        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

        bar_html = section_header("Risk Score Distribution", "Visual comparison across all evaluated tasks")
        max_score = max(t["risk_score"] for t in tasks) or 1
        bar_html += '<div style="display:flex;flex-direction:column;gap:10px;">'
        for t in tasks:
            bar_pct = (t["risk_score"] / max_score) * 100
            bar_color = "#FF4C6A" if t["risk_score"] >= 60 else \
                        "#FFB84C" if t["risk_score"] >= 30 else "#00E5A0"
            bar_html += f"""
            <div style="display:flex;align-items:center;gap:12px;">
                <div style="width:180px;color:#8899BB;font-size:0.8rem;white-space:nowrap;
                            overflow:hidden;text-overflow:ellipsis;">{t['task_name'][:24]}</div>
                <div style="flex:1;height:28px;background:#1A2540;border-radius:6px;overflow:hidden;position:relative;">
                    <div style="width:{bar_pct:.1f}%;height:100%;
                                background:linear-gradient(90deg,{bar_color}88,{bar_color});
                                border-radius:6px;transition:width 0.5s;
                                display:flex;align-items:center;padding-left:10px;">
                    </div>
                    <div style="position:absolute;right:10px;top:50%;transform:translateY(-50%);
                                color:{bar_color};font-size:0.78rem;font-weight:600;
                                font-family:'JetBrains Mono',monospace;">{t['risk_score']:.0f}</div>
                </div>
                <div style="width:90px;text-align:right;">{status_badge(t['decision'])}</div>
            </div>
            """
        bar_html += "</div>"
        st.markdown(card(bar_html, padding="24px"), unsafe_allow_html=True)

        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

        hm_cols = st.columns([1, 1])
        with hm_cols[0]:
            priv_dist = {}
            for t in tasks:
                p = t["privilege_level"]
                priv_dist[p] = priv_dist.get(p, 0) + 1
            priv_html = section_header("By Privilege Level", "Risk distribution by privilege")
            for p, cnt in priv_dist.items():
                pc = "#FF4C6A" if p == "Admin" else "#FFB84C" if p == "Elevated" else "#00E5A0"
                avg_p = sum(t["risk_score"] for t in tasks if t["privilege_level"] == p) / cnt
                priv_html += f"""
                <div style="background:rgba(13,19,33,0.8);border:1px solid #1A2540;border-radius:10px;
                            padding:14px 16px;margin-bottom:8px;display:flex;align-items:center;gap:16px;">
                    <div style="width:10px;height:10px;background:{pc};border-radius:50%;
                                box-shadow:0 0 8px {pc}77;flex-shrink:0;"></div>
                    <div style="flex:1;">
                        <div style="color:#F0F4FF;font-size:0.88rem;font-weight:500;">{p}</div>
                        <div style="color:#445577;font-size:0.72rem;">{cnt} task(s)</div>
                    </div>
                    <div style="color:{pc};font-family:'Syne',sans-serif;font-weight:700;font-size:1.2rem;">{avg_p:.0f}</div>
                    <div style="color:#445577;font-size:0.7rem;">avg</div>
                </div>
                """
            st.markdown(card(priv_html, padding="20px"), unsafe_allow_html=True)

        with hm_cols[1]:
            timing_dist = {}
            for t in tasks:
                w = t["timing_window"]
                timing_dist[w] = timing_dist.get(w, 0) + 1
            timing_html = section_header("By Execution Window", "Risk pattern by timing")
            for w, cnt in timing_dist.items():
                wc = "#FF4C6A" if w == "Night" else "#FFB84C" if w == "Weekend" else "#00E5A0"
                avg_w = sum(t["risk_score"] for t in tasks if t["timing_window"] == w) / cnt
                timing_html += f"""
                <div style="background:rgba(13,19,33,0.8);border:1px solid #1A2540;border-radius:10px;
                            padding:14px 16px;margin-bottom:8px;display:flex;align-items:center;gap:16px;">
                    <div style="width:10px;height:10px;background:{wc};border-radius:50%;
                                box-shadow:0 0 8px {wc}77;flex-shrink:0;"></div>
                    <div style="flex:1;">
                        <div style="color:#F0F4FF;font-size:0.88rem;font-weight:500;">{w}</div>
                        <div style="color:#445577;font-size:0.72rem;">{cnt} task(s)</div>
                    </div>
                    <div style="color:{wc};font-family:'Syne',sans-serif;font-weight:700;font-size:1.2rem;">{avg_w:.0f}</div>
                    <div style="color:#445577;font-size:0.7rem;">avg</div>
                </div>
                """
            st.markdown(card(timing_html, padding="20px"), unsafe_allow_html=True)

        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

        threshold_input = st.number_input("Policy Impact Threshold (identify tasks above this score)",
                                           min_value=0, max_value=100, value=50, step=5)
        impacted = [t for t in tasks if t["risk_score"] >= threshold_input]
        if impacted:
            imp_html = f"""
            <div style="color:#FFB84C;font-size:0.72rem;font-weight:600;letter-spacing:0.08em;
                        text-transform:uppercase;margin-bottom:14px;">
                {len(impacted)} task(s) at or above threshold {threshold_input}</div>
            """
            for t in impacted:
                imp_html += f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                            padding:10px 0;border-bottom:1px solid #1A2540;">
                    <div style="color:#F0F4FF;font-size:0.88rem;">{t['task_name']}</div>
                    <div style="display:flex;gap:10px;align-items:center;">
                        {status_badge(t['decision'])}
                        <span style="color:#FF4C6A;font-family:'JetBrains Mono',monospace;
                                     font-size:0.85rem;font-weight:600;">{t['risk_score']:.0f}</span>
                    </div>
                </div>
                """
            st.markdown(card(section_header("Policy-Impacted Tasks") + imp_html, padding="20px"), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

def render_governance_rules():
    user = st.session_state.user
    st.markdown(page_header("Governance Rules",
        "Configure, enable, disable and manage governance policies.",
        "SecureIntent / Governance Rules"), unsafe_allow_html=True)

    st.markdown('<div style="padding:0 32px;">', unsafe_allow_html=True)

    tab_view, tab_add = st.tabs(["Active Rules", "Add New Rule"])

    with tab_view:
        rules = db_fetch("SELECT * FROM governance_rules ORDER BY is_active DESC, weight DESC")
        type_colors = {
            "Privilege": "#FF4C6A", "Timing": "#FFB84C", "Script": "#7B61FF",
            "Dependency": "#00D4FF", "Ownership": "#00E5A0", "Resource": "#FFB84C"
        }
        for r in rules:
            tc = type_colors.get(r["rule_type"], "#8899BB")
            active_label = status_badge("Approved") if r["is_active"] else status_badge("Rejected")
            active_label = active_label.replace("Approved", "Active").replace("Rejected", "Inactive")

            rule_html = f"""
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">
                <div style="display:flex;align-items:center;gap:12px;">
                    <div style="width:36px;height:36px;background:{tc}11;border:1px solid {tc}33;
                                border-radius:8px;display:flex;align-items:center;justify-content:center;">
                        <div style="width:8px;height:8px;background:{tc};border-radius:50%;"></div>
                    </div>
                    <div>
                        <div style="font-family:'Syne',sans-serif;font-size:0.95rem;
                                    font-weight:600;color:#F0F4FF;">{r['rule_name']}</div>
                        <div style="color:#445577;font-size:0.72rem;margin-top:2px;">
                            <span style="color:{tc};font-weight:600;">{r['rule_type']}</span>
                            &nbsp;·&nbsp; Weight: <span style="color:#FFB84C;">{r['weight']} pts</span>
                            &nbsp;·&nbsp; ID #{r['rule_id']}
                        </div>
                    </div>
                </div>
                <div style="display:flex;align-items:center;gap:10px;">
                    {active_label}
                </div>
            </div>
            <div style="color:#8899BB;font-size:0.82rem;margin-left:48px;">{r['rule_definition']}</div>
            """
            st.markdown(card(rule_html, padding="16px",
                            border_color=f"{tc}33" if r["is_active"] else "#1A2540"), unsafe_allow_html=True)

            btn_c1, btn_c2, _ = st.columns([1, 1, 3])
            with btn_c1:
                toggle_label = "Disable Rule" if r["is_active"] else "Enable Rule"
                if st.button(toggle_label, key=f"toggle_rule_{r['rule_id']}"):
                    new_val = 0 if r["is_active"] else 1
                    db_exec("UPDATE governance_rules SET is_active=? WHERE rule_id=?", (new_val, r["rule_id"]))
                    log_action(None, "Rule Updated", user["user_id"],
                               f"Rule '{r['rule_name']}' {'disabled' if r['is_active'] else 'enabled'}")
                    st.rerun()
            with btn_c2:
                if st.button("Edit Weight", key=f"edit_rule_{r['rule_id']}"):
                    st.session_state[f"editing_rule_{r['rule_id']}"] = True

            if st.session_state.get(f"editing_rule_{r['rule_id']}"):
                new_weight = st.number_input(f"New weight for '{r['rule_name']}'",
                                              min_value=1, max_value=100, value=r["weight"],
                                              key=f"wt_{r['rule_id']}")
                if st.button("Save Weight", key=f"save_wt_{r['rule_id']}"):
                    db_exec("UPDATE governance_rules SET weight=? WHERE rule_id=?", (new_weight, r["rule_id"]))
                    log_action(None, "Rule Weight Changed", user["user_id"],
                               f"Rule '{r['rule_name']}' weight changed to {new_weight}")
                    st.session_state[f"editing_rule_{r['rule_id']}"] = False
                    st.rerun()

            st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

    with tab_add:
        st.markdown(section_header("Create New Governance Rule"), unsafe_allow_html=True)
        with st.form("add_rule_form"):
            rn = st.text_input("Rule Name *", placeholder="e.g. Network Access Restriction")
            rt = st.selectbox("Rule Type *", ["Privilege", "Timing", "Script", "Dependency", "Ownership", "Resource", "Other"])
            rd = st.text_area("Rule Definition *", placeholder="Describe what this rule enforces...", height=90)
            rw = st.slider("Rule Weight (risk points added on violation)", 1, 50, 15)
            ra = st.checkbox("Active immediately", value=True)
            sub = st.form_submit_button("Create Rule")
            if sub:
                if not rn.strip() or not rd.strip():
                    st.error("Rule Name and Definition required.")
                else:
                    db_exec("INSERT INTO governance_rules (rule_name,rule_type,rule_definition,weight,is_active) VALUES(?,?,?,?,?)",
                            (rn.strip(), rt, rd.strip(), rw, 1 if ra else 0))
                    log_action(None, "Rule Created", user["user_id"], f"New rule: {rn}")
                    st.success(f"Rule '**{rn}**' created successfully.")
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

def render_policy_impact():
    user = st.session_state.user
    st.markdown(page_header("Policy Impact Analysis",
        "Identify automation tasks affected by governance rule changes.",
        "SecureIntent / Policy Impact"), unsafe_allow_html=True)

    st.markdown('<div style="padding:0 32px;">', unsafe_allow_html=True)

    rules = db_fetch("SELECT * FROM governance_rules ORDER BY rule_name")
    rule_options = {r["rule_name"]: r for r in rules}

    selected_rule_name = st.selectbox("Select a governance rule to analyze impact",
                                       list(rule_options.keys()))

    if selected_rule_name:
        rule = rule_options[selected_rule_name]
        active_rules = db_fetch("SELECT * FROM governance_rules WHERE is_active=1")
        all_tasks = db_fetch("""
            SELECT t.*, u.full_name as owner_name FROM automation_tasks t
            LEFT JOIN users u ON t.owner_id = u.user_id
            WHERE t.state = 'Evaluated'
        """)

        impacted = []
        for t in all_tasks:
            scripts = db_fetch("SELECT * FROM scripts WHERE task_id=?", (t["task_id"],))
            all_findings = []
            for sc in scripts:
                findings, _ = StaticAnalyzer.analyze(sc["script_content"])
                all_findings.extend(findings)
            score, violations = RiskEngine.calculate(t, all_findings, active_rules)

            hit = False
            if rule["rule_type"] == "Privilege" and t["privilege_level"] in ["Admin", "Elevated"]:
                hit = True
            elif rule["rule_type"] == "Timing" and t["timing_window"] in ["Night", "Weekend"]:
                hit = True
            elif rule["rule_type"] == "Script" and len(all_findings) > 0:
                hit = True
            elif rule["rule_type"] == "Resource" and t["resource_limit"] == "High":
                hit = True
            elif rule["rule_type"] == "Dependency":
                deps = db_fetch("SELECT * FROM task_dependencies WHERE task_id=?", (t["task_id"],))
                if len(deps) > 0:
                    hit = True
            if hit:
                impacted.append((t, score, violations))

        st.markdown(f"""
        <div style="background:rgba(255,184,76,0.05);border:1px solid rgba(255,184,76,0.2);
                    border-radius:10px;padding:16px;margin:16px 0;">
            <div style="display:flex;align-items:center;gap:12px;">
                <div style="width:8px;height:8px;background:#FFB84C;border-radius:50%;
                            box-shadow:0 0 8px #FFB84C77;"></div>
                <div>
                    <div style="color:#FFB84C;font-size:0.9rem;font-weight:600;">
                        {len(impacted)} task(s) impacted by "{selected_rule_name}"</div>
                    <div style="color:#8899BB;font-size:0.78rem;margin-top:2px;">
                        Rule Type: {rule['rule_type']} &nbsp;·&nbsp; Weight: {rule['weight']} pts
                        &nbsp;·&nbsp; Status: {'Active' if rule['is_active'] else 'Inactive'}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if impacted:
            for t, score, violations in impacted:
                dec_color = "#00E5A0" if t["decision"] == "Approved" else \
                            "#FF4C6A" if t["decision"] == "Rejected" else "#FFB84C"
                impact_html = f"""
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                    <div>
                        <div style="font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:600;color:#F0F4FF;">
                            {t['task_name']}</div>
                        <div style="color:#445577;font-size:0.72rem;margin-top:2px;">
                            Owner: {t['owner_name'] or 'Unassigned'} · Privilege: {t['privilege_level']}</div>
                    </div>
                    <div style="display:flex;gap:10px;align-items:center;">
                        {status_badge(t['decision'])}
                        <span style="color:{dec_color};font-family:'JetBrains Mono',monospace;
                                     font-weight:700;font-size:0.9rem;">{score:.0f}</span>
                    </div>
                </div>
                """
                st.markdown(card(impact_html, padding="16px",
                                border_color="rgba(255,184,76,0.2)"), unsafe_allow_html=True)
        else:
            st.info("No evaluated tasks are directly impacted by this rule.")

    st.markdown("</div>", unsafe_allow_html=True)

def render_audit_logs():
    user = st.session_state.user
    st.markdown(page_header("Audit Logs",
        "Complete audit trail of all governance actions and decisions.",
        "SecureIntent / Audit Logs"), unsafe_allow_html=True)

    st.markdown('<div style="padding:0 32px;">', unsafe_allow_html=True)

    tab_logs, tab_transitions, tab_export = st.tabs(["Action Logs", "State Transitions", "Export Records"])

    with tab_logs:
        logs = db_fetch("""
            SELECT l.*, u.full_name as actor_name, t.task_name
            FROM audit_logs l
            LEFT JOIN users u ON l.action_by = u.user_id
            LEFT JOIN automation_tasks t ON l.task_id = t.task_id
            ORDER BY l.action_time DESC LIMIT 100
        """)

        if not logs:
            st.info("No audit records found.")
        else:
            action_colors = {
                "Login": "#7B61FF", "Task Created": "#00D4FF",
                "Task Submitted": "#FFB84C", "Task Evaluated": "#00E5A0",
                "Rule Updated": "#FF4C6A", "Rule Created": "#00D4FF",
                "User Added": "#7B61FF", "Rule Weight Changed": "#FFB84C",
            }
            log_html = section_header("System Audit Trail", f"{len(logs)} most recent records")
            log_html += '<div style="display:flex;flex-direction:column;gap:6px;">'
            for lg in logs:
                ac = action_colors.get(lg["action_type"], "#8899BB")
                task_ref = f"Task: {lg['task_name']}" if lg.get("task_name") else "System Action"
                log_html += f"""
                <div style="display:flex;align-items:center;gap:14px;padding:10px 14px;
                            background:rgba(13,19,33,0.6);border:1px solid #1A2540;border-radius:8px;">
                    <div style="width:8px;height:8px;background:{ac};border-radius:50%;
                                box-shadow:0 0 6px {ac}77;flex-shrink:0;"></div>
                    <div style="flex:1;">
                        <div style="display:flex;gap:10px;align-items:center;">
                            <span style="color:{ac};font-size:0.8rem;font-weight:600;">{lg['action_type']}</span>
                            <span style="color:#445577;font-size:0.72rem;">{task_ref}</span>
                        </div>
                        <div style="color:#8899BB;font-size:0.75rem;margin-top:2px;">{lg.get('remarks','')}</div>
                    </div>
                    <div style="text-align:right;flex-shrink:0;">
                        <div style="color:#F0F4FF;font-size:0.78rem;">{lg.get('actor_name','System')}</div>
                        <div style="color:#445577;font-size:0.68rem;font-family:'JetBrains Mono',monospace;">
                            {str(lg['action_time'])[:16]}</div>
                    </div>
                </div>
                """
            log_html += "</div>"
            st.markdown(card(log_html, padding="20px"), unsafe_allow_html=True)

    with tab_transitions:
        transitions = db_fetch("""
            SELECT st.*, u.full_name as actor_name, t.task_name
            FROM state_transitions st
            LEFT JOIN users u ON st.transitioned_by = u.user_id
            LEFT JOIN automation_tasks t ON st.task_id = t.task_id
            ORDER BY st.transition_time DESC LIMIT 50
        """)
        if not transitions:
            st.info("No state transitions recorded yet.")
        else:
            tr_html = section_header("Task State Transition History", "Complete lifecycle tracking")
            tr_html += '<div style="position:relative;">'
            for i, tr in enumerate(transitions):
                from_c = "#445577"
                to_c = "#00E5A0" if tr["to_state"] in ["Evaluated", "Approved"] else \
                       "#FF4C6A" if tr["to_state"] == "Rejected" else \
                       "#00D4FF" if tr["to_state"] == "Submitted" else "#7B61FF"
                tr_html += f"""
                <div style="display:flex;gap:14px;margin-bottom:12px;align-items:flex-start;">
                    <div style="display:flex;flex-direction:column;align-items:center;flex-shrink:0;">
                        <div style="width:10px;height:10px;background:{to_c};border-radius:50%;
                                    box-shadow:0 0 8px {to_c}77;"></div>
                        {'<div style="width:1px;flex:1;background:#1A2540;margin:4px 0;min-height:24px;"></div>' if i < len(transitions)-1 else ''}
                    </div>
                    <div style="flex:1;padding-bottom:6px;">
                        <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
                            <span style="color:#F0F4FF;font-size:0.88rem;font-weight:500;">
                                {tr.get('task_name','N/A')}</span>
                            <span style="color:{from_c};font-size:0.75rem;">
                                {tr['from_state']} →</span>
                            <span style="color:{to_c};font-size:0.75rem;font-weight:600;">
                                {tr['to_state']}</span>
                        </div>
                        <div style="color:#445577;font-size:0.72rem;margin-top:3px;">
                            By: {tr.get('actor_name','System')} ·
                            {str(tr['transition_time'])[:16]}
                            {' · ' + tr['notes'] if tr.get('notes') else ''}
                        </div>
                    </div>
                </div>
                """
            tr_html += "</div>"
            st.markdown(card(tr_html, padding="20px"), unsafe_allow_html=True)

    with tab_export:
        st.markdown(section_header("Export Audit Records", "Download audit data as CSV for compliance reporting"), unsafe_allow_html=True)
        logs_all = db_fetch("""
            SELECT l.audit_id, l.action_type, l.remarks, l.action_time,
                   u.full_name as actor, t.task_name
            FROM audit_logs l
            LEFT JOIN users u ON l.action_by = u.user_id
            LEFT JOIN automation_tasks t ON l.task_id = t.task_id
            ORDER BY l.action_time DESC
        """)
        if logs_all:
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=["audit_id", "action_type", "actor", "task_name", "remarks", "action_time"])
            writer.writeheader()
            writer.writerows(logs_all)
            st.download_button("Download Audit Log CSV", output.getvalue(),
                               file_name=f"secureintent_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                               mime="text/csv")

        reports_all = db_fetch("""
            SELECT r.report_id, r.risk_score, r.decision, r.explanation, r.evaluated_date,
                   t.task_name, u.full_name as evaluator
            FROM evaluation_reports r
            LEFT JOIN automation_tasks t ON r.task_id = t.task_id
            LEFT JOIN users u ON r.evaluated_by = u.user_id
            ORDER BY r.evaluated_date DESC
        """)
        if reports_all:
            out2 = io.StringIO()
            w2 = csv.DictWriter(out2, fieldnames=["report_id", "task_name", "risk_score", "decision",
                                                    "evaluator", "evaluated_date", "explanation"])
            w2.writeheader()
            w2.writerows(reports_all)
            st.download_button("Download Evaluation Reports CSV", out2.getvalue(),
                               file_name=f"secureintent_reports_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                               mime="text/csv")

    st.markdown("</div>", unsafe_allow_html=True)

def render_reports():
    user = st.session_state.user
    st.markdown(page_header("Reports & Analytics",
        "Governance summaries, risk trends and compliance reporting.",
        "SecureIntent / Reports"), unsafe_allow_html=True)

    st.markdown('<div style="padding:0 32px;">', unsafe_allow_html=True)

    all_tasks = db_fetch("""
        SELECT t.*, u.full_name as owner_name FROM automation_tasks t
        LEFT JOIN users u ON t.owner_id = u.user_id
    """)
    evaluated = [t for t in all_tasks if t["risk_score"] > 0]
    all_reports = db_fetch("""
        SELECT r.*, t.task_name, t.privilege_level, t.timing_window, u.full_name as owner_name
        FROM evaluation_reports r
        LEFT JOIN automation_tasks t ON r.task_id = t.task_id
        LEFT JOIN users u ON t.owner_id = u.user_id
        ORDER BY r.evaluated_date DESC
    """)

    rc = st.columns(4)
    metrics = [
        ("Total Evaluations", len(all_reports), "#00D4FF", "◎"),
        ("Compliance Rate", f"{(sum(1 for t in evaluated if t['decision']=='Approved')/max(len(evaluated),1)*100):.0f}%", "#00E5A0", "◈"),
        ("Avg Risk Score", f"{(sum(t['risk_score'] for t in evaluated)/max(len(evaluated),1)):.1f}", "#FFB84C", "◬"),
        ("Active Authors", db_fetchone("SELECT COUNT(DISTINCT owner_id) as cnt FROM automation_tasks")["cnt"], "#7B61FF", "◑"),
    ]
    for i, (label, val, color, icon) in enumerate(metrics):
        with rc[i]:
            st.markdown(metric_card(label, val, icon=icon, color=color), unsafe_allow_html=True)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        violator_html = section_header("Repeated Policy Violators", "Authors with multiple high-risk tasks")
        author_violations = defaultdict(list)
        for t in evaluated:
            if t["decision"] in ["Rejected", "Needs Revision"]:
                author_violations[t["owner_name"] or "Unknown"].append(t)
        sorted_violators = sorted(author_violations.items(), key=lambda x: len(x[1]), reverse=True)
        if sorted_violators:
            for author, tasks_list in sorted_violators[:5]:
                vcount = len(tasks_list)
                vc = "#FF4C6A" if vcount >= 3 else "#FFB84C" if vcount >= 2 else "#8899BB"
                violator_html += f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                            padding:10px 0;border-bottom:1px solid #1A2540;">
                    <div>
                        <div style="color:#F0F4FF;font-size:0.88rem;">{author}</div>
                        <div style="color:#445577;font-size:0.72rem;">
                            {', '.join([t['task_name'][:20] for t in tasks_list[:2]])}
                            {'...' if len(tasks_list) > 2 else ''}</div>
                    </div>
                    <div style="background:{vc}11;border:1px solid {vc}33;border-radius:6px;
                                padding:3px 10px;color:{vc};font-size:0.82rem;font-weight:700;">
                        {vcount} violations</div>
                </div>
                """
        else:
            violator_html += '<div style="color:#445577;text-align:center;padding:20px;">No violations detected.</div>'
        st.markdown(card(violator_html, padding="20px"), unsafe_allow_html=True)

    with col_b:
        risk_trend_html = section_header("Risk Score Trend", "Recent evaluations by score")
        recent_evals = all_reports[:10]
        if recent_evals:
            max_score = max(r["risk_score"] for r in recent_evals) or 1
            risk_trend_html += '<div style="display:flex;flex-direction:column;gap:8px;">'
            for r in recent_evals:
                bar_w = (r["risk_score"] / max_score) * 100
                dc = "#00E5A0" if r["decision"] == "Approved" else \
                     "#FF4C6A" if r["decision"] == "Rejected" else "#FFB84C"
                risk_trend_html += f"""
                <div style="display:flex;align-items:center;gap:10px;">
                    <div style="width:120px;color:#8899BB;font-size:0.75rem;overflow:hidden;
                                text-overflow:ellipsis;white-space:nowrap;">{r['task_name'][:16]}</div>
                    <div style="flex:1;height:6px;background:#1A2540;border-radius:3px;overflow:hidden;">
                        <div style="width:{bar_w:.1f}%;height:100%;background:{dc};border-radius:3px;"></div>
                    </div>
                    <div style="color:{dc};font-size:0.75rem;font-weight:600;
                                font-family:'JetBrains Mono',monospace;width:28px;">{r['risk_score']:.0f}</div>
                </div>
                """
            risk_trend_html += "</div>"
        else:
            risk_trend_html += '<div style="color:#445577;text-align:center;padding:20px;">No evaluation data.</div>'
        st.markdown(card(risk_trend_html, padding="20px"), unsafe_allow_html=True)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    st.markdown(section_header("Full Evaluation Report Table"), unsafe_allow_html=True)
    if all_reports:
        table_html = """
        <div style="overflow-x:auto;">
        <table style="width:100%;border-collapse:collapse;font-size:0.82rem;">
            <thead>
                <tr style="border-bottom:2px solid #1A2540;">
                    <th style="padding:10px 12px;text-align:left;color:#445577;
                               font-size:0.68rem;letter-spacing:0.08em;text-transform:uppercase;">Task</th>
                    <th style="padding:10px 12px;text-align:left;color:#445577;
                               font-size:0.68rem;letter-spacing:0.08em;text-transform:uppercase;">Owner</th>
                    <th style="padding:10px 12px;text-align:center;color:#445577;
                               font-size:0.68rem;letter-spacing:0.08em;text-transform:uppercase;">Risk</th>
                    <th style="padding:10px 12px;text-align:center;color:#445577;
                               font-size:0.68rem;letter-spacing:0.08em;text-transform:uppercase;">Decision</th>
                    <th style="padding:10px 12px;text-align:left;color:#445577;
                               font-size:0.68rem;letter-spacing:0.08em;text-transform:uppercase;">Privilege</th>
                    <th style="padding:10px 12px;text-align:left;color:#445577;
                               font-size:0.68rem;letter-spacing:0.08em;text-transform:uppercase;">Evaluated</th>
                </tr>
            </thead>
            <tbody>
        """
        for r in all_reports[:20]:
            dc = "#00E5A0" if r["decision"] == "Approved" else \
                 "#FF4C6A" if r["decision"] == "Rejected" else "#FFB84C"
            pc = "#FF4C6A" if r.get("privilege_level") == "Admin" else \
                 "#FFB84C" if r.get("privilege_level") == "Elevated" else "#8899BB"
            table_html += f"""
            <tr style="border-bottom:1px solid #1A2540;transition:background 0.15s;">
                <td style="padding:10px 12px;color:#F0F4FF;font-weight:500;">{r['task_name']}</td>
                <td style="padding:10px 12px;color:#8899BB;">{r.get('owner_name','N/A')}</td>
                <td style="padding:10px 12px;text-align:center;color:{dc};font-weight:700;
                           font-family:'JetBrains Mono',monospace;">{r['risk_score']:.0f}</td>
                <td style="padding:10px 12px;text-align:center;">{status_badge(r['decision'])}</td>
                <td style="padding:10px 12px;color:{pc};">{r.get('privilege_level','N/A')}</td>
                <td style="padding:10px 12px;color:#445577;font-family:'JetBrains Mono',monospace;
                           font-size:0.72rem;">{str(r['evaluated_date'])[:16]}</td>
            </tr>
            """
        table_html += "</tbody></table></div>"
        st.markdown(card(table_html, padding="16px"), unsafe_allow_html=True)
    else:
        st.info("No evaluation reports available.")

    st.markdown("</div>", unsafe_allow_html=True)

def render_all_tasks_admin():
    user = st.session_state.user
    st.markdown(page_header("All Automation Tasks",
        "Complete system-wide view of all tasks and governance outcomes.",
        "SecureIntent / All Tasks"), unsafe_allow_html=True)

    st.markdown('<div style="padding:0 32px;">', unsafe_allow_html=True)

    tasks = db_fetch("""
        SELECT t.*, u.full_name as owner_name
        FROM automation_tasks t
        LEFT JOIN users u ON t.owner_id = u.user_id
        ORDER BY t.updated_date DESC
    """)

    fc1, fc2 = st.columns([1, 2])
    with fc1:
        dec_filter = st.selectbox("Filter by Decision", ["All", "Approved", "Rejected", "Needs Revision", "Pending"])
    with fc2:
        search = st.text_input("Search tasks", placeholder="Search by task name or intent...")

    filtered = tasks
    if dec_filter != "All":
        filtered = [t for t in filtered if t["decision"] == dec_filter]
    if search.strip():
        s = search.strip().lower()
        filtered = [t for t in filtered if s in t["task_name"].lower() or s in t["intent"].lower()]

    for t in filtered:
        dec_color = "#00E5A0" if t["decision"] == "Approved" else \
                    "#FF4C6A" if t["decision"] == "Rejected" else \
                    "#FFB84C" if t["decision"] == "Needs Revision" else "#7B61FF"
        task_html = f"""
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">
            <div>
                <div style="font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:600;color:#F0F4FF;">
                    {t['task_name']}
                    <span style="color:#445577;font-size:0.72rem;font-family:'JetBrains Mono',monospace;
                                 font-weight:400;margin-left:8px;">#{t['task_id']}</span>
                </div>
                <div style="color:#445577;font-size:0.72rem;margin-top:2px;">
                    Owner: <span style="color:#8899BB;">{t['owner_name'] or 'Unassigned'}</span>
                    &nbsp;·&nbsp; {t['privilege_level']} &nbsp;·&nbsp; {t['timing_window']}
                    &nbsp;·&nbsp; Created: {str(t['created_date'])[:10]}
                </div>
            </div>
            <div style="display:flex;gap:8px;align-items:center;">
                {status_badge(t['state'])}
                {status_badge(t['decision'])}
                <span style="color:{dec_color};font-family:'JetBrains Mono',monospace;
                             font-weight:700;font-size:0.9rem;">{t['risk_score']:.0f}</span>
            </div>
        </div>
        <div style="height:2px;background:#1A2540;border-radius:1px;overflow:hidden;">
            <div style="width:{min(t['risk_score'],100):.0f}%;height:100%;background:{dec_color};border-radius:1px;"></div>
        </div>
        """
        st.markdown(card(task_html, padding="16px",
                        border_color=f"{dec_color}22"), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="SecureIntent — Governance Platform",
        page_icon="◈",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    init_db()
    inject_css()

    if "user" not in st.session_state:
        st.session_state.user = None
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"

    if st.session_state.user is None:
        render_login_register()
        return

    user = st.session_state.user
    role = user["role"]

    st.markdown(top_navbar(user["full_name"], role), unsafe_allow_html=True)

    nav_items = get_nav_items(role)
    nav_labels = {item["page"]: item["label"] for item in nav_items}

    nav_col, main_col = st.columns([1, 5])

    with nav_col:
        st.markdown(f"""
        <div style="background:rgba(8,12,20,0.8);border-right:1px solid #1A2540;
                    padding:20px 12px;min-height:calc(100vh - 65px);backdrop-filter:blur(20px);">
            <div style="color:#445577;font-size:0.62rem;letter-spacing:0.15em;text-transform:uppercase;
                        margin-bottom:16px;padding:0 4px;font-family:'JetBrains Mono',monospace;">Navigation</div>
        """, unsafe_allow_html=True)

        for item in nav_items:
            is_active = item["page"] == st.session_state.page
            if is_active:
                btn_style = "background:linear-gradient(135deg,rgba(0,212,255,0.12),rgba(123,97,255,0.08));border-color:rgba(0,212,255,0.25);color:#00D4FF;"
            else:
                btn_style = ""
            if st.button(f"{item['icon']}  {item['label']}", key=f"nav_{item['page']}",
                         use_container_width=True):
                st.session_state.page = item["page"]
                st.rerun()

        if role == "Admin":
            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
            st.markdown("""<div style="color:#445577;font-size:0.62rem;letter-spacing:0.15em;
                            text-transform:uppercase;padding:0 4px;margin-bottom:8px;
                            font-family:'JetBrains Mono',monospace;">Admin</div>""", unsafe_allow_html=True)
            if st.button("⊞  All Tasks", key="nav_all_tasks", use_container_width=True):
                st.session_state.page = "all_tasks"
                st.rerun()
            if st.button("◐  Manage Users", key="nav_users", use_container_width=True):
                st.session_state.page = "manage_users"
                st.rerun()

        st.markdown("<div style='height:auto;flex:1;'></div>", unsafe_allow_html=True)
        st.markdown("""<div style="height:1px;background:linear-gradient(90deg,transparent,#1A2540,transparent);
                        margin:20px 0 12px;"></div>""", unsafe_allow_html=True)

        if st.button("⟵  Sign Out", key="nav_logout", use_container_width=True):
            log_action(None, "Logout", user["user_id"], "User signed out")
            st.session_state.user = None
            st.session_state.page = "dashboard"
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with main_col:
        page = st.session_state.page
        if page == "dashboard":
            render_dashboard()
        elif page == "create_task":
            render_create_task()
        elif page == "my_tasks":
            render_my_tasks()
        elif page == "evaluate":
            render_evaluate()
        elif page == "risk_analysis":
            render_risk_analysis()
        elif page == "governance_rules":
            render_governance_rules()
        elif page == "policy_impact":
            render_policy_impact()
        elif page == "audit_logs":
            render_audit_logs()
        elif page == "reports":
            render_reports()
        elif page == "all_tasks":
            render_all_tasks_admin()
        elif page == "manage_users":
            render_manage_users()
        else:
            render_dashboard()

def render_manage_users():
    user = st.session_state.user
    st.markdown(page_header("Manage Users",
        "View all platform users and manage access.",
        "SecureIntent / Manage Users"), unsafe_allow_html=True)

    st.markdown('<div style="padding:0 32px;">', unsafe_allow_html=True)

    users = db_fetch("SELECT user_id,full_name,username,role,status,created_at FROM users ORDER BY created_at DESC")

    role_colors = {"Admin": "#FFB84C", "Analyst": "#7B61FF", "Author": "#00D4FF", "Auditor": "#00E5A0"}

    users_html = section_header("Platform Users", f"{len(users)} registered accounts")
    users_html += '<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;font-size:0.85rem;">'
    users_html += """<thead><tr style="border-bottom:2px solid #1A2540;">
        <th style="padding:10px 12px;text-align:left;color:#445577;font-size:0.68rem;
                   letter-spacing:0.08em;text-transform:uppercase;">Name</th>
        <th style="padding:10px 12px;text-align:left;color:#445577;font-size:0.68rem;
                   letter-spacing:0.08em;text-transform:uppercase;">Username</th>
        <th style="padding:10px 12px;text-align:center;color:#445577;font-size:0.68rem;
                   letter-spacing:0.08em;text-transform:uppercase;">Role</th>
        <th style="padding:10px 12px;text-align:center;color:#445577;font-size:0.68rem;
                   letter-spacing:0.08em;text-transform:uppercase;">Status</th>
        <th style="padding:10px 12px;text-align:left;color:#445577;font-size:0.68rem;
                   letter-spacing:0.08em;text-transform:uppercase;">Joined</th>
    </tr></thead><tbody>"""

    for u in users:
        rc = role_colors.get(u["role"], "#8899BB")
        sc = "#00E5A0" if u["status"] == "Active" else "#FF4C6A"
        users_html += f"""
        <tr style="border-bottom:1px solid #1A2540;">
            <td style="padding:12px;color:#F0F4FF;font-weight:500;">{u['full_name']}</td>
            <td style="padding:12px;color:#8899BB;font-family:'JetBrains Mono',monospace;
                       font-size:0.8rem;">@{u['username']}</td>
            <td style="padding:12px;text-align:center;">
                <span style="background:{rc}11;color:{rc};border:1px solid {rc}33;
                             padding:3px 10px;border-radius:20px;font-size:0.72rem;font-weight:600;">
                    {u['role']}</span></td>
            <td style="padding:12px;text-align:center;">
                <span style="color:{sc};font-size:0.8rem;font-weight:600;">{u['status']}</span></td>
            <td style="padding:12px;color:#445577;font-size:0.75rem;
                       font-family:'JetBrains Mono',monospace;">{str(u['created_at'])[:10]}</td>
        </tr>
        """
    users_html += "</tbody></table></div>"
    st.markdown(card(users_html, padding="20px"), unsafe_allow_html=True)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    st.markdown(section_header("Add New User"), unsafe_allow_html=True)
    with st.form("admin_add_user"):
        fn = st.text_input("Full Name *")
        un = st.text_input("Username *")
        pw = st.text_input("Password *", type="password")
        rl = st.selectbox("Role *", ["Author", "Analyst", "Admin", "Auditor"])
        sub = st.form_submit_button("Create User")
        if sub:
            if not all([fn, un, pw]):
                st.error("All fields required.")
            else:
                ok, msg = register_user(fn, un, pw, rl)
                if ok:
                    log_action(None, "User Added", user["user_id"], f"Admin created user {un} as {rl}")
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()