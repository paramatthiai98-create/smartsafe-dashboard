import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import random

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="SmartSafe: AI Decision Support System for Factory Safety",
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
.ai-box {
    border-radius: 18px;
    padding: 18px 20px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 14px;
    font-size: 1.02rem;
    font-weight: 700;
}
.ai-box-safe {
    background: rgba(22,163,74,0.14);
    border: 1px solid rgba(22,163,74,0.30);
    color: #bbf7d0;
}
.ai-box-warning {
    background: rgba(245,158,11,0.16);
    border: 1px solid rgba(245,158,11,0.32);
    color: #fde68a;
}
.ai-box-risk {
    background: rgba(239,68,68,0.16);
    border: 1px solid rgba(239,68,68,0.32);
    color: #fecaca;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# FUNCTIONS
# -------------------------
def generate_data():
    helmet = random.choice([True, False])
    distance = random.randint(10, 100)
    vibration = random.randint(0, 100)
    temperature = random.randint(28, 65)
    return {
        "helmet": helmet,
        "distance": distance,
        "vibration": vibration,
        "temperature": temperature
    }

def calculate_risk(data):
    risk = 0
    reasons = []

    if not data["helmet"]:
        risk += 30
        reasons.append("No helmet detected")

    if data["distance"] < 30:
        risk += 40
        reasons.append("Worker too close to machine")

    if data["vibration"] > 70:
        risk += 35
        reasons.append("High machine vibration")

    return risk, reasons

def decision_logic(risk):
    if risk > 80:
        return "HIGH RISK", "STOP MACHINE IMMEDIATELY"
    elif risk > 50:
        return "WARNING", "CHECK SYSTEM AND REDUCE EXPOSURE"
    else:
        return "SAFE", "NORMAL OPERATION"

def ai_solution(reasons):
    solutions = []
    if "No helmet detected" in reasons:
        solutions.append("Provide PPE alert and require worker to wear a safety helmet before continuing operation.")
    if "Worker too close to machine" in reasons:
        solutions.append("Increase safety distance and reposition worker outside the restricted machine zone.")
    if "High machine vibration" in reasons:
        solutions.append("Inspect machine condition, reduce load, and perform maintenance to lower abnormal vibration.")
    if not solutions:
        solutions.append("No immediate corrective action required. Continue monitoring in real time.")
    return solutions

def demo_data_from_risk(risk_target):
    mapping = {
        0:   {"helmet": True,  "distance": 60, "vibration": 40, "temperature": 32},
        30:  {"helmet": False, "distance": 60, "vibration": 40, "temperature": 34},
        35:  {"helmet": True,  "distance": 60, "vibration": 85, "temperature": 48},
        40:  {"helmet": True,  "distance": 20, "vibration": 40, "temperature": 36},
        65:  {"helmet": False, "distance": 60, "vibration": 85, "temperature": 50},
        70:  {"helmet": False, "distance": 20, "vibration": 40, "temperature": 38},
        75:  {"helmet": True,  "distance": 20, "vibration": 85, "temperature": 52},
        105: {"helmet": False, "distance": 20, "vibration": 85, "temperature": 56},
    }
    return mapping[risk_target]

def get_status_chip_class(status):
    if status == "HIGH RISK":
        return "status-chip status-risk"
    elif status == "WARNING":
        return "status-chip status-warning"
    return "status-chip status-safe"

def get_alert_class(status):
    if status == "HIGH RISK":
        return "alert-main alert-risk"
    elif status == "WARNING":
        return "alert-main alert-warning"
    return "alert-main alert-safe"

def decision_box_class(status):
    if status == "HIGH RISK":
        return "ai-box ai-box-risk"
    elif status == "WARNING":
        return "ai-box ai-box-warning"
    return "ai-box ai-box-safe"

# -------------------------
# SESSION STATE
# -------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.header("Demo Control")

demo_mode = st.sidebar.toggle("Enable Demo Mode", value=True)
risk_options = [0, 30, 35, 40, 65, 70, 75, 105]

risk_target = st.sidebar.select_slider(
    "Risk Score",
    options=risk_options,
    value=70,
    disabled=not demo_mode
)

# -------------------------
# CURRENT DATA
# -------------------------
if demo_mode:
    d = demo_data_from_risk(risk_target)
else:
    d = generate_data()

risk, reasons = calculate_risk(d)
status, action = decision_logic(risk)
solutions = ai_solution(reasons)

# Sidebar info
st.sidebar.markdown("### Current Inputs")
st.sidebar.write(f"Helmet: {'YES' if d['helmet'] else 'NO'}")
st.sidebar.write(f"Distance: {d['distance']} cm")
st.sidebar.write(f"Vibration: {d['vibration']}")
st.sidebar.write(f"Temperature: {d['temperature']} °C")
st.sidebar.write(f"Status: {status}")

# -------------------------
# STORE HISTORY
# -------------------------
st.session_state.history.append({
    "time": datetime.now().strftime("%H:%M:%S"),
    "risk": risk
})

if len(st.session_state.history) > 30:
    st.session_state.history = st.session_state.history[-30:]

df = pd.DataFrame(st.session_state.history)

# -------------------------
# HEADER
# -------------------------
st.markdown('<div class="main-title">SmartSafe: AI Decision Support System for Factory Safety</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Real-time safety analytics for worker protection, machine monitoring, and explainable AI recommendations.</div>', unsafe_allow_html=True)

# -------------------------
# TOP CARDS
# -------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Worker Status</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="{get_status_chip_class(status)}">{status}</div>', unsafe_allow_html=True)
    st.markdown('<div class="label">HELMET STATUS</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="big-sub-value">{"YES" if d["helmet"] else "NO"}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-line">Distance from machine: <b>{d["distance"]} cm</b></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Machine Status</div>', unsafe_allow_html=True)
    st.markdown('<div class="label">VIBRATION LEVEL</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="big-value">{d["vibration"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-line">Temperature: <b>{d["temperature"]} °C</b></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Risk Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="label">RISK SCORE</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="big-value">{risk}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="{get_alert_class(status)}">{status}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# MAIN PANELS
# -------------------------
left, right = st.columns([1.15, 1])

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">AI Decision Support</div>', unsafe_allow_html=True)

    st.markdown(
        f'''
        <div class="{decision_box_class(status)}">
            Recommended Action: <b>{action}</b><br>
            Current Status: <b>{status}</b><br>
            Risk Score: <b>{risk}</b>
        </div>
        ''',
        unsafe_allow_html=True
    )

    st.markdown('<div class="section-title">Explainable AI</div>', unsafe_allow_html=True)
    if reasons:
        for r in reasons:
            st.markdown(f'<div class="info-line">• {r}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-line">• No active risk detected</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">AI Recommended Fix</div>', unsafe_allow_html=True)
    for sol in solutions:
        st.markdown(f'<div class="fix-box">{sol}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Risk Trend</div>', unsafe_allow_html=True)
    chart_df = df[["time", "risk"]].set_index("time")
    st.line_chart(chart_df)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Active Alerts</div>', unsafe_allow_html=True)

    if status == "HIGH RISK":
        st.markdown('<div class="small-alert small-risk">Critical condition detected. Immediate intervention required.</div>', unsafe_allow_html=True)
    elif status == "WARNING":
        st.markdown('<div class="small-alert small-warning">Warning condition detected. Operator should inspect the process.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="small-alert" style="background: rgba(22,163,74,0.10); color:#bbf7d0;">System operating within normal safety conditions.</div>', unsafe_allow_html=True)

    if not d["helmet"]:
        st.markdown('<div class="small-alert small-risk">PPE violation: Worker is not wearing a helmet.</div>', unsafe_allow_html=True)

    if d["distance"] < 30:
        st.markdown('<div class="small-alert small-warning">Unsafe distance: Worker is too close to machine.</div>', unsafe_allow_html=True)

    if d["vibration"] > 70:
        st.markdown('<div class="small-alert small-warning">Machine vibration exceeded safe threshold.</div>', unsafe_allow_html=True)

    if d["helmet"] and d["distance"] >= 30 and d["vibration"] <= 70:
        st.markdown('<div class="small-alert" style="background: rgba(22,163,74,0.10); color:#bbf7d0;">No active alert in current cycle.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# FOOTER DATA TABLE
# -------------------------
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Recent Risk History</div>', unsafe_allow_html=True)
st.dataframe(df.iloc[::-1], use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
