import streamlit as st
import random
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

st.set_page_config(layout="wide")
st_autorefresh(interval=2000, key="datarefresh")


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
        solutions.append("ติดตั้งระบบตรวจจับ PPE อัตโนมัติ")

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


st.title("SmartSafe Co-Pilot Dashboard")

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

# บันทึกเฉพาะ alert สำคัญ
if status in ["WARNING", "HIGH RISK"]:
    new_alert = {
        "time": record["time"],
        "risk": record["risk"],
        "status": record["status"],
        "reasons": record["reasons"],
        "action": record["action"]
    }

    if len(st.session_state.alerts) == 0 or st.session_state.alerts[-1]["reasons"] != new_alert["reasons"] or st.session_state.alerts[-1]["status"] != new_alert["status"]:
        st.session_state.alerts.append(new_alert)

if len(st.session_state.alerts) > 20:
    st.session_state.alerts = st.session_state.alerts[-20:]

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Worker Status")
    st.write(f"Helmet: {'YES' if d['helmet'] else 'NO'}")
    st.write(f"Distance: {d['distance']} cm")

with col2:
    st.subheader("Machine Status")
    st.write(f"Vibration: {d['vibration']}")
    st.write(f"Temperature: {d['temperature']} °C")

with col3:
    st.subheader("Risk Analysis")
    st.metric("Risk Score", risk)

    if status == "HIGH RISK":
        st.error(status)
    elif status == "WARNING":
        st.warning(status)
    else:
        st.success(status)

# กล่องแจ้งเตือนหลัก
st.subheader("Live Alert")

if status == "HIGH RISK":
    st.error(f"🚨 HIGH RISK: {', '.join(reasons)}")
elif status == "WARNING":
    st.warning(f"⚠️ WARNING: {', '.join(reasons)}")
else:
    st.success("✅ SAFE: No active critical risk")

st.subheader("AI Decision Support")
st.write(f"Recommended Action: **{action}**")

st.subheader("AI Recommended Fix")
for s in solutions:
    st.write(f"- {s}")

st.subheader("Risk Trend")
df = pd.DataFrame(st.session_state.history)
st.line_chart(df[["risk"]], use_container_width=True)

st.subheader("Recent Alerts")
if st.session_state.alerts:
    for alert in reversed(st.session_state.alerts[-5:]):
        if alert["status"] == "HIGH RISK":
            st.error(f"[{alert['time']}] HIGH RISK | Score {alert['risk']} | {alert['reasons']} | Action: {alert['action']}")
        else:
            st.warning(f"[{alert['time']}] WARNING | Score {alert['risk']} | {alert['reasons']} | Action: {alert['action']}")
else:
    st.info("ยังไม่มีประวัติการแจ้งเตือน")
