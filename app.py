import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest
import time

st.set_page_config(
    page_title="AI Embedded Immune System",
    page_icon="🛡️",
    layout="wide"
)

# ---------- STYLE ----------
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 800;
}
.subtitle {
    font-size: 20px;
    color: #555;
}
.status-normal {
    padding: 18px;
    background: #d9f7df;
    border-radius: 15px;
    font-size: 22px;
    font-weight: bold;
}
.status-warning {
    padding: 18px;
    background: #fff0bd;
    border-radius: 15px;
    font-size: 22px;
    font-weight: bold;
}
.status-critical {
    padding: 18px;
    background: #ffd6d6;
    border-radius: 15px;
    font-size: 22px;
    font-weight: bold;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background: white;
    box-shadow: 0 3px 15px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "history" not in st.session_state:
    st.session_state.history = []

if "isolated" not in st.session_state:
    st.session_state.isolated = False

if "recovered" not in st.session_state:
    st.session_state.recovered = False

# ---------- AI MODEL ----------
normal_data = np.random.normal(
    [45, 5, 1.8, 2],
    [5, 0.3, 0.3, 0.5],
    (500, 4)
)

ai_model = IsolationForest(
    contamination=0.08,
    random_state=42
)

ai_model.fit(normal_data)

# ---------- SENSOR SIMULATION ----------
def generate_sensor_data():

    temperature = np.random.normal(45, 4)
    voltage = np.random.normal(5, 0.25)
    current = np.random.normal(1.8, 0.2)
    vibration = np.random.normal(2, 0.5)

    # Automatic abnormal event
    if np.random.random() < 0.25:

        fault = np.random.choice([
            "temperature",
            "voltage",
            "vibration",
            "multiple"
        ])

        if fault == "temperature":
            temperature += np.random.uniform(30, 45)

        elif fault == "voltage":
            voltage -= np.random.uniform(1.5, 2.5)

        elif fault == "vibration":
            vibration += np.random.uniform(5, 8)

        else:
            temperature += 35
            voltage -= 1.7
            vibration += 6

    return temperature, voltage, current, vibration


# ---------- AI ANALYSIS ----------
def analyze_system(temp, voltage, current, vibration):

    risk = 0

    if temp > 75:
        risk += 40
    elif temp > 60:
        risk += 20

    if voltage < 3.5:
        risk += 35
    elif voltage < 4.2:
        risk += 20

    if vibration > 7:
        risk += 30
    elif vibration > 4.5:
        risk += 15

    prediction = ai_model.predict(
        [[temp, voltage, current, vibration]]
    )[0]

    if prediction == -1:
        risk += 15

    risk = min(risk, 100)

    if risk >= 60:
        status = "CRITICAL"
    elif risk >= 25:
        status = "WARNING"
    else:
        status = "NORMAL"

    return risk, status


# ---------- SIDEBAR ----------
st.sidebar.title("🛡️ SYSTEM MENU")

page = st.sidebar.radio(
    "Select Module",
    [
        "🏠 Digital Twin",
        "🧪 Virtual ET&T Lab",
        "🤖 AI Anomaly Detection",
        "💥 Fault Injection",
        "🔍 Fault Diagnosis",
        "🔒 Automatic Node Isolation",
        "🧬 Immune Response",
        "♻️ Self Recovery",
        "📊 Analytics"
    ]
)

st.sidebar.markdown("---")
st.sidebar.success("SYSTEM ONLINE")
st.sidebar.info("Software-only simulation")


# =========================================================
# DIGITAL TWIN
# =========================================================

if page == "🏠 Digital Twin":

    st.markdown(
        '<div class="main-title">🛡️ AI Embedded Immune System</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Autonomous Digital Twin + AI Fault Detection + Virtual ET&T Laboratory</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader("🖥️ LIVE VIRTUAL EMBEDDED DEVICE")

    temp, voltage, current, vibration = generate_sensor_data()

    risk, status = analyze_system(
        temp,
        voltage,
        current,
        vibration
    )

    health = 100 - risk

    st.session_state.history.append({
        "Time": time.strftime("%H:%M:%S"),
        "Temperature": round(temp, 2),
        "Voltage": round(voltage, 2),
        "Current": round(current, 2),
        "Vibration": round(vibration, 2),
        "AI Risk": risk,
        "Status": status
    })

    if len(st.session_state.history) > 50:
        st.session_state.history.pop(0)

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("🌡 Temperature", f"{temp:.1f} °C")
    c2.metric("⚡ Voltage", f"{voltage:.2f} V")
    c3.metric("🔌 Current", f"{current:.2f} A")
    c4.metric("📳 Vibration", f"{vibration:.2f}")
    c5.metric("🧠 Health", f"{health}%")

    st.subheader("🤖 AI SYSTEM DECISION")

    if status == "NORMAL":

        st.markdown(
            '<div class="status-normal">🟢 SYSTEM NORMAL</div>',
            unsafe_allow_html=True
        )

    elif status == "WARNING":

        st.markdown(
            '<div class="status-warning">⚠️ WARNING — ABNORMAL BEHAVIOUR DETECTED</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<div class="status-critical">🚨 CRITICAL FAULT — IMMUNE RESPONSE ACTIVATED</div>',
            unsafe_allow_html=True
        )

        st.error(
            "🚨 Automatic protection sequence: DETECT → DIAGNOSE → ISOLATE → PROTECT"
        )

    if len(st.session_state.history) > 1:

        df = pd.DataFrame(st.session_state.history)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            y=df["Temperature"],
            mode="lines+markers",
            name="Temperature"
        ))

        fig.add_trace(go.Scatter(
            y=df["Voltage"],
            mode="lines+markers",
            name="Voltage"
        ))

        fig.add_trace(go.Scatter(
            y=df["Vibration"],
            mode="lines+markers",
            name="Vibration"
        ))

        fig.update_layout(
            title="Live Digital Twin",
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    time.sleep(2)
    st.rerun()


# =========================================================
# VIRTUAL ET&T LAB
# =========================================================

elif page == "🧪 Virtual ET&T Lab":

    st.title("🧪 Virtual ET&T Embedded Systems Laboratory")

    st.write(
        "Perform embedded-system experiments virtually without physical hardware."
    )

    experiment = st.selectbox(
        "Select Experiment",
        [
            "🌡 Thermal Stress",
            "⚡ Voltage Stability",
            "📳 Vibration Analysis",
            "💥 Multi-Fault Experiment"
        ]
    )

    if experiment == "🌡 Thermal Stress":

        value = st.slider(
            "Temperature (°C)",
            20,
            110,
            45
        )

        st.metric("Virtual Temperature", f"{value} °C")

        if value > 75:
            st.error("🚨 THERMAL FAILURE")
        elif value > 60:
            st.warning("⚠️ THERMAL WARNING")
        else:
            st.success("🟢 TEMPERATURE NORMAL")

    elif experiment == "⚡ Voltage Stability":

        value = st.slider(
            "Voltage (V)",
            0.0,
            6.0,
            5.0
        )

        st.metric("Virtual Voltage", f"{value} V")

        if value < 3.5:
            st.error("🚨 VOLTAGE COLLAPSE")
        elif value < 4.2:
            st.warning("⚠️ VOLTAGE WARNING")
        else:
            st.success("🟢 VOLTAGE STABLE")

    elif experiment == "📳 Vibration Analysis":

        value = st.slider(
            "Vibration Level",
            0.0,
            12.0,
            2.0
        )

        st.metric("Vibration", f"{value}")

        if value > 7:
            st.error("🚨 EXCESSIVE VIBRATION")
        elif value > 4.5:
            st.warning("⚠️ ABNORMAL VIBRATION")
        else:
            st.success("🟢 VIBRATION NORMAL")

    else:

        st.subheader("💥 Multiple Fault Simulation")

        temp = st.slider("Temperature", 20, 110, 90)
        voltage = st.slider("Voltage", 0.0, 6.0, 3.0)
        vibration = st.slider("Vibration", 0.0, 12.0, 8.0)

        risk, status = analyze_system(
            temp,
            voltage,
            1.8,
            vibration
        )

        st.metric("AI Risk Score", f"{risk}/100")

        if status == "CRITICAL":
            st.error("🚨 CRITICAL MULTI-FAULT CONDITION")
        elif status == "WARNING":
            st.warning("⚠️ WARNING")
        else:
            st.success("🟢 NORMAL")


# =========================================================
# AI ANOMALY DETECTION
# =========================================================

elif page == "🤖 AI Anomaly Detection":

    st.title("🤖 AI Anomaly Detection Engine")

    temp = st.number_input(
        "Temperature (°C)",
        0.0,
        150.0,
        45.0
    )

    voltage = st.number_input(
        "Voltage (V)",
        0.0,
        10.0,
        5.0
    )

    current = st.number_input(
        "Current (A)",
        0.0,
        20.0,
        1.8
    )

    vibration = st.number_input(
        "Vibration",
        0.0,
        20.0,
        2.0
    )

    risk, status = analyze_system(
        temp,
        voltage,
        current,
        vibration
    )

    st.metric("AI Anomaly Score", f"{risk}/100")
    st.metric("Device Health", f"{100-risk}%")

    if status == "CRITICAL":
        st.error("🚨 AI DETECTED CRITICAL ANOMALY")
    elif status == "WARNING":
        st.warning("⚠️ AI DETECTED ABNORMAL BEHAVIOUR")
    else:
        st.success("🟢 AI FOUND NORMAL BEHAVIOUR")


# =========================================================
# FAULT INJECTION
# =========================================================

elif page == "💥 Fault Injection":

    st.title("💥 Virtual Fault Injection Simulator")

    fault = st.selectbox(
        "Inject Fault",
        [
            "🔥 Thermal Runaway",
            "⚡ Voltage Collapse",
            "📳 Excessive Vibration",
            "💥 Multiple Faults",
            "⏳ Gradual Degradation"
        ]
    )

    if fault == "🔥 Thermal Runaway":

        temp = 95
        voltage = 5
        vibration = 2

    elif fault == "⚡ Voltage Collapse":

        temp = 45
        voltage = 2.5
        vibration = 2

    elif fault == "📳 Excessive Vibration":

        temp = 45
        voltage = 5
        vibration = 10

    elif fault == "💥 Multiple Faults":

        temp = 95
        voltage = 2.5
        vibration = 10

    else:

        temp = np.random.uniform(60, 90)
        voltage = np.random.uniform(3, 4)
        vibration = np.random.uniform(5, 8)

    risk, status = analyze_system(
        temp,
        voltage,
        1.8,
        vibration
    )

    st.metric("Temperature", f"{temp:.1f} °C")
    st.metric("Voltage", f"{voltage:.2f} V")
    st.metric("Vibration", f"{vibration:.2f}")
    st.metric("AI Risk", f"{risk}/100")

    if status == "CRITICAL":
        st.error("🚨 CRITICAL FAULT")
        st.warning("🛡️ IMMUNE RESPONSE ACTIVATED")
    else:
        st.warning("⚠️ ABNORMAL CONDITION")


# =========================================================
# DIAGNOSIS
# =========================================================

elif page == "🔍 Fault Diagnosis":

    st.title("🔍 Intelligent Fault Diagnosis")

    fault = st.selectbox(
        "Detected Fault",
        [
            "High Temperature",
            "Low Voltage",
            "Excessive Vibration",
            "Multiple Faults"
        ]
    )

    if fault == "High Temperature":

        st.error("🌡 THERMAL FAULT")
        st.write(
            "Possible overheating or excessive processing load."
        )

    elif fault == "Low Voltage":

        st.error("⚡ POWER FAULT")
        st.write(
            "Possible unstable power supply or voltage drop."
        )

    elif fault == "Excessive Vibration":

        st.error("📳 VIBRATION FAULT")
        st.write(
            "Possible mechanical instability or abnormal operation."
        )

    else:

        st.error("💥 SYSTEM-LEVEL FAULT")
        st.write(
            "Multiple abnormal parameters detected."
        )

    st.success(
        "🤖 AI Recommendation: Isolate affected node and activate protection."
    )


# =========================================================
# NODE ISOLATION
# =========================================================

elif page == "🔒 Automatic Node Isolation":

    st.title("🔒 Autonomous Node Isolation")

    node = st.selectbox(
        "Faulty Virtual Node",
        [
            "🌡 Temperature Sensor",
            "⚡ Power Monitoring",
            "📳 Vibration Sensor",
            "🧠 Processing Node",
            "📡 Communication Node"
        ]
    )

    st.error(
        f"🚨 ABNORMAL BEHAVIOUR DETECTED → {node}"
    )

    st.session_state.isolated = True

    st.warning(
        f"🔒 {node} → AUTOMATICALLY ISOLATED"
    )

    st.success(
        "🟢 Healthy nodes remain operational."
    )

    st.info(
        "🛡️ Fault propagation has been prevented."
    )


# =========================================================
# IMMUNE RESPONSE
# =========================================================

elif page == "🧬 Immune Response":

    st.title("🧬 Artificial Immune Response")

    steps = [
        "1️⃣ DETECT — abnormal behaviour detected",
        "2️⃣ ANALYSE — AI calculates anomaly score",
        "3️⃣ DIAGNOSE — fault identified",
        "4️⃣ ISOLATE — faulty node isolated",
        "5️⃣ PROTECT — healthy nodes continue operating",
        "6️⃣ RECOVER — system attempts recovery"
    ]

    for step in steps:
        st.info(step)

    st.success(
        "🧠 The software imitates the protective behaviour of a biological immune system."
    )


# =========================================================
# SELF RECOVERY
# =========================================================

elif page == "♻️ Self Recovery":

    st.title("♻️ Autonomous Self-Recovery")

    if st.session_state.isolated:

        st.warning("🔒 Faulty node is isolated.")

        progress = st.progress(0)

        for i in range(0, 101, 20):
            progress.progress(i)
            time.sleep(0.2)

        st.session_state.recovered = True

        st.success("♻️ SYSTEM RECOVERY SUCCESSFUL")

        st.metric("Recovered System Health", "96%")

        st.info(
            "Healthy virtual nodes continue operating while the faulty node remains isolated."
        )

    else:

        st.info(
            "No isolated fault detected. Open Automatic Node Isolation first."
        )


# =========================================================
# ANALYTICS
# =========================================================

elif page == "📊 Analytics":

    st.title("📊 System Intelligence Analytics")

    st.metric(
        "Recorded Events",
        len(st.session_state.history)
    )

    st.metric(
        "Isolation",
        "ACTIVE" if st.session_state.isolated else "READY"
    )

    st.metric(
        "Recovery",
        "SUCCESS" if st.session_state.recovered else "READY"
    )

    if st.session_state.history:

      "AI_Embedded_Immune_Report.csv",
            "text/csv"
            )

    
