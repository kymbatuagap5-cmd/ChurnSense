import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import plotly.graph_objects as go
from streamlit_extras.stylable_container import stylable_container

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------
# Professional SVG icon system (Lucide-style)
# -------------------------------------------------
ICONS = {
    "logo": "<path d='M3 3v18h18'/><path d='M18 17V9'/><path d='M13 17V5'/><path d='M8 17v-3'/>",
    "home": "<path d='M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z'/><polyline points='9 22 9 12 15 12 15 22'/>",
    "target": "<circle cx='12' cy='12' r='10'/><circle cx='12' cy='12' r='6'/><circle cx='12' cy='12' r='2'/>",
    "trend": "<polyline points='22 7 13.5 15.5 8.5 10.5 2 17'/><polyline points='16 7 22 7 22 13'/>",
    "clock": "<circle cx='12' cy='12' r='10'/><polyline points='12 6 12 12 16 14'/>",
    "cpu": "<rect x='4' y='4' width='16' height='16' rx='2'/><rect x='9' y='9' width='6' height='6'/><path d='M9 2v2M15 2v2M9 20v2M15 20v2M2 9h2M2 15h2M20 9h2M20 15h2'/>",
    "info": "<circle cx='12' cy='12' r='10'/><line x1='12' y1='16' x2='12' y2='12'/><line x1='12' y1='8' x2='12.01' y2='8'/>",
    "user": "<path d='M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2'/><circle cx='12' cy='7' r='4'/>",
    "users": "<path d='M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2'/><circle cx='9' cy='7' r='4'/><path d='M23 21v-2a4 4 0 0 0-3-3.87'/><path d='M16 3.13a4 4 0 0 1 0 7.75'/>",
    "calendar": "<rect x='3' y='4' width='18' height='18' rx='2'/><line x1='16' y1='2' x2='16' y2='6'/><line x1='8' y1='2' x2='8' y2='6'/><line x1='3' y1='10' x2='21' y2='10'/>",
    "refresh": "<path d='M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8'/><path d='M21 3v5h-5'/><path d='M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16'/><path d='M8 16H3v5'/>",
    "headphones": "<path d='M3 14h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a9 9 0 0 1 18 0v7a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3'/>",
    "card": "<rect x='1' y='4' width='22' height='16' rx='2'/><line x1='1' y1='10' x2='23' y2='10'/>",
    "dollar": "<line x1='12' y1='1' x2='12' y2='23'/><path d='M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6'/>",
    "file": "<path d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'/><polyline points='14 2 14 8 20 8'/><line x1='16' y1='13' x2='8' y2='13'/><line x1='16' y1='17' x2='8' y2='17'/>",
    "layers": "<polygon points='12 2 2 7 12 12 22 7 12 2'/><polyline points='2 17 12 22 22 17'/><polyline points='2 12 12 17 22 12'/>",
    "alert": "<path d='M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z'/><line x1='12' y1='9' x2='12' y2='12'/><line x1='12' y1='16' x2='12.01' y2='16'/>",
    "phone": "<path d='M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z'/>",
    "gift": "<polyline points='20 12 20 22 4 22 4 12'/><rect x='2' y='7' width='20' height='5'/><line x1='12' y1='22' x2='12' y2='7'/><path d='M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z'/><path d='M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z'/>",
    "clipboard": "<path d='M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2'/><rect x='8' y='2' width='8' height='4' rx='1'/>",
    "activity": "<polyline points='22 12 18 12 15 21 9 3 6 12 2 12'/>",
    "pie": "<path d='M21.21 15.89A10 10 0 1 1 8 2.83'/><path d='M22 12A10 10 0 0 0 12 2v10z'/>",
    "usercheck": "<path d='M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2'/><circle cx='9' cy='7' r='4'/><polyline points='16 11 18 13 22 9'/>",
    "userx": "<path d='M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2'/><circle cx='9' cy='7' r='4'/><line x1='17' y1='8' x2='22' y2='13'/><line x1='22' y1='8' x2='17' y2='13'/>",
    "shield": "<path d='M12 22s8-4 8-10V5l-8-3-8 3v11c0 6 8 10 8 10z'/><polyline points='9 12 11 14 15 10'/>",
    "award": "<circle cx='12' cy='8' r='7'/><polyline points='8.21 13.89 7 23 12 20 17 23 15.79 13.88'/>",
    "zap": "<polygon points='13 2 3 14 12 14 11 22 21 10 12 10 13 2'/>",
    "wave": "<path d='M18 11V6a2 2 0 0 0-2-2a2 2 0 0 0-2 2'/><path d='M14 10V4a2 2 0 0 0-2-2a2 2 0 0 0-2 2v2'/><path d='M10 10.5V6a2 2 0 0 0-2-2a2 2 0 0 0-2 2v8'/><path d='M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15'/>",
    "checks": "<path d='m3 17 2 2 4-4'/><path d='m3 7 2 2 4-4'/><path d='M13 6h8'/><path d='M13 12h8'/><path d='M13 18h8'/>",
}

def icn(name, size=16):
    return (
        f"<svg class='icn' width='{size}' height='{size}' viewBox='0 0 24 24' "
        f"fill='none' stroke='currentColor' stroke-width='2' "
        f"stroke-linecap='round' stroke-linejoin='round'>{ICONS[name]}</svg>"
    )

# -------------------------------------------------
# Global CSS — dark purple dashboard theme
# -------------------------------------------------
st.markdown("""
<style>
/* ============ BASE ============ */
html, body, .stApp{
    background: radial-gradient(circle at top left, #2b0b57 0%, #170a33 45%, #0d0620 100%) !important;
    color:#fff;
}
#MainMenu, footer{ visibility:hidden; }
div[data-testid="stSidebarCollapsedControl"]{ visibility:visible !important; }
section[data-testid="stSidebar"] button[kind="header"]{ display:none; }
p, span, label{ color:#c9bdf2; }
h1,h2,h3,h4{ color:#fff !important; }
.stCaption, small{ color:#7f6fb2 !important; }
.icn{ flex-shrink:0; vertical-align:middle; }

/* ============ SIDEBAR ============ */
section[data-testid="stSidebar"]{
    background: linear-gradient(180deg, #200a44 0%, #140724 60%, #0f051c 100%) !important;
    border-right:1px solid rgba(255,255,255,.06);
}

/* ============ INPUTS ============ */
label{ font-size:13px !important; color:#b9a9e8 !important; }
.stNumberInput input, .stTextInput input{
    background:#221240 !important;
    border:1px solid #3c2a6a !important;
    color:#fff !important;
    border-radius:12px !important;
    height:42px;
}
div[data-baseweb="select"] > div{
    background:#221240 !important;
    border:1px solid #3c2a6a !important;
    border-radius:12px !important;
}
div[data-baseweb="select"] span{ color:#fff !important; }

/* custom field labels (replace native labels inside customer card) */
div[data-testid-key="customer_card"] label{ display:none !important; }
.f-label{ display:flex; align-items:center; gap:8px; font-size:13px; font-weight:600;
    color:#b9a9e8; margin:2px 0 6px 2px; }
.f-label .icn{ color:#8b5cf6; }

/* ============ BUTTONS ============ */
.stButton > button{
    width:100%; height:52px; border:none; border-radius:14px;
    background:linear-gradient(90deg,#7b2ff7 0%,#c437f5 55%,#f107a3 100%);
    color:#fff; font-size:16px; font-weight:700; transition:all .3s ease;
}
.stButton > button:hover{
    transform:translateY(-2px);
    box-shadow:0 10px 30px rgba(196,55,245,.45);
}
/* Hide native Streamlit widget labels */
div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label{
    display:none !important;
}
div[data-testid-key="predict_btn"] button{
    background-image:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20width='18'%20height='18'%20viewBox='0%200%2024%2024'%20fill='none'%20stroke='white'%20stroke-width='2'%20stroke-linecap='round'%20stroke-linejoin='round'%3E%3Cpath%20d='M13%202%203%2014h9l-1%208%2010-12h-9l1-8z'/%3E%3C/svg%3E"),
    linear-gradient(90deg,#7b2ff7 0%,#c437f5 55%,#f107a3 100%);
    background-repeat:no-repeat,no-repeat;
    background-position:left 26px center,center;
    background-size:18px 18px,cover;
}
div[data-testid-key="download_btn"] button,
div[data-testid-key="clear_btn"] button{
    height:46px; font-size:14px; border-radius:12px;
    background-color:#221240; border:1px solid #3c2a6a;
    background-repeat:no-repeat; background-position:left 16px center; background-size:16px 16px;
    box-shadow:none;
}
div[data-testid-key="download_btn"] button{
    background-image:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20width='16'%20height='16'%20viewBox='0%200%2024%2024'%20fill='none'%20stroke='%23a78bfa'%20stroke-width='2'%20stroke-linecap='round'%20stroke-linejoin='round'%3E%3Cpath%20d='M21%2015v4a2%202%200%200%201-2%202H5a2%202%200%200%201-2-2v-4'/%3E%3Cpolyline%20points='7%2010%2012%2015%2017%2010'/%3E%3Cline%20x1='12'%20y1='15'%20x2='12'%20y2='3'/%3E%3C/svg%3E");
}
div[data-testid-key="clear_btn"] button{
    background-image:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20width='16'%20height='16'%20viewBox='0%200%2024%2024'%20fill='none'%20stroke='%23ff5c86'%20stroke-width='2'%20stroke-linecap='round'%20stroke-linejoin='round'%3E%3Cpolyline%20points='3%206%205%206%2021%206'/%3E%3Cpath%20d='M19%206v14a2%202%200%200%201-2%202H7a2%202%200%200%201-2-2V6h3a2%202%200%200%203-3h4a2%202%200%200%203%203z'/%3E%3C/svg%3E");
}

/* ============ MISC WIDGETS ============ */
details[data-testid="stExpander"]{
    background:#1b1038; border:1px solid rgba(255,255,255,.08); border-radius:16px;
}
div[data-testid="stAlert"]{ border-radius:16px; }

/* ============ SIDEBAR COMPONENTS ============ */
.sb-logo{ display:flex; align-items:center; gap:12px; padding:6px 4px 16px 4px; }
.sb-logo-icon{ width:44px;height:44px;border-radius:12px; color:#fff;
    background:linear-gradient(135deg,#7b2ff7,#f107a3);
    display:flex;align-items:center;justify-content:center; }
.sb-logo-title{ font-size:20px;font-weight:800;color:#fff; }
.sb-logo-sub{ font-size:11px;color:#9d8cc9; }

.sb-model{ background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.08);
    border-radius:14px; padding:12px 14px; margin-top:6px; }
.sb-model-row{ display:flex; justify-content:space-between; align-items:center;
    font-size:13px; color:#9d8cc9; padding:4px 0; }
.sb-model-row span{ display:flex; align-items:center; gap:8px; }
.sb-model-row .icn{ color:#8b5cf6; }
.sb-model-row b{ color:#fff; }
.sb-model-row b.green{ color:#22e58f; }

.sb-chart{ display:flex; align-items:flex-end; gap:8px; height:110px; padding:20px 6px 0 6px; }
.sb-chart .bar{ flex:1; border-radius:6px 6px 0 0;
    background:linear-gradient(180deg,#8b5cf6,#4c1d95); opacity:.9; }
.sb-chart .bar.pink{ background:linear-gradient(180deg,#f472b6,#a21caf); }
.sb-footer{ margin-top:18px; font-size:11px; color:#7f6fb2; text-align:center; }

/* ============ HEADER ============ */
.page-head h1{ margin:0; font-size:30px; font-weight:800; color:#fff; }
.page-head p{ margin:4px 0 0 0; color:#9d8cc9; font-size:14px; }
.head-right{ display:flex; align-items:center; justify-content:flex-end; gap:10px; margin-top:8px; }
.badge-ready{ display:inline-flex; align-items:center; gap:8px;
    background:rgba(34,229,143,.12); border:1px solid rgba(34,229,143,.35);
    color:#22e58f; padding:8px 14px; border-radius:999px; font-size:13px; font-weight:700; }
.badge-ready .dot{ width:8px;height:8px;border-radius:50%;background:#22e58f; box-shadow:0 0 8px #22e58f; }
.avatar{ width:40px;height:40px;border-radius:50%; color:#fff;
    background:linear-gradient(135deg,#7b2ff7,#f107a3);
    display:inline-flex;align-items:center;justify-content:center; }

/* ============ CARDS ============ */
.card-title{ display:flex; align-items:center; gap:10px; font-size:16px; font-weight:700;
    color:#fff; margin-bottom:14px; }
.card-title .ico{ width:28px;height:28px;border-radius:8px;background:rgba(139,92,246,.2);
    color:#a78bfa; display:flex;align-items:center;justify-content:center; }

/* ============ PREDICTION RESULT ============ */
.pred-wrap{ text-align:center; padding:8px 0 4px 0; }
.pred-glow{ width:86px;height:86px;border-radius:50%;margin:0 auto 12px auto;
    display:flex;align-items:center;justify-content:center; }
.pred-glow.churn{ background:rgba(255,46,99,.12); border:2px solid rgba(255,46,99,.6);
    box-shadow:0 0 35px rgba(255,46,99,.45); color:#ff5c86; }
.pred-glow.safe{ background:rgba(34,229,143,.12); border:2px solid rgba(34,229,143,.55);
    box-shadow:0 0 35px rgba(34,229,143,.4); color:#22e58f; }
.pred-glow.idle{ background:rgba(139,92,246,.12); border:2px solid rgba(139,92,246,.5);
    box-shadow:0 0 30px rgba(139,92,246,.35); color:#a78bfa; }
.pred-title{ font-size:24px; font-weight:800; margin:0 0 4px 0; }
.pred-title.churn{ color:#ff2e63; }
.pred-title.safe{ color:#22e58f; }
.pred-title.idle{ color:#a78bfa; font-size:20px; }
.pred-sub{ color:#9d8cc9; font-size:13px; margin:0; }

.action-head{ font-size:14px; font-weight:700; color:#fff; margin:16px 0 10px 0; }
.action-list{ display:flex; flex-direction:column; gap:9px; }
.action-item{ display:flex; align-items:center; gap:10px; background:rgba(255,255,255,.04);
    border:1px solid rgba(255,255,255,.07); padding:9px 12px; border-radius:12px;
    color:#d5c9f7; font-size:13.5px; }
.action-item .ai-ico{ width:30px;height:30px;border-radius:9px;display:flex;
    align-items:center;justify-content:center; }
.ai-ico.purple{ background:rgba(139,92,246,.18); color:#a78bfa; }
.ai-ico.pink{ background:rgba(255,46,99,.16); color:#ff5c86; }
.ai-ico.blue{ background:rgba(59,130,246,.16); color:#60a5fa; }
.ai-ico.orange{ background:rgba(245,158,11,.16); color:#fbbf24; }

/* ============ RISK PILLS ============ */
div[data-testid="stVerticalBlockBorderWrapper"]{
    overflow:hidden;
    max-width:100%;
}
.risk-strip{
    display:flex;
    flex-direction:column;
    align-items:flex-start;
    gap:12px;
    width:100%;
    min-width:0;
}
.risk-strip .card-title{ margin-bottom:0; }
.pill-row{
    display:flex;
    flex-wrap:wrap;
    gap:10px;
    align-items:center;
    min-width:0;
    max-width:100%;
}
.pill{ max-width:100%; }
.pill{ display:inline-flex; align-items:center; gap:8px; padding:8px 14px; border-radius:12px;
    font-size:13px; font-weight:700; }
.pill.red{ background:rgba(255,46,99,.14); border:1px solid rgba(255,46,99,.4); color:#ff5c86; }
.pill.orange{ background:rgba(245,158,11,.14); border:1px solid rgba(245,158,11,.4); color:#fbbf24; }
.pill.green{ background:rgba(34,229,143,.14); border:1px solid rgba(34,229,143,.4); color:#22e58f; }
.pill.gray{ background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.12); color:#b6a7e6; }

/* ============ METRIC CARDS ============ */
.metric-grid{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; }
.metric-card{ background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.07);
    border-radius:14px; padding:14px; }
.metric-card .m-ico{ width:36px;height:36px;border-radius:10px;display:flex;
    align-items:center;justify-content:center;margin-bottom:10px; }
.m-ico.purple{ background:rgba(139,92,246,.2); color:#a78bfa; }
.m-ico.pink{ background:rgba(255,46,99,.18); color:#ff5c86; }
.m-ico.green{ background:rgba(34,229,143,.16); color:#22e58f; }
.m-ico.orange{ background:rgba(245,158,11,.18); color:#fbbf24; }
.metric-card .m-value{ font-size:22px; font-weight:800; color:#fff; }
.metric-card .m-label{ font-size:11.5px; color:#9d8cc9; margin-top:2px; }

/* ============ LEGEND / CHART ============ */
.legend{ display:flex; flex-direction:column; gap:10px; justify-content:center; }
.legend-item{ display:flex; align-items:center; gap:8px; font-size:12.5px; color:#d5c9f7; }
.legend-item b{ color:#fff; }
.legend-item .sq{ width:10px;height:10px;border-radius:3px; }
.sq.pink{ background:#ff2e63; }
.sq.teal{ background:#00d1b2; }

/* ============ HISTORY TABLE ============ */
.hist-wrap{ max-height:260px; overflow:auto; border-radius:12px;
    border:1px solid rgba(255,255,255,.08); }
.hist-table{ width:100%; border-collapse:collapse; font-size:12.5px; }
.hist-table th{ position:sticky; top:0; background:#241540; color:#cfc3f5;
    padding:10px 12px; text-align:left; font-weight:700; }
.hist-table td{ padding:9px 12px; color:#e6def8; border-top:1px solid rgba(255,255,255,.05); }
.hist-table tr:nth-child(even) td{ background:rgba(255,255,255,.02); }
.td-dot{ width:8px;height:8px;border-radius:50%;display:inline-block;margin-right:8px; }
.td-dot.pink{ background:#ff2e63; }
.td-dot.teal{ background:#00d1b2; }

.empty{ color:#8d7cc0; font-size:13px; }
.html-card{
    background: rgba(26,14,51,.85);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 12px 32px rgba(0,0,0,.35);
    max-width: 100%;
}

/* keep the expand arrow visible, just in case */
div[data-testid="stSidebarCollapsedControl"]{
    visibility:visible !important;
}
.page-head h1 .icn{ color:#fbbf24; margin-left:8px; vertical-align:-4px; }
.action-head{ display:flex; align-items:center; gap:8px; }
.action-head .icn{ color:#a78bfa; }
</style>
""", unsafe_allow_html=True)

CARD_CSS = """
{
    background: rgba(26,14,51,.85);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 12px 32px rgba(0,0,0,.35);
}
"""
# -------------------------------------------------
# Load trained model
# -------------------------------------------------
@st.cache_resource
def load_model():
    return joblib.load("models/churn_model.pkl")

model = load_model()

# -------------------------------------------------
# Session state
# -------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
st.sidebar.markdown(f"""
<div class="sb-logo">
    <div class="sb-logo-icon">{icn('logo', 22)}</div>
    <div>
        <div class="sb-logo-title">ChurnSense</div>
        <div class="sb-logo-sub">AI-Powered Churn Prediction</div>
    </div>
</div>
""", unsafe_allow_html=True)
st.write("")
PAGES = [
    "Dashboard",
    "Predict Customer",
    "Analytics",
    "History",
    "Model Info",
    "About Us",
]

page = st.sidebar.radio(
    "Navigation",
    PAGES,
    key="nav_menu",
    label_visibility="collapsed",
)

page = page.strip()

st.sidebar.markdown(f"""
<div class="sb-model">
    <div class="sb-model-row"><span>{icn('cpu', 14)} Model</span><b>Decision Tree</b></div>
    <div class="sb-model-row"><span>{icn('award', 14)} Accuracy</span><b class="green">99.97%</b></div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown('''
<div class="sb-chart">
    <div class="bar" style="height:35%"></div>
    <div class="bar pink" style="height:60%"></div>
    <div class="bar" style="height:45%"></div>
    <div class="bar pink" style="height:80%"></div>
    <div class="bar" style="height:55%"></div>
    <div class="bar pink" style="height:95%"></div>
</div>
<div class="sb-footer">© 2026 StarTrio</div>
''', unsafe_allow_html=True)

# -------------------------------------------------
# Header (always visible)
# -------------------------------------------------
header1, header2 = st.columns([6, 1])
with header1:
    st.markdown(f"""
    <div class="page-head">
        <h1>Welcome back! {icn('wave', 28)}</h1>
        <p>Predict customer churn and take action to retain your valuable customers.</p>
    </div>
    """, unsafe_allow_html=True)
with header2:
    st.markdown(f"""
    <div class="head-right">
        <span class="badge-ready"><span class="dot"></span> Model Ready</span>
        <span class="avatar">{icn('user', 18)}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =================================================
# PAGES
# =================================================

if page == "Dashboard":
    # ---------- Customer form + Prediction result ----------
    left_panel, right_panel = st.columns([2, 1], gap="medium")
    with left_panel:
        with stylable_container(key="customer_card", css_styles=CARD_CSS):
            st.markdown(f"""
            <div class="card-title"><span class="ico">{icn('user', 15)}</span>Customer Information</div>
            """, unsafe_allow_html=True)
            st.write("")
            left, right = st.columns(2)
            with left:
                st.markdown(f"<div class='f-label'>{icn('user', 15)}<span>Age</span></div>", unsafe_allow_html=True)
                age = st.number_input("Age", min_value=18, max_value=100, value=30, step=1)
                st.markdown(f"<div class='f-label'>{icn('calendar', 15)}<span>Tenure</span></div>", unsafe_allow_html=True)
                tenure = st.number_input("Tenure", min_value=0, max_value=100, value=10, step=1)
                st.markdown(f"<div class='f-label'>{icn('refresh', 15)}<span>Usage Frequency</span></div>", unsafe_allow_html=True)
                usage_frequency = st.number_input("Usage Frequency", min_value=0, max_value=50, value=10, step=1)
                st.markdown(f"<div class='f-label'>{icn('headphones', 15)}<span>Support Calls</span></div>", unsafe_allow_html=True)
                support_calls = st.number_input("Support Calls", min_value=0, max_value=20, value=2, step=1)
                st.markdown(f"<div class='f-label'>{icn('card', 15)}<span>Payment Delay</span></div>", unsafe_allow_html=True)
                payment_delay = st.number_input("Payment Delay", min_value=0, max_value=100, value=5, step=1)
            with right:
                st.markdown(f"<div class='f-label'>{icn('users', 15)}<span>Gender</span></div>", unsafe_allow_html=True)
                gender = st.selectbox("Gender", ["Male", "Female"])
                st.markdown(f"<div class='f-label'>{icn('layers', 15)}<span>Subscription Type</span></div>", unsafe_allow_html=True)
                subscription_type = st.selectbox("Subscription Type", ["Basic", "Standard", "Premium"])
                st.markdown(f"<div class='f-label'>{icn('file', 15)}<span>Contract Length</span></div>", unsafe_allow_html=True)
                contract_length = st.selectbox("Contract Length", ["Monthly", "Quarterly", "Annual"])
                st.markdown(f"<div class='f-label'>{icn('dollar', 15)}<span>Total Spend ($)</span></div>", unsafe_allow_html=True)
                total_spend = st.number_input("Total Spend ($)", min_value=0.0, value=500.0)
                st.markdown(f"<div class='f-label'>{icn('clock', 15)}<span>Last Interaction (days)</span></div>", unsafe_allow_html=True)
                last_interaction = st.number_input("Last Interaction (days)", min_value=0, max_value=100, value=10)
            st.write("")
            predict_button = st.button("Predict Customer", use_container_width=True, key="predict_btn")
    input_data = pd.DataFrame({
            "Age": [age],
            "Tenure": [tenure],
            "Usage Frequency": [usage_frequency],
            "Support Calls": [support_calls],
            "Payment Delay": [payment_delay],
            "Total Spend": [total_spend],
            "Last Interaction": [last_interaction],
            "Gender_Male": [1 if gender == "Male" else 0],
            "Subscription Type_Premium": [1 if subscription_type == "Premium" else 0],
            "Subscription Type_Standard": [1 if subscription_type == "Standard" else 0],
            "Contract Length_Monthly": [1 if contract_length == "Monthly" else 0],
            "Contract Length_Quarterly": [1 if contract_length == "Quarterly" else 0]
    })
    if predict_button:
        prediction = int(model.predict(input_data)[0])
        prediction_text = "Likely to Churn" if prediction == 1 else "No Churn"
        reasons = []
        if support_calls >= 5:
            reasons.append(("phone", "High support calls", "red"))
        if payment_delay >= 10:
            reasons.append(("card", "Payment delays", "red"))
        if tenure <= 6:
            reasons.append(("calendar", "Short tenure", "orange"))
        if contract_length == "Monthly":
            reasons.append(("file", "Monthly contract", "red"))
        if total_spend < 300:
            reasons.append(("dollar", "Low total spending", "orange"))
        if usage_frequency <= 3:
            reasons.append(("activity", "Low usage", "orange"))
        st.session_state.last_result = {"prediction": prediction, "reasons": reasons}
        customer_record = {
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Prediction": prediction_text,
                "Age": age,
                "Gender": gender,
                "Subscription": subscription_type,
                "Contract": contract_length,
                "Support Calls": support_calls,
                "Payment Delay": payment_delay,
                "Total Spend": round(total_spend, 2),
                "Tenure": tenure,
                "Usage Frequency": usage_frequency,
        }
        st.session_state.history.append(customer_record)
        st.toast("Prediction added to history!")
    result = st.session_state.last_result
    with right_panel:
        with stylable_container(key="prediction_card", css_styles=CARD_CSS):
            st.markdown(f"""
            <div class="card-title"><span class="ico">{icn('target', 15)}</span>Prediction Result</div>
            """, unsafe_allow_html=True)
            st.write("")
            result = st.session_state.last_result
            if result is None:
                st.markdown(f"""
                <div class="pred-wrap">
                    <div class="pred-glow idle">{icn('user', 34)}</div>
                    <div class="pred-title idle">Awaiting Prediction</div>
                    <p class="pred-sub">Fill in the customer details and click Predict Customer.</p>
                </div>
                """, unsafe_allow_html=True)
            elif result["prediction"] == 1:
                st.markdown(f"""
                <div class="pred-wrap">
                    <div class="pred-glow churn">{icn('user', 34)}</div>
                    <div class="pred-title churn">Likely to Churn</div>
                    <p class="pred-sub">High Risk Customer</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="pred-wrap">
                    <div class="pred-glow safe">{icn('usercheck', 34)}</div>
                    <div class="pred-title safe">No Churn</div>
                    <p class="pred-sub">Loyal Customer</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown(f"<div class='action-head'>{icn('checks', 16)} Recommended Actions</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="action-list">
                <div class="action-item"><span class="ai-ico purple">{icn('phone', 15)}</span>Contact customer proactively</div>
                <div class="action-item"><span class="ai-ico pink">{icn('gift', 15)}</span>Offer retention incentives</div>
                <div class="action-item"><span class="ai-ico blue">{icn('clipboard', 15)}</span>Review support history</div>
                <div class="action-item"><span class="ai-ico orange">{icn('activity', 15)}</span>Monitor customer activity</div>
            </div>
            """, unsafe_allow_html=True)
            st.write("")

    # ---------- Run prediction ----------
    

    # ---------- Risk Indicators ----------
    st.write("")
    if result is None:
        pills_html = f"<span class='pill gray'>{icn('info', 14)} Run a prediction to see risk indicators</span>"
    elif result["reasons"]:
        pills_html = ""
        for icon_name, label, sev in result["reasons"]:
            pills_html += f"<span class='pill {sev}'>{icn(icon_name, 14)} {label}</span>"
    else:
        pills_html = f"<span class='pill green'>{icn('shield', 14)} No major risk indicators</span>"
    st.markdown(f"""
    <div class="html-card">
        <div class="risk-strip">
            <div class="card-title"><span class="ico">{icn('alert', 15)}</span>Risk Indicators</div>
            <div class="pill-row">{pills_html}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.write("")

    # ---------- Session Overview + Distribution ----------
    stats_left, stats_right = st.columns([2, 1], gap="medium")
    history_df = pd.DataFrame(st.session_state.history) if st.session_state.history else None
    if history_df is not None:
        total = len(history_df)
        churn_count = int((history_df["Prediction"] == "Likely to Churn").sum())
        safe_count = int((history_df["Prediction"] == "No Churn").sum())
        churn_rate = (churn_count / total) * 100 if total else 0.0
        safe_rate = 100.0 - churn_rate
    else:
        total = churn_count = safe_count = 0
        churn_rate = safe_rate = 0.0
    with stats_left:
        with stylable_container(key="statistics_card", css_styles=CARD_CSS):
            st.markdown(f"""
            <div class="card-title"><span class="ico">{icn('trend', 15)}</span>Session Overview</div>
            """, unsafe_allow_html=True)
            st.write("")
            if history_df is None:
                st.markdown("<p class='empty'>No predictions yet — make your first prediction to see analytics.</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="metric-grid">
                    <div class="metric-card">
                        <div class="m-ico purple">{icn('users', 17)}</div>
                        <div class="m-value">{total}</div>
                        <div class="m-label">Total Predictions</div>
                    </div>
                    <div class="metric-card">
                        <div class="m-ico pink">{icn('userx', 17)}</div>
                        <div class="m-value">{churn_count}</div>
                        <div class="m-label">Likely to Churn</div>
                    </div>
                    <div class="metric-card">
                        <div class="m-ico green">{icn('usercheck', 17)}</div>
                        <div class="m-value">{safe_count}</div>
                        <div class="m-label">No Churn</div>
                    </div>
                    <div class="metric-card">
                        <div class="m-ico orange">{icn('pie', 17)}</div>
                        <div class="m-value">{churn_rate:.0f}%</div>
                        <div class="m-label">Churn Rate</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.write("")
    with stats_right:
        with stylable_container(key="distribution_card", css_styles=CARD_CSS):
            st.markdown(f"""
            <div class="card-title"><span class="ico">{icn('pie', 15)}</span>Prediction Distribution</div>
            """, unsafe_allow_html=True)
            st.write("")
            if history_df is None:
                st.markdown("<p class='empty'>No data yet.</p>", unsafe_allow_html=True)
            else:
                chart_col, legend_col = st.columns([1.1, 1])
                with chart_col:
                    fig = go.Figure(go.Pie(
                        labels=["Likely to Churn", "No Churn"],
                        values=[churn_count, safe_count],
                        hole=0.62,
                        marker=dict(colors=["#ff2e63", "#00d1b2"]),
                        textinfo="none",
                        hoverinfo="label+value",
                    ))
                    fig.update_layout(
                        showlegend=False,
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=10, r=10, t=10, b=10),
                        height=210,
                    )
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                with legend_col:
                    st.markdown(f"""
                    <div class="legend">
                        <div class="legend-item"><span class="sq pink"></span>
                            Likely to Churn&nbsp;<b>{churn_rate:.0f}% ({churn_count})</b></div>
                        <div class="legend-item"><span class="sq teal"></span>
                            No Churn&nbsp;<b>{safe_rate:.0f}% ({safe_count})</b></div>
                    </div>
                    """, unsafe_allow_html=True)

    # ---------- History ----------
    st.write("")
    with stylable_container(key="history_card", css_styles=CARD_CSS):
        st.markdown(f"""
        <div class="card-title"><span class="ico">{icn('clock', 15)}</span>Customer Prediction History</div>
        """, unsafe_allow_html=True)
        st.write("")
        if history_df is None:
            st.info("Make your first prediction to view analytics and prediction history.")
        else:
            csv = history_df.to_csv(index=False).encode("utf-8")
            btn_left, spacer, btn_right = st.columns([0.5, 1, 0.5], gap="small")
            with btn_left:
                st.download_button(
                    label="Download History as CSV",
                    data=csv,
                    file_name="prediction_history.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="download_btn"
                )
            with btn_right:
                if st.button("Clear History", use_container_width=True, key="clear_btn"):
                    st.session_state.history = []
                    st.session_state.last_result = None
                    st.rerun()
            rows_html = ""
            for _, r in history_df.iterrows():
                dot = "pink" if r["Prediction"] == "Likely to Churn" else "teal"
                rows_html += (
                    f"<tr><td>{r['Time']}</td>"
                    f"<td><span class='td-dot {dot}'></span>{r['Prediction']}</td>"
                    f"<td>{r['Age']}</td><td>{r['Gender']}</td>"
                    f"<td>{r['Subscription']}</td><td>{r['Contract']}</td>"
                    f"<td>{r['Support Calls']}</td><td>{r['Payment Delay']}</td>"
                    f"<td>{r['Total Spend']}</td></tr>"
                )
            st.markdown(f"""
            <div class="hist-wrap">
                <table class="hist-table">
                    <thead>
                        <tr>
                            <th>Time</th><th>Prediction</th><th>Age</th><th>Gender</th>
                            <th>Subscription</th><th>Contract</th><th>Support Calls</th>
                            <th>Payment Delay</th><th>Total Spend</th>
                        </tr>
                    </thead>
                    <tbody>{rows_html}</tbody>
                </table>
            </div>
            """, unsafe_allow_html=True)
        st.write("")    
    st.write("")

elif page == "Predict Customer":
    # ---------- Customer form + Prediction result + Risk ----------
    left_panel, right_panel = st.columns([2, 1], gap="medium")
    with left_panel:
        with stylable_container(key="customer_card", css_styles=CARD_CSS):
            st.markdown(f"""
            <div class="card-title"><span class="ico">{icn('user', 15)}</span>Customer Information</div>
            """, unsafe_allow_html=True)
            st.write("")
            left, right = st.columns(2)
            with left:
                st.markdown(f"<div class='f-label'>{icn('user', 15)}<span>Age</span></div>", unsafe_allow_html=True)
                age = st.number_input("Age", min_value=18, max_value=100, value=30, step=1)
                st.markdown(f"<div class='f-label'>{icn('calendar', 15)}<span>Tenure</span></div>", unsafe_allow_html=True)
                tenure = st.number_input("Tenure", min_value=0, max_value=100, value=10, step=1)
                st.markdown(f"<div class='f-label'>{icn('refresh', 15)}<span>Usage Frequency</span></div>", unsafe_allow_html=True)
                usage_frequency = st.number_input("Usage Frequency", min_value=0, max_value=50, value=10, step=1)
                st.markdown(f"<div class='f-label'>{icn('headphones', 15)}<span>Support Calls</span></div>", unsafe_allow_html=True)
                support_calls = st.number_input("Support Calls", min_value=0, max_value=20, value=2, step=1)
                st.markdown(f"<div class='f-label'>{icn('card', 15)}<span>Payment Delay</span></div>", unsafe_allow_html=True)
                payment_delay = st.number_input("Payment Delay", min_value=0, max_value=100, value=5, step=1)
            with right:
                st.markdown(f"<div class='f-label'>{icn('users', 15)}<span>Gender</span></div>", unsafe_allow_html=True)
                gender = st.selectbox("Gender", ["Male", "Female"])
                st.markdown(f"<div class='f-label'>{icn('layers', 15)}<span>Subscription Type</span></div>", unsafe_allow_html=True)
                subscription_type = st.selectbox("Subscription Type", ["Basic", "Standard", "Premium"])
                st.markdown(f"<div class='f-label'>{icn('file', 15)}<span>Contract Length</span></div>", unsafe_allow_html=True)
                contract_length = st.selectbox("Contract Length", ["Monthly", "Quarterly", "Annual"])
                st.markdown(f"<div class='f-label'>{icn('dollar', 15)}<span>Total Spend ($)</span></div>", unsafe_allow_html=True)
                total_spend = st.number_input("Total Spend ($)", min_value=0.0, value=500.0)
                st.markdown(f"<div class='f-label'>{icn('clock', 15)}<span>Last Interaction (days)</span></div>", unsafe_allow_html=True)
                last_interaction = st.number_input("Last Interaction (days)", min_value=0, max_value=100, value=10)
            st.write("")
            predict_button = st.button("Predict Customer", use_container_width=True, key="predict_btn")
    with right_panel:
        with stylable_container(key="prediction_card", css_styles=CARD_CSS):
            st.markdown(f"""
            <div class="card-title"><span class="ico">{icn('target', 15)}</span>Prediction Result</div>
            """, unsafe_allow_html=True)
            st.write("")
            result = st.session_state.last_result
            if result is None:
                st.markdown(f"""
                <div class="pred-wrap">
                    <div class="pred-glow idle">{icn('user', 34)}</div>
                    <div class="pred-title idle">Awaiting Prediction</div>
                    <p class="pred-sub">Fill in the customer details and click Predict Customer.</p>
                </div>
                """, unsafe_allow_html=True)
            elif result["prediction"] == 1:
                st.markdown(f"""
                <div class="pred-wrap">
                    <div class="pred-glow churn">{icn('user', 34)}</div>
                    <div class="pred-title churn">Likely to Churn</div>
                    <p class="pred-sub">High Risk Customer</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="pred-wrap">
                    <div class="pred-glow safe">{icn('usercheck', 34)}</div>
                    <div class="pred-title safe">No Churn</div>
                    <p class="pred-sub">Loyal Customer</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<div class='action-head'>Recommended Actions</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="action-list">
                <div class="action-item"><span class="ai-ico purple">{icn('phone', 15)}</span>Contact customer proactively</div>
                <div class="action-item"><span class="ai-ico pink">{icn('gift', 15)}</span>Offer retention incentives</div>
                <div class="action-item"><span class="ai-ico blue">{icn('clipboard', 15)}</span>Review support history</div>
                <div class="action-item"><span class="ai-ico orange">{icn('activity', 15)}</span>Monitor customer activity</div>
            </div>
            """, unsafe_allow_html=True)
            st.write("")

    input_data = pd.DataFrame({
        "Age": [age],
        "Tenure": [tenure],
        "Usage Frequency": [usage_frequency],
        "Support Calls": [support_calls],
        "Payment Delay": [payment_delay],
        "Total Spend": [total_spend],
        "Last Interaction": [last_interaction],
        "Gender_Male": [1 if gender == "Male" else 0],
        "Subscription Type_Premium": [1 if subscription_type == "Premium" else 0],
        "Subscription Type_Standard": [1 if subscription_type == "Standard" else 0],
        "Contract Length_Monthly": [1 if contract_length == "Monthly" else 0],
        "Contract Length_Quarterly": [1 if contract_length == "Quarterly" else 0]
    })

    if predict_button:
        prediction = int(model.predict(input_data)[0])
        prediction_text = "Likely to Churn" if prediction == 1 else "No Churn"
        reasons = []
        if support_calls >= 5:
            reasons.append(("phone", "High support calls", "red"))
        if payment_delay >= 10:
            reasons.append(("card", "Payment delays", "red"))
        if tenure <= 6:
            reasons.append(("calendar", "Short tenure", "orange"))
        if contract_length == "Monthly":
            reasons.append(("file", "Monthly contract", "red"))
        if total_spend < 300:
            reasons.append(("dollar", "Low total spending", "orange"))
        if usage_frequency <= 3:
            reasons.append(("activity", "Low usage", "orange"))
        st.session_state.last_result = {"prediction": prediction, "reasons": reasons}
        customer_record = {
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Prediction": prediction_text,
            "Age": age,
            "Gender": gender,
            "Subscription": subscription_type,
            "Contract": contract_length,
            "Support Calls": support_calls,
            "Payment Delay": payment_delay,
            "Total Spend": round(total_spend, 2),
            "Tenure": tenure,
            "Usage Frequency": usage_frequency,
        }
        st.session_state.history.append(customer_record)
        st.toast("Prediction added to history!")
        result = st.session_state.last_result

    st.write("")
    if result is None:
        pills_html = f"<span class='pill gray'>{icn('info', 14)} Run a prediction to see risk indicators</span>"
    elif result["reasons"]:
        pills_html = ""
        for icon_name, label, sev in result["reasons"]:
            pills_html += f"<span class='pill {sev}'>{icn(icon_name, 14)} {label}</span>"
    else:
        pills_html = f"<span class='pill green'>{icn('shield', 14)} No major risk indicators</span>"
    st.markdown(f"""
    <div class="html-card">
        <div class="risk-strip">
            <div class="card-title"><span class="ico">{icn('alert', 15)}</span>Risk Indicators</div>
            <div class="pill-row">{pills_html}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")

elif page == "Analytics":
    stats_left, stats_right = st.columns([2, 1], gap="medium")
    history_df = pd.DataFrame(st.session_state.history) if st.session_state.history else None
    if history_df is not None:
        total = len(history_df)
        churn_count = int((history_df["Prediction"] == "Likely to Churn").sum())
        safe_count = int((history_df["Prediction"] == "No Churn").sum())
        churn_rate = (churn_count / total) * 100 if total else 0.0
        safe_rate = 100.0 - churn_rate
    else:
        total = churn_count = safe_count = 0
        churn_rate = safe_rate = 0.0
    with stats_left:
        with stylable_container(key="statistics_card", css_styles=CARD_CSS):
            st.markdown(f"""
            <div class="card-title"><span class="ico">{icn('trend', 15)}</span>Session Overview</div>
            """, unsafe_allow_html=True)
            st.write("")
            if history_df is None:
                st.markdown("<p class='empty'>No predictions yet — make your first prediction to see analytics.</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="metric-grid">
                    <div class="metric-card">
                        <div class="m-ico purple">{icn('users', 17)}</div>
                        <div class="m-value">{total}</div>
                        <div class="m-label">Total Predictions</div>
                    </div>
                    <div class="metric-card">
                        <div class="m-ico pink">{icn('userx', 17)}</div>
                        <div class="m-value">{churn_count}</div>
                        <div class="m-label">Likely to Churn</div>
                    </div>
                    <div class="metric-card">
                        <div class="m-ico green">{icn('usercheck', 17)}</div>
                        <div class="m-value">{safe_count}</div>
                        <div class="m-label">No Churn</div>
                    </div>
                    <div class="metric-card">
                        <div class="m-ico orange">{icn('pie', 17)}</div>
                        <div class="m-value">{churn_rate:.0f}%</div>
                        <div class="m-label">Churn Rate</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.write("")
    with stats_right:
        with stylable_container(key="distribution_card", css_styles=CARD_CSS):
            st.markdown(f"""
            <div class="card-title"><span class="ico">{icn('pie', 15)}</span>Prediction Distribution</div>
            """, unsafe_allow_html=True)
            st.write("")
            if history_df is None:
                st.markdown("<p class='empty'>No data yet.</p>", unsafe_allow_html=True)
            else:
                chart_col, legend_col = st.columns([1.1, 1])
                with chart_col:
                    fig = go.Figure(go.Pie(
                        labels=["Likely to Churn", "No Churn"],
                        values=[churn_count, safe_count],
                        hole=0.62,
                        marker=dict(colors=["#ff2e63", "#00d1b2"]),
                        textinfo="none",
                        hoverinfo="label+value",
                    ))
                    fig.update_layout(
                        showlegend=False,
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=10, r=10, t=10, b=10),
                        height=210,
                    )
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                with legend_col:
                    st.markdown(f"""
                    <div class="legend">
                        <div class="legend-item"><span class="sq pink"></span>
                            Likely to Churn&nbsp;<b>{churn_rate:.0f}% ({churn_count})</b></div>
                        <div class="legend-item"><span class="sq teal"></span>
                            No Churn&nbsp;<b>{safe_rate:.0f}% ({safe_count})</b></div>
                    </div>
                    """, unsafe_allow_html=True)

elif page == "History":
    history_df = pd.DataFrame(st.session_state.history) if st.session_state.history else None
    with stylable_container(key="history_card", css_styles=CARD_CSS):
        st.markdown(f"""
        <div class="card-title"><span class="ico">{icn('clock', 15)}</span>Customer Prediction History</div>
        """, unsafe_allow_html=True)
        st.write("")
        if history_df is None:
            st.info("Make your first prediction to view analytics and prediction history.")
        else:
            csv = history_df.to_csv(index=False).encode("utf-8")
            btn_left, spacer, btn_right = st.columns([0.5, 1, 0.5], gap="small")
            with btn_left:
                st.download_button(
                    label="Download History as CSV",
                    data=csv,
                    file_name="prediction_history.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="download_btn"
                )
            with btn_right:
                if st.button("Clear History", use_container_width=True, key="clear_btn"):
                    st.session_state.history = []
                    st.session_state.last_result = None
                    st.rerun()
            rows_html = ""
            for _, r in history_df.iterrows():
                dot = "pink" if r["Prediction"] == "Likely to Churn" else "teal"
                rows_html += (
                    f"<tr><td>{r['Time']}</td>"
                    f"<td><span class='td-dot {dot}'></span>{r['Prediction']}</td>"
                    f"<td>{r['Age']}</td><td>{r['Gender']}</td>"
                    f"<td>{r['Subscription']}</td><td>{r['Contract']}</td>"
                    f"<td>{r['Support Calls']}</td><td>{r['Payment Delay']}</td>"
                    f"<td>{r['Total Spend']}</td></tr>"
                )
            st.markdown(f"""
            <div class="hist-wrap">
                <table class="hist-table">
                    <thead>
                        <tr>
                            <th>Time</th><th>Prediction</th><th>Age</th><th>Gender</th>
                            <th>Subscription</th><th>Contract</th><th>Support Calls</th>
                            <th>Payment Delay</th><th>Total Spend</th>
                        </tr>
                    </thead>
                    <tbody>{rows_html}</tbody>
                </table>
            </div>
            """, unsafe_allow_html=True)
    st.write("")

elif page == "Model Info":
    st.markdown(f"""
    <div class="html-card">
        <div class="card-title"><span class="ico">{icn('cpu', 15)}</span>Model Information</div>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="m-ico purple">{icn('cpu', 17)}</div>
                <div class="m-value" style="font-size:16px;">Decision Tree</div>
                <div class="m-label">Algorithm</div>
            </div>
            <div class="metric-card">
                <div class="m-ico green">{icn('award', 17)}</div>
                <div class="m-value">99.97%</div>
                <div class="m-label">Accuracy</div>
            </div>
            <div class="metric-card">
                <div class="m-ico pink">{icn('layers', 17)}</div>
                <div class="m-value">440,833</div>
                <div class="m-label">Dataset Samples</div>
            </div>
            <div class="metric-card">
                <div class="m-ico orange">{icn('shield', 17)}</div>
                <div class="m-value">1.0</div>
                <div class="m-label">Version</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:  # About Us
    st.markdown(f"""
    <div class="html-card">
        <div class="card-title"><span class="ico">{icn('info', 15)}</span>About Us</div>
        <div class="action-list">
            <div class="action-item"><span class="ai-ico purple">{icn('target', 15)}</span>ChurnSense is an educational machine-learning dashboard that predicts customer churn.</div>
            <div class="action-item"><span class="ai-ico blue">{icn('cpu', 15)}</span>Decision Tree classifier with 99.97% accuracy on 440,833 samples.</div>
            <div class="action-item"><span class="ai-ico orange">{icn('users', 15)}</span>Built by StarTrio as an educational practice project with Streamlit.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# About & footer (always visible)
# -------------------------------------------------
#st.write("")
with st.expander("About the Model"):
    st.write("""
    This application uses a Decision Tree classifier trained on a customer churn dataset.
    The model analyzes customer behavior and predicts whether a customer is likely to leave the service.
    The final Decision Tree model achieved an accuracy of 99.97% on the evaluation dataset.
    """)

st.caption("© 2026 StarTrio | Educational Practice Project | Built with Streamlit")
from urllib.parse import quote

NAV_ICONS = [("Dashboard", "home"), ("Predict Customer", "target"), ("Analytics", "trend"),
             ("History", "clock"), ("Model Info", "cpu"), ("About Us", "info")]

_nav_css = ["input[type='radio']{ display:none !important; }"]
for _i, (_name, _icon) in enumerate(NAV_ICONS, 1):
    _svg = ("<svg xmlns='http://www.w3.org/2000/svg' width='17' height='17' viewBox='0 0 24 24' "
            "fill='none' stroke='#a78bfa' stroke-width='2' stroke-linecap='round' "
            "stroke-linejoin='round'>" + ICONS[_icon] + "</svg>")
    _nav_css.append(
        'div[data-testid="stRadio"] [role="radiogroup"] > label:nth-child(' + str(_i) + '){'
        'background-image:url("data:image/svg+xml,' + quote(_svg) + '");'
        'background-repeat:no-repeat; background-position:14px center; background-size:17px 17px;'
        'padding-left:44px; }'
    )

st.markdown("<style>" + "\n".join(_nav_css) + "</style>", unsafe_allow_html=True)