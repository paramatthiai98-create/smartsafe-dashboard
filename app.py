import streamlit as st
import random
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from streamlit_plotly_events import plotly_events
from datetime import datetime

st.set_page_config(layout="wide")

# รีเฟรชทุก 10 นาที
st_autorefresh(interval=600000, key="datarefresh")


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

# -------------------------
# เก็บ history
# -------------------------
if "history" not in st.session_state:
    st.session_state.history = []

record = {
    "time": datetime.now().strftime("%H:%M"),
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

df = pd.DataFrame(st.session_state.history).reset_index(drop=True)
df["point_id"] = df.index

# -------------------------
# ปุ่มกรอง
# -------------------------
filter_option = st.radio(
    "Select status to view",
    ["ALL", "SAFE", "WARNING", "HIGH RISK"],
    horizontal=True
)

if filter_option == "ALL":
    filtered_df = df.copy()
else:
    filtered_df = df[df["status"] == filter_option].copy()

# -------------------------
# กราฟคลิกได้
# -------------------------
st.subheader("Risk Trend by Level")

if not filtered_df.empty:
    fig = px.line(
        filtered_df,
        x="point_id",
        y="risk",
        markers=True,
        color="status",
        hover_data=["time", "helmet", "distance", "vibration", "temperature", "reasons", "action"],
        color_discrete_map={
            "SAFE": "green",
            "WARNING": "gold",
            "HIGH RISK": "red"
        }
    )

    fig.update_traces(marker=dict(size=10))
    fig.update_layout(
        xaxis_title="Record",
        yaxis_title="Risk Score",
        legend_title="Risk Level",
        template="plotly_dark",
        height=450
    )

    selected_points = plotly_events(
        fig,
        click_event=True,
        hover_event=False,
        select_event=False,
        override_height=450,
        key="risk_chart"
    )

    # แสดงเฉพาะจุดที่คลิก
    if selected_points:
        selected_x = selected_points[0]["x"]
        selected_row = filtered_df[filtered_df["point_id"] == selected_x].iloc[0]

        st.subheader("Selected Risk Event")

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
            st.markdown("### Why Risk Was This Level")
            st.write(selected_row["reasons"])

            st.markdown("### AI Recommended Fix")
            for item in str(selected_row["solutions"]).split(" | "):
                st.write(f"- {item}")
else:
    st.info("ไม่มีข้อมูลตามสถานะที่เลือก")
