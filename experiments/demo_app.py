import streamlit as st
import requests

# ----------------------------
# Configuration
# ----------------------------
# LIVE FastAPI backend on Render
API_URL = "https://latency-aware-decision-system-citadel.onrender.com/decide"

st.set_page_config(
    page_title="Latency-Aware Explainable Decision System",
    layout="centered",
)

st.title("Latency-Aware Explainable Decision System")
st.caption(
    "Live demo of a probabilistic decision system with latency constraints and explainability."
)

# ----------------------------
# Input Controls
# ----------------------------
st.subheader("Input Controls")

sample_index = st.slider(
    "Select sample index",
    min_value=0,
    max_value=500,
    value=0,
    step=1,
)

confidence_threshold = st.slider(
    "Confidence threshold",
    min_value=0.3,
    max_value=0.9,
    value=0.65,
    step=0.05,
)

run_button = st.button("Run decision")

# ----------------------------
# API Call & Results
# ----------------------------
if run_button:
    try:
        response = requests.post(
            API_URL,
            params={
                "sample_index": sample_index,
                "confidence_threshold": confidence_threshold,
            },
            timeout=15,  # Render free tier can be slow on first request
        )
        response.raise_for_status()
        result = response.json()

        st.divider()

        # ----------------------------
        # Decision Outcome
        # ----------------------------
        st.subheader("Decision Outcome")

        decision = result["decision"]

        if decision["execute"]:
            st.success("✅ Decision Accepted")
        else:
            st.error("❌ Decision Rejected")

        reason_map = {
            "accepted": "Meets confidence and latency requirements",
            "probability_below_threshold": "Confidence below required threshold",
            "latency_budget_exceeded": "Latency exceeded system budget",
        }

        st.write(
            f"**Reason:** {reason_map.get(decision['reason'], decision['reason'])}"
        )

        col1, col2 = st.columns(2)
        col1.metric("Probability", f"{decision['probability']:.2f}")
        col2.metric("Latency (ms)", f"{decision['latency_ms']:.1f}")

        # ----------------------------
        # Explanation
        # ----------------------------
        st.subheader("Decision Explanation")
        st.info(result["explanation"])

    except requests.exceptions.RequestException as e:
        st.error("❌ Could not connect to the decision API.")
        st.code(str(e))

# ----------------------------
# Footer
# ----------------------------
st.divider()
st.caption(
    "Backend powered by FastAPI, frontend by Streamlit. "
    "Designed to demonstrate system design, robustness, and explainability."
)
