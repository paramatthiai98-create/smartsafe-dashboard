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
        solutions.append("ติดตั้งระบบแจ้งเตือนเมื่อไม่พบอุปกรณ์ PPE")

    if "Worker too close to machine" in reasons:
        solutions.append("เพิ่มระยะปลอดภัยระหว่างคนงานกับเครื่องจักร")
        solutions.append("ตีเส้นเขตอันตรายหรือกำหนด safe zone ให้ชัดเจน")

    if "High machine vibration" in reasons:
        solutions.append("ตรวจสอบการสั่นสะเทือนของเครื่องจักรทันที")
        solutions.append("หยุดเครื่องเพื่อตรวจเช็กชิ้นส่วนที่อาจหลวม/เสื่อมสภาพ")
        solutions.append("วางแผนบำรุงรักษาเชิงป้องกัน")

    if not solutions:
        solutions.append("ระบบอยู่ในเกณฑ์ปกติ ให้ติดตามต่อเนื่อง")

    return solutions


st.title("SmartSafe Co-Pilot Dashboard")

d = generate_data()
risk, reasons = calculate_risk(d)
status, action = decision_logic(risk)
solutions = ai_solution(reasons)

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

st.subheader("AI Decision Support")
st.write(f"Recommended Action: **{action}**")

st.subheader("Explainable AI")
if reasons:
    for r in reasons:
        st.write(f"- {r}")
else:
    st.write("- No active risk detected")

st.subheader("AI Suggested Solutions")
for s in solutions:
    st.write(f"- {s}")

# -------------------------
# เก็บ history แบบละเอียด
# -------------------------
if "history" not in st.session_state:
    st.session_state.history = []

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

# จำกัดจำนวน record เพื่อไม่ให้ยาวเกิน
if len(st.session_state.history) > 100:
    st.session_state.history = st.session_state.history[-100:]

df = pd.DataFrame(st.session_state.history)

# -------------------------
# กราฟ
# -------------------------
st.subheader("Risk Trend")
st.line_chart(df.set_index("time")["risk"])

# -------------------------
# ตารางย้อนหลัง
# -------------------------
st.subheader("Risk History Table")
st.dataframe(
    df[["time", "risk", "status", "helmet", "distance", "vibration", "reasons", "action"]],
    use_container_width=True
)

# -------------------------
# เลือกดูรายละเอียดแต่ละจุด
# -------------------------
st.subheader("Inspect Past Risk Event")

selected_index = st.selectbox(
    "Select record to inspect",
    options=df.index,
    format_func=lambda x: f"{df.loc[x, 'time']} | Risk {df.loc[x, 'risk']} | {df.loc[x, 'status']}"
)

selected_row = df.loc[selected_index]

detail_col1, detail_col2 = st.columns(2)

with detail_col1:
    st.markdown("### Event Details")
    st.write(f"**Time:** {selected_row['time']}")
    st.write(f"**Risk Score:** {selected_row['risk']}")
    st.write(f"**Status:** {selected_row['status']}")
    st.write(f"**Helmet:** {selected_row['helmet']}")
    st.write(f"**Distance:** {selected_row['distance']} cm")
    st.write(f"**Vibration:** {selected_row['vibration']}")
    st.write(f"**Temperature:** {selected_row['temperature']} °C")

with detail_col2:
    st.markdown("### Why Risk Was High")
    st.write(selected_row["reasons"])

    st.markdown("### AI Recommended Fix")
    for item in str(selected_row["solutions"]).split(" | "):
        st.write(f"- {item}")

# -------------------------
# กรองเฉพาะช่วงเสี่ยงสูง
# -------------------------
st.subheader("High Risk Events Only")
high_risk_df = df[df["risk"] >= 50]

if not high_risk_df.empty:
    st.dataframe(
        high_risk_df[["time", "risk", "status", "reasons", "action"]],
        use_container_width=True
    )
else:
    st.info("ยังไม่มีเหตุการณ์ที่เสี่ยงสูง")
