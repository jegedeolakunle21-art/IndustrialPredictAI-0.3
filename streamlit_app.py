import os
import random
import joblib
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from streamlit_autorefresh import st_autorefresh


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="IndustrialPredictAI",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "models",
    "failure_prediction_bundle.joblib"
)


# ============================================================
# INDUSTRIAL DARK THEME
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b1220;
        color: #e5e7eb;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    div[data-testid="stMetric"] {
        background-color: #172033;
        border: 1px solid #263449;
        padding: 14px;
        border-radius: 10px;
    }

    .main-title {
        font-size: 32px;
        font-weight: 800;
        color: #e5e7eb;
    }

    .sub-title {
        color: #94a3b8;
        font-size: 14px;
    }

    .status-card {
        background-color: #172033;
        border: 1px solid #263449;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }

    .disclaimer {
        color: #fbbf24;
        font-size: 13px;
        background-color: #292313;
        border-radius: 8px;
        padding: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MODEL LOADING
# ============================================================

@st.cache_resource
def load_model_bundle():
    """Returns (bundle, error_message). Never raises, so the app
    still starts on Streamlit Cloud if the model is missing or was
    saved with an incompatible library version."""
    if not os.path.exists(MODEL_PATH):
        return None, "Model file not found."

    try:
        return joblib.load(MODEL_PATH), None
    except Exception as exc:
        return None, f"Model could not be loaded: {exc}"


bundle, bundle_error = load_model_bundle()


# ============================================================
# SIMULATED EQUIPMENT TELEMETRY
# ============================================================

EQUIPMENT_CONFIG = {
    "Motor-001": {
        "type": "Motor",
        "temperature": 65,
        "vibration": 3.0,
        "current": 18,
        "pressure": 0
    },
    "Pump-001": {
        "type": "Pump",
        "temperature": 58,
        "vibration": 2.5,
        "current": 14,
        "pressure": 5.0
    },
    "Generator-001": {
        "type": "Generator",
        "temperature": 75,
        "vibration": 3.5,
        "current": 45,
        "pressure": 0
    },
    "Motor-002": {
        "type": "Motor",
        "temperature": 62,
        "vibration": 2.8,
        "current": 16,
        "pressure": 0
    },
    "Pump-002": {
        "type": "Pump",
        "temperature": 60,
        "vibration": 2.7,
        "current": 15,
        "pressure": 4.5
    }
}


def initialize_equipment_state():
    if "equipment_history" not in st.session_state:
        st.session_state.equipment_history = {
            name: []
            for name in EQUIPMENT_CONFIG
        }

    if "telemetry_tick" not in st.session_state:
        st.session_state.telemetry_tick = 0


def generate_reading(name, config):
    previous = (
        st.session_state.equipment_history[name][-1]
        if st.session_state.equipment_history[name]
        else config
    )

    temperature = max(
        20,
        previous["temperature"] + random.uniform(-1.5, 1.8)
    )

    vibration = max(
        0.1,
        previous["vibration"] + random.uniform(-0.25, 0.30)
    )

    current = max(
        1,
        previous["current"] + random.uniform(-1.2, 1.2)
    )

    pressure = config["pressure"]

    if pressure > 0:
        pressure = max(
            0.1,
            previous["pressure"] + random.uniform(-0.15, 0.15)
        )

    return {
        "timestamp": pd.Timestamp.now(),
        "equipment": name,
        "equipment_type": config["type"],
        "temperature": round(temperature, 2),
        "vibration": round(vibration, 3),
        "current": round(current, 2),
        "pressure": round(pressure, 2)
    }


def calculate_health(reading):
    """
    Illustrative rule-based score for simulated telemetry.
    It is not an AI model prediction or an engineering diagnosis.
    """

    score = 100

    if reading["temperature"] > 85:
        score -= 35
    elif reading["temperature"] > 75:
        score -= 15

    if reading["vibration"] > 7:
        score -= 35
    elif reading["vibration"] > 5:
        score -= 15

    if reading["equipment_type"] == "Pump":
        if reading["pressure"] < 2:
            score -= 20

    if reading["equipment_type"] == "Generator":
        if reading["temperature"] > 90:
            score -= 15

    score = max(0, min(100, score))

    if score >= 80:
        status = "Healthy"
    elif score >= 60:
        status = "Warning"
    else:
        status = "Critical"

    return score, status


def update_telemetry():
    initialize_equipment_state()

    st.session_state.telemetry_tick += 1

    for name, config in EQUIPMENT_CONFIG.items():
        reading = generate_reading(name, config)

        health, status = calculate_health(reading)

        reading["health"] = health
        reading["status"] = status

        history = st.session_state.equipment_history[name]
        history.append(reading)

        st.session_state.equipment_history[name] = history[-60:]


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ IndustrialPredictAI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Live Equipment Monitor",
        "AI4I Failure Predictor",
        "About"
    ]
)

st.sidebar.divider()

st.sidebar.caption("IndustrialPredictAI v0.3")
st.sidebar.caption("Industrial equipment intelligence")


# ============================================================
# LIVE EQUIPMENT MONITOR
# ============================================================

def show_live_monitor():

    st.markdown(
        '<div class="main-title">Industrial Equipment Monitor</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">'
        'Live simulated telemetry for motors, pumps and generators'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="disclaimer">
        DEMONSTRATION MODE: Sensor readings are simulated.
        Health scores and alerts are illustrative rule-based indicators,
        not validated failure probabilities or engineering diagnoses.
        </div>
        """,
        unsafe_allow_html=True
    )

    st_autorefresh(
        interval=5000,
        key="industrial_refresh"
    )

    update_telemetry()

    latest = []

    for name in EQUIPMENT_CONFIG:
        if st.session_state.equipment_history[name]:
            latest.append(
                st.session_state.equipment_history[name][-1]
            )

    if not latest:
        st.info("Waiting for telemetry...")
        return

    telemetry_df = pd.DataFrame(latest)

    total_equipment = len(telemetry_df)
    healthy = int((telemetry_df["status"] == "Healthy").sum())
    warning = int((telemetry_df["status"] == "Warning").sum())
    critical = int((telemetry_df["status"] == "Critical").sum())
    average_health = telemetry_df["health"].mean()

    st.subheader("Operational Overview")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Equipment", total_equipment)
    c2.metric("Healthy", healthy)
    c3.metric("Warning", warning)
    c4.metric("Critical", critical)
    c5.metric("Average Health", f"{average_health:.1f}%")

    st.divider()

    st.subheader("Equipment Status")

    for _, row in telemetry_df.iterrows():

        with st.container(border=True):
            col1, col2, col3, col4 = st.columns(4)

            col1.markdown(f"**{row['equipment']}**")
            col1.caption(row["equipment_type"])

            col2.metric(
                "Health Score",
                f"{row['health']}%"
            )

            col3.metric(
                "Temperature",
                f"{row['temperature']:.1f} °C"
            )

            col4.metric(
                "Vibration",
                f"{row['vibration']:.2f} mm/s"
            )

            if row["status"] == "Healthy":
                st.success("Status: Healthy")
            elif row["status"] == "Warning":
                st.warning("Status: Warning")
            else:
                st.error("Status: Critical")

    st.divider()

    st.subheader("Telemetry Trends")

    equipment_names = list(EQUIPMENT_CONFIG.keys())

    selected_equipment = st.selectbox(
        "Select equipment",
        equipment_names,
        key="trend_equipment"
    )

    history = pd.DataFrame(
        st.session_state.equipment_history[selected_equipment]
    )

    if not history.empty:

        metric_choice = st.selectbox(
            "Select telemetry variable",
            [
                "temperature",
                "vibration",
                "current",
                "pressure",
                "health"
            ],
            key="trend_metric"
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=history["timestamp"],
                y=history[metric_choice],
                mode="lines+markers",
                name=metric_choice
            )
        )

        fig.update_layout(
            template="plotly_dark",
            title=f"{selected_equipment} — {metric_choice}",
            xaxis_title="Time",
            yaxis_title=metric_choice,
            height=380
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Active Alerts")

    alerts = telemetry_df[
        telemetry_df["status"] != "Healthy"
    ]

    if alerts.empty:
        st.success("No active simulated alerts.")
    else:
        for _, row in alerts.iterrows():
            st.warning(
                f"{row['equipment']}: {row['status']} "
                f"(health score: {row['health']}%)"
            )

    st.caption(
        "Dashboard refreshes every 5 seconds. "
        "Readings are generated locally for demonstration."
    )


# ============================================================
# AI4I FAILURE PREDICTOR
# ============================================================

def show_failure_predictor():

    st.title("AI4I Machine Failure Predictor")

    st.markdown(
        """
        This page uses the trained AI4I 2020 manufacturing
        failure-prediction model.

        It is separate from the simulated equipment monitor.
        The model is not validated for direct prediction on
        real motors, pumps or generators.
        """
    )

    if bundle is None:
        st.error(
            f"{bundle_error} "
            "Place failure_prediction_bundle.joblib "
            "inside the models folder and commit it to the repository. "
            "If it exists, make sure scikit-learn/xgboost versions in "
            "requirements.txt match the ones used for training."
        )
        return

    st.info(
        f"Selected model: {bundle['model_name']} | "
        f"Decision threshold: {bundle['threshold']:.2f}"
    )

    st.subheader("Enter manufacturing operating conditions")

    col1, col2 = st.columns(2)

    with col1:
        product_type = st.selectbox(
            "Product Type",
            ["L", "M", "H"]
        )

        air_temp = st.number_input(
            "Air Temperature (K)",
            min_value=295.0,
            max_value=305.0,
            value=300.0,
            step=0.1
        )

        process_temp = st.number_input(
            "Process Temperature (K)",
            min_value=305.0,
            max_value=315.0,
            value=310.0,
            step=0.1
        )

    with col2:
        rotational_speed = st.number_input(
            "Rotational Speed (rpm)",
            min_value=1000,
            max_value=3000,
            value=1500
        )

        torque = st.number_input(
            "Torque (Nm)",
            min_value=0.0,
            max_value=100.0,
            value=40.0,
            step=0.5
        )

        tool_wear = st.number_input(
            "Tool Wear (minutes)",
            min_value=0,
            max_value=300,
            value=100
        )

    if st.button(
        "Predict Machine Failure",
        type="primary",
        use_container_width=True
    ):

        input_data = pd.DataFrame([{
            "Type": product_type,
            "Air temperature [K]": air_temp,
            "Process temperature [K]": process_temp,
            "Rotational speed [rpm]": rotational_speed,
            "Torque [Nm]": torque,
            "Tool wear [min]": tool_wear
        }])

        probability = float(
            bundle["pipeline"].predict_proba(
                input_data
            )[0, 1]
        )

        prediction = int(
            probability >= bundle["threshold"]
        )

        st.divider()
        st.subheader("Prediction Result")

        st.metric(
            "Estimated Failure Probability",
            f"{probability * 100:.2f}%"
        )

        st.progress(
            min(1.0, max(0.0, probability))
        )

        if prediction == 1:
            st.error(
                "MODEL ALERT: The input is classified "
                "as a potential machine failure."
            )
            st.write(
                "Review the operating conditions and "
                "consider an appropriate inspection."
            )
        else:
            st.success(
                "The input is classified as no machine "
                "failure at the selected threshold."
            )

        st.caption(
            "This is a model estimate from a synthetic "
            "benchmark dataset, not a guarantee of equipment condition."
        )

    with st.expander("Model evaluation information"):
        st.write("Model:", bundle["model_name"])
        st.write("Dataset:", bundle["dataset"])
        st.write("Dataset type:", bundle["dataset_type"])
        st.json(bundle["metrics"])


# ============================================================
# ABOUT PAGE
# ============================================================

def show_about():

    st.title("About IndustrialPredictAI")

    st.markdown(
        """
        **IndustrialPredictAI v0.3** is an industrial equipment
        intelligence prototype.

        Its initial capabilities are:

        - Simulated live equipment monitoring
        - Motor, pump and generator telemetry demonstration
        - Illustrative equipment health indicators
        - AI4I manufacturing failure prediction
        - Interactive telemetry visualisation
        - Predictive-maintenance development foundation

        **Technology stack**

        - Python
        - Pandas and NumPy
        - Scikit-learn
        - XGBoost
        - Streamlit
        - Plotly

        **Development roadmap**

        1. Validate the software with real maintenance workflows.
        2. Collect equipment-specific operating and failure data.
        3. Integrate real IoT sensors and industrial data sources.
        4. Develop and validate equipment-specific predictive models.
        5. Add user accounts, historical data storage and reporting.
        """
    )

    st.warning(
        "This version is a prototype. It is not a certified "
        "industrial control, safety or protection system."
    )


# ============================================================
# ROUTING
# ============================================================

if page == "Live Equipment Monitor":
    show_live_monitor()

elif page == "AI4I Failure Predictor":
    show_failure_predictor()

else:
    show_about()
