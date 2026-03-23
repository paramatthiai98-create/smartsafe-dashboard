import streamlit as st
import random
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

st.set_page_config(
    page_title="SmartSafe Co-Pilot Dashboard",
    layout="wide"
)

st_autorefresh(interval=2000, key="datarefresh")

# -------------------------
# STYLE
# -------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #03101f 0%, #06172b 100%);
    color: #f8fafc;
}
.block-container {
    max-width: 96rem;
    padding-top: 1rem;
    padding-bottom: 1rem;
}
.main-title {
    font-size: 2.35rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.15rem;
}
.sub-title {
    color: #b6c2cf;
    margin-bottom: 1.3rem;
    font-size: 1.02rem;
}
.card {
    background: linear-gradient(180deg, rgba(7,20,40,0.98), rgba(5,17,34,0.98));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 22px;
    margin-bottom: 16px;
    box-shadow: 0 0 0 1px rgba(255,255,255,0.02) inset;
}
.card-title {
    font-size: 1.55rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 1.2rem;
}
.label {
    font-size: 0.96rem;
    color: #9fb0c3;
    margin-bottom: 0.25rem;
}
.big-value {
    font-size: 2.55rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.1;
    margin-bottom: 1rem;
}
.big-sub-value {
    font-size: 2.05rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.15;
    margin-bottom: 0.9rem;
}
.info-line {
    font-size: 1rem;
    color: #e5e7eb;
    margin: 0.38rem 0;
}
.panel {
    background: rgba(8, 20, 38, 0.97);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 18px 20px;
    margin-bottom: 16px;
}
.section-title {
    font-size: 1.38rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.9rem;
}
.alert-main {
    border-radius: 18px;
    padding: 18px 20px;
    font-weight: 700;
    font-size: 1.08rem;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 16px;
}
.alert-safe {
    background: rgba(22,163,74,0.16);
    color: #bbf7d0;
}
.alert-warning {
    background: rgba(245,158,11,0.18);
    color: #fde68a;
}
.alert-risk {
    background: rgba(239,68,68,0.18);
    color: #fecaca;
}
.fix-box {
    background: rgba(59,130,246,0.12);
    border: 1px solid rgba(59,130,246,0.28);
    border-radius: 16px;
    padding: 14px 16px;
    margin-bottom: 10px;
    color: #dbeafe;
    font-size: 1rem;
}
.small-alert {
    border-radius: 14px;
    padding: 12px 14px;
    font-size: 0.98rem;
    margin-bottom: 10px;
    border: 1px solid rgba(255,255,255,0.08);
}
.small-warning {
    background: rgba(245,158,11,0.12);
    color: #fde68a;
}
.small-risk {
    background: rgba(239,68,68,0.14);
    color: #fecaca;
}
.status-chip {
    display: inline-block;
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 0.84rem;
    font-weight: 800;
    margin-bottom: 1rem;
}
.status-safe {
    background: rgba(22,163,74,0.18);
    color: #86efac;
    border: 1px solid rgba(22,163,74,0.32);
}
.status-warning {
    background: rgba(245,158,11,0.18);
    color: #fcd34d;
    border: 1px solid rgba(245,158,11,0.32);
}
.status-risk {
    background: rgba(239,68,68,0.18);
    color: #fca5a5;
    border: 1px solid rgba(239,68,68,0.32);
}
div[data-testid="stMetric"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# DATA / LOGIC
# -------------------------
def generate_data():
    return {
        "helmet": random.choice([True, False]),
        "distance": random.randint(10, 100),
        "vibration": random.randint(0, 100),
        "temperature": random.randint(25, 80)
    }


def calculate_risk(d):
    risk = 0
    reasons = []

    if not d["helmet"]:
        risk += 30
        reasons.append("No helmet detected")

    if d["distance"] < 30:
        risk += 40
        reasons.append("Worker too close to machine")

    if d["vibration"] > 70:
        risk += 35
        reasons.append("High machine vibration")

    return risk, reasons


def decision_logic(risk):
    if risk > 80:
        return "HIGH RISK", "STOP MACHINE"
    elif risk > 50:
        return "WARNING", "CHECK SYSTEM"
    else:
        return "SAFE", "NORMAL OPERATION"


def ai_solution(reasons):
    solutions = []

    if "No helmet detected" in reasons:
        solutions.append("ให้พนักงานสวมหมวกนิรภัยก่อนเข้าพื้นที่ปฏิบัติงาน")

    if "Worker too close to machine" in reasons:
        solutions.append("เพิ่มระยะปลอดภัยระหว่างคนงานกับเครื่องจักร")
        solutions.append("กำหนดเขต safe zone ให้ชัดเจน")

    if "High machine vibration" in reasons:
        solutions.append("ตรวจสอบการสั่นสะเทือนของเครื่องจักรทันที")
        solutions.append("หยุดเครื่องเพื่อตรวจเช็กความผิดปกติ")
        solutions.append("วางแผนบำรุงรักษาเชิงป้องกัน")

    if not solutions:
        solutions.append("ระบบอยู่ในเกณฑ์ปกติ ให้ติดตามต่อเนื่อง")

    return solutions


def render_status_chip(status):
    if status == "HIGH RISK":
        return '<span class="status-chip status-risk">HIGH RISK</span>'
    elif status == "WARNING":
        return '<span class="status-chip status-warning">WARNING</span>'
    return '<span class="status-chip status-safe">SAFE</span>'


# -------------------------
# CURRENT DATA
# -------------------------
d = generate_data()
risk, reasons = calculate_risk(d)
status, action = decision_logic(risk)
solutions = ai_solution(reasons)

if "history" not in st.session_state:
    st.session_state.history = []

if "alerts" not in st.session_state:
    st.session_state.alerts = []

record = {
    "time": datetime.now().strftime("%H:%M:%S"),
    "helmet": "YES" if d["helmet"] else "NO",
    "distance": d["distance"],
    "vibration": d["vibration"],
    "temperature": d["temperature"],
    "risk": risk,
    "status": status,
    "action": action,
    "reasons": ", ".join(reasons) if reasons else "No active risk detected",
    "solutions": " | ".join(solutions)
}
st.session_state.history.append(record)

if len(st.session_state.history) > 100:
    st.session_state.history = st.session_state.history[-100:]

if status in ["WARNING", "HIGH RISK"]:
    new_alert = {
        "time": record["time"],
        "risk": record["risk"],
        "status": record["status"],
        "reasons": record["reasons"],
        "action": record["action"]
    }

    if (
        len(st.session_state.alerts) == 0
        or st.session_state.alerts[-1]["reasons"] != new_alert["reasons"]
        or st.session_state.alerts[-1]["status"] != new_alert["status"]
    ):
        st.session_state.alerts.append(new_alert)

if len(st.session_state.alerts) > 20:
    st.session_state.alerts = st.session_state.alerts[-20:]

# -------------------------
# HEADER
# -------------------------
st.markdown('<div class="main-title">SmartSafe Co-Pilot Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Worker safety monitoring and machine risk awareness</div>', unsafe_allow_html=True)

# -------------------------
# TOP KPI CARDS
# -------------------------
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Worker Status</div>', unsafe_allow_html=True)

    st.markdown('<div class="label">Helmet</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="big-value">{"YES" if d["helmet"] else "NO"}</div>', unsafe_allow_html=True)

    st.markdown('<div class="label">Distance</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="big-sub-value">{d["distance"]} cm</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Machine Status</div>', unsafe_allow_html=True)

    st.markdown('<div class="label">Vibration</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="big-value">{d["vibration"]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="label">Temperature</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="big-sub-value">{d["temperature"]} °C</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Risk Analysis</div>', unsafe_allow_html=True)

    st.markdown('<div class="label">Risk Score</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="big-value">{risk}</div>', unsafe_allow_html=True)
    st.markdown(render_status_chip(status), unsafe_allow_html=True)
    st.progress(min(risk, 100) / 100)

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# LIVE ALERT
# -------------------------
st.markdown('<div class="section-title">Live Alert</div>', unsafe_allow_html=True)

if status == "HIGH RISK":
    st.markdown(
        f'<div class="alert-main alert-risk">🚨 HIGH RISK: {", ".join(reasons)}</div>',
        unsafe_allow_html=True
    )
elif status == "WARNING":
    st.markdown(
        f'<div class="alert-main alert-warning">⚠️ WARNING: {", ".join(reasons)}</div>',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        '<div class="alert-main alert-safe">✅ SAFE: No active critical risk</div>',
        unsafe_allow_html=True
    )

# -------------------------
# AI DECISION + FIX
# -------------------------
left, right = st.columns([1, 1.15], gap="large")

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">AI Decision Support</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-line">Recommended Action: <b>{action}</b></div>', unsafe_allow_html=True)

    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Explainable AI</div>', unsafe_allow_html=True)
    if reasons:
        for r in reasons:
            st.markdown(f'<div class="info-line">• {r}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-line">• No active risk detected</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">AI Recommended Fix</div>', unsafe_allow_html=True)
    for s in solutions:
        st.markdown(f'<div class="fix-box">• {s}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# RISK TREND
# -------------------------
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Risk Trend</div>', unsafe_allow_html=True)
df = pd.DataFrame(st.session_state.history)
st.line_chart(df[["risk"]], use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# RECENT ALERTS
# -------------------------
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Recent Alerts</div>', unsafe_allow_html=True)

if st.session_state.alerts:
    for alert in reversed(st.session_state.alerts[-5:]):
        if alert["status"] == "HIGH RISK":
            st.markdown(
                f'<div class="small-alert small-risk">[{alert["time"]}] HIGH RISK | Score {alert["risk"]} | {alert["reasons"]} | Action: {alert["action"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="small-alert small-warning">[{alert["time"]}] WARNING | Score {alert["risk"]} | {alert["reasons"]} | Action: {alert["action"]}</div>',
                unsafe_allow_html=True
            )
else:
    st.info("ยังไม่มีประวัติการแจ้งเตือน")

st.markdown('</div>', unsafe_allow_html=True)
