import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.graph_objects as go
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Embedded Immune System AI Lab",
    page_icon="🛡️",
    layout="wide"
)

# ---------- STYLE ----------
st.markdown("""
<style>
.main {background:#f5f7fb;}
.title {
    font-size:42px;
    font-weight:800;
}
.card {
    padding:20px;
    border-radius:18px;
    background:white;
    box-shadow:0 3px 15px rgba(0,0,0,.08);
    margin-bottom:15px;
}
.normal {
    padding:15px;
    border-radius:15px;
    background:#dff7e5;
    color:#116329;
    font-weight:700;
}
.warning {
    padding:15px;
    border-radius:15px;
    background:#fff1c7;
    color:#805900;
    font-weight:700;
}
.critical {
    padding:15px;
    border-radius:15px;
    background:#ffd9d9;
    color:#a40000;
    font-weight:800;
    animation: blink 1s infinite;
}
@keyframes blink {
    50% {opacity:.55;}
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "running" not in st.session_state:
    st.session_state.running = True

if "history" not in st.session_state:
    st.session_state.history = []

if "fault_count" not in st.session_state:
    st.session_state.fault_count = 0

# ---------- SIDEBAR ----------
st.sidebar.title("🛡️ SYSTEM MENU")

page = st.sidebar.radio(
    "Select Module",
    [
        "🏠 Digital Twin",
        "🧪 Virtual ET&T Lab",
        "🤖 AI Anomaly Detection",
        "🔍 Fault Diagnosis",
        "🔒 Automatic Node Isolation",
        "🧬 Immune Response",
        "📊 Analytics"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Software-only simulation\n\n"
    "No physical hardware required."
)

# ---------- SENSOR SIMULATION ----------
def generate_sensor_data():
    temperature = np.random.normal(45, 3)
    voltage = np.random.normal(5.0, 0.25)
    current = np.random.normal(1.8, 0.2)
    vibration = np.random.normal(2.0, 0.5)

    # Occasionally create abnormal condition
    if np.random.random() < 0.18:
        temperature += np.random.uniform(20, 35)
        voltage -= np.random.uniform(1.0, 2.0)
        vibration += np.random.uniform(4, 7)

    return temperature, voltage, current, vibration


# ---------- ALARM ----------
def automatic_alarm(critical):
    if critical:
        st.markdown("""
        <div class="critical">
        🚨 CRITICAL FAULT DETECTED — IMMUNE RESPONSE ACTIVATED 🚨
        </div>
        """, unsafe_allow_html=True)

        # Browser alarm. Browsers may require one initial user interaction
        # to allow sound; after permission, alarm is triggered automatically.
        components.html("""
        <script>
        try {
            let ctx = new (window.AudioContext ||
                           window.webkitAudioContext)();

            if (ctx.state === "suspended") {
                ctx.resume();
            }

            let osc = ctx.createOscillator();
            let gain = ctx.createGain();

            osc.connect(gain);
            gain.connect(ctx.destination);

            osc.frequency.value = 850;
            gain.gain.value = 0.25;

            osc.start();

            setTimeout(() => {
                osc.stop();
            }, 700);
        } catch(e) {}
        </script>
        """, height=1)

    else:
        st.markdown(
            '<div class="normal">🟢 SYSTEM HEALTHY — No Critical Fault</div>',
            unsafe_allow_html=True
        )


# ==========================================================
# DIGITAL TWIN
# ==========================================================

if page == "🏠 Digital Twin":

    st.markdown(
        '<div class="title">🛡️ Embedded Immune System</div>',
        unsafe_allow_html=True
    )

    st.subheader("AI-Powered Digital Twin & Virtual Protection Lab")

    temperature, voltage, current, vibration = generate_sensor_data()

    critical = (
        temperature > 75
        or voltage < 3.5
        or vibration > 7
    )

    warning = (
        temperature > 60
        or voltage < 4.2
        or vibration > 4.5
    )

    if critical:
        status = "CRITICAL"
        st.session_state.fault_count += 1
    elif warning:
        status = "WARNING"
    else:
        status = "NORMAL"

    st.session_state.history.append({
        "Time": time.strftime("%H:%M:%S"),
        "Temperature": round(temperature, 2),
        "Voltage": round(voltage, 2),
        "Current": round(current, 2),
        "Vibration": round(vibration, 2)
    })

    if len(st.session_state.history) > 30:
        st.session_state.history.pop(0)

    # Sensor cards
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🌡️ Temperature", f"{temperature:.1f} °C")
    c2.metric("⚡ Voltage", f"{voltage:.2f} V")
    c3.metric("🔌 Current", f"{current:.2f} A")
    c4.metric("📳 Vibration", f"{vibration:.2f}")

    st.markdown("### System Status")

    automatic_alarm(critical)

    if warning and not critical:
        st.markdown(
            '<div class="warning">⚠️ WARNING — Abnormal behaviour detected</div>',
            unsafe_allow_html=True
        )

    # Graph
    df = pd.DataFrame(st.session_state.history)

    if len(df) > 1:
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
            title="Live Digital Twin Sensor Behaviour",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    st.info(
        "🔄 The embedded device is continuously simulated. "
        "The system automatically detects abnormal conditions "
        "without a physical sensor."
    )

    time.sleep(2)
    st.rerun()


# ==========================================================
# VIRTUAL ET&T LAB
# ==========================================================

elif page == "🧪 Virtual ET&T Lab":

    st.title("🧪 Virtual Embedded & Electronics Lab")

    st.write(
        "Experiment with a virtual embedded device and observe "
        "how faults affect the system."
    )

    experiment = st.selectbox(
        "Select Experiment",
        [
            "Temperature Stress Test",
            "Voltage Drop Test",
            "Vibration Fault Test",
            "Combined Fault Test"
        ]
    )

    if experiment == "Temperature Stress Test":
        value = st.slider("Virtual Temperature (°C)", 20, 100, 45)

        if value > 75:
            st.error("🚨 CRITICAL: Thermal fault")
        elif value > 60:
            st.warning("⚠️ WARNING: High temperature")
        else:
            st.success("🟢 NORMAL")

    elif experiment == "Voltage Drop Test":
        value = st.slider("Virtual Voltage (V)", 0.0, 6.0, 5.0)

        if value < 3.5:
            st.error("🚨 CRITICAL: Voltage instability")
        elif value < 4.2:
            st.warning("⚠️ WARNING: Low voltage")
        else:
            st.success("🟢 NORMAL")

    elif experiment == "Vibration Fault Test":
        value = st.slider("Virtual Vibration", 0.0, 12.0, 2.0)

        if value > 7:
            st.error("🚨 CRITICAL: Mechanical/embedded vibration fault")
        elif value > 4.5:
            st.warning("⚠️ WARNING: Abnormal vibration")
        else:
            st.success("🟢 NORMAL")

    else:
        st.write("Simulating multiple simultaneous faults...")

        temp = st.slider("Temperature", 20, 100, 85)
        voltage = st.slider("Voltage", 0.0, 6.0, 3.0)
        vibration = st.slider("Vibration", 0.0, 12.0, 8.0)

        if temp > 75 or voltage < 3.5 or vibration > 7:
            st.error("🚨 MULTI-FAULT CONDITION DETECTED")

    st.markdown("---")
    st.subheader("💡 What makes this different?")

    st.write("""
    This module works like a **Virtual Laboratory**:
    
    • No physical sensor required  
    • Faults can be injected virtually  
    • System response can be observed immediately  
    • Useful for ET&T/ECE students  
    • Can demonstrate embedded-system behaviour
    """)


# ==========================================================
# AI ANOMALY DETECTION
# ==========================================================

elif page == "🤖 AI Anomaly Detection":

    st.title("🤖 AI Anomaly Detection Engine")

    st.write(
        "The AI engine analyses embedded-device parameters "
        "and identifies abnormal behaviour."
    )

    temperature = st.number_input(
        "Temperature (°C)", 0.0, 150.0, 45.0
    )

    voltage = st.number_input(
        "Voltage (V)", 0.0, 10.0, 5.0
    )

    vibration = st.number_input(
        "Vibration", 0.0, 20.0, 2.0
    )

    score = 0

    if temperature > 75:
        score += 40
    elif temperature > 60:
        score += 20

    if voltage < 3.5:
        score += 40
    elif voltage < 4.2:
        score += 20

    if vibration > 7:
        score += 30
    elif vibration > 4.5:
        score += 15

    st.metric("AI Anomaly Score", f"{score}/100")

    if score >= 60:
        st.error("🚨 AI RESULT: HIGH ANOMALY")
    elif score >= 25:
        st.warning("⚠️ AI RESULT: POSSIBLE ANOMALY")
    else:
        st.success("🟢 AI RESULT: NORMAL")


# ==========================================================
# FAULT DIAGNOSIS
# =================================================
