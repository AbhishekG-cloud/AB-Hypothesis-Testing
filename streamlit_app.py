import json
import streamlit as st

from src.ab_framework import ABTestFramework
from src.comparison import comparison_plots


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Bayesian A/B Testing Framework",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Bayesian A/B Testing Framework")

st.write(
    """
Compare two product variants using Frequentist and Bayesian
statistical analysis.
"""
)

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

st.sidebar.header("Experiment Settings")

visitors_A = st.sidebar.number_input(
    "Visitors (A)",
    min_value=1,
    value=1000,
)

visitors_B = st.sidebar.number_input(
    "Visitors (B)",
    min_value=1,
    value=1000,
)

conversions_A = st.sidebar.number_input(
    "Conversions (A)",
    min_value=0,
    value=52,
)

conversions_B = st.sidebar.number_input(
    "Conversions (B)",
    min_value=0,
    value=61,
)

PRIORS = {
    "Uniform": (1.0, 1.0),
    "Jeffreys": (0.5, 0.5),
    "Informative": (5.0, 5.0),
}

prior_name_A = st.sidebar.selectbox(
    "Prior A",
    list(PRIORS.keys()),
    key="prior_A"
)

prior_name_B = st.sidebar.selectbox(
    "Prior B",
    list(PRIORS.keys()),
    key="prior_B"
)

prior_A = PRIORS[prior_name_A]
prior_B = PRIORS[prior_name_B]

st.sidebar.subheader("Decision Thresholds")

alpha = st.sidebar.slider(
    "Frequentist α",
    min_value=0.01,
    max_value=0.10,
    value=0.05,
    step=0.01,
)

probability_threshold = st.sidebar.slider(
    "Bayesian Probability Threshold",
    min_value=0.50,
    max_value=0.99,
    value=0.95,
    step=0.01,
)

loss_threshold = st.sidebar.number_input(
    "Maximum Expected Loss",
    min_value=0.0000,
    max_value=0.0100,
    value=0.0010,
    step=0.0001,
    format="%.4f",
)


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------

if conversions_A > visitors_A:
    st.error("Conversions (A) cannot exceed Visitors (A).")
    st.stop()

if conversions_B > visitors_B:
    st.error("Conversions (B) cannot exceed Visitors (B).")
    st.stop()

# ---------------------------------------------------------
# Run Analysis
# ---------------------------------------------------------

framework = ABTestFramework()

results = framework.run_full_analysis(
    n_A=visitors_A,
    conv_A=conversions_A,
    n_B=visitors_B,
    conv_B=conversions_B,
    prior_A=prior_A,
    prior_B=prior_B,
    alpha=alpha,
    probability_threshold=probability_threshold,
    loss_threshold=loss_threshold,
)

# ---------------------------------------------------------
# Tabs
# ---------------------------------------------------------
st.subheader("Decision Thresholds")

thresholds = results["thresholds"]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "α",
        f"{thresholds['alpha']:.2f}"
    )

with col2:
    st.metric(
        "Probability Threshold",
        f"{thresholds['probability_threshold']:.0%}"
    )

with col3:
    st.metric(
        "Max Expected Loss",
        f"{thresholds['loss_threshold']:.4%}"
    )

tab1, tab2, tab3 = st.tabs(
    [
        "Summary",
        "Analysis",
        "Visualization"
    ]
)

# =========================================================
# SUMMARY
# =========================================================

with tab1:

    st.header("Experiment Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Conversion Rate A",
            f"{conversions_A / visitors_A:.2%}"
        )

    with col2:
        st.metric(
            "Conversion Rate B",
            f"{conversions_B / visitors_B:.2%}"
        )

    st.divider()

    st.subheader("Posterior Means")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Posterior Mean A",
            f"{results['bayesian']['A']['mean']:.2%}"
        )

    with col2:
        st.metric(
            "Posterior Mean B",
            f"{results['bayesian']['B']['mean']:.2%}"
        )

    st.divider()

    st.subheader("Recommendation")

    recommendation = results["recommendation"]

    if recommendation["recommendation"] == "Launch Variant B":
        st.success(f"✅ {recommendation['recommendation']}")

    elif recommendation["recommendation"] == "Keep Variant A":
        st.warning(f"⚠️ {recommendation['recommendation']}")

    else:
        st.info(recommendation["recommendation"])

    st.info(recommendation["reason"])

# =========================================================
# ANALYSIS
# =========================================================

with tab2:

    st.header("Frequentist Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "P-value",
            f"{results['frequentist']['p_value']:.4f}"
        )

    with col2:
        st.metric(
            "Z Statistic",
            f"{results['frequentist']['z_statistic']:.4f}"
        )

    ci_low, ci_high = results["frequentist"]["confidence_interval"]

    st.write(
        f"95% Confidence Interval: ({ci_low:.4f}, {ci_high:.4f})"
    )

    if results["frequentist"]["p_value"] < alpha:
        st.success(
            "Difference is statistically significant."
        )
    else:
        st.warning(
            "Difference is NOT statistically significant."
        )

    st.divider()

    st.header("Bayesian Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "P(B > A)",
            f"{results['monte_carlo']['probability_B_beats_A']:.2%}"
        )

    with col2:
        st.metric(
            "Expected Lift",
            f"{results['monte_carlo']['expected_uplift']:.2%}"
        )

    with col3:
        st.metric(
            "Expected Loss",
            f"{results['monte_carlo']['expected_loss']:.4%}"
        )

# =========================================================
# VISUALIZATION
# =========================================================

with tab3:

    st.header("Interactive Dashboard")

    fig = comparison_plots(results)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------------------------------------------------
# Raw Results
# ---------------------------------------------------------

st.divider()

with st.expander("Raw Results Dictionary"):

    st.json(results)

# ---------------------------------------------------------
# Download
# ---------------------------------------------------------

st.download_button(
    label="⬇ Download Results (JSON)",
    data=json.dumps(results, indent=4, default=str),
    file_name="ab_test_results.json",
    mime="application/json",
)
